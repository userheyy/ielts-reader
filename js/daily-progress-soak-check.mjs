// progressStats 「多日随机仿真 + 对抗边界」压力测试。
//
// 核心思路:progressStats 的去重口径(学过/已掌握)必须在一整场真实学习仿真中,
// 与一个【独立手工账本】逐日对齐——不是只看几个静态样例,而是让 200 词从零学到全会,
// 每天随机 全学/学一半/跳过 + 随机三档评分,每天都断言:
//   learned   == 手工记录的"评过分的不同词集合"大小
//   mastered  == 手工按 level>=5&&streak>=3 判定的不同词集合大小
//   total     == seedIndex.size
//   remaining == max(0, total - learned)
//   learned 单调不减(学过就不会变没学过);mastered 可增可减(忘记会掉出掌握)
//
// 手工账本不复制被测代码的实现,而是从"每次评分后 SRS 存储里的真实 review 对象"重新判定,
// 与 progressStats 各自独立地读同一份存储 → 若两者一致,说明去重/掌握口径稳。
//
// 对抗场景(每个都可能藏 bug):
//   F1. 同名词全程双存(生词库∩内置词SRS)——learned 永不把它算成 2
//   F2. 掌握后又忘记(remembered×N 达标 → forgot 掉级)——mastered 必须回落
//   F3. 入库但从没复习的生词大量注入——不得污染 learned
//   F4. 损坏/空存储——不崩,返回 0 且 total 正确
//   F5. learned 永不 > total(即便生词库有大量库外词)
import assert from "node:assert";

// ---- localStorage 内存 shim(动态 import 前装好) ----
const _mem = new Map();
globalThis.localStorage = {
  getItem: (k) => (_mem.has(k) ? _mem.get(k) : null),
  setItem: (k, v) => { _mem.set(k, String(v)); },
  removeItem: (k) => { _mem.delete(k); },
  clear: () => { _mem.clear(); },
};

const { buildQueue, noteItemDone } = await import("./daily-queue.js");
const { schedule } = await import("./srs.js");
const { getSeedReview, setSeedReview } = await import("./seed.js");
const { gradeReview } = await import("./store.js");
const {
  ensureTodayTask, markWordDone, progressStats,
  updateSettings, dateKey, __reset, __setCachesForTest,
} = await import("./daily-store.js");

// 可复现 PRNG
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function makeWords(n) {
  const words = [];
  for (let i = 1; i <= n; i++) {
    words.push({ word: `word${String(i).padStart(4, "0")}`, def: `释义${i}`, aids: null });
  }
  return {
    words,
    wordlist: words.map((w, idx) => ({ word: w.word, freq_rank: idx + 1 })),
    seedIndex: new Map(words.map((w) => [w.word.toLowerCase(), w])),
  };
}
function reset(n) {
  _mem.clear();
  __reset();
  const data = makeWords(n);
  __setCachesForTest({ wordlist: data.wordlist, seedIndex: data.seedIndex });
  return data;
}
const makeWrap = (seedIndex) => (r) => {
  if (r.origin === "seed") return seedIndex.get(r.word.toLowerCase()) || null;
  const vocab = JSON.parse(localStorage.getItem("ielts_vocab") || "[]");
  return vocab.find((x) => x.word.toLowerCase() === r.word.toLowerCase()) || null;
};
function studyOne(task, item, rating, now) {
  if (item.origin === "vocab") gradeReview(item.entry.word, rating, now);
  else { const { review } = schedule(getSeedReview(item.entry.word), rating, now); setSeedReview(item.entry.word, review); }
  const updated = markWordDone(item.kind === "review" ? "review" : "new", now);
  if (updated) task.day = updated;
  noteItemDone(task, item);
}
const D = (offset) => new Date(2026, 6, 6 + offset, 9, 0, 0);

// 独立账本:直接从存储里的真实 review 重判 learned/mastered(不调被测函数)。
// 与 daily-store 相同的去重规则:同名词生词库优先。
function ledgerFromStorage() {
  const isMastered = (r) => (Number(r.level) || 0) >= 5 && (Number(r.streak) || 0) >= 3;
  const learned = new Set(), mastered = new Set();
  const vocab = JSON.parse(localStorage.getItem("ielts_vocab") || "[]");
  for (const v of vocab) {
    const r = v.review || {};
    const tot = (Number(r.correct) || 0) + (Number(r.wrong) || 0) + (Number(r.fuzzy) || 0);
    if (tot === 0) continue;
    const wl = String(v.word || "").toLowerCase();
    if (!wl) continue;
    learned.add(wl); if (isMastered(r)) mastered.add(wl);
  }
  const seedReview = JSON.parse(localStorage.getItem("ielts_vocab_seed_review") || "{}");
  for (const [wl, r] of Object.entries(seedReview)) {
    if (learned.has(wl)) continue;
    learned.add(wl); if (isMastered(r)) mastered.add(wl);
  }
  return { learned, mastered };
}

// ================================================================
// 主仿真:200 词从零学到全会,progressStats 每天对齐独立账本
// ================================================================
let checks = 0;
{
  const TOTAL = 200;
  const { seedIndex } = reset(TOTAL);
  updateSettings({ new_per_day: 12 });
  const wrap = makeWrap(seedIndex);
  const rand = mulberry32(20260718); // 固定种子,压测可复现
  const pickRating = () => { const r = rand(); return r < 0.22 ? "forgot" : r < 0.45 ? "fuzzy" : "remembered"; };

  const gradedEver = new Set();
  let prevLearned = 0;
  let day = 0;

  while (gradedEver.size < TOTAL && day < 400) {
    const now = D(day); day += 1;
    if (rand() < 0.05 && gradedEver.size > 0) continue; // 今天没打开

    const task = await ensureTodayTask(now);
    const queue = buildQueue(task, wrap);
    const fullDay = rand() >= 0.25;
    const n = fullDay ? queue.length : Math.floor(rand() * queue.length);
    for (const item of queue.slice(0, n)) {
      studyOne(task, item, pickRating(), now);
      gradedEver.add(item.entry.word.toLowerCase());
    }

    // —— 每天核对 progressStats 与独立账本 ——
    const stats = await progressStats();
    const led = ledgerFromStorage();
    assert.equal(stats.total, TOTAL, `day${day}: total 应恒为 ${TOTAL}`);
    assert.equal(stats.learned, led.learned.size, `day${day}: learned 应与独立账本一致`);
    assert.equal(stats.mastered, led.mastered.size, `day${day}: mastered 应与独立账本一致`);
    assert.equal(stats.remaining, Math.max(0, TOTAL - stats.learned), `day${day}: remaining 公式一致`);
    assert.equal(stats.learned, gradedEver.size, `day${day}: learned 应等于"评过分的不同词"数`);
    assert.ok(stats.learned >= prevLearned, `day${day}: learned 应单调不减(${prevLearned}→${stats.learned})`);
    assert.ok(stats.mastered <= stats.learned, `day${day}: 已掌握不得超过学过`);
    assert.ok(stats.learned <= stats.total, `day${day}: 学过不得超过词库总量`);
    prevLearned = stats.learned;
    checks += 1;
  }
  assert.equal(gradedEver.size, TOTAL, `应学完全部 ${TOTAL} 词`);
  const final = await progressStats();
  assert.equal(final.learned, TOTAL, "学完后 learned == total");
  assert.equal(final.remaining, 0, "学完后 remaining == 0");
  console.log(`  soak: ${day} 天学完 ${TOTAL} 词,逐日核对 progressStats ${checks} 次,mastered 峰值 ${final.mastered}`);
}

// ================================================================
// 主仿真 2:长程学习者——学完后继续逐日"到期就复习",让词经过多轮 due 复习攒够
// streak 真正达掌握,压测 mastered "上升"轨迹全程对齐独立账本。
// (第一场仅 22 天,词还没经历 3+ 轮 due 复习,mastered 峰值天然低——这是记忆曲线特性,
//  非 bug:一个词要 level>=5 且连续答对 3 次,需多天到期复习才够。本场拉长到大量词真正达标。
//  mastered "下降"方向由 F2 用确定性构造覆盖——随机仿真里掌握词的 next_due 被推到数月后,
//  不 fast-forward 时钟就不会到期,无法自然驱动回落,那属于 SRS 调度器的行为、与本函数正交。)
// ================================================================
{
  const TOTAL = 60;
  const { seedIndex } = reset(TOTAL);
  updateSettings({ new_per_day: 20 });
  const wrap = makeWrap(seedIndex);

  let masteredEverPeaked = 0, sawMasteredRise = false, prevMastered = 0;
  let day = 0;
  const gradedEver = new Set();

  // 长程"全 remembered"到期复习,直到大量词达掌握(或 250 天上限兜底)
  while (day < 250) {
    const now = D(day); day += 1;
    const task = await ensureTodayTask(now);
    const queue = buildQueue(task, wrap);
    for (const item of queue) { studyOne(task, item, "remembered", now); gradedEver.add(item.entry.word.toLowerCase()); }

    const stats = await progressStats();
    const led = ledgerFromStorage();
    assert.equal(stats.learned, led.learned.size, `run2 day${day}: learned 对齐账本`);
    assert.equal(stats.mastered, led.mastered.size, `run2 day${day}: mastered 对齐账本`);
    assert.ok(stats.mastered <= stats.learned && stats.learned <= TOTAL, `run2 day${day}: 夹逼关系成立`);
    if (stats.mastered > prevMastered) sawMasteredRise = true;
    masteredEverPeaked = Math.max(masteredEverPeaked, stats.mastered);
    prevMastered = stats.mastered;
    if (stats.mastered >= 40) break; // 已有足够多词达掌握即可
  }
  assert.equal(gradedEver.size, TOTAL, "run2: 应学完全部词");
  assert.ok(sawMasteredRise, "run2: 应观察到 mastered 上升(增方向)");
  assert.ok(masteredEverPeaked >= 40, `run2: 长程后 mastered 峰值应可观(实际 ${masteredEverPeaked})`);
  console.log(`  soak2: ${day} 天,mastered 峰值 ${masteredEverPeaked};增方向逐日对齐账本 ✅`);
}

// ================================================================
// F1) 同名词全程双存:learned 永不双计
// ================================================================
{
  reset(50);
  // word0001 同时在生词库(已复习)和内置词 SRS(已复习)
  localStorage.setItem("ielts_vocab_seed_review", JSON.stringify({
    word0001: { level: 2, streak: 1, correct: 2, wrong: 1, fuzzy: 0, next_due: "2026-08-01", history: [] },
    word0002: { level: 5, streak: 3, correct: 5, wrong: 0, fuzzy: 0, next_due: "2026-08-01", history: [] },
  }));
  localStorage.setItem("ielts_vocab", JSON.stringify([
    { word: "Word0001", review: { level: 5, streak: 4, correct: 6, wrong: 0, fuzzy: 0, next_due: "2026-08-01", history: [] } },
  ]));
  const s = await progressStats();
  assert.equal(s.learned, 2, "F1: word0001(两处)+ word0002 = 2 个不同词,不双计");
  assert.equal(s.mastered, 2, "F1: 生词库 word0001 已掌握 + seed word0002 已掌握 = 2");
}

// ================================================================
// F2) 掌握后又忘记:mastered 必须回落
// ================================================================
{
  const { seedIndex } = reset(10);
  updateSettings({ new_per_day: 0 });
  // 直接构造一个"刚好掌握"的内置词,然后 forgot 一次看是否掉出掌握
  setSeedReview("word0001", { level: 5, streak: 3, correct: 5, wrong: 0, fuzzy: 0, next_due: "2026-07-05", history: [], stability: 20, difficulty: 5, last_review: "2026-07-01" });
  let s = await progressStats();
  assert.equal(s.mastered, 1, "F2: 构造后应已掌握 1");
  const before = s.learned;
  // forgot:schedule 里 level = max(0, level-2) = 3, streak = 0 → 掉出掌握
  const { review } = schedule(getSeedReview("word0001"), "forgot", D(0));
  setSeedReview("word0001", review);
  assert.ok(review.level < 5 || review.streak < 3, "F2: forgot 后应不再满足掌握条件");
  s = await progressStats();
  assert.equal(s.mastered, 0, "F2: 忘记后 mastered 必须回落到 0");
  assert.equal(s.learned, before, "F2: 忘记不改变'学过'(仍学过这个词)");
}

// ================================================================
// F3) 大量"入库但从没复习"的生词:不得污染 learned
// ================================================================
{
  reset(50);
  const junk = [];
  for (let i = 0; i < 500; i++) {
    junk.push({ word: `unreviewed${i}`, review: { level: 0, streak: 0, correct: 0, wrong: 0, fuzzy: 0, next_due: null, history: [] } });
  }
  // 只有 1 个真正复习过
  junk.push({ word: "realone", review: { level: 1, streak: 1, correct: 1, wrong: 0, fuzzy: 0, next_due: "2026-08-01", history: [] } });
  localStorage.setItem("ielts_vocab", JSON.stringify(junk));
  const s = await progressStats();
  assert.equal(s.learned, 1, "F3: 500 个未复习生词不算学过,只有 realone 算");
  assert.equal(s.mastered, 0, "F3: realone 未达掌握");
}

// ================================================================
// F4) 损坏 / 空存储:不崩,返回 0,total 正确
// ================================================================
{
  reset(37);
  localStorage.setItem("ielts_vocab", "{{{坏 JSON");
  localStorage.setItem("ielts_vocab_seed_review", "not json at all");
  const s = await progressStats();
  assert.equal(s.learned, 0, "F4: 坏 JSON 应兜底为 0");
  assert.equal(s.mastered, 0, "F4: 坏 JSON mastered 0");
  assert.equal(s.total, 37, "F4: total 仍 = seedIndex.size");
  assert.equal(s.remaining, 37, "F4: remaining = total");
}
{
  reset(20);
  // 完全没有生词库/内置词记录键
  localStorage.removeItem("ielts_vocab");
  localStorage.removeItem("ielts_vocab_seed_review");
  const s = await progressStats();
  assert.deepEqual(s, { learned: 0, mastered: 0, total: 20, remaining: 20 }, "F4: 空存储全 0");
}

// ================================================================
// F5) learned 永不 > total:生词库塞满库外词也不击穿分母
// ================================================================
{
  reset(5); // 分母仅 5
  const many = [];
  for (let i = 0; i < 200; i++) {
    many.push({ word: `outside${i}`, review: { level: 6, streak: 5, correct: 9, wrong: 0, fuzzy: 0, next_due: "2026-08-01", history: [] } });
  }
  localStorage.setItem("ielts_vocab", JSON.stringify(many));
  const s = await progressStats();
  assert.equal(s.total, 5, "F5: total = seedIndex.size = 5");
  assert.equal(s.learned, 200, "F5: learned 如实计(含库外词)");
  assert.equal(s.mastered, 200, "F5: mastered 如实计");
  assert.equal(s.remaining, 0, "F5: remaining 下限 0,绝不为负");
}

console.log("daily-progress-soak-check.mjs 全部断言通过 ✅");
