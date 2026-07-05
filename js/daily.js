// 每日单词页控制器:日历热力图 + 今日任务卡 + 过词(B交互) + 节奏设置。
import { renderAids, renderMorphemes, aidsHasContent } from "./aids.js?v=1";
import { gradeReview } from "./store.js?v=6";
import { loadSeed, getSeedReview, setSeedReview } from "./seed.js?v=1";
import {speakEnglish, speechSupported} from "./speech.js?v=6";
import {
  ensureTodayTask, markWordDone, heatmapCells, currentStreak, totalWordsDone,
  getSettings, updateSettings, dateKey,
} from "./daily-store.js?v=1";

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
  const reviewN = task.review.length;
  const newN = task.newWords.length;
  const done = rec.reviewed_done + rec.new_done;
  const planned = rec.planned;
  $("today-date").textContent = formatDate(task.date);
  $("review-count").textContent = reviewN;
  $("new-count").textContent = newN;
  $("prog-fill").style.width = planned ? `${Math.round((done / planned) * 100)}%` : "0%";
  $("prog-txt").textContent = `今日已完成 ${done} / ${planned} 词`;
  const startBtn = $("start-btn");
  if (planned === 0) {
    startBtn.disabled = true;
    startBtn.textContent = "今日无待学词 ✓";
    $("mini-note").textContent = "没有到期复习，新词也已学完当前批次。可去「词库」浏览，或等更多词上线。";
  } else if (done >= planned) {
    startBtn.disabled = false;
    startBtn.textContent = "今日已完成，再过一遍 →";
  } else if (done > 0) {
    startBtn.disabled = false;
    startBtn.textContent = `继续今日任务（还剩 ${planned - done}）→`;
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

// ---- 构建过词队列(复习优先) ----
function buildQueue() {
  const rec = task.day;
  const q = [];
  // 复习词:从当前到期列表里,取"还没在今天完成计数覆盖"的。
  // 简化:每次进入学习都按 (planned - done) 现取现排;复习先、新词后。
  // 复习项
  for (const r of task.review) {
    const entry = wrapReviewEntry(r);
    if (entry) q.push({ entry, kind: "review", origin: r.origin });
  }
  // 新词项
  for (const s of task.newWords) {
    q.push({ entry: s, kind: "new", origin: "seed" });
  }
  // 跳过已完成的数量(reviewed_done + new_done),让"继续"从断点开始
  const skip = rec.reviewed_done + rec.new_done;
  return q.slice(skip);
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
  $("study-aids").innerHTML = aidsHasContent(entry.aids)
    ? renderAids(entry.aids, { skipMorphemes: true }) : "";
  $("study-answer").hidden = true;
  $("study-actions").hidden = true;
  $("study-reveal").hidden = false;
  $("study-reveal").textContent = morphHTML ? "显示释义 + 记忆法" : "显示释义";
  $("study-speak").disabled = !speechSupported();
}

$("study-reveal").addEventListener("click", () => {
  $("study-answer").hidden = false;
  $("study-actions").hidden = false;
  $("study-reveal").hidden = true;
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
  queue.shift();
  refreshVocabCache();
  showStudyCard(); // 下一词(或结束)
});

// 评分路由:生词走 store.gradeReview;内置词走独立 SRS(computeReview + setSeedReview)
function gradeItem(item, rating) {
  const w = item.entry.word;
  if (item.origin === "vocab") {
    try { gradeReview(w, rating); } catch { /* 万一不在生词库,忽略 */ }
  } else {
    const cur = getSeedReview(w) || { level: 0, next_due: null, history: [] };
    setSeedReview(w, computeReview(cur, rating));
  }
}

// 与 store.gradeReview 同款记忆曲线(不依赖 localStorage 生词库),供内置词用
function computeReview(review, rating, now = new Date()) {
  const r = {
    level: Number(review.level) || 0, next_due: review.next_due || null,
    history: Array.isArray(review.history) ? review.history.slice() : [],
    correct: Number(review.correct) || 0, wrong: Number(review.wrong) || 0,
    fuzzy: Number(review.fuzzy) || 0, streak: Number(review.streak) || 0,
    lapses: Number(review.lapses) || 0,
  };
  const day = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  let interval = 0;
  if (rating === "forgot") { r.wrong += 1; r.lapses += 1; r.streak = 0; r.level = Math.max(0, r.level - 2); }
  else if (rating === "fuzzy") { r.fuzzy += 1; r.streak = 0; r.level = Math.max(0, r.level - 1); interval = 1; }
  else if (rating === "remembered") { r.correct += 1; r.streak += 1; r.level = Math.min(7, r.level + 1); interval = [0,1,3,7,14,30,60,120][r.level]; }
  day.setDate(day.getDate() + interval);
  r.next_due = dateKey(day);
  r.history.push({ date: now.toISOString(), rating, level: r.level, interval });
  if (r.history.length > 100) r.history = r.history.slice(-100);
  return r;
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
  queue = buildQueue();
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
  // 若今天还没开始(done==0),重建今日任务以套用新配额
  reloadTask();
});

// ---- 生词库缓存(过词卡取生词用) ----
function refreshVocabCache() {
  try {
    window.__vocabCache = JSON.parse(localStorage.getItem("ielts_vocab") || "[]");
  } catch { window.__vocabCache = []; }
}

// ---- 初始化 / 刷新 ----
async function reloadTask() {
  task = await ensureTodayTask();
  renderTodayOverview();
  renderHeatmap();
}

(async function init() {
  const seed = await loadSeed();
  seedIndex = new Map((seed.words || []).map((w) => [w.word.toLowerCase(), w]));
  refreshVocabCache();
  await reloadTask();
})();
