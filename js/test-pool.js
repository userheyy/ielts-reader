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
