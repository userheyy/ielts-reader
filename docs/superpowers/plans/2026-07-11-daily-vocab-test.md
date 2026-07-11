# 每日单词 Test（打卡词池现场组卷）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把生词页「测试」tab 的单词测试从「静态 quiz-bank 完形填空」改成「从用户打卡过的词现场组卷的中英互选测试」，每次最多 100 题。

**Architecture:** 新增纯逻辑模块 `js/test-pool.js`（收集打卡词池 + 组卷，可注入依赖便于 Node 单测），改造 `js/test.js` 把数据源与渲染换掉，`test.html` 微调文案。错题本 `test-store.js` 复用不改。

**Tech Stack:** 原生 ES module（浏览器 `<script type="module">`）、`node:assert` 单测（`*-check.mjs`，`node js/xxx-check.mjs` 运行）、localStorage 存储、fetch 加载 `data/vocab-seed.json`。

**规格：** `docs/superpowers/specs/2026-07-11-daily-vocab-test-design.md`

---

## 文件结构

| 文件 | 职责 | 动作 |
|---|---|---|
| `js/test-pool.js` | 收集打卡词池（seed_review ∪ 复习过的生词）+ 组卷（中英互选、双向、随机干扰）。纯逻辑，依赖可注入。 | 新建 |
| `js/test-pool-check.mjs` | test-pool 的 Node 单测（注入内存数据，绕过 fetch/localStorage）。 | 新建 |
| `js/test.js` | 改数据源为 test-pool；题型渲染改中英互选双向；去掉完形填空/挖空/quiz-bank。 | 改 |
| `test.html` | 首页文案（100 题、打卡词库提示）；解析区结构；脚本版本号。 | 改 |
| `css/style.css` | 复用现有 `.quiz-*`/`.q-*` 类；如需方向徽标样式则少量新增。 | 改（少量） |

---

## Task 1: test-pool.js — 收集打卡词池

**Files:**
- Create: `js/test-pool.js`
- Test: `js/test-pool-check.mjs`

设计要点：`buildTestPool` 接受可注入依赖 `{ seedIndex, seedReview, vocab }`，默认在浏览器里 fetch(seed) + 读 localStorage/loadVocab；Node 测试直接注入，绕过网络与 localStorage（仿 `daily-store.js` 的 `__setCachesForTest`）。

- [ ] **Step 1: 写失败测试（收集词池）**

创建 `js/test-pool-check.mjs`（**本 Task 只 import `buildTestPool`**；Task 2 再追加 `buildOneQuestion/buildQuestions` 的 import —— 这样每个 Task 结束时测试文件都能独立跑通，无需占位导出）：

```js
// test-pool.js 单测：词池收集 + 组卷。注入内存依赖，绕过 fetch/localStorage。
import assert from "node:assert";
import { buildTestPool } from "./test-pool.js";

// 造一个假 seedIndex：Map<wordLower, {word, def, pos, sentence_en, sentence_zh, phonetic}>
function fakeSeed(words) {
  return new Map(words.map((w) => [w.word.toLowerCase(), w]));
}

const SEED = fakeSeed([
  { word: "predict", def: "预测", pos: "v.", sentence_en: "They predict rain.", sentence_zh: "他们预测有雨。", phonetic: "prɪˈdɪkt" },
  { word: "reduce", def: "减少", pos: "v.", sentence_en: "Reduce costs.", sentence_zh: "减少成本。", phonetic: "rɪˈdjuːs" },
  { word: "benefit", def: "好处", pos: "n.", sentence_en: "A clear benefit.", sentence_zh: "明显的好处。", phonetic: "ˈbenɪfɪt" },
  { word: "ancient", def: "古代的", pos: "adj.", sentence_en: "Ancient ruins.", sentence_zh: "古代遗迹。", phonetic: "ˈeɪnʃənt" },
  { word: "verdict", def: "裁决", pos: "n.", sentence_en: "The final verdict.", sentence_zh: "最终裁决。", phonetic: "ˈvɜːdɪkt" },
]);

// ---- 1) 只收集打卡过（有 seed_review）的词 ----
{
  const seedReview = { predict: { level: 1 }, reduce: { level: 0 } }; // 打卡过 2 个
  const pool = buildTestPool({ seedIndex: SEED, seedReview, vocab: [] });
  const wordset = new Set(pool.map((p) => p.word.toLowerCase()));
  assert.equal(pool.length, 2, "只应收集打卡过的 2 个内置词");
  assert.ok(wordset.has("predict") && wordset.has("reduce"), "应含 predict/reduce");
  assert.ok(!wordset.has("benefit"), "没打卡过的不应入池");
  assert.ok(pool.every((p) => p.def && p.word), "每个词条应有 word 和 def");
}
```

- [ ] **Step 2: 运行测试确认失败**

Run: `node js/test-pool-check.mjs`
Expected: FAIL —— `Cannot find module ... test-pool.js` 或 `buildTestPool is not a function`。

- [ ] **Step 3: 实现 test-pool.js 的词池收集部分**

创建 `js/test-pool.js`：

```js
// 单词测试的「打卡词池」+ 组卷（纯逻辑，依赖可注入，便于 Node 单测）。
// 打卡词 = 有 SRS 记录的词：内置词(ielts_vocab_seed_review) ∪ 复习过的生词(ielts_vocab)。
// 题型：中英互选，逐题随机方向（zh2en / en2zh），干扰项从池内随机抽。
import { loadAll as loadVocab } from "./store.js?v=7";
import { loadSeed, getSeedReview } from "./seed.js?v=3";

const SEED_REVIEW_KEY = "ielts_vocab_seed_review";

// 浏览器默认依赖：fetch seed + 读 localStorage。Node 测试可整体注入 deps 绕过。
async function defaultDeps() {
  const seed = await loadSeed();
  const seedIndex = new Map();
  for (const w of seed.words || []) {
    if (w && w.word) seedIndex.set(w.word.toLowerCase(), w);
  }
  let seedReview = {};
  try {
    if (typeof localStorage !== "undefined") {
      seedReview = JSON.parse(localStorage.getItem(SEED_REVIEW_KEY) || "{}") || {};
    }
  } catch { seedReview = {}; }
  const vocab = loadVocab();
  return { seedIndex, seedReview, vocab };
}

// 收集打卡词池。deps 省略时用浏览器默认；测试时注入 { seedIndex, seedReview, vocab }。
// 返回 [{ word, def, pos, sentence_en, sentence_zh, phonetic }]，按小写去重（生词优先）。
export function buildTestPool(deps) {
  const { seedIndex, seedReview, vocab } = deps;
  const byWord = new Map();

  // 内置词：出现在 seed_review 里、且能在 seedIndex 找到完整词条、且 def 非空
  for (const key of Object.keys(seedReview || {})) {
    const wl = key.toLowerCase();
    const entry = seedIndex.get(wl);
    if (!entry || !entry.def || !entry.def.trim()) continue;
    byWord.set(wl, {
      word: entry.word,
      def: entry.def,
      pos: entry.pos || "",
      sentence_en: entry.sentence_en || "",
      sentence_zh: entry.sentence_zh || "",
      phonetic: entry.phonetic || "",
    });
  }
  // 生词：复习过（correct+wrong+fuzzy>0）、def 非空；同名覆盖内置（生词优先）
  for (const v of vocab || []) {
    const r = v.review || {};
    const n = (Number(r.correct) || 0) + (Number(r.wrong) || 0) + (Number(r.fuzzy) || 0);
    if (n === 0) continue;
    if (!v.def || !v.def.trim()) continue;
    const wl = (v.word || "").toLowerCase();
    if (!wl) continue;
    byWord.set(wl, {
      word: v.word,
      def: v.def,
      pos: v.pos || "",
      sentence_en: v.sentence_en || "",
      sentence_zh: v.sentence_zh || "",
      phonetic: "",
    });
  }
  return [...byWord.values()];
}

// 浏览器用：加载默认依赖后收集词池。
export async function loadTestPool() {
  return buildTestPool(await defaultDeps());
}
```

- [ ] **Step 4: 运行测试确认通过**

Run: `node js/test-pool-check.mjs`
Expected: PASS —— Step 1 的词池断言通过（本 Task 测试文件只 import 了 `buildTestPool`，不会因组卷函数未实现而报错）。

- [ ] **Step 5: 提交**

```bash
git add js/test-pool.js js/test-pool-check.mjs
git commit -m "feat(测试): test-pool 收集打卡词池(seed_review ∪ 复习过生词)"
```

---

## Task 2: test-pool.js — 组卷（中英互选、双向、随机干扰）

**Files:**
- Modify: `js/test-pool.js`
- Test: `js/test-pool-check.mjs`

- [ ] **Step 1: 追加失败测试（组卷）**

先把 `js/test-pool-check.mjs` 顶部的 import 补全：
```js
import { buildTestPool, buildOneQuestion, buildQuestions } from "./test-pool.js";
```

再在文件末尾追加以下断言（若已有结尾的 `console.log` 成功行，把新断言插到它之前；没有则追加后在最后加 `console.log("test-pool.js 全部断言通过 ✅");`）：

```js
// 固定 random 工厂：给一串 [0,1) 值，按序返回，用尽后回 0。便于确定性断言。
function seqRandom(vals) {
  let i = 0;
  return () => (i < vals.length ? vals[i++] : 0);
}

// ---- 2) buildOneQuestion：zh2en 方向 ----
{
  const pool = buildTestPool({ seedIndex: SEED, seedReview: { predict: 1, reduce: 1, benefit: 1, ancient: 1, verdict: 1 }, vocab: [] });
  const target = pool.find((p) => p.word === "predict");
  // direction 由第一个 random 决定：<0.5 => zh2en
  const q = buildOneQuestion(target, pool, seqRandom([0.1, 0.2, 0.4, 0.6]));
  assert.equal(q.direction, "zh2en", "random<0.5 应为 zh2en");
  assert.equal(q.stem, "预测", "zh2en 题干应是中文释义");
  assert.equal(q.options.length, 4, "应有 4 个选项");
  const correct = q.options.filter((o) => o.correct);
  assert.equal(correct.length, 1, "恰好 1 个正确项");
  assert.equal(correct[0].text, "predict", "zh2en 正确项文本应是英文词");
  // 选项文本互不相同
  assert.equal(new Set(q.options.map((o) => o.text)).size, 4, "选项文本不重复");
  // 所有选项英文都来自池
  const poolWords = new Set(pool.map((p) => p.word));
  assert.ok(q.options.every((o) => poolWords.has(o.text)), "zh2en 选项都应来自池内英文词");
}

// ---- 3) buildOneQuestion：en2zh 方向 ----
{
  const pool = buildTestPool({ seedIndex: SEED, seedReview: { predict: 1, reduce: 1, benefit: 1, ancient: 1, verdict: 1 }, vocab: [] });
  const target = pool.find((p) => p.word === "predict");
  const q = buildOneQuestion(target, pool, seqRandom([0.9, 0.2, 0.4, 0.6]));
  assert.equal(q.direction, "en2zh", "random>=0.5 应为 en2zh");
  assert.equal(q.stem, "predict", "en2zh 题干应是英文词");
  const correct = q.options.filter((o) => o.correct);
  assert.equal(correct[0].text, "预测", "en2zh 正确项文本应是中文释义");
  const poolDefs = new Set(pool.map((p) => p.def));
  assert.ok(q.options.every((o) => poolDefs.has(o.text)), "en2zh 选项都应来自池内中文释义");
}

// ---- 4) buildQuestions：题数 = min(count, poolSize)，每题唯一考点 ----
{
  const pool = buildTestPool({ seedIndex: SEED, seedReview: { predict: 1, reduce: 1, benefit: 1, ancient: 1, verdict: 1 }, vocab: [] });
  const qs = buildQuestions(pool, 100, { random: () => 0.3 });
  assert.equal(qs.length, 5, "池只有 5 词，应出 5 题(上限 100)");
  const targets = qs.map((q) => q.word.toLowerCase());
  assert.equal(new Set(targets).size, 5, "每题考点词应互不相同");
  const qs3 = buildQuestions(pool, 3, { random: () => 0.3 });
  assert.equal(qs3.length, 3, "count=3 应出 3 题");
}
```

- [ ] **Step 2: 运行测试确认失败**

Run: `node js/test-pool-check.mjs`
Expected: FAIL —— 组卷相关断言失败（占位函数返回 undefined）。

- [ ] **Step 3: 实现组卷**

在 `js/test-pool.js` 里，把占位的 `buildOneQuestion/buildQuestions`（若有）替换为真实实现（放在 `loadTestPool` 之后）：

```js
// --- 组卷工具 ---
function shuffle(arr, random = Math.random) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// 从 pool 里排除若干词后随机取 n 个（用于抽考点/干扰）。
function sampleExcept(pool, excludeWordsLower, n, random) {
  const cand = pool.filter((p) => !excludeWordsLower.has(p.word.toLowerCase()));
  return shuffle(cand, random).slice(0, n);
}

// 生成一道题。random 省略用 Math.random。
// 返回 { word, direction:'zh2en'|'en2zh', stem, options:[{text,correct}], target:{word,def,pos,phonetic,sentence_en,sentence_zh} }
export function buildOneQuestion(target, pool, random = Math.random) {
  const direction = random() < 0.5 ? "zh2en" : "en2zh";
  const textOf = (p) => (direction === "zh2en" ? p.word : p.def);
  const correctText = textOf(target);

  // 干扰项：从池内排除 target 随机抽，按「显示文本」去重（防同义 def 撞车），补到 3 个。
  const chosen = [];
  const usedText = new Set([correctText]);
  const excluded = new Set([target.word.toLowerCase()]);
  // 先抽一批候选（多抽些以便去重后仍够）
  const cands = sampleExcept(pool, excluded, pool.length, random);
  for (const c of cands) {
    if (chosen.length >= 3) break;
    const t = textOf(c);
    if (usedText.has(t)) continue; // 显示文本去重
    usedText.add(t);
    chosen.push(c);
  }
  const optionObjs = [{ text: correctText, correct: true }, ...chosen.map((c) => ({ text: textOf(c), correct: false }))];
  const options = shuffle(optionObjs, random);

  return {
    word: target.word,
    direction,
    stem: direction === "zh2en" ? target.def : target.word,
    options,
    target: {
      word: target.word, def: target.def, pos: target.pos || "",
      phonetic: target.phonetic || "", sentence_en: target.sentence_en || "", sentence_zh: target.sentence_zh || "",
    },
  };
}

// 从 pool 抽 min(count, poolSize) 个考点词，各出一题。opts.random 可注入。
export function buildQuestions(pool, count = 100, opts = {}) {
  const random = opts.random || Math.random;
  const picked = shuffle(pool, random).slice(0, Math.min(count, pool.length));
  return picked.map((t) => buildOneQuestion(t, pool, random));
}
```

若 Task 1 Step 4 加了占位 `export function buildOneQuestion(){}...`，此处删除占位、换成上面实现。

- [ ] **Step 4: 运行测试确认通过**

Run: `node js/test-pool-check.mjs`
Expected: PASS —— 打印 `test-pool.js 全部断言通过 ✅`（记得在文件末尾加这行 `console.log`）。

- [ ] **Step 5: 提交**

```bash
git add js/test-pool.js js/test-pool-check.mjs
git commit -m "feat(测试): test-pool 组卷(中英互选/双向/随机干扰/文本去重)"
```

---

## Task 3: 改造 test.js — 数据源换成打卡词池

**Files:**
- Modify: `js/test.js`（整体重写数据加载与组卷部分；保留错题本/结果页/按钮骨架）

- [ ] **Step 1: 替换 import 与常量**

打开 `js/test.js`，把顶部 import 与常量段替换：

原（第 6~11 行附近）：
```js
import { ensureDict, lookup } from "./dict.js?v=1";
import { recordResult, wrongWords, wrongCount, summary } from "./test-store.js?v=1";
import {speakEnglish, speechSupported} from "./speech.js?v=6";

const GROUP_SIZE = 10;
const BANK_URL = "data/quiz-bank.json";
```

改为：
```js
import { recordResult, wrongWords, wrongCount, summary } from "./test-store.js?v=1";
import { speakEnglish, speechSupported } from "./speech.js?v=6";
import { loadTestPool, buildQuestions, buildOneQuestion } from "./test-pool.js?v=1";

const TEST_SIZE = 100; // 每次测试题量上限
```

（`dict.js` 不再需要 —— 中英互选不做题干悬停查词。）

- [ ] **Step 2: 替换状态变量与词池加载**

把状态段（`let BANK = []; let bankByWord = ...` 与 `loadBank()` 整个函数）替换为：

```js
// ---- 状态 ----
let POOL = [];            // 打卡词池 [{word,def,pos,sentence_en,sentence_zh,phonetic}]
let session = null;       // { items:[题], idx, right, wrong, mode:'normal'|'wrong', missed:[] }

async function loadPool() {
  try { POOL = await loadTestPool(); }
  catch { POOL = []; }
}
```

删除原 `shuffle/sample/esc` 里与题库无关的部分？——保留 `esc`；`shuffle/sample` 若组卷已移到 test-pool，可保留 `esc` 一个即可，`shuffle/sample` 删除（不再在 test.js 组卷）。确认删除：`shuffle`、`sample`、`buildQuestion`（旧完形填空组卷）、`renderStem`、`attachHover`、`closeHover`、`hoverTip`。

- [ ] **Step 3: 重写首页统计 + 就绪判断**

把 `renderSetup` 与 `bankReady`（原 66~93 行）替换为：

```js
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
```

- [ ] **Step 4: 重写 startSession**

把 `startSession`（原 110~133 行）替换为：

```js
function startSession(mode) {
  let items;
  if (mode === "wrong") {
    const ww = new Set(wrongWords().map((w) => w.toLowerCase()));
    const wrongPool = POOL.filter((p) => ww.has(p.word.toLowerCase()));
    if (wrongPool.length === 0) return; // 错题本空
    // 错题也用相同题型：每个错题词出一题，干扰项仍从整池抽（选项更多样）
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
```

（删掉原来的 `ensureDict()` 预热调用。）

- [ ] **Step 5: 提交（此时渲染仍是旧的，下一 Task 修）**

```bash
git add js/test.js
git commit -m "refactor(测试): test.js 数据源换成打卡词池 + 组卷改 test-pool"
```

> 注：本 Task 结束后 test.js 尚不能运行（renderQuestion 仍引用旧完形填空结构）。Task 4 补齐渲染，浏览器验收放在 Task 5。

---

## Task 4: 改造 test.js 渲染 + test.html 结构

**Files:**
- Modify: `js/test.js`（renderQuestion / pick / renderExplain）
- Modify: `test.html`（题干区结构、解析区、版本号、首页文案）
- Modify: `css/style.css`（方向徽标样式，少量）

- [ ] **Step 1: 重写 renderQuestion**

把 `renderQuestion`（原 185~206 行）替换为：

```js
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
```

- [ ] **Step 2: 重写 pick**

把 `pick`（原 209~230 行）替换为：

```js
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
```

（注意：`pick` 不再是 async；`renderExplain` 也不再 async。）

- [ ] **Step 3: 重写 renderExplain**

把 `renderExplain`（原 232~274 行）替换为：

```js
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
```

- [ ] **Step 4: 修 showResult 里的错题渲染**

`showResult`（原 287~308 行）里 `session.missed` 现在装的是 question item（有 `.target`），不是旧的 `q`。把 missed 渲染那段改为：

```js
  const missedHtml = session.missed.length
    ? session.missed.map((it) => {
        const t = it.target;
        return `<li><b>${esc(t.word)}</b> <span>${esc(t.def || t.pos || "")}</span></li>`;
      }).join("")
    : `<li class="q-none">全对，没有错题 🎉</li>`;
```

同时删除 `showResult` 顶部对 `lookup` 的使用（已无 dict import）。其余（分数、正确率、错题按钮态）不变。

- [ ] **Step 5: 修 init**

把文件末尾 init（原 324~328 行）替换为：

```js
(async function init() {
  await loadPool();
  poolReady();
  renderSetup();
})();
```

- [ ] **Step 6: 改 test.html**

`test.html` 修改点：

1. 第 27 行 intro 文案，改为中英互选口径：
```html
      <p class="quiz-intro">从你打卡过的词里出题：看中文选英文、看英文选中文，混合出。答错的词进错题本，可以只刷错题，连续答对两次才移出。</p>
```
2. 第 25 行 eyebrow `CLOZE TEST` → `DAILY TEST`。
3. 第 30 行按钮文案（初值即可，JS 会覆盖）：`开始测试（10 题）` → `开始测试`。
4. 题干容器：第 44 行 `<div class="quiz-stem" id="q-stem"></div>` 保留（renderQuestion 会填 `.q-dir`/`.q-prompt`）。
5. 第 64 行脚本版本号 bump：`<script type="module" src="js/test.js?v=2"></script>` → `?v=3`。

- [ ] **Step 7: 加方向徽标/题干样式（css/style.css）**

在 `css/style.css` 末尾追加（复用现有配色变量风格；若无变量则用与 `.quiz-*` 相近的值）：

```css
/* 单词测试:中英互选题干 */
.q-dir { display:inline-block; font-size:12px; letter-spacing:.08em; color:#2b6cb0; background:#ebf4ff; border-radius:999px; padding:3px 10px; margin-bottom:12px; }
.q-prompt { font-size:26px; font-weight:700; line-height:1.35; margin-bottom:4px; }
.q-answer-line { font-size:18px; margin-bottom:8px; }
.q-answer-line .q-fill { color:#276749; }
.q-ph { color:#718096; font-weight:400; font-size:15px; }
.q-pos { color:#a0aec0; font-size:14px; margin:0 4px; }
.q-def { font-weight:600; }
```

（若 `css/style.css` 已定义同名类 —— 先 grep 确认无冲突：`grep -n "q-dir\|q-prompt\|q-answer-line" css/style.css`；有冲突则改用不同类名。）

- [ ] **Step 8: 运行单测确保没弄坏 test-pool**

Run: `node js/test-pool-check.mjs`
Expected: PASS（本 Task 没动 test-pool，应仍全绿）。

- [ ] **Step 9: 提交**

```bash
git add js/test.js test.html css/style.css
git commit -m "feat(测试): 中英互选双向渲染 + 打卡词库文案 + 方向徽标样式"
```

---

## Task 5: 浏览器端到端验收

**Files:** 无（验证 + 可能回修）

- [ ] **Step 1: 起本地静态服务器**

用 Claude Preview 起服务器（本机 Chrome 扩展常连不上，但 Preview 本地静态服务器可用）。根目录 = `ielts-app`。打开 `test.html`（或 `vocab.html` 切到「测试」tab）。

- [ ] **Step 2: 注入打卡数据（模拟已打卡若干词）**

在浏览器 console（javascript_tool）执行，塞入 8 个内置词的 seed_review，制造一个可考的池：

```js
const words = ["predict","reduce","benefit","ancient","graduate","analyze","significant","establish"];
const rev = {}; words.forEach(w => rev[w] = { level: 1, next_due: null, history: [] });
localStorage.setItem("ielts_vocab_seed_review", JSON.stringify(rev));
location.reload();
```

- [ ] **Step 3: 核对首页**

read_page / 截图确认：
- 统计行显示「打卡词库共 8 词」；
- 开始按钮显示「开始测试（8 题）」且可点；
- 错题按钮禁用（0）。

- [ ] **Step 4: 走完一轮**

点开始，逐题作答（故意答错至少 1 题）。核对：
- 题干出现方向徽标（能看到 zh2en / en2zh 两种都有出现）；
- zh2en 题干是中文、选项是英文；en2zh 反之；
- 答完解析显示词/音标/词性/中文释义/例句 + 🔊；
- 进度、✅❌ 计数正确；
- 结果页分数/正确率/本轮错题正确。

- [ ] **Step 5: 核对错题本**

回首页确认「重做错题（N）」变为可点（N=刚才答错数）；点进去只考错题词；连续答对同一词 2 次后，回首页错题数应减少。可再用 console 检查：
```js
JSON.parse(localStorage.getItem("ielts_quiz_stats"));
```
确认答错的词 `wrong_open:true`。

- [ ] **Step 6: 核对边界**

console 清空池，确认禁用提示：
```js
localStorage.setItem("ielts_vocab_seed_review", "{}"); location.reload();
```
应显示「还没有打卡过的词…」且开始禁用。再放 2 个词，应显示「打卡词只有 2 个，凑不齐四个选项…」。

- [ ] **Step 7: 若发现问题**

按 systematic-debugging 定位 → 改源码 → 从 Step 2 重验。全绿后：

- [ ] **Step 8: 清理测试注入（可选）**

验收用的 localStorage 是浏览器里的，不影响仓库。无需提交。若之前为验收改了任何源码，提交之。

---

## Task 6: 收尾

- [ ] **Step 1: 全量单测**

Run: `node js/test-pool-check.mjs`（+ 顺手 `node js/sample-check.mjs` 确认没波及 store）
Expected: 全 PASS。

- [ ] **Step 2: 确认 quiz-bank 已断开引用**

Run: `grep -rn "quiz-bank" js/ test.html`
Expected: 无匹配（test.js 已不再引用）。data/quiz-bank.json 文件保留不删。

- [ ] **Step 3: 更新规格/计划勾选状态并提交（可选）**

如需，把本计划内已完成的 `- [ ]` 勾成 `- [x]`。

```bash
git add -A
git commit -m "docs(测试): 每日单词 test 计划完成勾选"
```

- [ ] **Step 4: 推送（等用户确认后）**

按仓库约定，推送时机由用户决定；同事在并行开发，合并/推送前与用户确认。

---

## 自审记录

- **规格覆盖**：7 决策 → 词池(Task1)、不足100(Task3 renderSetup/poolReady)、纯随机(buildQuestions 无日期)、中英互选(buildOneQuestion)、双向(direction 随机)、随机干扰(sampleExcept)、错题本(复用 test-store，Task3/4)。边界 6 情况 → poolReady + startSession('wrong')。✅
- **占位符**：无 TBD/TODO；每个改动都给了完整代码。✅
- **类型一致**：`buildTestPool/buildOneQuestion/buildQuestions` 签名与返回结构（`{word,direction,stem,options:[{text,correct}],target:{...}}`）在 Task1/2 定义、Task3/4 消费一致；`session.missed` 存 item、showResult 用 `it.target`，一致。✅
- **风险点**：Task3 结束后 test.js 暂不可运行（renderQuestion 未改），已在 Task3 注明、Task4 补齐、Task5 才验收 —— 提交粒度可接受（中间态不上线）。
