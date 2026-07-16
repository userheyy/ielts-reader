// 每日单词页控制器:日历热力图 + 今日任务卡 + 过词(B交互) + 节奏设置。
import { renderAids, renderMorphemes, aidsHasContent, renderCollocations } from "./aids.js?v=2";
import { gradeReview } from "./store.js?v=7";
import { loadSeed, getSeedReview, setSeedReview } from "./seed.js?v=3";
import {speakEnglish, speechSupported} from "./speech.js?v=6";
import { judgeSpelling, ratingFromResult, blankSentence, feedbackFor } from "./cloze.js?v=1";
import { schedule } from "./srs.js?v=1";
import { buildQueue, noteItemDone } from "./daily-queue.js?v=2";
import {
  ensureTodayTask, rebuildTodayTask, markWordDone, heatmapCells, currentStreak, totalWordsDone,
  getSettings, updateSettings, dateKey,
} from "./daily-store.js?v=3";

// ---- DOM ----
const $ = (id) => document.getElementById(id);
const heatmapEl = $("heatmap");
const studyWrap = $("study-wrap");
const todayCard = $("today-card");
const doneCard = $("done-card");

let task = null;          // { date, review:[], newWords:[], day }
let queue = [];           // 待过的词队列: [{entry, kind:'review'|'new', origin}]
let currentItem = null;
let seedIndex = new Map();
let studySuggestedRating = null;

function clearStudySuggestion() {
  $("study-actions").querySelectorAll("button").forEach((b) => b.classList.remove("suggested"));
}
function highlightStudyRating(rating) {
  clearStudySuggestion();
  const b = rating && $("study-actions").querySelector(`button[data-rating="${rating}"]`);
  if (b) b.classList.add("suggested");
}

/* 朗读控件已迁移到 settings.html(F5) */

// ---- 热力图 ----
function renderHeatmap() {
  const cells = heatmapCells(18);
  // 颜色分档:按当天完成词数
  const level = (c) => c === 0 ? "" : c < 10 ? "l1" : c < 25 ? "l2" : c < 40 ? "l3" : "l4";
  heatmapEl.innerHTML = cells.map((c) => {
    const cls = ["cell", level(c.count), c.isToday ? "today" : "", c.completed ? "done" : ""]
      .filter(Boolean).join(" ");
    const title = `${c.date}：${c.count} 词${c.completed ? "（已完成）" : ""}`;
    return `<div class="${cls}" title="${title}"></div>`;
  }).join("");
  $("streak-days").textContent = currentStreak();
  $("total-words").textContent = totalWordsDone();
}

// ---- 今日任务概览 ----
function renderTodayOverview() {
  const rec = task.day;
  const reviewN = task.review.length;      // 当前仍到期的复习词(现算,会随完成/在别处复习而减少)
  const newDone = Math.max(0, rec.new_done || 0);
  const newLeft = Math.max(0, task.newWords.length - newDone); // 还没学的新词
  const done = rec.reviewed_done + rec.new_done;
  const planned = rec.planned;
  // “还能学的”= 现存到期复习 + 未学新词。这才是点“继续”后队列真正的长度,
  // 用它驱动按钮,避免出现“还剩 N 但点了没反应”(复习词在别处/今天已过,自过滤没了)。
  const studiable = reviewN + newLeft;
  $("today-date").textContent = formatDate(task.date);
  $("review-count").textContent = reviewN;
  $("new-count").textContent = newLeft;
  $("prog-fill").style.width = planned ? `${Math.round((done / planned) * 100)}%` : "0%";
  $("prog-txt").textContent = `今日已完成 ${done} / ${planned} 词`;
  const startBtn = $("start-btn");
  if (studiable === 0) {
    // 没有可学的词了。区分“今天做过” vs “本就无词”。
    startBtn.disabled = true;
    if (done > 0) {
      startBtn.textContent = "今日已完成 ✓";
      $("mini-note").textContent = "今天到期的复习和新词都过完了，格子已点亮。明天到期的复习会自动回来。";
    } else {
      startBtn.textContent = "今日无待学词 ✓";
      $("mini-note").textContent = "没有到期复习，新词也已学完当前批次。可去「词库」浏览，或等更多词上线。";
    }
  } else if (done > 0) {
    startBtn.disabled = false;
    startBtn.textContent = `继续今日任务（还剩 ${studiable}）→`;
  } else {
    startBtn.disabled = false;
    startBtn.textContent = "开始今日任务 →";
  }
}

function formatDate(key) {
  const [y, m, d] = key.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  const wk = "日一二三四五六"[dt.getDay()];
  return `${m}月${d}日 · 周${wk}`;
}

// 复习项可能来自生词库或内置词,统一取出展示所需字段
function wrapReviewEntry(r) {
  if (r.origin === "seed") {
    const s = seedIndex.get(r.word.toLowerCase());
    return s || null;
  }
  // vocab:从 localStorage 生词库取
  // 这里用 seedIndex 兜底不到,直接读生词库
  const v = (window.__vocabCache || []).find((x) => x.word.toLowerCase() === r.word.toLowerCase());
  return v || { word: r.word, def: "", aids: null };
}

// ---- 过词卡(B交互) ----
function showStudyCard() {
  if (!queue.length) { finishStudy(); return; }
  currentItem = queue[0];
  const entry = currentItem.entry;
  studyWrap.hidden = false;
  todayCard.hidden = true;
  doneCard.hidden = true;
  $("study-card").classList.remove("revealed");
  studySuggestedRating = null;
  clearStudySuggestion();

  const rec = task.day;
  const done = rec.reviewed_done + rec.new_done;
  $("study-progress").textContent =
    `${currentItem.kind === "review" ? "🔁 复习" : "✨ 新学"} · 今日 ${done + 1}/${rec.planned}`;
  $("study-top").innerHTML = currentItem.kind === "new"
    ? `<span class="study-badge new">新词</span>`
    : `<span class="study-badge review">复习</span>`;
  $("study-word").textContent = entry.word;
  $("study-pos").textContent = entry.pos || "";

  // 词根提示(B交互)
  const morphHTML = renderMorphemes(entry.aids);
  if (morphHTML) { $("study-hint-morph").innerHTML = morphHTML; $("study-hint").hidden = false; }
  else { $("study-hint").hidden = true; }

  // 释义 + 完整 aids(先隐藏)
  $("study-def").textContent = entry.def || "暂无释义";
  $("study-example").textContent = entry.sentence_en || "";
  $("study-aids").innerHTML = (aidsHasContent(entry.aids)
    ? renderAids(entry.aids, { skipMorphemes: true }) : "") + renderCollocations(entry.collocations);
  $("study-answer").hidden = true;
  $("study-actions").hidden = true;

  // 今日过词固定走「认词」流程(显示释义 + 记忆法 → 自评),不出拼写测试。
  // 拼写主动回忆仍保留在「复习」页(vocab.html 的 拼写/认词 切换)。
  const useSpell = false;
  const wordLine = $("study-card").querySelector(".review-word-line");
  if (useSpell) {
    wordLine.hidden = true;
    $("study-reveal").hidden = true;
    $("study-cloze").hidden = false;
    $("study-cloze-def").textContent = entry.def || "（凭词根/例句拼出这个词）";
    const bl = blankSentence(entry.sentence_en, entry.word);
    $("study-cloze-sentence").hidden = !bl.ok;
    if (bl.ok) $("study-cloze-sentence").innerHTML = bl.html;
    $("study-feedback").hidden = true;
    $("study-feedback").className = "cloze-feedback";
    $("study-input").value = "";
    $("study-input").disabled = false;
    $("study-submit").disabled = false;
    $("study-speak").disabled = true; // 别用发音泄露拼写
    setTimeout(() => $("study-input").focus(), 30);
  } else {
    wordLine.hidden = false;
    $("study-cloze").hidden = true;
    $("study-reveal").hidden = false;
    $("study-reveal").textContent = morphHTML ? "显示释义 + 记忆法" : "显示释义";
    $("study-speak").disabled = !speechSupported();
  }
}

// 拼写模式提交(今日过词):判分 → 反馈 → 亮答案 + 预选建议评分
function submitStudySpelling() {
  if (!currentItem || $("study-card").classList.contains("revealed")) return;
  const result = judgeSpelling($("study-input").value, currentItem.entry.word);
  studySuggestedRating = ratingFromResult(result);
  const fb = feedbackFor(result, currentItem.entry.word);
  $("study-feedback").innerHTML = fb.text;
  $("study-feedback").className = "cloze-feedback " + fb.cls;
  $("study-feedback").hidden = false;
  $("study-input").disabled = true;
  $("study-submit").disabled = true;
  $("study-card").classList.add("revealed");
  $("study-card").querySelector(".review-word-line").hidden = false;
  $("study-answer").hidden = false;
  $("study-actions").hidden = false;
  highlightStudyRating(studySuggestedRating);
  $("study-speak").disabled = !speechSupported();
}

$("study-reveal").addEventListener("click", () => {
  $("study-answer").hidden = false;
  $("study-actions").hidden = false;
  $("study-reveal").hidden = true;
});

// 拼写模式:提交 / 回车提交
$("study-submit").addEventListener("click", submitStudySpelling);
$("study-input").addEventListener("keydown", (ev) => {
  if (ev.key === "Enter") { ev.preventDefault(); submitStudySpelling(); }
});

$("study-speak").addEventListener("click", () => {
  if (!currentItem) return;
  const btn = $("study-speak");
  speakEnglish(currentItem.entry.word, {
    onstart: () => btn.classList.add("speaking"),
    onend: () => btn.classList.remove("speaking"),
    onerror: () => btn.classList.remove("speaking"),
  });
});

$("study-actions").addEventListener("click", (ev) => {
  const btn = ev.target.closest("button[data-rating]");
  if (!btn || !currentItem) return;
  const rating = btn.dataset.rating;
  gradeItem(currentItem, rating);
  // markWordDone 返回更新后的当天记录;同步回 task.day,避免用陈旧引用算进度
  const updated = markWordDone(currentItem.kind === "review" ? "review" : "new");
  if (updated) task.day = updated;
  // 复习词过完要从会话内 task.review 移除,否则回总览再点"继续"会重复入队(突破上限)
  noteItemDone(task, currentItem);
  queue.shift();
  refreshVocabCache();
  showStudyCard(); // 下一词(或结束)
});

// 评分路由:生词走 store.gradeReview;内置词走独立 SRS(共享 schedule + setSeedReview)
function gradeItem(item, rating) {
  const w = item.entry.word;
  if (item.origin === "vocab") {
    try { gradeReview(w, rating); } catch { /* 万一不在生词库,忽略 */ }
  } else {
    const { review } = schedule(getSeedReview(w), rating);
    setSeedReview(w, review);
  }
}

function finishStudy() {
  studyWrap.hidden = true;
  const rec = task.day;
  if (rec.reviewed_done + rec.new_done >= rec.planned && rec.planned > 0) {
    doneCard.hidden = false;
    $("done-msg").textContent = `今天过了 ${rec.planned} 词，格子已点亮。明天到期的复习会自动回来。`;
    renderHeatmap();
  } else {
    todayCard.hidden = false;
    renderTodayOverview();
    renderHeatmap();
  }
}

$("study-quit").addEventListener("click", () => {
  studyWrap.hidden = true; todayCard.hidden = false;
  renderTodayOverview(); renderHeatmap();
});
$("done-back").addEventListener("click", () => {
  doneCard.hidden = true; todayCard.hidden = false;
  renderTodayOverview();
});

// ---- 开始/继续 ----
$("start-btn").addEventListener("click", () => {
  refreshVocabCache();
  queue = buildQueue(task, wrapReviewEntry);
  if (!queue.length) { finishStudy(); return; }
  showStudyCard();
});

// ---- 节奏设置 ----
const paceModal = $("pace-modal");
$("pace-btn").addEventListener("click", () => {
  const s = getSettings();
  $("pace-custom-new").value = s.new_per_day;
  highlightPacePreset(s.new_per_day);
  paceModal.hidden = false;
});
$("pace-cancel").addEventListener("click", () => { paceModal.hidden = true; });
$("pace-list").addEventListener("click", (ev) => {
  const opt = ev.target.closest(".pace-opt");
  if (!opt) return;
  $("pace-custom-new").value = opt.dataset.new;
  highlightPacePreset(Number(opt.dataset.new));
});
function highlightPacePreset(n) {
  document.querySelectorAll(".pace-opt").forEach((o) =>
    o.classList.toggle("active", Number(o.dataset.new) === n));
}
$("pace-save").addEventListener("click", () => {
  const n = Math.max(0, Number($("pace-custom-new").value) || 0);
  updateSettings({ new_per_day: n });
  paceModal.hidden = true;
  // 若今天还没开始(done==0),重建今日任务以套用新配额;已开始则不冲掉进度。
  reloadTask({ rebuild: true });
});

// ---- 生词库缓存(过词卡取生词用) ----
function refreshVocabCache() {
  try {
    window.__vocabCache = JSON.parse(localStorage.getItem("ielts_vocab") || "[]");
  } catch { window.__vocabCache = []; }
}

// ---- 初始化 / 刷新 ----
// rebuild=true:套用最新任务设置重排当天(仅未开始时真正换词);默认复原,保持幂等。
async function reloadTask({ rebuild = false } = {}) {
  task = rebuild ? await rebuildTodayTask() : await ensureTodayTask();
  renderTodayOverview();
  renderHeatmap();
}

(async function init() {
  const seed = await loadSeed();
  seedIndex = new Map((seed.words || []).map((w) => [w.word.toLowerCase(), w]));
  refreshVocabCache();
  await reloadTask();
})();
