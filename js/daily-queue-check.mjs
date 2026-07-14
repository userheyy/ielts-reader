// daily-queue 过词队列构建测试。核心回归:「继续今日任务」点了没反应。
//
// 根因:复习词是每次进页现算(reviewDue 只返回“今天仍到期”的),完成的复习词
// 会自己从列表消失;而旧 buildQueue 又用 slice(reviewed_done + new_done) 再砍一刀,
// 把复习进度重复计了两次,连未学的新词一起砍没 → 队列空 → 点按钮像没反应。
//
// 正确契约(见 2026-07-03 设计文档):
//   队列 = 全部“当前仍到期”的复习词(复习词自过滤,不需位移) ++ 新词.slice(new_done)
import assert from "node:assert";
import { buildQueue } from "./daily-queue.js";

const R = (n) => Array.from({ length: n }, (_, i) => ({ entry: { word: "r" + i }, kind: "review", origin: "seed" }));
const N = (n) => Array.from({ length: n }, (_, i) => ({ word: "n" + i }));

// ---- 1) 全新一天:没做任何词,队列 = 复习 + 新词 ----
{
  const task = { review: R(300).map((x) => ({ origin: x.origin, word: x.entry.word })), newWords: N(100),
    day: { planned: 400, reviewed_done: 0, new_done: 0 } };
  const q = buildQueue(task, () => ({ word: "x" }));
  assert.equal(q.length, 400, "全新一天队列应为 300+100=400");
}

// ---- 2) 复现 BUG 场景:做了 200 复习后,复习词只剩 100(自过滤),新词一个没动 ----
//    旧代码 slice(200) 会把队列砍空;修复后应剩 100(复习)+100(新)=200。
{
  const task = { review: R(100).map((x) => ({ origin: x.origin, word: x.entry.word })), newWords: N(100),
    day: { planned: 400, reviewed_done: 200, new_done: 0 } };
  const q = buildQueue(task, () => ({ word: "x" }));
  assert.equal(q.length, 200, "复习自过滤后不应再被 reviewed_done 二次砍;应剩 200");
  assert.equal(q.filter((i) => i.kind === "new").length, 100, "新词一个没学,应全部保留");
}

// ---- 3) 用户报告的截图场景:复习144 新100,已完成244(其中新词也学了些) ----
//    关键:new_done 才驱动新词跳过;reviewed_done 不砍复习(已自过滤)。
{
  const task = { review: R(144).map((x) => ({ origin: x.origin, word: x.entry.word })), newWords: N(100),
    day: { planned: 439, reviewed_done: 195, new_done: 49 } }; // done=244
  const q = buildQueue(task, () => ({ word: "x" }));
  // 复习 144 全留 + 新词跳过已学的 49 → 100-49=51
  assert.equal(q.length, 144 + 51, "复习144全留 + 新词剩51 = 195");
  assert.ok(q.length > 0, "队列非空 —— 点“继续”应能进入过词,而不是没反应");
}

// ---- 4) 新词学完一部分:只跳过 new_done 个新词,不多不少 ----
{
  const task = { review: [], newWords: N(30), day: { planned: 30, reviewed_done: 0, new_done: 12 } };
  const q = buildQueue(task, () => ({ word: "x" }));
  assert.equal(q.length, 18, "30 新词学了 12,应剩 18");
  assert.equal(q[0].entry.word, "n12", "应从第 13 个(index 12)新词继续");
}

// ---- 5) 真正全部学完:复习自过滤为空 + 新词全跳过 → 空队列(此时才该显示完成) ----
//    内部自洽:新词全学完 new_done 必须等于 newWords.length(30),复习词已到期完毕故为空。
{
  const task = { review: [], newWords: N(30), day: { planned: 30, reviewed_done: 10, new_done: 30 } };
  const q = buildQueue(task, () => ({ word: "x" }));
  assert.equal(q.length, 0, "复习清空 + 新词全学完,队列应为空");
}

// ---- 6) 复习词取不到词条(wrapReview 返回 null)应被过滤,不进队列 ----
{
  const task = { review: [{ origin: "vocab", word: "ghost" }], newWords: N(2),
    day: { planned: 3, reviewed_done: 0, new_done: 0 } };
  const q = buildQueue(task, () => null); // 词条取不到
  assert.equal(q.length, 2, "取不到词条的复习项应被跳过,只剩 2 个新词");
  assert.ok(q.every((i) => i.kind === "new"), "剩下的都应是新词");
}

console.log("daily-queue.js 全部断言通过 ✅");
