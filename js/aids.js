// 记忆法卡片渲染组件。三处共用:复习抽词卡、生词库列表展开、词库页。
// 只负责把一个 `aids` 对象渲染成 HTML 片段;不含任何存储/状态逻辑。
//
// aids 结构(所有子字段可空,见 spec §4.1):
//   morphemes:  [{text, type:'prefix'|'root'|'suffix'|'connector', gloss}]
//   derivation: "pre(在前)+dict(说) → 事先说出 → 预测"
//   family:     { root, gloss, words:[{word, def}] }
//   mnemonic:   "联想句"
//   forms:      [{word, pos, def}]

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// 判断 aids 是否有任何可展示内容(用于降级:全空则不渲染卡片)
export function aidsHasContent(aids) {
  if (!aids || typeof aids !== "object") return false;
  const m = Array.isArray(aids.morphemes) && aids.morphemes.length > 0;
  const d = !!(aids.derivation && aids.derivation.trim());
  const f = !!(aids.family && Array.isArray(aids.family.words) && aids.family.words.length > 0);
  const n = !!(aids.mnemonic && aids.mnemonic.trim());
  const w = Array.isArray(aids.forms) && aids.forms.length > 0;
  return m || d || f || n || w;
}

// ① 词根词缀色块(前缀红/词根蓝/后缀琥珀)。connector 用中性灰。
// 返回一行 chips 的 HTML;morphemes 为空则返回 ""。
export function renderMorphemes(aids, { showGloss = true } = {}) {
  const parts = aids && Array.isArray(aids.morphemes) ? aids.morphemes : [];
  if (!parts.length) return "";
  const cls = { prefix: "pre", root: "rt", suffix: "suf", connector: "con" };
  const chips = parts.map((p) => {
    const c = cls[p.type] || "con";
    const gloss = showGloss && p.gloss ? `<small>${esc(p.gloss)}</small>` : "";
    return `<span class="mchip ${c}">${esc(p.text)}${gloss}</span>`;
  });
  return `<div class="mchips">${chips.join('<span class="mplus">+</span>')}</div>`;
}

// 完整记忆法卡:词根拆解 + 推导 + 词族 + 联想 + 词形。
// opts.skipMorphemes: 复习卡里词根已在提示区显示过,正文可跳过避免重复。
export function renderAids(aids, opts = {}) {
  if (!aidsHasContent(aids)) return "";
  const { skipMorphemes = false } = opts;
  const blocks = [];

  if (!skipMorphemes) {
    const m = renderMorphemes(aids);
    if (m) blocks.push(`<div class="aid-block"><span class="aid-label">词根词缀</span>${m}</div>`);
  }
  if (aids.derivation && aids.derivation.trim()) {
    blocks.push(`<div class="aid-block aid-deriv">${esc(aids.derivation)}</div>`);
  }
  if (aids.family && Array.isArray(aids.family.words) && aids.family.words.length) {
    const rootTag = aids.family.root
      ? `<b class="fam-root">${esc(aids.family.root)}${aids.family.gloss ? "（" + esc(aids.family.gloss) + "）" : ""}</b>`
      : "";
    const pills = aids.family.words
      .map((w) => `<span class="fam-pill">${esc(w.word)}<i>${esc(w.def)}</i></span>`)
      .join("");
    blocks.push(`<div class="aid-block"><span class="aid-label">词族</span>${rootTag}<div class="fam-pills">${pills}</div></div>`);
  }
  if (aids.mnemonic && aids.mnemonic.trim()) {
    blocks.push(`<div class="aid-block aid-mnemo"><span class="aid-label">联想</span>${esc(aids.mnemonic)}</div>`);
  }
  if (Array.isArray(aids.forms) && aids.forms.length) {
    const items = aids.forms
      .map((f) => `<span class="form-item"><b>${esc(f.word)}</b> ${esc(f.pos || "")} ${esc(f.def || "")}</span>`)
      .join("");
    blocks.push(`<div class="aid-block"><span class="aid-label">词形</span><div class="form-list">${items}</div></div>`);
  }
  return `<div class="aids">${blocks.join("")}</div>`;
}
