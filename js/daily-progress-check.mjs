// progressStats 去重统计测试 —— 防回归:顶部胶囊「学过/已掌握」与总进度条的口径。
//
// 契约:
//   learned   = 学过的不同单词数(有复习历史即算):生词库复习过的词 ∪ 内置词 SRS 有记录的词。
//   mastered  = 上述词里 level>=5 且 streak>=3 的不同词数(复用 store.js 的 mastered 口径)。
//   total     = 核心词库词数(seedIndex.size)。
//   remaining = max(0, total - learned)。
// 关键不变量:① 同名词(生词库∩内置词SRS)只算一次(生词优先),不双计;
//            ② 入库但从没复习过(correct+wrong+fuzzy===0)的生词不计入 learned。
//
// 与其它 *-check.mjs 一致:node:assert + localStorage 内存 shim + __setCachesForTest 注入。
import assert from "node:assert";

// ---- localStorage 内存 shim(必须在动态 import 前装好:store/seed/daily-store 都用它) ----
const _mem = new Map();
globalThis.localStorage = {
  getItem: (k) => (_mem.has(k) ? _mem.get(k) : null),
  setItem: (k, v) => { _mem.set(k, String(v)); },
  removeItem: (k) => { _mem.delete(k); },
  clear: () => { _mem.clear(); },
};

const { progressStats, __reset, __setCachesForTest } = await import("./daily-store.js");

// 造 total 个内置词并注入 seedIndex(充当"核心词库")。
function setSeed(total) {
  const words = [];
  for (let i = 1; i <= total; i++) {
    words.push({ word: `word${String(i).padStart(4, "0")}`, def: `释义${i}`, aids: null });
  }
  const seedIndex = new Map(words.map((w) => [w.word.toLowerCase(), w]));
  __setCachesForTest({ seedIndex });
  return words;
}

// 一个 review 对象:reviewed 决定是否算"学过",mastered 决定是否达标。
function review({ reviewed = true, mastered = false } = {}) {
  return {
    level: mastered ? 5 : 1,
    streak: mastered ? 3 : 1,
    next_due: "2026-08-01", history: [],
    correct: reviewed ? 1 : 0, wrong: 0, fuzzy: 0, lapses: 0,
  };
}

function reset(total = 100) {
  _mem.clear();
  __reset();
  return setSeed(total);
}

function setSeedReviews(map) { localStorage.setItem("ielts_vocab_seed_review", JSON.stringify(map)); }
function setVocab(list) { localStorage.setItem("ielts_vocab", JSON.stringify(list)); }

// ---- 1) 空库:全 0,分母 = seedIndex.size ----
reset(100);
let s = await progressStats();
assert.deepEqual(s, { learned: 0, mastered: 0, total: 100, remaining: 100 }, "空库应全 0、分母 100");

// ---- 2) 纯内置词 SRS:3 词学过,其中 1 词已掌握 ----
reset(100);
setSeedReviews({
  word0001: review({ reviewed: true, mastered: true }),
  word0002: review({ reviewed: true }),
  word0003: review({ reviewed: true }),
});
s = await progressStats();
assert.equal(s.learned, 3, "内置词学过 3");
assert.equal(s.mastered, 1, "内置词已掌握 1");
assert.equal(s.remaining, 97, "还剩 97");

// ---- 3) 纯生词库:复习过的才算;从没复习过的(total===0)不算 ----
reset(100);
setVocab([
  { word: "Alpha", review: review({ reviewed: true, mastered: true }) },
  { word: "beta",  review: review({ reviewed: true }) },
  { word: "gamma", review: review({ reviewed: false }) },      // 入库未复习 → 不算
  { word: "delta", review: { level: 0, next_due: null, history: [] } }, // 全新 → 不算
]);
s = await progressStats();
assert.equal(s.learned, 2, "生词库只有 2 个复习过的算学过(gamma/delta 不算)");
assert.equal(s.mastered, 1, "Alpha 已掌握");

// ---- 4) 同名词去重(生词库 ∩ 内置词SRS):只算一次,不双计 ----
reset(100);
setSeedReviews({ word0001: review({ reviewed: true }) });        // 内置词也有 word0001
setVocab([{ word: "Word0001", review: review({ reviewed: true, mastered: true }) }]); // 生词库同名(大小写不同)
s = await progressStats();
assert.equal(s.learned, 1, "同名词只算一次(不是 2)");
assert.equal(s.mastered, 1, "以生词库记录为准 → 已掌握");

// ---- 5) mastered 边界:level>=5 且 streak>=3 才算;差一点都不算 ----
reset(100);
setSeedReviews({
  word0001: { level: 5, streak: 3, correct: 5, wrong: 0, fuzzy: 0 }, // 恰好达标
  word0002: { level: 5, streak: 2, correct: 5, wrong: 0, fuzzy: 0 }, // streak 差 1
  word0003: { level: 4, streak: 9, correct: 9, wrong: 0, fuzzy: 0 }, // level 差 1
});
s = await progressStats();
assert.equal(s.learned, 3, "三词都学过");
assert.equal(s.mastered, 1, "只有恰好 level>=5&&streak>=3 的算掌握");

// ---- 6) 学过不超过分母 / remaining 下限 0(库外来源不会击穿) ----
reset(2); // 分母仅 2
setSeedReviews({ word0001: review({ reviewed: true }), word0002: review({ reviewed: true }) });
setVocab([{ word: "stray", review: review({ reviewed: true }) }]); // 不在 seedIndex 的生词
s = await progressStats();
assert.equal(s.total, 2, "分母 = seedIndex.size = 2");
assert.equal(s.learned, 3, "learned 如实计数(含库外生词)");
assert.equal(s.remaining, 0, "remaining 下限为 0,不出现负数");

console.log("daily-progress.js(progressStats)全部断言通过 ✅");
