// 听写判分模块:纯函数、无 DOM,供 listening 页与 node 测试(dictation-check.mjs)共用。
//
// scoreDictation(用户输入, 参考句) → { percent, tokens }
//   percent: 正确词数 / 参考句词数 * 100,四舍五入取整;参考句为空时恒为 0。
//   tokens:  按阅读顺序排列的对照结果,每项 {t, status, hint?}
//     correct  写对了(绿)          t = 参考词
//     missing  漏掉的词(灰删除线)   t = 参考词
//     wrong    写错的词(红)         t = 参考词,hint = 用户实际写的词
//     extra    多写的词(橙)         t = 用户多写的词
//
// 对齐算法:经典 LCS(最长公共子序列)动态规划。两个匹配点之间的"缺口"里,
// 参考侧与用户侧的词一一配对记为 wrong(写错),配不上对的分别记 missing / extra。

// 单词归一:小写、去首尾标点(如 "21." → "21"、"(word)" → "word"),
// 保留词内部的撇号(don't)、连字符(twenty-one)和小数点(3.5)。
export function normalizeToken(t) {
  let w = String(t == null ? "" : t).toLowerCase();
  w = w.replace(/[‘’`]/g, "'"); // 弯引号/反引号统一成直撇号
  w = w.replace(/^[^a-z0-9]+|[^a-z0-9]+$/g, ""); // 只削首尾的非字母数字
  return w;
}

function tokenize(text) {
  return String(text == null ? "" : text)
    .split(/\s+/)
    .map(normalizeToken)
    .filter(Boolean);
}

export function scoreDictation(userText, refText) {
  const ref = tokenize(refText);
  const user = tokenize(userText);
  const n = ref.length;
  const m = user.length;

  // LCS 长度表:dp[i][j] = ref[i:] 与 user[j:] 的最长公共子序列长度
  const dp = [];
  for (let i = 0; i <= n; i++) dp.push(new Array(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[i][j] = ref[i] === user[j]
        ? dp[i + 1][j + 1] + 1
        : Math.max(dp[i + 1][j], dp[i][j + 1]);
    }
  }

  // 回溯产出 token 序列;两个匹配点之间的缺口先攒着,再配对成 wrong/missing/extra
  const tokens = [];
  let correct = 0;
  let refGap = [];
  let userGap = [];
  const flushGap = () => {
    const k = Math.min(refGap.length, userGap.length);
    for (let x = 0; x < k; x++) tokens.push({ t: refGap[x], status: "wrong", hint: userGap[x] });
    for (let x = k; x < refGap.length; x++) tokens.push({ t: refGap[x], status: "missing" });
    for (let x = k; x < userGap.length; x++) tokens.push({ t: userGap[x], status: "extra" });
    refGap = [];
    userGap = [];
  };

  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (ref[i] === user[j]) {
      flushGap();
      tokens.push({ t: ref[i], status: "correct" });
      correct += 1;
      i += 1;
      j += 1;
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      refGap.push(ref[i]);
      i += 1;
    } else {
      userGap.push(user[j]);
      j += 1;
    }
  }
  while (i < n) refGap.push(ref[i++]);
  while (j < m) userGap.push(user[j++]);
  flushGap();

  const percent = n === 0 ? 0 : Math.round((correct / n) * 100);
  return { percent, tokens };
}
