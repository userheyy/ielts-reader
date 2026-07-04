// 听写判分模块自检:node js/dictation-check.mjs
// 全部通过输出 PASS 汇总并退出码 0;任一失败输出 FAIL 明细并退出码 1。
import { scoreDictation, normalizeToken } from "./dictation.js";

let passed = 0;
const failures = [];

function check(name, cond, detail) {
  if (cond) {
    passed += 1;
  } else {
    failures.push(`  ✗ ${name}${detail ? ` — ${detail}` : ""}`);
  }
}

function statuses(r) {
  return r.tokens.map((x) => x.status).join(",");
}

// 1. 完全正确 = 100,全部 correct
{
  const r = scoreDictation("The cat sat on the mat.", "The cat sat on the mat.");
  check("完全正确 percent=100", r.percent === 100, `got ${r.percent}`);
  check("完全正确 全部 correct", r.tokens.every((t) => t.status === "correct"), statuses(r));
}

// 2. 大小写与标点无关
{
  const r = scoreDictation("hello world", "Hello, World!");
  check("大小写标点无关 percent=100", r.percent === 100, `got ${r.percent}`);
}

// 3. 漏词
{
  const r = scoreDictation("the sat", "the cat sat");
  check("漏词 percent=67", r.percent === 67, `got ${r.percent}`);
  const miss = r.tokens.find((t) => t.status === "missing");
  check("漏词 标出 missing cat", !!miss && miss.t === "cat", JSON.stringify(r.tokens));
}

// 4. 错词(替换)→ wrong,带 hint
{
  const r = scoreDictation("I like red apples", "I like green apples");
  check("错词 percent=75", r.percent === 75, `got ${r.percent}`);
  const wrong = r.tokens.find((t) => t.status === "wrong");
  check("错词 标出 wrong green(hint=red)", !!wrong && wrong.t === "green" && wrong.hint === "red",
    JSON.stringify(r.tokens));
}

// 5. 多词 → extra,percent 仍按参考句算
{
  const r = scoreDictation("hello big world", "hello world");
  check("多词 percent=100", r.percent === 100, `got ${r.percent}`);
  const extra = r.tokens.find((t) => t.status === "extra");
  check("多词 标出 extra big", !!extra && extra.t === "big", JSON.stringify(r.tokens));
}

// 6. 数字:"21." 归一成 "21"
{
  const r = scoreDictation("it costs 21", "It costs 21.");
  check("数字归一 percent=100", r.percent === 100, `got ${r.percent}`);
}

// 7. 空输入 = 0,参考词全部 missing
{
  const r = scoreDictation("", "some words here");
  check("空输入 percent=0", r.percent === 0, `got ${r.percent}`);
  check("空输入 全部 missing", r.tokens.length === 3 && r.tokens.every((t) => t.status === "missing"),
    statuses(r));
}

// 8. 双空 = 0,不崩
{
  const r = scoreDictation("", "");
  check("双空 percent=0 且无 token", r.percent === 0 && r.tokens.length === 0, JSON.stringify(r));
}

// 9. 撇号词保留(don't)
{
  const r = scoreDictation("don't stop now", "Don't stop now!");
  check("撇号词 percent=100", r.percent === 100, `got ${r.percent}`);
}

// 10. 弯引号 ’ 与直撇号 ' 等价
{
  const r = scoreDictation("don't stop", "Don’t stop");
  check("弯引号等价 percent=100", r.percent === 100, `got ${r.percent}`);
}

// 11. normalizeToken 单元
check("normalizeToken 去尾逗号保撇号", normalizeToken("Don't,") === "don't", normalizeToken("Don't,"));
check("normalizeToken 括号句点数字", normalizeToken("(21).") === "21", normalizeToken("(21)."));
check("normalizeToken 保连字符", normalizeToken("TWENTY-one") === "twenty-one", normalizeToken("TWENTY-one"));
check("normalizeToken 空值", normalizeToken(null) === "", JSON.stringify(normalizeToken(null)));

// 12. 乱序不全对:LCS 不会把顺序错的词全部记对
{
  const r = scoreDictation("mat the on sat cat the", "the cat sat on the mat");
  check("乱序 percent<100", r.percent < 100, `got ${r.percent}`);
}

const total = passed + failures.length;
if (failures.length === 0) {
  console.log(`PASS  ${passed}/${total} 项断言全部通过`);
  process.exit(0);
} else {
  console.error(`FAIL  ${failures.length}/${total} 项断言未通过:`);
  for (const f of failures) console.error(f);
  process.exit(1);
}
