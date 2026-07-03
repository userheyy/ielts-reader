import { loadAll, removeWord, exportJSON, importJSON, pickReviewWord, gradeReview, getReviewStats } from "./store.js?v=5";
import { bindProfileBackupUI } from "./profile-backup.js";
import { initSpeechControls, speakEnglish, speechSupported } from "./speech.js?v=6";

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
let currentReviewWord = null;
let sessionReviewed = 0;
let sessionRemembered = 0;
let rolling = false;

initSpeechControls(
  document.getElementById("speech-voice"),
  document.getElementById("speech-rate"),
  document.getElementById("speech-stop"),
);

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
  reviewCard.classList.remove("idle", "rolling", "revealed");
  reviewWord.textContent = entry.word;
  reviewPos.textContent = entry.pos || "";
  reviewDef.textContent = entry.def || "暂无释义";
  reviewExample.textContent = entry.sentence_en || "";
  reviewAnswer.hidden = true;
  reviewActions.hidden = true;
  revealButton.hidden = false;
  revealButton.disabled = false;
  speakReviewButton.disabled = !speechSupported();
  reviewProgress.textContent = `本轮 ${sessionReviewed} 词 · 记住 ${sessionRemembered} 词`;
}

function rollNext() {
  if (rolling) return;
  const list = loadAll();
  if (!list.length) {
    reviewWord.textContent = "生词库还是空的";
    reviewProgress.textContent = "阅读文章时点击单词即可入库";
    speakReviewButton.disabled = true;
    return;
  }
  rolling = true;
  reviewCard.classList.add("rolling");
  reviewActions.hidden = true;
  reviewAnswer.hidden = true;
  revealButton.disabled = true;
  speakReviewButton.disabled = true;
  let tick = 0;
  const ticker = setInterval(() => {
    reviewWord.textContent = list[Math.floor(Math.random() * list.length)].word;
    tick += 1;
    if (tick >= 10) {
      clearInterval(ticker);
      rolling = false;
      showReviewWord(pickReviewWord(currentReviewWord?.word || ""));
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
reviewActions.addEventListener("click", (ev) => {
  const button = ev.target.closest("button[data-rating]");
  if (!button || !currentReviewWord) return;
  const rating = button.dataset.rating;
  gradeReview(currentReviewWord.word, rating);
  sessionReviewed += 1;
  if (rating === "remembered") sessionRemembered += 1;
  renderReviewStats();
  rollNext();
});

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
    tr.innerHTML = `
      <td><button class="speak-vocab-word" data-word="${escapeAttr(e.word)}" title="朗读 ${escapeAttr(e.word)}" ${speechSupported() ? "" : "disabled"}>🔊</button>${e.word} <span style="color:#999">${e.pos || ""}</span></td>
      <td>${e.def || ""}</td>
      <td>${e.sentence_en || ""}</td>
      <td>${srcCell}</td>
      <td>${e.added_at || ""}</td>
      <td><span class="del" data-word="${e.word}">删除</span></td>`;
    tr.querySelector(".del").addEventListener("click", () => {
      removeWord(e.word);
      render(searchEl.value);
    });
    rowsEl.appendChild(tr);
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
