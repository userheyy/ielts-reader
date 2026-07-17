// 今日过词「会话级」压力测试 —— 复现并防回归:突破单词上限、可以一直记。
//
// 根因:daily.js 的 task.review 是进页时算好的快照;复习词评分后 next_due 已推到
// 未来,但会话内没人把它从 task.review 移除。「自过滤」只在重新进页(reviewDue)
// 时发生。于是 完成全部 → 回总览 → 按钮仍显示"还剩 N" → 再点 → buildQueue 把
// 刚复习完的词原样再入队 → done 无限涨、突破 planned。
//
// 契约(本次修复):过完一个复习词,必须同步从会话内 task.review 移除
// (daily-queue.js 的 noteItemDone),使会话内状态与"进页现算"对齐。
//
// 模拟的是 daily.js 的完整会话流(不含 DOM):ensureTodayTask → buildQueue →
// 逐词 schedule+setSeedReview / markWordDone / noteItemDone → 重入 → 断言不增。
import assert from "node:assert";

// ---- localStorage 内存 shim(必须在动态 import 前装好,seed/store/daily-store 都用它) ----
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
  ensureTodayTask, markWordDone, totalWordsDone, dateKey,
  __reset, __setCachesForTest,
} = await import("./daily-store.js");

const NOW = new Date("2026-07-16T09:00:00");
const YESTERDAY = "2026-07-15";

// 造数据:total 个内置词(都有 aids 资格),前 dueN 个是"学过且今天到期"的复习词。
function setup({ total = 40, dueN = 10, newPerDay = 30 } = {}) {
  _mem.clear();
  __reset();
  const words = [];
  for (let i = 1; i <= total; i++) {
    words.push({ word: `word${String(i).padStart(4, "0")}`, def: `释义${i}`, aids: null });
  }
  const wordlist = words.map((w, idx) => ({ word: w.word, freq_rank: idx + 1 }));
  const seedIndex = new Map(words.map((w) => [w.word.toLowerCase(), w]));
  __setCachesForTest({ wordlist, seedIndex });
  // 前 dueN 个词:有 seed_review 记录、昨天到期 → 今天该复习
  const reviews = {};
  for (let i = 0; i < dueN; i++) {
    reviews[words[i].word.toLowerCase()] = {
      level: 1, next_due: YESTERDAY, history: [], correct: 1, wrong: 0, fuzzy: 0,
      streak: 1, lapses: 0, stability: 1.5, difficulty: 5, last_review: "2026-07-14",
    };
  }
  localStorage.setItem("ielts_vocab_seed_review", JSON.stringify(reviews));
  localStorage.setItem("ielts_daily", JSON.stringify({ settings: { new_per_day: newPerDay } }));
  return { seedIndex };
}

// 模拟 daily.js 的 wrapReviewEntry:seed 查索引,vocab 查生词库
const wrap = (seedIndex) => (r) => {
  if (r.origin === "seed") return seedIndex.get(r.word.toLowerCase()) || null;
  const vocab = JSON.parse(localStorage.getItem("ielts_vocab") || "[]");
  return vocab.find((x) => x.word.toLowerCase() === r.word.toLowerCase()) || null;
};

// 模拟一次完整过词会话:把当前队列全部过完(评分 rating),返回过词数。
// 与 daily.js 的评分处理器逐行对应:gradeItem(按 origin 路由) → markWordDone →
// noteItemDone → shift。now 可指定,用于跨午夜等时间场景。
function studyAll(task, seedIndex, rating = "remembered", now = NOW) {
  const queue = buildQueue(task, wrap(seedIndex));
  for (const item of queue) {
    if (item.origin === "vocab") {
      gradeReview(item.entry.word, rating, now);
    } else {
      const { review } = schedule(getSeedReview(item.entry.word), rating, now);
      setSeedReview(item.entry.word, review);
    }
    const updated = markWordDone(item.kind === "review" ? "review" : "new", now);
    if (updated) task.day = updated;
    noteItemDone(task, item); // ← 无限刷修复的核心:会话内同步移除已过的复习词
  }
  return queue.length;
}

// ---- 1) 基本盘:10 复习 + 30 新词,一次过完,done == planned ----
{
  const { seedIndex } = setup();
  const task = await ensureTodayTask(NOW);
  assert.equal(task.review.length, 10, "应有 10 个到期复习词");
  assert.equal(task.newWords.length, 30, "应放出 30 个新词");
  assert.equal(task.day.planned, 40, "planned = 40");
  const n = studyAll(task, seedIndex);
  assert.equal(n, 40, "一次会话应过 40 词");
  assert.equal(task.day.reviewed_done + task.day.new_done, 40, "done 应为 40");
}

// ---- 2) 核心回归(用户报告的 bug):过完后不重进页,直接再点"继续" ----
//     旧代码:task.review 还是 10 个 → 又入队 10 个 → 可以一直记。
//     修复后:会话内 task.review 已清空 → 队列为空 → done 不再涨。
{
  const { seedIndex } = setup();
  const task = await ensureTodayTask(NOW);
  studyAll(task, seedIndex);
  assert.equal(task.review.length, 0, "过完后会话内 task.review 应已清空(不等重进页)");
  const q2 = buildQueue(task, wrap(seedIndex));
  assert.equal(q2.length, 0, "重入队列应为空 —— 不能把刚复习完的词再入队");
}

// ---- 3) 压力:狂点"继续"100 次,done 必须钉死在 planned,不突破上限 ----
{
  const { seedIndex } = setup();
  const task = await ensureTodayTask(NOW);
  studyAll(task, seedIndex);
  for (let i = 0; i < 100; i++) studyAll(task, seedIndex);
  const done = task.day.reviewed_done + task.day.new_done;
  assert.equal(done, task.day.planned, `狂点重进 100 次后 done(${done}) 仍应 == planned(${task.day.planned})`);
  assert.equal(totalWordsDone(), 40, "累计词数也不能被刷上去");
}

// ---- 4) 压力:大词量(500 复习 + 100 新),中途退出再继续,总量恰好 = planned ----
{
  const { seedIndex } = setup({ total: 800, dueN: 500, newPerDay: 100 });
  const task = await ensureTodayTask(NOW);
  assert.equal(task.day.planned, 600, "planned = 500+100");
  // 模拟中途退出:只过前 137 个(手动切片,与 daily.js 的 queue.shift 等价)
  const q = buildQueue(task, wrap(seedIndex));
  for (const item of q.slice(0, 137)) {
    const { review } = schedule(getSeedReview(item.entry.word), "remembered", NOW);
    setSeedReview(item.entry.word, review);
    const updated = markWordDone(item.kind === "review" ? "review" : "new", NOW);
    if (updated) task.day = updated;
    noteItemDone(task, item);
  }
  // 回总览再继续:剩余应恰好 600-137,且过完即封顶
  const rest = buildQueue(task, wrap(seedIndex));
  assert.equal(rest.length, 600 - 137, "中途退出后重入,剩余应 = planned - 已过");
  studyAll(task, seedIndex);
  for (let i = 0; i < 20; i++) studyAll(task, seedIndex);
  assert.equal(task.day.reviewed_done + task.day.new_done, 600, "大词量下也不能突破上限");
}

// ---- 5) 全按「忘记」也不能当天无限刷(FSRS 最短间隔 1 天,到期在明天) ----
{
  const { seedIndex } = setup();
  const task = await ensureTodayTask(NOW);
  studyAll(task, seedIndex, "forgot");
  for (let i = 0; i < 50; i++) studyAll(task, seedIndex, "forgot");
  assert.equal(task.day.reviewed_done + task.day.new_done, 40, "全按忘记也应封顶在 planned");
}

// ---- 6) 重新进页(刷新)后:复习已推到未来,恢复的任务队列应为空 ----
{
  const { seedIndex } = setup();
  let task = await ensureTodayTask(NOW);
  studyAll(task, seedIndex);
  task = await ensureTodayTask(NOW); // 模拟刷新页面
  assert.equal(task.review.length, 0, "刷新后 reviewDue 应为空(都推到未来了)");
  assert.equal(buildQueue(task, wrap(seedIndex)).length, 0, "刷新后队列也应为空");
  assert.equal(task.day.completed, true, "当天应标记完成");
}

// ---- 7) noteItemDone 只删对应的那一个:同名不同源、未过的词不受影响 ----
{
  const task = {
    review: [
      { word: "alpha", origin: "seed" },
      { word: "alpha", origin: "vocab" },
      { word: "beta", origin: "seed" },
    ],
    newWords: [],
    day: { planned: 3, reviewed_done: 0, new_done: 0 },
  };
  noteItemDone(task, { entry: { word: "Alpha" }, kind: "review", origin: "vocab" });
  assert.deepEqual(
    task.review.map((r) => r.word + ":" + r.origin),
    ["alpha:seed", "beta:seed"],
    "只应移除 vocab 源的 alpha(大小写不敏感),seed 源的保留",
  );
  noteItemDone(task, { entry: { word: "gamma" }, kind: "new", origin: "seed" });
  assert.equal(task.review.length, 2, "新词过完不动 task.review");
}

// ---- 8) 生词来源的复习词:评分走 store.gradeReview,同样不能重复入队 ----
{
  const { seedIndex } = setup({ total: 40, dueN: 2, newPerDay: 2 }); // 2 个 seed 复习 + 2 新词
  // 再加 2 个到期的生词(词名与 seed 词表不同,避免同名去重介入)
  localStorage.setItem("ielts_vocab", JSON.stringify([
    { word: "vword1", def: "生词1", review: { level: 1, next_due: YESTERDAY, history: [], correct: 1, wrong: 0, fuzzy: 0, streak: 1, lapses: 0 } },
    { word: "vword2", def: "生词2", review: { level: 1, next_due: YESTERDAY, history: [], correct: 1, wrong: 0, fuzzy: 0, streak: 1, lapses: 0 } },
  ]));
  const task = await ensureTodayTask(NOW);
  assert.equal(task.review.length, 4, "复习应为 2 生词 + 2 内置词");
  assert.equal(task.day.planned, 6, "planned = 4 复习 + 2 新词");
  const n = studyAll(task, seedIndex);
  assert.equal(n, 6, "混合来源一次会话应过 6 词");
  assert.equal(task.review.length, 0, "vocab 来源的复习词也应被 noteItemDone 移除");
  for (let i = 0; i < 20; i++) studyAll(task, seedIndex);
  assert.equal(task.day.reviewed_done + task.day.new_done, 6, "混合来源狂点重进也不能突破上限");
  const vocab = JSON.parse(localStorage.getItem("ielts_vocab"));
  for (const v of vocab) {
    assert.ok(v.review.next_due > dateKey(NOW), `生词 ${v.word} 评分后 next_due 应推到未来`);
  }
}

// ---- 9) 空态:无到期复习 + 配额 0,不崩、队列空、planned 0 ----
{
  const { seedIndex } = setup({ total: 10, dueN: 0, newPerDay: 0 });
  const task = await ensureTodayTask(NOW);
  assert.equal(task.day.planned, 0, "无复习无新词:planned 0");
  assert.equal(buildQueue(task, wrap(seedIndex)).length, 0, "队列应为空");
  const again = await ensureTodayTask(NOW);
  assert.equal(again.day.planned, 0, "幂等:再进一次仍是 0");
}

// ---- 10) 跨午夜:23:59 开始,00:01 评分 —— 不崩,SRS 生效,第二天正常 ----
{
  const { seedIndex } = setup({ total: 10, dueN: 2, newPerDay: 0 });
  const day1 = new Date("2026-07-16T23:59:00");
  const day2 = new Date("2026-07-17T00:01:00");
  const task = await ensureTodayTask(day1);
  assert.equal(task.day.planned, 2, "day1 应有 2 个复习");
  // 队列在 day1 建好,评分动作发生在 day2 凌晨(markWordDone 找不到 day2 记录返回 null)
  const n = studyAll(task, seedIndex, "remembered", day2);
  assert.equal(n, 2, "跨午夜过词不崩,2 个都能过完");
  const d = JSON.parse(localStorage.getItem("ielts_daily"));
  assert.equal(d.days["2026-07-16"].reviewed_done, 0, "跨午夜的进度记不到前一天(已知取舍,别崩就行)");
  const t2 = await ensureTodayTask(day2);
  assert.equal(t2.review.length, 0, "SRS 已生效:day2 不再到期");
  assert.equal(t2.day.planned, 0, "day2 新一天正常生成");
}

console.log("daily-session-check.mjs 全部断言通过 ✅");
