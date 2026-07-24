// 深度句子解析卡渲染模块(Schema v2 的 sentence.deep / item.paraphrase → HTML)。
// 与 aids.js 同范式:纯函数、只拼 HTML 字符串,不含任何存储/网络/DOM 事件逻辑。
// 交互(「+入库」按钮、考点替换 chip 点击)由页面脚本(reader.js)事件委托处理。
//
// deep 结构(所有字段可选,向后兼容):
//   pattern:        {id:'sv|svc|svo|svoo|svoc', label, tag, skeleton:[{role,text,zh}], plain}
//   chunks:         [{text, role, zh, note, tag?}]  role∈S/V/O/IO/C/attr/adv/app/conn/clause
//   grammar_points: [{tag, name, explain}]          tag∈data/grammar-tags.json
//   vocab:          [{w, lemma, pos, def, aids, synonyms:[{w,note}], confusables:[{w,note}]}]
//                   aids 与 data/vocab-seed.json 同构,直接喂给 aids.js 的 renderAids()
//   expressions:    [{text, zh, usage}]
import { renderAids } from "./aids.js";

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// 成分角色 → 彩色块样式(主语绿/谓语红/宾语蓝/补语琥珀/修饰类灰,参照 .mchip 的配色思路)
const ROLE_CLS = { S: "role-s", V: "role-v", O: "role-o", IO: "role-o", C: "role-c" };
const ROLE_ZH = {
  S: "主语", V: "谓语", O: "宾语", IO: "间接宾语", C: "补语",
  attr: "定语", adv: "状语", app: "同位语", conn: "连接词", clause: "从句",
};
const KIND_ZH = { syn: "同义词", verbatim: "原词", para: "意译", neg: "反向" };

function roleCls(role) { return ROLE_CLS[role] || "role-m"; }
function roleZh(role) { return ROLE_ZH[role] || role || ""; }

function tagLink(tag, text) {
  return `<a class="deep-taglink" href="grammar.html#${esc(tag)}">${esc(text)}</a>`;
}

// 一个可折叠小节;body 为空则整节不渲染
function section(title, body, open) {
  if (!body) return "";
  return `<details class="deep-sec"${open ? " open" : ""}><summary>${esc(title)}</summary><div class="deep-sec-body">${body}</div></details>`;
}

// ① 句型主干:skeleton 彩色块 + 白话主干
function renderPattern(p) {
  if (!p || typeof p !== "object" || !Array.isArray(p.skeleton) || !p.skeleton.length) return "";
  const chips = p.skeleton.map((k) =>
    `<span class="skel ${roleCls(k.role)}"><i>${esc(roleZh(k.role))}</i><b>${esc(k.text)}</b><small>${esc(k.zh)}</small></span>`,
  ).join('<span class="skel-plus">→</span>');
  const label = p.label
    ? `<div class="deep-pattern-label">${p.tag ? tagLink(p.tag, p.label) : esc(p.label)}</div>` : "";
  const plain = p.plain ? `<div class="deep-plain">${esc(p.plain)}</div>` : "";
  return `${label}<div class="deep-skel">${chips}</div>${plain}`;
}

// ② 成分拆解:线性覆盖整句的 chunks 列表
function renderChunks(chunks) {
  if (!Array.isArray(chunks) || !chunks.length) return "";
  return chunks.map((c) => {
    const link = c.tag ? ` ${tagLink(c.tag, "📖 语法详解")}` : "";
    const note = (c.note || c.tag)
      ? `<div class="chunk-note">${esc(c.note)}${link}</div>` : "";
    return `<div class="chunk">
      <div class="chunk-row"><span class="chunk-en ${roleCls(c.role)}">${esc(c.text)}</span><span class="chunk-role">${esc(roleZh(c.role))}</span><span class="chunk-zh">${esc(c.zh)}</span></div>
      ${note}</div>`;
  }).join("");
}

// ③ 语法点:名称链到语法书 + 白话讲解
function renderGrammarPoints(points) {
  if (!Array.isArray(points) || !points.length) return "";
  return points.map((g) => `<div class="gp">
      <div class="gp-name">${g.tag ? tagLink(g.tag, g.name) : esc(g.name)}</div>
      <div class="gp-explain">${esc(g.explain)}</div>
    </div>`).join("");
}

function pills(list, cls) {
  return (list || [])
    .map((s) => `<span class="${cls}">${esc(s.w)}${s.note ? `<i>${esc(s.note)}</i>` : ""}</span>`)
    .join("");
}

// ④ 词汇深挖:词头 + 入库按钮 + renderAids 复用 + 同义/易混 pills
function renderVocab(vocab) {
  if (!Array.isArray(vocab) || !vocab.length) return "";
  return vocab.map((v) => {
    const syn = Array.isArray(v.synonyms) && v.synonyms.length
      ? `<div class="dw-line"><span class="aid-label">同义替换</span><span class="dw-pills">${pills(v.synonyms, "syn-pill")}</span></div>` : "";
    const conf = Array.isArray(v.confusables) && v.confusables.length
      ? `<div class="dw-line"><span class="aid-label">易混词</span><span class="dw-pills">${pills(v.confusables, "conf-pill")}</span></div>` : "";
    return `<div class="deep-word">
      <div class="deep-word-head">
        <b class="dw-w">${esc(v.w)}</b><span class="dw-pos">${esc(v.pos)}</span><span class="dw-def">${esc(v.def)}</span>
        <button type="button" class="deep-add-word" data-word="${esc(v.lemma || v.w)}" data-pos="${esc(v.pos)}" data-def="${esc(v.def)}" data-aids="${esc(JSON.stringify(v.aids || null))}">+ 入库</button>
      </div>
      ${renderAids(v.aids)}${syn}${conf}</div>`;
  }).join("");
}

// ⑤ 同义替换汇总:聚合本句所有 vocab 的 synonyms
function renderSynAgg(vocab) {
  if (!Array.isArray(vocab)) return "";
  return vocab
    .filter((v) => Array.isArray(v.synonyms) && v.synonyms.length)
    .map((v) => `<div class="syn-agg-row"><b>${esc(v.lemma || v.w)}</b><span class="syn-agg-eq">⇄</span><span class="dw-pills">${pills(v.synonyms, "syn-pill")}</span></div>`)
    .join("");
}

// ⑥ 表达积累
function renderExpressions(exprs) {
  if (!Array.isArray(exprs) || !exprs.length) return "";
  return exprs.map((e) => `<div class="expr">
      <div class="expr-head"><b class="expr-text">${esc(e.text)}</b><span class="expr-zh">${esc(e.zh)}</span></div>
      ${e.usage ? `<div class="expr-usage">${esc(e.usage)}</div>` : ""}</div>`).join("");
}

// 主入口:deep 对象 → 两层渐进展示。语法拆解(默认展开) + 词汇深挖(默认折叠)。
export function renderDeep(deep) {
  if (!deep || typeof deep !== "object") return "";

  // 语法拆解:骨架 + 成分拆解 + 语法点(合为一体,默认展开)
  const grammarBody = [
    renderPattern(deep.pattern),
    renderChunks(deep.chunks),
    renderGrammarPoints(deep.grammar_points),
  ].filter(Boolean).join("");
  const grammar = grammarBody
    ? `<details class="deep-tier" open><summary>语法拆解</summary><div class="deep-tier-body">${grammarBody}</div></details>`
    : "";

  // 词汇深挖
  const vocabBody = [renderVocab(deep.vocab), renderSynAgg(deep.vocab), renderExpressions(deep.expressions)].filter(Boolean).join("");
  const vocab = vocabBody
    ? `<details class="deep-tier"><summary>词汇深挖<small>重点词 · 同义替换 · 好表达</small></summary><div class="deep-tier-body">${vocabBody}</div></details>`
    : "";

  const parts = [grammar, vocab].filter(Boolean);
  if (!parts.length) return "";
  return `<div class="deep">${parts.join("")}</div>`;
}

// 「考点替换」折叠块:题干词 ⇄ 原文词 chips + kind 徽标 + 陷阱/解题讲解。
// opts.sid = evidence 句 id,写进 chip 的 data-sid 供 reader.js 定位原文。
export function renderParaphrase(pp, { sid = null } = {}) {
  if (!pp || typeof pp !== "object" || !Array.isArray(pp.pairs) || !pp.pairs.length) return "";
  const sidAttr = sid ? ` data-sid="${esc(sid)}"` : "";
  const rows = pp.pairs.map((pr) => {
    const kind = pr.kind && KIND_ZH[pr.kind]
      ? `<span class="pp-kind kind-${esc(pr.kind)}">${KIND_ZH[pr.kind]}</span>` : "";
    const note = pr.note ? `<div class="pp-note">${esc(pr.note)}</div>` : "";
    return `<div class="pp-pair">
      <button type="button" class="pp-chip" title="点击定位原文并高亮" data-p="${esc(pr.p)}"${sidAttr}><span class="pp-q">${esc(pr.q)}</span><span class="pp-arrow">⇄</span><span class="pp-p">${esc(pr.p)}</span>${kind}</button>
      ${note}</div>`;
  }).join("");
  const trap = pp.trap ? `<div class="pp-trap">⚠ 易错陷阱:${esc(pp.trap)}</div>` : "";
  const explain = pp.explain ? `<div class="pp-explain">${esc(pp.explain)}</div>` : "";
  return `<details class="deep-sec para-sec" open><summary>考点替换(题干 ⇄ 原文)</summary><div class="deep-sec-body">${rows}${trap}${explain}</div></details>`;
}
