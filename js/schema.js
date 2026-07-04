// passage JSON 运行时校验。返回 { ok: boolean, errors: string[] }。
// Schema v2:sentences[].deep 与 questions[].items[].paraphrase 均为可选字段,
// 不存在时完全不校验(48 篇旧文章零影响);存在时才检查内部结构。

const DEEP_PATTERN_IDS = ["sv", "svc", "svo", "svoo", "svoc"];
const DEEP_CHUNK_ROLES = ["S", "V", "O", "IO", "C", "attr", "adv", "app", "conn", "clause"];
const PARAPHRASE_KINDS = ["syn", "verbatim", "para", "neg"];

function validateDeepField(s, errors) {
  const d = s.deep;
  const where = `句${s.id}`;
  if (!d || typeof d !== "object" || Array.isArray(d)) { errors.push(`${where}: deep 应为对象`); return; }
  if (d.pattern !== undefined) {
    const p = d.pattern;
    if (!p || typeof p !== "object") errors.push(`${where}: deep.pattern 应为对象`);
    else {
      if (!DEEP_PATTERN_IDS.includes(p.id)) errors.push(`${where}: deep.pattern.id 非法(${p.id})`);
      if (!Array.isArray(p.skeleton) || p.skeleton.length === 0) {
        errors.push(`${where}: deep.pattern.skeleton 应为非空数组`);
      } else for (const k of p.skeleton) {
        if (typeof k.role !== "string" || typeof k.text !== "string") {
          errors.push(`${where}: skeleton 每项需含 role/text 字符串`);
        }
      }
    }
  }
  if (d.chunks !== undefined) {
    if (!Array.isArray(d.chunks) || d.chunks.length === 0) errors.push(`${where}: deep.chunks 应为非空数组`);
    else for (const c of d.chunks) {
      if (typeof c.text !== "string" || typeof c.zh !== "string") errors.push(`${where}: chunk 需含 text/zh 字符串`);
      if (!DEEP_CHUNK_ROLES.includes(c.role)) errors.push(`${where}: chunk.role 非法(${c.role})`);
    }
  }
  if (d.grammar_points !== undefined) {
    if (!Array.isArray(d.grammar_points)) errors.push(`${where}: deep.grammar_points 应为数组`);
    else for (const g of d.grammar_points) {
      if (typeof g.tag !== "string" || typeof g.name !== "string" || typeof g.explain !== "string") {
        errors.push(`${where}: grammar_point 需含 tag/name/explain 字符串`);
      }
    }
  }
  if (d.vocab !== undefined) {
    if (!Array.isArray(d.vocab)) errors.push(`${where}: deep.vocab 应为数组`);
    else for (const v of d.vocab) {
      if (typeof v.w !== "string" || typeof v.def !== "string") errors.push(`${where}: vocab 每词需含 w/def 字符串`);
      for (const key of ["synonyms", "confusables"]) {
        if (v[key] !== undefined && !Array.isArray(v[key])) errors.push(`${where}: vocab.${key} 应为数组`);
      }
      if (v.aids !== undefined && v.aids !== null && (typeof v.aids !== "object" || Array.isArray(v.aids))) {
        errors.push(`${where}: vocab.aids 应为对象`);
      }
    }
  }
  if (d.expressions !== undefined) {
    if (!Array.isArray(d.expressions)) errors.push(`${where}: deep.expressions 应为数组`);
    else for (const e of d.expressions) {
      if (typeof e.text !== "string" || typeof e.zh !== "string") errors.push(`${where}: expression 需含 text/zh 字符串`);
    }
  }
}

function validateParaphraseField(q, errors) {
  const pp = q.paraphrase;
  const where = `题${q.number}`;
  if (!pp || typeof pp !== "object" || Array.isArray(pp)) { errors.push(`${where}: paraphrase 应为对象`); return; }
  if (!Array.isArray(pp.pairs) || pp.pairs.length === 0) { errors.push(`${where}: paraphrase.pairs 应为非空数组`); return; }
  for (const pr of pp.pairs) {
    if (typeof pr.q !== "string" || typeof pr.p !== "string") errors.push(`${where}: 每对替换需含 q/p 字符串`);
    if (!PARAPHRASE_KINDS.includes(pr.kind)) errors.push(`${where}: 替换 kind 非法(${pr.kind})`);
  }
}

export function validatePassage(d) {
  const errors = [];
  for (const k of ["id", "source", "title", "sentences"]) {
    if (!(k in d)) errors.push(`缺字段 ${k}`);
  }
  if (!Array.isArray(d.sentences) || d.sentences.length === 0) {
    errors.push("sentences 应为非空数组");
    return { ok: false, errors };
  }
  let prevId = 0, prevPara = 1;
  for (const s of d.sentences) {
    for (const k of ["id", "para", "en", "zh", "grammar", "words"]) {
      if (!(k in s)) errors.push(`句${s.id ?? "?"}: 缺字段 ${k}`);
    }
    if (s.id !== prevId + 1) errors.push(`句 id 不连续:期望 ${prevId + 1} 得 ${s.id}`);
    prevId = s.id;
    if (s.para < prevPara) errors.push(`句${s.id}: para 递减`);
    prevPara = s.para;
    if (!s.grammar || typeof s.grammar.type !== "string" || typeof s.grammar.note !== "string") {
      errors.push(`句${s.id}: grammar 需含 type 与 note 字符串`);
    }
    if (!Array.isArray(s.words)) errors.push(`句${s.id}: words 应为数组`);
    if (s.deep !== undefined) validateDeepField(s, errors);
    if (s.details !== undefined) {
      if (!Array.isArray(s.details) || s.details.length === 0) errors.push(`段${s.para}: details 应为非空数组`);
      else for (const [i, detail] of s.details.entries()) {
        if (typeof detail.zh !== "string" || !detail.grammar ||
            typeof detail.grammar.type !== "string" || typeof detail.grammar.note !== "string") {
          errors.push(`段${s.para}第${i + 1}句: 需含 zh 及 grammar.type/note`);
        }
      }
    }
  }
  if (d.questions !== undefined) {
    if (!Array.isArray(d.questions)) errors.push("questions 应为数组");
    else for (const [gi, group] of d.questions.entries()) {
      if (!group || typeof group.title !== "string" || !Array.isArray(group.items)) {
        errors.push(`题组${gi + 1}: 需含 title 与 items 数组`);
        continue;
      }
      for (const q of group.items) {
        if (typeof q.number !== "number" || typeof q.prompt !== "string") {
          errors.push(`题组${gi + 1}: 每题需含 number 与 prompt`);
        }
        if (q.paraphrase !== undefined) validateParaphraseField(q, errors);
      }
    }
  }
  return { ok: errors.length === 0, errors };
}
