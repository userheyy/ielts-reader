import { addWord, has, loadAll, removeWord, exportJSON, importJSON, gradeReview, reviewWeight, pickReviewWord, getReviewStats, __resetMem } from "./store.js";
import { validatePassage } from "./schema.js";
import assert from "node:assert";

__resetMem();

// 1) 新增
let r = addWord({ word: "Practically", def: "实际上", source: "剑2·T1·P1" });
assert.equal(r.added, true, "首次应新增");
assert.equal(loadAll().length, 1);

// 2) 去重(大小写不敏感)
r = addWord({ word: "practically", def: "实际上(更新)", source: "剑2·T1·P2" });
assert.equal(r.added, false, "同词应更新而非新增");
assert.equal(loadAll().length, 1, "仍应只有 1 条");
assert.equal(has("PRACTICALLY"), true, "has 应大小写不敏感");
assert.equal(loadAll()[0].source, "剑2·T1·P2", "出处应被更新");

// 3) 预留字段存在
assert.ok(loadAll()[0].review && loadAll()[0].status === "new", "应含 status/review 预留字段");

// 4) 复习曲线：遗忘会增加错误/遗忘次数，并保持立即到期
const beforeWeight = reviewWeight(loadAll()[0], new Date("2026-07-02T12:00:00"));
const graded = gradeReview("practically", "forgot", new Date("2026-07-02T12:00:00"));
assert.equal(graded.review.wrong, 1);
assert.equal(graded.review.lapses, 1);
assert.ok(reviewWeight(loadAll()[0], new Date("2026-07-02T12:00:00")) > beforeWeight, "遗忘后优先级应提高");
assert.equal(pickReviewWord("", () => 0).word, "practically");
assert.equal(getReviewStats().due, 1);
const remembered = gradeReview("practically", "remembered", new Date("2026-07-02T12:00:00"));
assert.equal(remembered.review.next_due, "2026-07-03", "本地日期加一天不应受 UTC 时区影响");

// 5) 导出/导入往返
const dump = exportJSON();
__resetMem();
assert.equal(loadAll().length, 0, "重置后应为空");
const imp = importJSON(dump);
assert.equal(imp.total, 1, "导入后应有 1 条");
assert.equal(loadAll()[0].word, "practically");

// 6) 删除
removeWord("practically");
assert.equal(loadAll().length, 0, "删除后应为空");

// 7) importJSON 错误输入应抛出
assert.throws(() => importJSON("not json"), /JSON/, "非法 JSON 应抛出");
assert.throws(() => importJSON('"a string"'), /数组/, "非数组应抛出");

// --- schema.js 校验 ---
const good = { id: "x", source: "s", title: "t", sentences: [
  { id: 1, para: 1, en: "a", zh: "啊", grammar: { type: "t", note: "n" }, words: [] },
] };
assert.equal(validatePassage(good).ok, true, "合法 passage 应通过");
const bad = { id: "x", source: "s", title: "t", sentences: [
  { id: 2, para: 1, en: "a", zh: "啊", grammar: { type: "t" }, words: [] },
] };
const res = validatePassage(bad);
assert.equal(res.ok, false, "非法 passage 应失败");
assert.ok(res.errors.length >= 2, "应报出 id 不连续与 grammar 缺 note");

console.log("store.js 全部断言通过 ✅");
