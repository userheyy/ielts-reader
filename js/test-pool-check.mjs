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

// ---- 1b) 生词：只收集复习过（计数>0）且 def 非空的 ----
{
  const vocab = [
    { word: "mitigate", def: "缓解", pos: "v.", review: { correct: 1, wrong: 0, fuzzy: 0 } }, // 复习过 → 入池
    { word: "collect", def: "", review: { correct: 2 } },                                      // def 空 → 跳过
    { word: "saved", def: "已保存", review: { correct: 0, wrong: 0, fuzzy: 0 } },              // 没复习过 → 跳过
  ];
  const pool = buildTestPool({ seedIndex: SEED, seedReview: {}, vocab });
  const wordset = new Set(pool.map((p) => p.word.toLowerCase()));
  assert.equal(pool.length, 1, "只 mitigate 应入池");
  assert.ok(wordset.has("mitigate"), "复习过的生词应入池");
  assert.ok(!wordset.has("collect") && !wordset.has("saved"), "def 空 / 没复习过的不应入池");
}

// ---- 1c) 生词与内置词同名去重（生词优先）----
{
  const seedReview = { predict: { level: 1 } };
  const vocab = [{ word: "Predict", def: "预测(生词版)", pos: "v.", review: { correct: 1 } }];
  const pool = buildTestPool({ seedIndex: SEED, seedReview, vocab });
  assert.equal(pool.length, 1, "同名应去重为 1 条");
  assert.equal(pool[0].def, "预测(生词版)", "同名时生词优先");
}

console.log("test-pool.js 全部断言通过 ✅");
