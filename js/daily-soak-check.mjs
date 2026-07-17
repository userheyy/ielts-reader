// 今日板块「跨天 + 多日仿真」压力测试。
//
// 定向场景(每个都曾是/可能是真 bug):
//   A. 跨天不漏:昨天放出没学完的新词,今天必须回来(设计§5"游标不重不漏")
//   B. review_cap 一致性:generateDay 截断了,restoreDay 恢复时也要按剩余额度截断
//   C. 同词双计:一个词既在生词库又是已学内置词时,复习只出一条(生词优先,对齐 seed.js §5.4)
//   D. 损坏数据:ielts_daily 是垃圾 JSON / 配额是字符串,不许放出无限新词
//
// 随机仿真(soak):从 0 开始学完整个词表,逐日推进,每天随机 全学/学一半/跳过 +
// 随机三档评分,全程断言不变量:
//   - 不重:评过分的词永远不再作为"新词"放出
//   - 不漏:最终词表全部学完(没有词被永久遗漏)
//   - 封顶:done 永远 == 每天实际过词数,狂点重进不涨
//   - 账目:totalWordsDone == 各天之和;连续打卡与实际一致
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
  ensureTodayTask, markWordDone, totalWordsDone, currentStreak, heatmapCells,
  updateSettings, loadDaily, dateKey, __reset, __setCachesForTest,
} = await import("./daily-store.js");

// 可复现的 PRNG(mulberry32):压测要能复跑同一序列
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

function reset(n = 40) {
  _mem.clear();
  __reset();
  const data = makeWords(n);
  __setCachesForTest({ wordlist: data.wordlist, seedIndex: data.seedIndex });
  return data;
}

// 模拟 daily.js 的 wrapReviewEntry:seed 查索引,vocab 查生词库
const makeWrap = (seedIndex) => (r) => {
  if (r.origin === "seed") return seedIndex.get(r.word.toLowerCase()) || null;
  const vocab = JSON.parse(localStorage.getItem("ielts_vocab") || "[]");
  return vocab.find((x) => x.word.toLowerCase() === r.word.toLowerCase()) || null;
};

// 过一个词:按 daily.js 的评分处理器逐行模拟(评分路由 → markWordDone → noteItemDone)
function studyOne(task, item, rating, now) {
  if (item.origin === "vocab") {
    gradeReview(item.entry.word, rating, now);
  } else {
    const { review } = schedule(getSeedReview(item.entry.word), rating, now);
    setSeedReview(item.entry.word, review);
  }
  const updated = markWordDone(item.kind === "review" ? "review" : "new", now);
  if (updated) task.day = updated;
  noteItemDone(task, item);
  return updated;
}

const D = (offset) => new Date(2026, 6, 6 + offset, 9, 0, 0); // 2026-07-06 起逐日推进

// ================================================================
// A) 跨天不漏:昨天放出 10 个新词只学 3 个,今天剩下 7 个必须回来、且排最前
// ================================================================
{
  const { seedIndex } = reset(40);
  updateSettings({ new_per_day: 10 });
  const t1 = await ensureTodayTask(D(0));
  assert.equal(t1.newWords.length, 10, "day1 应放出 10 个新词");
  const wrap = makeWrap(seedIndex);
  const q1 = buildQueue(t1, wrap);
  for (const item of q1.slice(0, 3)) studyOne(t1, item, "remembered", D(0));

  const t2 = await ensureTodayTask(D(1));
  const day2Words = t2.newWords.map((w) => w.word);
  for (let i = 4; i <= 10; i++) {
    const w = `word${String(i).padStart(4, "0")}`;
    assert.ok(day2Words.includes(w), `昨天没学的 ${w} 今天必须回来(不漏)`);
  }
  assert.equal(day2Words[0], "word0004", "没学的词词频最高,应排在今天新词最前");
  assert.equal(t2.newWords.length, 10, "今天仍按配额放出 10 个");
  for (let i = 1; i <= 3; i++) {
    const w = `word${String(i).padStart(4, "0")}`;
    assert.ok(!day2Words.includes(w), `已学过的 ${w} 不许再作为新词放出(不重)`);
  }
}

// ================================================================
// B) review_cap:恢复当天任务时也要按"剩余额度"截断,不能靠刷新超量复习
// ================================================================
{
  const { seedIndex } = reset(40);
  // 5 个已学词全部到期
  const reviews = {};
  for (let i = 1; i <= 5; i++) {
    reviews[`word${String(i).padStart(4, "0")}`] = {
      level: 1, next_due: "2026-07-05", history: [], correct: 1, wrong: 0, fuzzy: 0,
      streak: 1, lapses: 0, stability: 1.5, difficulty: 5, last_review: "2026-07-04",
    };
  }
  localStorage.setItem("ielts_vocab_seed_review", JSON.stringify(reviews));
  updateSettings({ new_per_day: 0, review_cap: 2 });

  const t1 = await ensureTodayTask(D(0));
  assert.equal(t1.day.planned, 2, "cap=2:planned 应为 2");
  assert.equal(t1.review.length, 2, "cap=2:生成的任务只含 2 个复习词");
  const wrap = makeWrap(seedIndex);
  studyOne(t1, buildQueue(t1, wrap)[0], "remembered", D(0)); // 过 1 个

  const t1b = await ensureTodayTask(D(0)); // 模拟刷新恢复
  assert.equal(t1b.review.length, 1, "恢复当天:剩余额度 = cap(2) - 已复习(1) = 1");
  studyOne(t1b, buildQueue(t1b, wrap)[0], "remembered", D(0));
  const t1c = await ensureTodayTask(D(0));
  assert.equal(t1c.review.length, 0, "额度用完,恢复的任务不该再有复习词");
  assert.equal(t1c.day.reviewed_done, 2, "done 恰好 = planned,没突破 cap");
}

// ================================================================
// C) 同词双计:同一个词在生词库和内置词 SRS 都到期,复习只出一条(生词优先)
// ================================================================
{
  reset(40);
  localStorage.setItem("ielts_vocab_seed_review", JSON.stringify({
    word0001: { level: 1, next_due: "2026-07-05", history: [], correct: 1, wrong: 0, fuzzy: 0, streak: 1, lapses: 0, stability: 1.5, difficulty: 5, last_review: "2026-07-04" },
  }));
  localStorage.setItem("ielts_vocab", JSON.stringify([{
    word: "word0001", def: "生词库里的同名词", pos: "", sentence_en: "", sentence_zh: "",
    source: "", passage_id: "", sentence_id: null, added_at: "2026-07-01", status: "learning",
    aids: null, review: { level: 1, next_due: "2026-07-05", history: [], correct: 1, wrong: 0, fuzzy: 0, streak: 1, lapses: 0 },
  }]));
  updateSettings({ new_per_day: 0 });

  const t = await ensureTodayTask(D(0));
  const hits = t.review.filter((r) => r.word.toLowerCase() === "word0001");
  assert.equal(hits.length, 1, "同一个词只应出现一条复习,不能双计");
  assert.equal(hits[0].origin, "vocab", "同名去重应生词优先(对齐 seed.js 复习池语义)");
  assert.equal(t.day.planned, 1, "planned 也只按 1 计");
}

// C2) 生词今天不到期、内置词副本到期:生词记录是权威,当天不该出这个词
{
  reset(40);
  localStorage.setItem("ielts_vocab_seed_review", JSON.stringify({
    word0001: { level: 1, next_due: "2026-07-05", history: [], correct: 1, wrong: 0, fuzzy: 0, streak: 1, lapses: 0, stability: 1.5, difficulty: 5, last_review: "2026-07-04" },
  }));
  localStorage.setItem("ielts_vocab", JSON.stringify([{
    word: "word0001", def: "", review: { level: 3, next_due: "2026-08-01", history: [], correct: 5, wrong: 0, fuzzy: 0, streak: 5, lapses: 0 },
  }]));
  updateSettings({ new_per_day: 0 });
  const t = await ensureTodayTask(D(0));
  assert.equal(t.review.length, 0, "生词副本 8 月才到期 → 今天不该复习(生词优先裁决)");
}

// ================================================================
// D) 损坏数据:垃圾 JSON / 配额为字符串,不许崩、更不许放出无限新词
// ================================================================
{
  reset(40);
  localStorage.setItem("ielts_daily", "{{{垃圾");
  const t = await ensureTodayTask(D(0));
  assert.ok(t.day.planned >= 0, "垃圾 JSON 应兜底为空结构,正常生成任务");
  assert.equal(t.newWords.length, 30, "损坏后按默认配额 30 放出");
}
{
  reset(40);
  localStorage.setItem("ielts_daily", JSON.stringify({ settings: { new_per_day: "abc", review_cap: "xyz" } }));
  const t = await ensureTodayTask(D(0));
  assert.ok(t.newWords.length <= 40 && Number.isFinite(t.day.planned),
    "配额是字符串时不许放出无限新词");
  assert.equal(t.newWords.length, 0, "非法配额按 0 处理(与 updateSettings 归一化一致)");
}

// ================================================================
// E) 随机仿真:200 词从零学到全会,逐日随机 全学/学一半/跳过 + 随机评分
// ================================================================
{
  const TOTAL = 200;
  const { seedIndex } = reset(TOTAL);
  updateSettings({ new_per_day: 10 });
  const wrap = makeWrap(seedIndex);
  const rand = mulberry32(20260716);
  const pickRating = () => { const r = rand(); return r < 0.2 ? "forgot" : r < 0.4 ? "fuzzy" : "remembered"; };

  const gradedEver = new Set();   // 评过分的词(= 已学)
  let expectedTotal = 0;          // 手工账本:累计过词数
  let tailStreak = 0;             // 到最后一天为止的连续打卡
  let lastNow = D(0);
  let day = 0;

  while (gradedEver.size < TOTAL && day < 300) {
    const now = D(day); day += 1; lastNow = now;
    const roll = rand();
    if (roll < 0.05 && gradedEver.size > 0) { tailStreak = 0; continue; } // 今天没打开应用

    const task = await ensureTodayTask(now);
    // 不变量:planned = 到期复习 + 新词;新词全是没学过的(不重)
    assert.equal(task.day.planned, task.review.length + task.newWords.length,
      `day${day}: planned 应等于 复习+新词`);
    for (const w of task.newWords) {
      assert.ok(!gradedEver.has(w.word), `day${day}: 已学过的 ${w.word} 不许再作为新词放出`);
    }

    const queue = buildQueue(task, wrap);
    assert.equal(queue.length, task.day.planned, `day${day}: 全新一天队列应 == planned`);

    const fullDay = roll >= 0.25; // 20% 学一半,75% 学完
    const n = fullDay ? queue.length : Math.floor(rand() * queue.length);
    for (const item of queue.slice(0, n)) {
      studyOne(task, item, pickRating(), now);
      gradedEver.add(item.entry.word);
      expectedTotal += 1;
    }
    const done = task.day.reviewed_done + task.day.new_done;
    assert.equal(done, n, `day${day}: done 应恰好等于实际过词数`);

    if (fullDay && n > 0) {
      // 压测:学完后狂点"继续"3 次,一个词都不能多过
      for (let k = 0; k < 3; k++) {
        const q2 = buildQueue(task, wrap);
        assert.equal(q2.length, 0, `day${day}: 学完后重入队列必须为空`);
      }
      assert.equal(task.day.completed, true, `day${day}: 学完应标记 completed`);
    }
    assert.equal(totalWordsDone(), expectedTotal, `day${day}: 累计词数账目必须对上`);
    tailStreak = n > 0 ? tailStreak + 1 : 0;
  }

  // 不漏:全词表最终都学到了
  assert.equal(gradedEver.size, TOTAL, `词表 ${TOTAL} 词应全部学完,实际 ${gradedEver.size}(有词被永久遗漏)`);
  assert.ok(day < 300, "300 天内应能学完(否则说明有词在黑洞里转圈)");

  // 打卡与热力图账目
  assert.equal(currentStreak(lastNow), tailStreak, "连续打卡应与实际一致");
  const cells = heatmapCells(18, lastNow);
  const cellSum = cells.reduce((s, c) => s + c.count, 0);
  const d = loadDaily();
  const recentSum = Object.keys(d.days).filter((k) => cells.some((c) => c.date === k))
    .reduce((s, k) => s + d.days[k].reviewed_done + d.days[k].new_done, 0);
  assert.equal(cellSum, recentSum, "热力图格子计数应与存储一致");
  console.log(`  soak: ${day} 天学完 ${TOTAL} 词,累计过词 ${expectedTotal} 次(含复习)`);
}

console.log("daily-soak-check.mjs 全部断言通过 ✅");
