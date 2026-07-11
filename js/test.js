// 单词测试(中英互选)主逻辑。
// 题目从「打卡过的词」现场组卷(test-pool.js)：每次最多 100 题。
// 每题随机方向：看中文选英文 / 看英文选中文；正确词 + 池内随机 3 干扰词，运行时抽、打乱。
// 选完看答案词的音标/词性/释义/例句，可朗读。
// 对错记入独立错题本(test-store.js)，可只考错题、连续 2 次答对移出。

import { recordResult, wrongWords, wrongCount, summary } from "./test-store.js?v=1";
import { speakEnglish, speechSupported } from "./speech.js?v=6";
import { loadTestPool, buildQuestions, buildOneQuestion } from "./test-pool.js?v=1";

const TEST_SIZE = 100; // 每次测试题量上限

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

/* 朗读控件已迁移到 settings.html(F5) */

// ---- 状态 ----
let POOL = [];            // 打卡词池 [{word,def,pos,sentence_en,sentence_zh,phonetic}]
let session = null;       // { items:[题], idx, right, wrong, mode:'normal'|'wrong', missed:[] }

// ---- 工具 ----
function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// ---- 加载打卡词池 ----
async function loadPool() {
  try { POOL = await loadTestPool(); }
  catch { POOL = []; }
}

// ---- 首页统计 + 按钮态 ----
function renderSetup() {
  const s = summary();
  const poolN = POOL.length;
  const testN = Math.min(TEST_SIZE, poolN);
  const parts = [`打卡词库共 <b>${poolN}</b> 词`];
  if (s.testedWords) {
    parts.push(`累计考过 <b>${s.testedWords}</b> 词`);
    parts.push(`正确率 <b>${s.accuracy == null ? "—" : Math.round(s.accuracy * 100) + "%"}</b>`);
  }
  statSummaryEl.innerHTML = parts.join(" · ");
  startBtn.textContent = testN > 0 ? `开始测试（${testN} 题）` : "开始测试";
  const wc = wrongCount();
  startWrongBtn.disabled = wc === 0;
  startWrongBtn.textContent = wc ? `重做错题（${wc}）` : "重做错题（0）";
}

// 词池就绪判断；返回 true 表示可出题
function poolReady() {
  if (POOL.length === 0) {
    noticeEl.hidden = false;
    noticeEl.textContent = "还没有打卡过的词。先去『今日』学几个词，再回来测试。";
    startBtn.disabled = true;
    return false;
  }
  if (POOL.length < 4) {
    noticeEl.hidden = false;
    noticeEl.textContent = `打卡词只有 ${POOL.length} 个，凑不齐四个选项，先多学几个词。`;
    startBtn.disabled = true;
    return false;
  }
  noticeEl.hidden = true;
  startBtn.disabled = false;
  return true;
}

// ---- 组卷 / 开始 ----
function startSession(mode) {
  let items;
  if (mode === "wrong") {
    const ww = new Set(wrongWords().map((w) => w.toLowerCase()));
    const wrongPool = POOL.filter((p) => ww.has(p.word.toLowerCase()));
    if (wrongPool.length === 0) return; // 错题本空
    // 错题也用相同题型：每个错题词出一题，干扰项仍从整池抽(选项更多样)
    items = wrongPool.map((t) => buildOneQuestion(t, POOL));
  } else {
    items = buildQuestions(POOL, TEST_SIZE);
  }
  session = { items, idx: 0, right: 0, wrong: 0, mode, missed: [] };
  setupEl.hidden = true;
  resultEl.hidden = true;
  quizEl.hidden = false;
  renderQuestion();
}

// ---- 渲染当前题 ----
const DIR_LABEL = { zh2en: "看中文 · 选英文", en2zh: "看英文 · 选中文" };

function renderQuestion() {
  const item = session.items[session.idx];
  const total = session.items.length;
  progressEl.textContent = `第 ${session.idx + 1} / ${total} 题${session.mode === "wrong" ? " · 错题模式" : ""}`;
  scoreEl.textContent = `✅ ${session.right}　❌ ${session.wrong}`;
  barEl.style.width = `${(session.idx / total) * 100}%`;

  // 题干：方向徽标 + stem
  stemEl.innerHTML = `<span class="q-dir">${DIR_LABEL[item.direction]}</span><div class="q-prompt">${esc(item.stem)}</div>`;

  explainEl.hidden = true;
  explainEl.innerHTML = "";
  nextBtn.hidden = true;

  optionsEl.innerHTML = "";
  item.options.forEach((opt, i) => {
    const letter = "ABCD"[i];
    const btn = document.createElement("button");
    btn.className = "q-option";
    btn.innerHTML = `<b>${letter}</b><span>${esc(opt.text)}</span>`;
    btn.addEventListener("click", () => pick(item, opt, btn));
    optionsEl.appendChild(btn);
  });
}

// ---- 作答 ----
function pick(item, opt, btn) {
  if (item.answered) return;
  item.answered = true;
  item.picked = opt.text;
  const correct = !!opt.correct;
  if (correct) session.right += 1; else { session.wrong += 1; session.missed.push(item); }
  recordResult(item.word, correct, session.mode === "wrong");
  scoreEl.textContent = `✅ ${session.right}　❌ ${session.wrong}`;

  // 标记选项对错
  Array.from(optionsEl.children).forEach((b) => {
    const t = b.querySelector("span").textContent;
    b.classList.add("locked");
    const isCorrectOpt = item.options.find((o) => o.text === t)?.correct;
    if (isCorrectOpt) b.classList.add("right");
    else if (t === opt.text) b.classList.add("wrong");
    else b.classList.add("dim");
  });

  renderExplain(item);
  nextBtn.hidden = false;
  nextBtn.textContent = session.idx === session.items.length - 1 ? "查看结果 →" : "下一题 →";
}

function renderExplain(item) {
  const t = item.target;
  const ph = t.phonetic ? ` <span class="q-ph">/${esc(t.phonetic)}/</span>` : "";
  const posTxt = t.pos ? `<span class="q-pos">${esc(t.pos)}</span>` : "";
  const example = t.sentence_en
    ? `<div class="q-sentence"><div class="q-en">${esc(t.sentence_en)}</div><div class="q-zh">${esc(t.sentence_zh || "")}</div></div>`
    : "";

  explainEl.innerHTML = `
    <div class="q-answer-line"><b class="q-fill">${esc(t.word)}</b>${ph} ${posTxt} <span class="q-def">${esc(t.def)}</span></div>
    ${example}
  `;
  explainEl.hidden = false;

  // 读单词
  const speakWrap = document.createElement("div");
  speakWrap.className = "q-speak";
  const sb = document.createElement("button");
  sb.type = "button";
  sb.className = "q-speak-btn";
  sb.textContent = "🔊 读单词";
  sb.disabled = !speechSupported();
  sb.addEventListener("click", () => speakEnglish(t.word));
  speakWrap.appendChild(sb);
  explainEl.appendChild(speakWrap);
}

// ---- 下一题 / 结果 ----
nextBtn.addEventListener("click", () => {
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
  const pct = total ? Math.round((session.right / total) * 100) : 0;
  const missedHtml = session.missed.length
    ? session.missed.map((it) => {
        const t = it.target;
        return `<li><b>${esc(t.word)}</b> <span>${esc(t.def || t.pos || "")}</span></li>`;
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
startBtn.addEventListener("click", () => { if (POOL.length >= 4) startSession("normal"); });
startWrongBtn.addEventListener("click", () => { if (wrongCount()) startSession("wrong"); });

// ---- 初始化 ----
(async function init() {
  await loadPool();
  poolReady();
  renderSetup();
})();
