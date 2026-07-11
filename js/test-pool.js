// 单词测试的「打卡词池」+ 组卷（纯逻辑，依赖可注入，便于 Node 单测）。
// 打卡词 = 有 SRS 记录的词：内置词(ielts_vocab_seed_review) ∪ 复习过的生词(ielts_vocab)。
// 题型：中英互选，逐题随机方向（zh2en / en2zh），干扰项从池内随机抽。
import { loadAll as loadVocab } from "./store.js?v=7";
import { loadSeed } from "./seed.js?v=3";

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
// 返回 { word, direction:'zh2en'|'en2zh', stem, options:[{text,correct}],
//        target:{word,def,pos,phonetic,sentence_en,sentence_zh} }
export function buildOneQuestion(target, pool, random = Math.random) {
  const direction = random() < 0.5 ? "zh2en" : "en2zh";
  const textOf = (p) => (direction === "zh2en" ? p.word : p.def);
  const correctText = textOf(target);

  // 干扰项：从池内排除 target 随机抽，按「显示文本」去重（防同义 def 撞车），补到 3 个。
  const chosen = [];
  const usedText = new Set([correctText]);
  const excluded = new Set([target.word.toLowerCase()]);
  const cands = sampleExcept(pool, excluded, pool.length, random);
  for (const c of cands) {
    if (chosen.length >= 3) break;
    const t = textOf(c);
    if (usedText.has(t)) continue; // 显示文本去重
    usedText.add(t);
    chosen.push(c);
  }
  const optionObjs = [
    { text: correctText, correct: true },
    ...chosen.map((c) => ({ text: textOf(c), correct: false })),
  ];
  const options = shuffle(optionObjs, random);

  return {
    word: target.word,
    direction,
    stem: direction === "zh2en" ? target.def : target.word,
    options,
    target: {
      word: target.word, def: target.def, pos: target.pos || "",
      phonetic: target.phonetic || "",
      sentence_en: target.sentence_en || "", sentence_zh: target.sentence_zh || "",
    },
  };
}

// 从 pool 抽 min(count, poolSize) 个考点词，各出一题。opts.random 可注入。
export function buildQuestions(pool, count = 100, opts = {}) {
  const random = opts.random || Math.random;
  const picked = shuffle(pool, random).slice(0, Math.min(count, pool.length));
  return picked.map((t) => buildOneQuestion(t, pool, random));
}
