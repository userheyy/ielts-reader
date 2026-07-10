// 主动回忆(拼写 / 例句填空)辅助模块 —— 复习/今日两处共用。
// 研究依据:让学习者"打出"单词(产出式检索)比只"认得"记得更牢
// (testing effect + generation effect)。判分结果自动映射到现有 SRS 评分,
// 用户仍可手动覆盖。纯前端、无依赖。

function norm(s) {
  return String(s == null ? "" : s).trim().toLowerCase().replace(/\s+/g, " ");
}

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Levenshtein 编辑距离(容忍拼写手误)。滚动数组实现,O(mn) 时间 O(n) 空间。
export function levenshtein(a, b) {
  a = norm(a); b = norm(b);
  if (a === b) return 0;
  const m = a.length, n = b.length;
  if (!m) return n;
  if (!n) return m;
  let prev = Array.from({ length: n + 1 }, (_, i) => i);
  const cur = new Array(n + 1);
  for (let i = 1; i <= m; i++) {
    cur[0] = i;
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
    }
    for (let j = 0; j <= n; j++) prev[j] = cur[j];
  }
  return prev[n];
}

// 判分:'exact'(完全正确) / 'near'(差一两个字母,拼写手误) / 'wrong'
export function judgeSpelling(typed, target) {
  const t = norm(typed), g = norm(target);
  if (!t) return "wrong";
  if (t === g) return "exact";
  const d = levenshtein(t, g);
  const tol = g.length >= 8 ? 2 : 1; // 长词放宽到 2
  return d <= tol ? "near" : "wrong";
}

// 判分结果 → SRS 评分(可被用户覆盖)
export function ratingFromResult(result) {
  return result === "exact" ? "remembered" : result === "near" ? "fuzzy" : "forgot";
}

// 把例句里的目标词(含常见词尾变形)挖空。返回 { html, ok }。
// ok=false 表示例句里没找到该词(退回只给中文释义提示)。
export function blankSentence(sentence, target) {
  const s = String(sentence || "");
  if (!s || !target) return { html: esc(s), ok: false };
  const g = String(target).trim().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(`\\b${g}(?:s|es|ed|ing|d|ies|er|est|ly)?\\b`, "i");
  const m = s.match(re);
  if (!m) return { html: esc(s), ok: false };
  const width = Math.max(5, String(target).length);
  const blank = `<span class="cloze-blank">${" ".repeat(width)}</span>`;
  return { html: esc(s.slice(0, m.index)) + blank + esc(s.slice(m.index + m[0].length)), ok: true };
}

// 首字母 + 长度提示,例如 "r _ _ _ _ _ _ (7)"。答不出时可给的脚手架。
export function letterHint(target) {
  const w = String(target || "");
  if (!w) return "";
  const rest = w.length > 1 ? " " + "_ ".repeat(w.length - 1).trim() : "";
  return `${w[0]}${rest}　(${w.length})`;
}

// 反馈文案 + 状态类名
export function feedbackFor(result, target) {
  if (result === "exact") return { cls: "ok", text: "✓ 正确" };
  if (result === "near") return { cls: "near", text: `≈ 就差一点 · 正确拼写：${esc(target)}` };
  return { cls: "wrong", text: `✗ 正确答案：${esc(target)}` };
}
