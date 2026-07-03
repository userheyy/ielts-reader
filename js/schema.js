// passage JSON 运行时校验。返回 { ok: boolean, errors: string[] }。
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
      }
    }
  }
  return { ok: errors.length === 0, errors };
}
