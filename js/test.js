// 单词测试(完形填空)主逻辑。
// 一组 10 题。每题：题库句挖空 + 4 选项(正确词 + 题库随机 3 干扰词，运行时抽、打乱)。
// 选完→解析(完整句/翻译/为什么选它/四词释义)。题干非空词悬停查 dict.json。
// 对错记入独立错题本(test-store.js)，可只考错题、连续 2 次答对移出。

import { ensureDict, lookup } from "./dict.js?v=1";
import { recordResult, wrongWords, wrongCount, summary } from "./test-store.js?v=1";
import { initSpeechControls, speakEnglish, speechSupported } from "./speech.js?v=6";

const GROUP_SIZE = 10;
const BANK_URL = "data/quiz-bank.json";

// ---- DOM ----
const setupEl = document.getElementById("setup");
const quizEl = document.getElementById("quiz");
const resultEl = document.getElementById("result");
const noticeEl = document.getElementById("notice");

const startBtn = document.getElementById("start-normal");
const startWrongBtn = document.getElementById("start-wrong");
const statSummaryEl = document.getElementById("stat-summary");

const progressEl = document.getElementById("q-progress");
const scoreEl = document.getElementById("q-score");
const barEl = document.getElementById("q-bar");
const stemEl = document.getElementById("q-stem");
const optionsEl = document.getElementById("q-options");
const explainEl = document.getElementById("q-explain");
const nextBtn = document.getElementById("q-next");

initSpeechControls(
  document.getElementById("speech-voice"),
  document.getElementById("speech-rate"),
  document.getElementById("speech-stop"),
);

// ---- 状态 ----
let BANK = [];            // 题库 [{word,pos,sentence,sentence_zh,explain}]
let bankByWord = new Map();
let session = null;       // { items:[题], idx, right, wrong, mode:'normal'|'wrong', missed:[] }

// ---- 工具 ----
function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function sample(arr, n) { return shuffle(arr).slice(0, n); }
function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// ---- 加载题库 ----
async function loadBank() {
  try {
    const res = await fetch(BANK_URL, { cache: "no-cache" });
    if (!res.ok) throw new Error("no bank");
    const data = await res.json();
    BANK = Array.isArray(data.questions) ? data.questions : [];
  } catch {
    BANK = [];
  }
  bankByWord = new Map(BANK.map((q) => [q.word.toLowerCase(), q]));
}

// ---- 首页统计 + 按钮态 ----
function renderSetup() {
  const s = summary();
  statSummaryEl.innerHTML = s.testedWords
    ? `累计考过 <b>${s.testedWords}</b> 词 · 正确率 <b>${s.accuracy == null ? "—" : Math.round(s.accuracy * 100) + "%"}</b> · 错题本 <b>${s.wrongCount}</b> 词`
    : `还没有测试记录，开始第一组吧。`;
  const wc = wrongCount();
  startWrongBtn.disabled = wc === 0;
  startWrongBtn.textContent = wc ? `重做错题（${wc}）` : "重做错题（0）";
}

// 题库不可用时的提示；返回 true 表示可以出题
function bankReady() {
  if (BANK.length === 0) {
    noticeEl.hidden = false;
    noticeEl.textContent = "题库准备中。生成 data/quiz-bank.json 后即可开始测试。";
    startBtn.disabled = true;
    return false;
  }
  if (BANK.length < 4) {
    noticeEl.hidden = false;
    noticeEl.textContent = `题库当前只有 ${BANK.length} 题，凑不齐四个选项，暂无法测试。`;
    startBtn.disabled = true;
    return false;
  }
  noticeEl.hidden = true;
  startBtn.disabled = false;
  return true;
}

// ---- 组卷 ----
function buildQuestion(q) {
  // 干扰项：题库里其它词随机抽 3 个(按 word 去重)
  const pool = BANK.filter((x) => x.word.toLowerCase() !== q.word.toLowerCase());
  const distractors = sample(pool, 3).map((x) => x.word);
  const options = shuffle([q.word, ...distractors]);
  return { q, options, answered: false, picked: null };
}

function startSession(mode) {
  let words;
  if (mode === "wrong") {
    const ww = wrongWords().map((w) => w.toLowerCase());
    words = BANK.filter((q) => ww.includes(q.word.toLowerCase()));
    words = shuffle(words).slice(0, GROUP_SIZE);
    if (words.length === 0) return; // 保险：错题本空
  } else {
    words = sample(BANK, Math.min(GROUP_SIZE, BANK.length));
  }
  session = {
    items: words.map(buildQuestion),
    idx: 0,
    right: 0,
    wrong: 0,
    mode,
    missed: [],
  };
  setupEl.hidden = true;
  resultEl.hidden = true;
  quizEl.hidden = false;
  ensureDict(); // 预热词典，供题干悬停
  renderQuestion();
}

// ---- 渲染题干(挖空 + 非空词悬停查词) ----
function renderStem(sentence) {
  stemEl.innerHTML = "";
  // 按 ___ 切分，空位用下划线块；其余按词包 <span> 以便悬停
  const parts = sentence.split(/(_{2,})/g);
  for (const part of parts) {
    if (/^_{2,}$/.test(part)) {
      const blank = document.createElement("span");
      blank.className = "q-blank";
      blank.textContent = "";
      stemEl.appendChild(blank);
    } else {
      // 把普通文本按"词 / 非词"切，词加悬停
      const tokens = part.split(/([A-Za-z][A-Za-z'’-]*)/g);
      for (const tk of tokens) {
        if (/^[A-Za-z]/.test(tk)) {
          const w = document.createElement("span");
          w.className = "q-word";
          w.textContent = tk;
          attachHover(w, tk);
          stemEl.appendChild(w);
        } else if (tk) {
          stemEl.appendChild(document.createTextNode(tk));
        }
      }
    }
  }
}

let hoverTip = null;
function closeHover() { if (hoverTip) { hoverTip.remove(); hoverTip = null; } }
function attachHover(el, word) {
  el.addEventListener("mouseenter", async () => {
    await ensureDict();
    const def = lookup(word);
    closeHover();
    hoverTip = document.createElement("div");
    hoverTip.className = "q-tip";
    hoverTip.innerHTML = def
      ? `<span class="q-tip-w">${esc(def.w)}</span>${def.phonetic ? `<span class="q-tip-ph">/${esc(def.phonetic)}/</span>` : ""}<div class="q-tip-def">${esc(def.def)}</div>`
      : `<span class="q-tip-w">${esc(word)}</span><div class="q-tip-def" style="color:#999">暂无释义</div>`;
    document.body.appendChild(hoverTip);
    const r = el.getBoundingClientRect();
    hoverTip.style.left = Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - 260) + "px";
    hoverTip.style.top = (window.scrollY + r.bottom + 4) + "px";
  });
  el.addEventListener("mouseleave", closeHover);
}

// ---- 渲染当前题 ----
function renderQuestion() {
  const item = session.items[session.idx];
  const total = session.items.length;
  progressEl.textContent = `第 ${session.idx + 1} / ${total} 题${session.mode === "wrong" ? " · 错题模式" : ""}`;
  scoreEl.textContent = `✅ ${session.right}　❌ ${session.wrong}`;
  barEl.style.width = `${(session.idx / total) * 100}%`;

  renderStem(item.q.sentence);
  explainEl.hidden = true;
  explainEl.innerHTML = "";
  nextBtn.hidden = true;

  optionsEl.innerHTML = "";
  item.options.forEach((word, i) => {
    const letter = "ABCD"[i];
    const btn = document.createElement("button");
    btn.className = "q-option";
    btn.innerHTML = `<b>${letter}</b><span>${esc(word)}</span>`;
    btn.addEventListener("click", () => pick(item, word, btn));
    optionsEl.appendChild(btn);
  });
}

// ---- 作答 ----
async function pick(item, word, btn) {
  if (item.answered) return;
  item.answered = true;
  item.picked = word;
  const correct = word.toLowerCase() === item.q.word.toLowerCase();
  if (correct) session.right += 1; else { session.wrong += 1; session.missed.push(item.q); }
  recordResult(item.q.word, correct, session.mode === "wrong");
  scoreEl.textContent = `✅ ${session.right}　❌ ${session.wrong}`;

  // 标记选项对错
  Array.from(optionsEl.children).forEach((b) => {
    const w = b.querySelector("span").textContent;
    b.classList.add("locked");
    if (w.toLowerCase() === item.q.word.toLowerCase()) b.classList.add("right");
    else if (w === word) b.classList.add("wrong");
    else b.classList.add("dim");
  });

  await renderExplain(item);
  nextBtn.hidden = false;
  nextBtn.textContent = session.idx === session.items.length - 1 ? "查看结果 →" : "下一题 →";
}

async function renderExplain(item) {
  await ensureDict();
  const q = item.q;
  // 完整句(填回正确词并高亮)
  const filled = q.sentence.replace(/_{2,}/, `<b class="q-fill">${esc(q.word)}</b>`);
  // 四词释义：答案词优先用题库精炼释义(def)，带词性；查不到回退 dict。干扰词用 dict。
  const defs = item.options.map((w) => {
    const isAns = w.toLowerCase() === q.word.toLowerCase();
    const d = lookup(w);
    let text;
    if (isAns && q.def) {
      text = (q.pos ? q.pos + " " : "") + q.def;
    } else {
      text = d ? d.def : "暂无释义";
    }
    return `<div class="${isAns ? "q-def-ans" : ""}"><b>${esc(w)}</b> ${esc(text)}</div>`;
  }).join("");

  explainEl.innerHTML = `
    <div class="q-sentence">
      <div class="q-en">${filled}</div>
      <div class="q-zh">${esc(q.sentence_zh || "")}</div>
    </div>
    <div class="q-why">
      <div class="q-why-label">为什么选 ${esc(q.word)}</div>
      <div class="q-why-text">${esc(q.explain || "")}</div>
    </div>
    <div class="q-defs">${defs}</div>
  `;
  explainEl.hidden = false;

  // 让完整句里的正确词也能发音
  const speakWrap = document.createElement("div");
  speakWrap.className = "q-speak";
  const sb = document.createElement("button");
  sb.type = "button";
  sb.className = "q-speak-btn";
  sb.textContent = "🔊 读单词";
  sb.disabled = !speechSupported();
  sb.addEventListener("click", () => speakEnglish(q.word));
  speakWrap.appendChild(sb);
  explainEl.querySelector(".q-sentence").appendChild(speakWrap);
}

// ---- 下一题 / 结果 ----
nextBtn.addEventListener("click", () => {
  closeHover();
  if (session.idx < session.items.length - 1) {
    session.idx += 1;
    renderQuestion();
  } else {
    showResult();
  }
});

function showResult() {
  quizEl.hidden = true;
  resultEl.hidden = false;
  const total = session.items.length;
  const pct = Math.round((session.right / total) * 100);
  const missedHtml = session.missed.length
    ? session.missed.map((q) => {
        const d = lookup(q.word);
        return `<li><b>${esc(q.word)}</b> <span>${esc(d ? d.def : (q.pos || ""))}</span></li>`;
      }).join("")
    : `<li class="q-none">全对，没有错题 🎉</li>`;

  resultEl.querySelector("#r-score").innerHTML = `${session.right} <span>/ ${total}</span>`;
  resultEl.querySelector("#r-pct").textContent = `正确率 ${pct}%`;
  resultEl.querySelector("#r-missed").innerHTML = missedHtml;

  // 结果页也刷新错题按钮态
  const wc = wrongCount();
  const rWrongBtn = resultEl.querySelector("#r-again-wrong");
  rWrongBtn.disabled = wc === 0;
  rWrongBtn.textContent = wc ? `重做错题（${wc}）` : "重做错题（0）";
}

// ---- 结果页按钮 ----
resultEl.querySelector("#r-again").addEventListener("click", () => startSession("normal"));
resultEl.querySelector("#r-again-wrong").addEventListener("click", () => { if (wrongCount()) startSession("wrong"); });
resultEl.querySelector("#r-back").addEventListener("click", () => {
  resultEl.hidden = true;
  setupEl.hidden = false;
  renderSetup();
});

// ---- 首页按钮 ----
startBtn.addEventListener("click", () => { if (BANK.length >= 4) startSession("normal"); });
startWrongBtn.addEventListener("click", () => { if (wrongCount()) startSession("wrong"); });

// ---- 初始化 ----
(async function init() {
  await loadBank();
  bankReady();
  renderSetup();
})();
