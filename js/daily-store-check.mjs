// daily-store 今日任务逻辑测试。重点覆盖:任务设置(new_per_day)保存后要真正生效。
// 与其它 *-check.mjs 一致:node:assert + 内存后端 + 显式 now,避免时区/时间漂移。
//
// 注入测试数据(词表 / 内置词索引),绕过 fetch —— Node 环境下相对路径 fetch 拿不到文件。
import assert from "node:assert";
import {
  ensureTodayTask, rebuildTodayTask, markWordDone,
  getSettings, updateSettings, loadDaily, dateKey,
  getExcludedWords, removeWordFromMemoryQueue, restoreWordToMemoryQueue,
  __reset, __setCachesForTest,
} from "./daily-store.js";

const NOW = new Date("2026-07-06T09:00:00");

// 造 50 个"已生成 aids、未学过"的内置词,按词频升序,供新词选取。
function fakeData(n = 50) {
  const words = [];
  for (let i = 1; i <= n; i++) {
    words.push({ word: `word${String(i).padStart(3, "0")}`, def: `释义${i}`, aids: null });
  }
  const wordlist = words.map((w, idx) => ({ word: w.word, freq_rank: idx + 1 }));
  const seedIndex = new Map(words.map((w) => [w.word.toLowerCase(), w]));
  return { wordlist, seedIndex };
}

function reset() {
  __reset();
  const { wordlist, seedIndex } = fakeData();
  __setCachesForTest({ wordlist, seedIndex });
}

// ---- 1) 首次生成:配额 = new_per_day 默认 30 ----
reset();
let task = await ensureTodayTask(NOW);
assert.equal(task.newWords.length, 30, "默认配额应放出 30 个新词");
assert.equal(task.day.planned, 30, "planned 应为 30");

// ---- 2) BUG 复现:改设置后 ensureTodayTask 幂等,不换词(记录已存在) ----
updateSettings({ new_per_day: 5 });
assert.equal(getSettings().new_per_day, 5, "设置应已写入");
task = await ensureTodayTask(NOW);
assert.equal(task.newWords.length, 30, "ensureTodayTask 幂等:仍是旧的 30 词(证明需要显式 rebuild)");

// ---- 3) 核心修复:rebuildTodayTask 在未开始时应套用新配额 ----
task = await rebuildTodayTask(NOW);
assert.equal(task.newWords.length, 5, "rebuild 后应只剩 5 个新词");
assert.equal(task.day.planned, 5, "planned 应更新为 5");
assert.equal(loadDaily().days[dateKey(NOW)].new_words.length, 5, "落盘的 new_words 也应是 5");

// ---- 4) 提高配额也要生效 ----
updateSettings({ new_per_day: 40 });
task = await rebuildTodayTask(NOW);
assert.equal(task.newWords.length, 40, "提高到 40 后 rebuild 应放出 40 词");
assert.equal(task.day.planned, 40, "planned 应为 40");

// ---- 5) 保护已开始的进度:已完成词保留,新配额调整未完成新词 ----
reset();
await ensureTodayTask(NOW);            // 默认 30
markWordDone("new", NOW);              // 学了 1 个新词
updateSettings({ new_per_day: 5 });
task = await rebuildTodayTask(NOW);
assert.equal(task.newWords.length, 5, "已开始(done>0)时应保留已完成词并套用新配额");
assert.equal(task.day.new_done, 1, "已完成计数应保留");
assert.equal(task.day.planned, 5, "planned 应按新的新词配额更新");

// ---- 6) 移出当前新词:不计完成、今日总数减一、后续队列不再出现 ----
reset();
task = await ensureTodayTask(NOW);
const removedWord = task.newWords[0].word;
let removed = removeWordFromMemoryQueue(removedWord, "new", NOW);
assert.equal(removed.day.planned, 29, "移出 1 个新词后 planned 应减一");
assert.equal(removed.day.new_done, 0, "移出不是学会,不能增加完成数");
task = await ensureTodayTask(NOW);
assert.equal(task.newWords.length, 29, "今日新词列表应少 1 个");
assert.ok(!task.newWords.some((w) => w.word === removedWord), "被移出的词不应仍在今日列表");
assert.equal(getExcludedWords()[0].word, removedWord, "移出记录应持久化并可供设置页管理");

// ---- 7) 重复移出幂等:不能重复扣 planned ----
removeWordFromMemoryQueue(removedWord, "new", NOW);
assert.equal(loadDaily().days[dateKey(NOW)].planned, 29, "重复移出不能重复扣今日总数");

// ---- 8) 当天恢复:回到今日任务,planned 也恢复 ----
restoreWordToMemoryQueue(removedWord, NOW);
task = await ensureTodayTask(NOW);
assert.equal(task.day.planned, 30, "当天恢复后 planned 应加回");
assert.ok(task.newWords.some((w) => w.word === removedWord), "当天恢复后词应重新进入今日任务");
assert.equal(getExcludedWords().length, 0, "恢复后应从已移出列表消失");

// ---- 9) 跨天保持排除:被移出的词不会被下一天重新选作新词 ----
reset();
task = await ensureTodayTask(NOW);
const excludedTomorrow = task.newWords[0].word;
removeWordFromMemoryQueue(excludedTomorrow, "new", NOW);
const TOMORROW = new Date("2026-07-07T09:00:00");
task = await ensureTodayTask(TOMORROW);
assert.ok(!task.newWords.some((w) => w.word === excludedTomorrow), "被移出的词次日也不应重新进入任务");

console.log("daily-store.js 全部断言通过 ✅");
