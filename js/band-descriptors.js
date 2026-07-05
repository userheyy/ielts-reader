// IELTS 官方评分标准(Band Descriptors, Public Version)简化中文摘要,
// 用于 writing.html / speaking.html 面板展示,以及 DeepSeek 批改 prompt 里的锚点。
// 完整原文见 IDP / British Council 官网:
//   Writing Task 1 & 2 Band Descriptors
//   Speaking Band Descriptors
//
// 使用:
//   import { WRITING_BANDS, SPEAKING_BANDS, renderBandPanel, promptSnippet } from "./band-descriptors.js?v=1";

export const WRITING_BANDS = {
  headline: "IELTS Writing 评分标准(4 项 × Band 5-9)",
  criteria: [
    { key: "TR", name: "Task Response / Task Achievement", desc: "对题目要求的回应程度、观点清晰度、论据是否充分。" },
    { key: "CC", name: "Coherence & Cohesion", desc: "段落结构、逻辑衔接、指代替换手段。" },
    { key: "LR", name: "Lexical Resource", desc: "词汇丰富度、准确性、地道搭配、拼写。" },
    { key: "GRA", name: "Grammatical Range & Accuracy", desc: "句式多样性、语法正确率、标点。" },
  ],
  levels: {
    "9": {
      TR: "完全回应题目所有要求,论点极其清晰充分,论据引人入胜。",
      CC: "段落组织自然无缝,衔接手段几乎察觉不到、无误。",
      LR: "词汇丰富精准且地道,搭配自如,极少小误。",
      GRA: "句式灵活多样,语法完全正确、精准。",
    },
    "8": {
      TR: "覆盖题目所有要求,论点扩展充分,只有个别处稍粗略。",
      CC: "段落有序衔接流畅,过渡词使用得当。",
      LR: "词汇丰富、准确性高,偶尔有搭配/生僻词小误。",
      GRA: "多种复杂句结构,大部分句子无错,偶有小误但不影响理解。",
      target: "6.5+ 的进阶目标。",
    },
    "7": {
      TR: "涉及题目所有要求,但个别观点欠展开或过泛;论点总体清晰。",
      CC: "行文清晰,大部分衔接词使用得当,偶有过多/机械。",
      LR: "词汇较丰富有灵活性,能用一些少见表达,偶有搭配/形式错误。",
      GRA: "句式多样,大部分正确,复杂句偶有错但基本可懂。",
      target: "多数中国考生的目标分。",
    },
    "6": {
      TR: "涉及题目要求但概括/覆盖不到位;论点尚清晰但部分未充分展开。",
      CC: "整体连贯,衔接词有时使用不当/过多;段落有明确核心但推进略机械。",
      LR: "一般词汇够用,能尝试少见词但有拼写/搭配错;不影响理解。",
      GRA: "以简单句为主,尝试复杂句时有错;错误较多但不妨碍理解。",
      target: "本科申请常见门槛。",
    },
    "5": {
      TR: "部分回应题目;论点不清晰,论据薄弱或跑题。",
      CC: "衔接不足或不当,论点顺序易读性差,段落划分不清。",
      LR: "词汇局限,有重复/生僻误用;拼写/搭配错影响流畅。",
      GRA: "句式单一以简单句为主;错误频繁,有时影响理解。",
    },
  },
  tips: [
    "TR 首先关注:题目问什么、你答了几个方面、观点是否清晰。",
    "CC 首先关注:分段是否合理、段内是否 1 个中心论点、段间是否有过渡。",
    "LR 首先关注:是否重复用一个词、有没有 topic-specific 词汇。",
    "GRA 首先关注:主谓一致、时态、有没有尝试从句/条件句/被动语态。",
  ],
};

export const SPEAKING_BANDS = {
  headline: "IELTS Speaking 评分标准(4 项 × Band 5-9)",
  criteria: [
    { key: "FC", name: "Fluency & Coherence", desc: "语流连贯度、话题展开、逻辑衔接。" },
    { key: "LR", name: "Lexical Resource", desc: "词汇丰富度、话题词汇、灵活性。" },
    { key: "GRA", name: "Grammatical Range & Accuracy", desc: "句式多样性、语法正确率。" },
    { key: "PR", name: "Pronunciation", desc: "发音清晰度、语音语调、连读、重音。" },
  ],
  levels: {
    "9": {
      FC: "流利无停顿(除思考话题内容外),话题展开充分自然。",
      LR: "词汇丰富精准,能自然使用习语和地道搭配。",
      GRA: "句式全面灵活运用,几乎无错。",
      PR: "发音精准清晰,重音语调完美,几乎无本地口音干扰。",
    },
    "8": {
      FC: "语流自然,偶尔有语言性犹豫但不影响理解;话题展开充分。",
      LR: "词汇灵活,能用少见的表达和搭配,偶有小误。",
      GRA: "多种复杂句式,错误极少。",
      PR: "发音特点稳定,重音语调有效,偶有个别音发不准。",
    },
    "7": {
      FC: "能保持较长时间不停顿,偶用衔接词过多/机械;话题展开较充分。",
      LR: "词汇较丰富能达意,能用一些少见词/搭配;偶有 hesitation。",
      GRA: "多种句式,大部分句子无错;复杂句尝试较多。",
      PR: "整体清晰,单个词发音偶有本土色彩但可懂。",
      target: "留学申请常见门槛。",
    },
    "6": {
      FC: "能保持对话但有停顿/自我修正;衔接词有时不合适;能展开话题但偶尔跑题。",
      LR: "话题词汇够用,常见词汇为主,偶尔尝试少见词有误。",
      GRA: "简单句为主,尝试复杂句但常有错误;意思可懂。",
      PR: "大部分清晰,单个音/重音偶有问题,不影响交流。",
      target: "本科申请常见门槛。",
    },
    "5": {
      FC: "语流有明显停顿以搜词/纠正;衔接不足;话题展开不充分。",
      LR: "词汇有限重复,尝试转述但意思不总能到位。",
      GRA: "简单句为主且有错,复杂句罕见/错误多;意思偶尔难懂。",
      PR: "个别音发不准影响理解,重音节奏不稳定。",
    },
  },
  tips: [
    "FC 提升:多用衔接词(however, actually, for example),避免长时 uh/uhm。",
    "LR 提升:每天记 5 个 topic-specific 词并造句(如 environment: emissions / renewable / offset)。",
    "GRA 提升:多练 3 种句式:if 条件句、which/who 关系从句、被动语态。",
    "PR 提升:录音回听,注意 word stress 与 sentence rhythm。",
  ],
};

const CN_ACRO = { TR: "任务回应", CC: "连贯衔接", LR: "词汇资源", GRA: "语法多样与准确", FC: "流利连贯", PR: "发音" };

// 渲染一个"评分标准"面板到指定容器(<details> 折叠展开,不占太大空间)
export function renderBandPanel(container, kind /* "writing" | "speaking" */) {
  const data = kind === "speaking" ? SPEAKING_BANDS : WRITING_BANDS;
  const criteriaHtml = data.criteria.map((c) =>
    `<div class="bd-criterion"><b>${c.key}</b> <span class="bd-cn">${CN_ACRO[c.key] || c.name}</span>:<span class="bd-desc">${esc(c.desc)}</span></div>`
  ).join("");
  const levelsHtml = Object.entries(data.levels).map(([band, obj]) => {
    const items = data.criteria.map((c) =>
      `<li><b>${c.key}</b> ${esc(obj[c.key] || "")}</li>`).join("");
    const targetHtml = obj.target ? `<div class="bd-target">🎯 ${esc(obj.target)}</div>` : "";
    return `<details class="bd-level"><summary><b>Band ${band}</b>${targetHtml ? " " + targetHtml : ""}</summary><ul>${items}</ul></details>`;
  }).join("");
  const tipsHtml = data.tips.map((t) => `<li>${esc(t)}</li>`).join("");
  container.innerHTML = `
    <details class="bd-panel">
      <summary class="bd-heading">📊 ${esc(data.headline)}(点击展开)</summary>
      <div class="bd-body">
        <div class="bd-criteria">${criteriaHtml}</div>
        <div class="bd-levels">${levelsHtml}</div>
        <div class="bd-tips"><h4>提分要点</h4><ul>${tipsHtml}</ul></div>
      </div>
    </details>
  `;
}

// 给 DeepSeek 批改 prompt 用的简化文本:让 model 严格对齐官方 Band 描述
export function promptSnippet(kind) {
  const data = kind === "speaking" ? SPEAKING_BANDS : WRITING_BANDS;
  const lines = [];
  lines.push(`# IELTS ${kind === "speaking" ? "Speaking" : "Writing"} Band Descriptors(锚点)`);
  for (const [band, obj] of Object.entries(data.levels)) {
    lines.push(`- Band ${band}: ` + data.criteria.map((c) => `${c.key}=${obj[c.key] || ""}`).join(" · "));
  }
  return lines.join("\n");
}

function esc(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
