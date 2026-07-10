import { loadAll, removeWord, exportJSON, importJSON, gradeReview, getReviewStats } from "./store.js?v=7";
import { bindProfileBackupUI } from "./profile-backup.js";
import {speakEnglish, speechSupported} from "./speech.js?v=6";
import { renderAids, renderMorphemes, aidsHasContent, renderCollocations } from "./aids.js?v=2";
import { buildReviewPool, setSeedReview, getSeedReview } from "./seed.js?v=3";
import { judgeSpelling, ratingFromResult, blankSentence, feedbackFor } from "./cloze.js?v=1";
import { schedule } from "./srs.js?v=1";

const rowsEl = document.getElementById("rows");
const countEl = document.getElementById("count");
const emptyEl = document.getElementById("empty");
const searchEl = document.getElementById("search");
const reviewCard = document.getElementById("review-card");
const reviewWord = document.getElementById("review-word");
const reviewPos = document.getElementById("review-pos");
const reviewAnswer = document.getElementById("review-answer");
const reviewDef = document.getElementById("review-def");
const reviewExample = document.getElementById("review-example");
const reviewProgress = document.getElementById("review-progress");
const revealButton = document.getElementById("reveal-answer");
const reviewActions = document.getElementById("review-actions");
const speakReviewButton = document.getElementById("speak-review-word");
const reviewHint = document.getElementById("review-hint");
const reviewHintMorph = document.getElementById("review-hint-morph");
const reviewAids = document.getElementById("review-aids");
const reviewWordLine = reviewCard.querySelector(".review-word-line");
const reviewModeEl = document.getElementById("review-mode");
const reviewCloze = document.getElementById("review-cloze");
const reviewClozeDef = document.getElementById("review-cloze-def");
const reviewClozeSentence = document.getElementById("review-cloze-sentence");
const reviewInput = document.getElementById("review-input");
const reviewSubmit = document.getElementById("review-submit");
const reviewFeedback = document.getElementById("review-feedback");
let currentReviewWord = null;
let sessionReviewed = 0;
let sessionRemembered = 0;
let rolling = false;
let reviewPool = []; // 复习池:生词 ∪ 已加入的内置词(异步构建)
let suggestedRating = null; // 拼写判分给出的建议评分

// 复习方式:'spell'(拼写/主动回忆,默认) | 'recall'(认词)。存 localStorage。
const MODE_KEY = "ielts_review_mode";
let spellMode = (localStorage.getItem(MODE_KEY) || "spell") === "spell";
function applyModeUI() {
  reviewModeEl?.querySelectorAll("button").forEach((b) =>
    b.classList.toggle("active", (b.dataset.mode === "spell") === spellMode));
}
function clearRatingSuggestion() {
  reviewActions.querySelectorAll("button").forEach((b) => b.classList.remove("suggested"));
}
function highlightRating(rating) {
  clearRatingSuggestion();
  const b = rating && reviewActions.querySelector(`button[data-rating="${rating}"]`);
  if (b) b.classList.add("suggested");
}

async function refreshReviewPool() {
  reviewPool = await buildReviewPool();
  return reviewPool;
}

// 从池中按权重抽词(复用 store 的 pickReviewWord 权重逻辑,但作用于合并池)。
// pickReviewWord 只认 localStorage 生词,故这里自实现同样的加权抽取覆盖整个池。
function pickFromPool(excludeWord = "") {
  const pool = reviewPool.length > 1
    ? reviewPool.filter((e) => e.word.toLowerCase() !== excludeWord.toLowerCase())
    : reviewPool;
  if (!pool.length) return null;
  const weighted = pool.map((entry) => ({ entry, weight: poolWeight(entry) }));
  const total = weighted.reduce((n, x) => n + x.weight, 0);
  let cursor = Math.random() * total;
  for (const item of weighted) {
    cursor -= item.weight;
    if (cursor <= 0) return item.entry;
  }
  return weighted[weighted.length - 1].entry;
}

// 与 store.reviewWeight 同款的轻量记忆曲线权重(此处直接读 entry.review)
function poolWeight(entry, now = new Date()) {
  const r = entry.review || {};
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const due = r.next_due ? new Date(`${r.next_due}T00:00:00`) : null;
  const days = due ? Math.round((today - due) / 86400000) : 0;
  const correct = Number(r.correct) || 0, wrong = Number(r.wrong) || 0, fuzzy = Number(r.fuzzy) || 0;
  const total = correct + wrong + fuzzy;
  const errorRate = (wrong + fuzzy * 0.55) / Math.max(1, total);
  const dueScore = !due ? 5 : days >= 0 ? 3 + Math.min(8, days) : 0.35 / (1 + Math.abs(days));
  const newScore = total === 0 ? 4 : 0;
  const difficultyScore = errorRate * 9 + Math.min(5, (Number(r.lapses) || 0) * 0.8);
  const levelScore = Math.max(0, 3 - (Number(r.level) || 0) * 0.45);
  return Math.max(0.15, dueScore + newScore + difficultyScore + levelScore);
}

/* 朗读控件已迁移到 settings.html(F5) */

function speakWord(word, button) {
  if (!word) return;
  speakEnglish(word, {
    onstart: () => button?.classList.add("speaking"),
    onend: () => button?.classList.remove("speaking"),
    onerror: () => button?.classList.remove("speaking"),
  });
}

function escapeAttr(value) {
  return String(value || "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}

function renderReviewStats() {
  const s = getReviewStats();
  document.getElementById("review-stats").innerHTML = `
    <span><b>${s.due}</b> 今日待复习</span>
    <span><b>${s.difficult}</b> 高频错词</span>
    <span><b>${s.total}</b> 总词数</span>`;
}

function showReviewWord(entry) {
  currentReviewWord = entry;
  suggestedRating = null;
  reviewCard.classList.remove("idle", "rolling", "revealed");
  reviewWord.textContent = entry.word;
  reviewPos.textContent = entry.pos || "";
  reviewDef.textContent = entry.def || "暂无释义";
  reviewExample.textContent = entry.sentence_en || "";
  // B 交互:有词根拆解时,先只给词根提示,引导靠词根推词义
  const morphHTML = renderMorphemes(entry.aids);
  if (morphHTML) {
    reviewHintMorph.innerHTML = morphHTML;
    reviewHint.hidden = false;
  } else {
    reviewHint.hidden = true;
  }
  // 显示区(释义 + 完整记忆法)先隐藏,点"显示"才亮
  reviewAids.innerHTML = (aidsHasContent(entry.aids)
    ? renderAids(entry.aids, { skipMorphemes: true }) // 词根已在提示区,正文跳过避免重复
    : "") + renderCollocations(entry.collocations);
  reviewAnswer.hidden = true;
  reviewActions.hidden = true;
  clearRatingSuggestion();

  if (spellMode) {
    // 拼写模式:藏单词,给中文释义 + 挖空例句,让你打出这个词(主动产出更牢)
    reviewWordLine.hidden = true;
    revealButton.hidden = true;
    reviewCloze.hidden = false;
    reviewClozeDef.textContent = entry.def || "（凭词根/例句拼出这个词）";
    const bl = blankSentence(entry.sentence_en, entry.word);
    reviewClozeSentence.hidden = !bl.ok;
    if (bl.ok) reviewClozeSentence.innerHTML = bl.html;
    reviewFeedback.hidden = true;
    reviewFeedback.className = "cloze-feedback";
    reviewInput.value = "";
    reviewInput.disabled = false;
    reviewSubmit.disabled = false;
    speakReviewButton.disabled = true; // 别用发音泄露拼写
    setTimeout(() => reviewInput.focus(), 30);
  } else {
    // 认词模式(原行为):亮单词,点"显示"翻答案
    reviewWordLine.hidden = false;
    reviewCloze.hidden = true;
    revealButton.hidden = false;
    revealButton.disabled = false;
    revealButton.textContent = morphHTML ? "显示释义 + 记忆法" : "显示释义";
    speakReviewButton.disabled = !speechSupported();
  }
  reviewProgress.textContent = `本轮 ${sessionReviewed} 词 · 记住 ${sessionRemembered} 词`;
}

// 拼写模式提交:判分 → 反馈 → 亮答案 + 预选建议评分(用户仍可改)
function submitSpelling() {
  if (!currentReviewWord || reviewCard.classList.contains("revealed")) return;
  const result = judgeSpelling(reviewInput.value, currentReviewWord.word);
  suggestedRating = ratingFromResult(result);
  const fb = feedbackFor(result, currentReviewWord.word);
  reviewFeedback.innerHTML = fb.text;
  reviewFeedback.className = "cloze-feedback " + fb.cls;
  reviewFeedback.hidden = false;
  reviewInput.disabled = true;
  reviewSubmit.disabled = true;
  reviewCard.classList.add("revealed");
  reviewWordLine.hidden = false; // 现在把正确单词亮出来
  reviewAnswer.hidden = false;
  reviewActions.hidden = false;
  highlightRating(suggestedRating);
  speakReviewButton.disabled = !speechSupported();
}

async function rollNext() {
  if (rolling) return;
  await refreshReviewPool();
  const list = reviewPool;
  if (!list.length) {
    reviewWord.textContent = "复习池还是空的";
    reviewProgress.textContent = "阅读时点词入库,或到「词库」加入雅思核心词";
    reviewHint.hidden = true;
    reviewAids.innerHTML = "";
    speakReviewButton.disabled = true;
    return;
  }
  rolling = true;
  reviewCard.classList.add("rolling");
  reviewActions.hidden = true;
  reviewAnswer.hidden = true;
  reviewHint.hidden = true;
  reviewCloze.hidden = true;      // 抽词动画期间收起拼写面板
  reviewWordLine.hidden = false;  // 露出单词行做"老虎机"滚动
  clearRatingSuggestion();
  revealButton.disabled = true;
  speakReviewButton.disabled = true;
  let tick = 0;
  const ticker = setInterval(() => {
    reviewWord.textContent = list[Math.floor(Math.random() * list.length)].word;
    tick += 1;
    if (tick >= 10) {
      clearInterval(ticker);
      rolling = false;
      showReviewWord(pickFromPool(currentReviewWord?.word || ""));
    }
  }, 55 + tick * 8);
}

document.getElementById("start-review").addEventListener("click", rollNext);
speakReviewButton.addEventListener("click", () => {
  if (!currentReviewWord) return;
  speakWord(currentReviewWord.word, speakReviewButton);
});
revealButton.addEventListener("click", () => {
  if (!currentReviewWord) return;
  reviewCard.classList.add("revealed");
  reviewAnswer.hidden = false;
  reviewActions.hidden = false;
  revealButton.hidden = true;
});

// 拼写模式:提交 / 回车提交
reviewSubmit.addEventListener("click", submitSpelling);
reviewInput.addEventListener("keydown", (ev) => {
  if (ev.key === "Enter") { ev.preventDefault(); submitSpelling(); }
});
// 复习方式切换(拼写 / 认词);切换后若正在出题(未翻答案)则按新模式重出
reviewModeEl.addEventListener("click", (ev) => {
  const b = ev.target.closest("button[data-mode]");
  if (!b) return;
  const next = b.dataset.mode === "spell";
  if (next === spellMode) return;
  spellMode = next;
  localStorage.setItem(MODE_KEY, spellMode ? "spell" : "recall");
  applyModeUI();
  if (currentReviewWord && !rolling && !reviewCard.classList.contains("revealed")) {
    showReviewWord(currentReviewWord);
  }
});
applyModeUI();
reviewActions.addEventListener("click", (ev) => {
  const button = ev.target.closest("button[data-rating]");
  if (!button || !currentReviewWord) return;
  const rating = button.dataset.rating;
  gradePoolWord(currentReviewWord, rating);
  sessionReviewed += 1;
  if (rating === "remembered") sessionRemembered += 1;
  renderReviewStats();
  rollNext();
});

// 评分:生词走 store.gradeReview(写 localStorage 生词库);
// 纯内置词(未被点成生词)把 SRS 状态写到 seed 独立存储,避免"生词不存在"报错。
function gradePoolWord(entry, rating) {
  if (entry._origin === "vocab") {
    gradeReview(entry.word, rating);
  } else {
    // 内置词:同一套调度(FSRS/梯度),结果存到 seed_review 独立存储
    const { review } = schedule(getSeedReview(entry.word), rating);
    setSeedReview(entry.word, review);
  }
}

function render(filter = "") {
  const all = loadAll().slice().sort((a, b) => (b.added_at || "").localeCompare(a.added_at || ""));
  const f = filter.trim().toLowerCase();
  const list = f
    ? all.filter((e) => e.word.toLowerCase().includes(f) || (e.source || "").toLowerCase().includes(f))
    : all;
  rowsEl.innerHTML = "";
  emptyEl.style.display = all.length === 0 ? "block" : "none";
  for (const e of list) {
    const tr = document.createElement("tr");
    const srcCell = e.passage_id
      ? `<span class="src-link" data-pid="${e.passage_id}" data-sid="${e.sentence_id ?? ""}">${e.source}</span>`
      : (e.source || "");
    const hasAids = aidsHasContent(e.aids);
    const aidsBtn = hasAids
      ? `<button class="aids-expand-btn" data-word="${escapeAttr(e.word)}">🧠 记忆法</button>`
      : `<button class="aids-expand-btn empty" data-word="${escapeAttr(e.word)}" title="备份生词给 Claude 回填后即可查看">+ 补记忆法</button>`;
    tr.innerHTML = `
      <td><button class="speak-vocab-word" data-word="${escapeAttr(e.word)}" title="朗读 ${escapeAttr(e.word)}" ${speechSupported() ? "" : "disabled"}>🔊</button>${e.word} <span style="color:#999">${e.pos || ""}</span></td>
      <td>${e.def || ""}</td>
      <td>${aidsBtn}</td>
      <td>${srcCell}</td>
      <td>${e.added_at || ""}</td>
      <td><span class="del" data-word="${e.word}">删除</span></td>`;
    tr.querySelector(".del").addEventListener("click", () => {
      removeWord(e.word);
      render(searchEl.value);
    });
    rowsEl.appendChild(tr);
    // 展开行(默认隐藏),点"记忆法"按钮切换
    if (hasAids) {
      const aidsTr = document.createElement("tr");
      aidsTr.className = "vocab-aids-row";
      aidsTr.hidden = true;
      aidsTr.innerHTML = `<td colspan="6">${renderAids(e.aids)}</td>`;
      const btn = tr.querySelector(".aids-expand-btn");
      btn.addEventListener("click", () => {
        aidsTr.hidden = !aidsTr.hidden;
        btn.classList.toggle("open", !aidsTr.hidden);
      });
      rowsEl.appendChild(aidsTr);
    }
  }
  countEl.textContent = `共 ${all.length} 个生词`;
  renderReviewStats();
}

rowsEl.addEventListener("click", (ev) => {
  const speak = ev.target.closest(".speak-vocab-word");
  if (speak) {
    ev.preventDefault();
    ev.stopPropagation();
    speakWord(speak.dataset.word, speak);
    return;
  }
  const del = ev.target.closest(".del");
  if (del) return;
  const link = ev.target.closest(".src-link");
  if (link) {
    const pid = link.dataset.pid, sid = link.dataset.sid;
    location.href = `reader.html?id=${encodeURIComponent(pid)}${sid ? `&sentence=${sid}` : ""}`;
  }
});

searchEl.addEventListener("input", () => render(searchEl.value));

document.getElementById("export").addEventListener("click", () => {
  const blob = new Blob([exportJSON()], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ielts-vocab.json";
  a.click();
});

document.getElementById("import").addEventListener("change", async (ev) => {
  const file = ev.target.files[0];
  if (!file) return;
  const text = await file.text();
  try {
    const r = importJSON(text);
    alert(`导入成功,现共 ${r.total} 个生词。`);
    render(searchEl.value);
  } catch (e) {
    alert("导入失败:" + e.message);
  }
  ev.target.value = "";
});

bindProfileBackupUI({
  exportButtonId: "profile-export",
  importInputId: "profile-import",
  onRestored: () => render(searchEl.value),
});

render();
