// 深度解析卡渲染冒烟测试(纯函数,node 直接跑):
//   node js/deep-check.mjs
// 断言 renderDeep/renderParaphrase 对真实样例(c14-test1-p1 句1-3、Q1)输出健康 HTML。
import { renderDeep, renderParaphrase } from "./deep.js";
import assert from "node:assert";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const passage = JSON.parse(
  readFileSync(join(here, "..", "data", "passages", "c14-test1-p1.json"), "utf-8"));

let pass = 0;
function ok(cond, msg) { assert.ok(cond, msg); pass++; }

// 1) 前 3 句都有 deep,渲染都健康
for (const sid of [1, 2, 3]) {
  const s = passage.sentences.find((x) => x.id === sid);
  ok(s && s.deep, `句${sid} 应有 deep 样例`);
  const html = renderDeep(s.deep);
  ok(html.length > 200, `句${sid} 渲染应有实质内容`);
  ok(!html.includes("undefined"), `句${sid} 渲染不应含 undefined`);
  ok(!html.includes("[object Object]"), `句${sid} 不应有未序列化对象`);
  ok(html.includes("skel"), `句${sid} 应含句型主干彩色块`);
  ok(html.includes("grammar.html#"), `句${sid} 应含语法书 tag 链接`);
  ok(html.includes("deep-add-word"), `句${sid} 应含「入库」按钮`);
}

// 2) 句3 应体现让步从句 + help sb do 讲解关键词
const s3html = renderDeep(passage.sentences.find((x) => x.id === 3).deep);
ok(s3html.includes("让步") || s3html.includes("Although"), "句3 应讲到让步状语从句");
ok(s3html.includes("repercussion") || s3html.includes("percuss"), "句3 词汇深挖应含 repercussion 词根拆解");

// 3) 词根色块(morpheme)应通过 renderAids 出现(magical = magic + al)
ok(renderDeep(passage.sentences.find((x) => x.id === 1).deep).includes("magic"),
  "句1 应含 magic 词根");

// 4) 无 deep 的对象 → 空串,不炸
ok(renderDeep(null) === "", "renderDeep(null) 应为空串");
ok(renderDeep({}) === "", "renderDeep({}) 应为空串");
ok(renderDeep(undefined) === "", "renderDeep(undefined) 应为空串");

// 5) paraphrase 渲染(Q1)
const q1 = passage.questions[0].items.find((x) => x.number === 1);
ok(q1.paraphrase, "Q1 应有 paraphrase 样例");
const pphtml = renderParaphrase(q1.paraphrase, { sid: 3 });
ok(pphtml.includes("pp-chip"), "paraphrase 应渲染 chip");
ok(pphtml.includes('data-sid="3"'), "chip 应带 evidence 句号");
ok(pphtml.includes("creativity"), "paraphrase 应含答案词");
ok(!pphtml.includes("undefined"), "paraphrase 不应含 undefined");
ok(renderParaphrase(null) === "", "renderParaphrase(null) 应为空串");
ok(renderParaphrase({ pairs: [] }) === "", "空 pairs 应为空串");

// 6) 每个 paraphrase.p 必须逐字(忽略大小写)出现在 evidence 句 en 中(内容正确性)
const s3en = passage.sentences.find((x) => x.id === 3).en.toLowerCase();
for (const pr of q1.paraphrase.pairs) {
  ok(s3en.includes(pr.p.toLowerCase()), `Q1 替换 p="${pr.p}" 必须逐字存在于句3`);
}

console.log(`deep-check.mjs: PASS (${pass} 断言)`);
