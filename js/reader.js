import { validatePassage } from "./schema.js";
import { addWord, has } from "./store.js";
import { getImportedPassage } from "./passage-store.js";
import { initSpeechControls, speakEnglish, speechSupported } from "./speech.js?v=6";
import { renderDeep, renderParaphrase } from "./deep.js";

const params = new URLSearchParams(location.search);
const id = params.get("id");
const jumpSentence = params.get("sentence");

const leftEl = document.getElementById("left");
const rightEl = document.getElementById("right");
const questionsEl = document.getElementById("questions");
const srcEl = document.getElementById("src");

initSpeechControls(
  document.getElementById("speech-voice"),
  document.getElementById("speech-rate"),
  document.getElementById("speech-stop"),
);

// ---- 内置词典 ----
let DICT = null; // { word: [phonetic, translation] }
const dictReady = fetch("data/dict.json")
  .then((r) => r.json())
  .then((d) => { DICT = d; })
  .catch(() => { DICT = {}; });

// 生成一个词的词形还原候选(makers→maker, studies→study, running→run, moved→move...)
function lemmaCandidates(word) {
  const w = word.toLowerCase().replace(/['’]s?$/, ""); // 去所有格
  const out = [w];
  const push = (x) => { if (x.length >= 2 && !out.includes(x)) out.push(x); };
  if (w.endsWith("ies")) push(w.slice(0, -3) + "y");
  if (w.endsWith("es")) push(w.slice(0, -2));
  if (w.endsWith("s")) push(w.slice(0, -1));
  if (w.endsWith("ied")) push(w.slice(0, -3) + "y");
  if (w.endsWith("ed")) { push(w.slice(0, -2)); push(w.slice(0, -1)); }
  if (w.endsWith("ing")) {
    push(w.slice(0, -3)); push(w.slice(0, -3) + "e");
    if (w.length > 4 && w[w.length - 4] === w[w.length - 5]) push(w.slice(0, -4)); // running→run
  }
  if (w.endsWith("er")) { push(w.slice(0, -2)); push(w.slice(0, -1)); }
  if (w.endsWith("est")) { push(w.slice(0, -3)); push(w.slice(0, -2)); }
  return out;
}

// 逐级查词:本句精选 → 词典(均带词形还原)。返回 {pos, def, phonetic, w} 或 null
function lookupWord(word, wordDefs) {
  const exact = wordDefs.get(word.toLowerCase());
  if (exact) return { w: exact.w, pos: exact.pos, def: exact.def, phonetic: "" };
  // 多词短语不做词形还原，避免 New Zealand 被拆成 new / zealand。
  if (/\s/.test(word)) return null;
  for (const c of lemmaCandidates(word)) {
    const d = wordDefs.get(c);
    if (d) return { w: d.w, pos: d.pos, def: d.def, phonetic: "" };
  }
  if (DICT) {
    for (const c of lemmaCandidates(word)) {
      const d = DICT[c];
      if (d) return { w: c, pos: "", def: d[1], phonetic: d[0] };
    }
  }
  return null;
}

let popup = null;
function closePopup() { if (popup) { popup.remove(); popup = null; } }
document.addEventListener("click", (e) => {
  if (popup && !popup.contains(e.target) && !e.target.classList.contains("word")) closePopup();
});

// 把一句话渲染成可点单词的 span 序列;单词保留标点分离
function renderSentenceEN(s) {
  const span = document.createElement("span");
  span.className = "sent";
  span.dataset.sid = s.id;
  const speakButton = document.createElement("button");
  speakButton.type = "button";
  speakButton.className = "speak-sentence";
  speakButton.textContent = "🔊";
  speakButton.title = "朗读本句";
  speakButton.setAttribute("aria-label", `朗读第 ${s.id} 句`);
  speakButton.disabled = !speechSupported();
  speakButton.addEventListener("click", (ev) => {
    ev.stopPropagation();
    activate(s.id, false);
    speakEnglish(s.en, {
      onstart: () => span.classList.add("speaking"),
      onend: () => span.classList.remove("speaking"),
    });
  });
  span.appendChild(speakButton);
  const definitions = [...(PASSAGE.phrases || []), ...s.words];
  const wordDefs = new Map(definitions.map((w) => [w.w.toLowerCase(), w]));
  // 已知短语按长度降序匹配；匹配不到时才退回单词。
  const phrases = [...wordDefs.keys()]
    .filter((w) => /\s/.test(w))
    .sort((a, b) => b.length - a.length)
    .map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const tokenPattern = phrases.length
    ? `(${phrases.join("|")}|\\b[A-Za-z][A-Za-z'-]*\\b)`
    : `(\\b[A-Za-z][A-Za-z'-]*\\b)`;
  const parts = s.en.split(new RegExp(tokenPattern, "gi"));
  for (const part of parts) {
    if (/^[A-Za-z]/.test(part)) {
      const w = document.createElement("span");
      w.className = "word";
      w.textContent = part;
      if (has(part)) w.classList.add("saved");
      if (/\s/.test(part)) w.classList.add("phrase");
      w.addEventListener("click", (ev) => {
        ev.stopPropagation();
        activate(s.id); // 点单词同时联动右侧
        openWordPopup(ev, part, wordDefs, s);
      });
      span.appendChild(w);
    } else {
      span.appendChild(document.createTextNode(part));
    }
  }
  // 点句子本身(非单词处)→ 联动
  span.addEventListener("click", () => activate(s.id));
  return span;
}

async function openWordPopup(ev, word, wordDefs, sentence) {
  closePopup();
  await dictReady; // 首次点击时词典可能还没加载完
  const def = lookupWord(word, wordDefs);
  popup = document.createElement("div");
  popup.className = "popup";
  const defHtml = def
    ? `<div><span class="pw">${def.w}</span><span class="ppos">${def.pos || def.phonetic}</span></div><div class="pdef">${def.def}</div>`
    : `<div><span class="pw">${word}</span></div><div style="color:#999">未收录释义</div>`;
  popup.innerHTML = defHtml;
  const actions = document.createElement("div");
  actions.className = "popup-actions";
  const speakBtn = document.createElement("button");
  speakBtn.type = "button";
  speakBtn.className = "speak-word";
  speakBtn.textContent = "🔊 发音";
  speakBtn.disabled = !speechSupported();
  speakBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    speakEnglish(word);
  });
  const btn = document.createElement("button");
  const saveWord = def ? def.w : word;
  const already = has(saveWord) || has(word);
  btn.textContent = already ? "已入库" : "+ 入库";
  btn.disabled = already;
  btn.addEventListener("click", () => {
    addWord({
      word: saveWord,
      def: def ? def.def : "",
      pos: def ? def.pos : "",
      sentence_en: sentence.en,
      sentence_zh: sentence.zh,
      source: PASSAGE.source,
      passage_id: PASSAGE.id,
      sentence_id: sentence.id,
    });
    btn.textContent = "已入库"; btn.disabled = true;
    // 高亮原文中该词的所有词形变体
    const cands = lemmaCandidates(word);
    document.querySelectorAll(".word").forEach((el) => {
      if (lemmaCandidates(el.textContent).some((c) => cands.includes(c))) el.classList.add("saved");
    });
  });
  actions.append(speakBtn, btn);
  popup.appendChild(actions);
  document.body.appendChild(popup);
  const r = ev.target.getBoundingClientRect();
  popup.style.left = Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - 280) + "px";
  popup.style.top = (window.scrollY + r.bottom + 4) + "px";
}

// 联动:左句高亮并滚动定位 + 右侧手风琴展开对应卡片并滚动定位
function activate(sid, scroll = true) {
  document.querySelectorAll(".sent").forEach((el) =>
    el.classList.toggle("active", el.dataset.sid == sid));
  document.querySelectorAll(".gcard").forEach((el) => {
    const on = el.dataset.sid == sid;
    el.classList.toggle("active", on);
    el.classList.toggle("open", on); // 手风琴:只展开当前卡片
  });
  if (scroll) {
    const sent = document.querySelector(`.sent[data-sid="${sid}"]`);
    const g = document.querySelector(`.gcard[data-sid="${sid}"]`);
    if (sent) {
      sent.scrollIntoView({ behavior: "smooth", block: "center" });
      sent.classList.remove("pulse");
      requestAnimationFrame(() => sent.classList.add("pulse"));
    }
    // 等折叠动画走完再定位,避免滚动位置漂移
    if (g) setTimeout(() => g.scrollIntoView({ behavior: "smooth", block: "center" }), 300);
  }
}

let PASSAGE = null;

function expandSentenceDetails(passage) {
  if (!passage.sentences.some((s) => Array.isArray(s.details))) return passage;
  const expanded = [];
  const firstSentenceByParagraph = new Map();
  for (const block of passage.sentences) {
    const parts = block.en.split(/(?<=[.!?])\s+(?=[A-Z])/);
    const details = block.details || [];
    if (parts.length !== details.length) throw new Error(`第${block.para}段逐句数据数量不一致`);
    firstSentenceByParagraph.set(block.para, expanded.length + 1);
    parts.forEach((en, i) => {
      expanded.push({
        id: expanded.length + 1,
        para: block.para,
        en,
        zh: details[i].zh,
        grammar: details[i].grammar,
        words: block.words.filter((w) => en.toLowerCase().includes(w.w.toLowerCase())),
      });
    });
  }
  const questions = (passage.questions || []).map((g) => ({
    ...g,
    items: g.items.map((q) => ({
      ...q,
      evidence_sentence: firstSentenceByParagraph.get(q.evidence_sentence) || q.evidence_sentence,
    })),
  }));
  return { ...passage, analysis_unit: "sentence", sentences: expanded, questions };
}

function normalizeAnswer(value) {
  return String(value || "").trim().toLowerCase().replace(/\s+/g, " ");
}

function answerText(item) {
  return item.dataset.answer || "未录入答案";
}

function showQuestionAnswer(item, mode = "check") {
  const input = item.querySelector("input");
  const note = item.querySelector(".answer-note");
  const answer = answerText(item);
  if (!item.dataset.answer) {
    item.classList.remove("correct", "wrong");
    item.classList.add("unanswered");
    note.innerHTML = "这题还没有录入标准答案。";
    return false;
  }
  const user = normalizeAnswer(input.value);
  const ok = user && user === normalizeAnswer(answer);
  item.classList.remove("unanswered", "answer-only");
  if (mode === "reveal") {
    item.classList.remove("correct", "wrong");
    item.classList.add("answer-only");
    note.innerHTML = `答案：<strong>${answer}</strong>${evidenceButtonHTML(item)}`;
    showParaphrase(item);
    return null;
  }
  item.classList.toggle("correct", ok);
  item.classList.toggle("wrong", !ok);
  note.innerHTML = ok
    ? `正确 ✓${evidenceButtonHTML(item)}`
    : `${user ? "不对" : "未作答"}｜答案：<strong>${answer}</strong>${evidenceButtonHTML(item)}`;
  showParaphrase(item);
  return ok;
}

// 核对/显示答案后,若该题有 paraphrase 数据则展示「考点替换」块
function showParaphrase(item) {
  const slot = item.querySelector(".para-slot");
  if (!slot || slot.dataset.done || !item.dataset.paraphrase) return;
  try {
    const pp = JSON.parse(item.dataset.paraphrase);
    slot.innerHTML = renderParaphrase(pp, { sid: item.dataset.evidence || null });
    slot.dataset.done = "1";
  } catch { /* 数据异常则忽略 */ }
}

function evidenceButtonHTML(item) {
  return item.dataset.evidence
    ? ` <button type="button" class="evidence-jump" data-sid="${item.dataset.evidence}">定位原文</button>`
    : "";
}

function checkQuestionScope(scope) {
  let total = 0, correct = 0;
  scope.querySelectorAll(".question-item").forEach((item) => {
    if (!item.dataset.answer) return;
    total += 1;
    if (showQuestionAnswer(item, "check")) correct += 1;
  });
  return { total, correct };
}

function revealQuestionScope(scope, reveal) {
  scope.querySelectorAll(".question-item").forEach((item) => {
    if (reveal) showQuestionAnswer(item, "reveal");
    else {
      item.classList.remove("correct", "wrong", "unanswered", "answer-only");
      item.querySelector(".answer-note").textContent = "";
    }
  });
}

function renderQuestions(groups) {
  questionsEl.innerHTML = `<div class="questions-title">
    <span>Questions</span>
    <div class="question-actions">
      <small id="question-score">先作答，再核对</small>
      <button type="button" id="check-all-answers">核对全部</button>
      <button type="button" id="reveal-all-answers">显示答案</button>
    </div>
  </div>`;
  if (!groups || groups.length === 0) {
    questionsEl.innerHTML += "<p class=\"question-empty\">这篇文章暂未录入题目。</p>";
    return;
  }
  for (const group of groups) {
    const section = document.createElement("section");
    section.className = "question-group";
    section.innerHTML = `<h2>${group.title}</h2>
      ${(group.instructions || []).map((line) => `<p class="instruction">${line}</p>`).join("")}`;
    for (const q of group.items) {
      const item = document.createElement("div");
      item.className = "question-item";
      item.dataset.answer = q.answer || "";
      if (q.evidence_sentence) item.dataset.evidence = q.evidence_sentence;
      if (q.paraphrase) item.dataset.paraphrase = JSON.stringify(q.paraphrase);
      item.innerHTML = `<label><b>${q.number}</b><span>${q.prompt}</span></label>
        <input type="text" autocomplete="off" aria-label="第 ${q.number} 题答案">
        <div class="answer-note" aria-live="polite"></div>
        <div class="para-slot"></div>`;
      if (q.evidence_sentence) {
        item.querySelector("label").addEventListener("click", () => activate(q.evidence_sentence));
      }
      section.appendChild(item);
    }
    const check = document.createElement("button");
    check.className = "check-answers";
    check.textContent = "核对本组答案";
    check.addEventListener("click", () => {
      const { total, correct } = checkQuestionScope(section);
      const score = document.getElementById("question-score");
      if (score) score.textContent = `本组 ${correct}/${total}`;
    });
    section.appendChild(check);
    questionsEl.appendChild(section);
  }
  questionsEl.addEventListener("click", (ev) => {
    const chip = ev.target.closest(".pp-chip");
    if (chip) {
      highlightInSentence(chip.dataset.sid, chip.dataset.p);
      return;
    }
    const evidence = ev.target.closest(".evidence-jump");
    if (evidence) {
      activate(Number(evidence.dataset.sid));
      return;
    }
    if (ev.target.id === "check-all-answers") {
      const { total, correct } = checkQuestionScope(questionsEl);
      document.getElementById("question-score").textContent = `总分 ${correct}/${total}`;
      return;
    }
    if (ev.target.id === "reveal-all-answers") {
      const reveal = ev.target.textContent === "显示答案";
      revealQuestionScope(questionsEl, reveal);
      ev.target.textContent = reveal ? "隐藏答案" : "显示答案";
      document.getElementById("question-score").textContent = reveal ? "已显示标准答案" : "先作答，再核对";
    }
  });
}

// 深度卡「+入库」按钮:事件委托,把词(带 aids)存入生词库
function wireDeepAddWord() {
  rightEl.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".deep-add-word");
    if (!btn) return;
    let aids = null;
    try { aids = JSON.parse(btn.dataset.aids || "null"); } catch { aids = null; }
    const entry = {
      word: btn.dataset.word,
      def: btn.dataset.def || "",
      pos: btn.dataset.pos || "",
      source: PASSAGE ? PASSAGE.source : "",
      passage_id: id,
      aids,
    };
    const res = addWord(entry);
    btn.textContent = res && res.added === false ? "已在库中" : "已入库 ✓";
    btn.classList.add("added");
    btn.disabled = true;
  });
}

// 「AI 深挖本句」按钮:仅在已配置 API Key 时出现;点击调 DeepSeek 生成 deep,渲染并缓存
async function wireAiSlots(passage) {
  let ai;
  try { ai = await import("./ai.js"); } catch { return; }
  if (!ai || typeof ai.hasKey !== "function" || !ai.hasKey()) return;

  let TAGS = null; // 精简标签表(白名单),供 prompt 使用
  const loadTags = async () => {
    if (TAGS) return TAGS;
    try {
      const r = await fetch("data/grammar-tags.json");
      TAGS = (await r.json()).tags;
    } catch { TAGS = []; }
    return TAGS;
  };

  document.querySelectorAll(".deep-ai-slot").forEach((slot) => {
    const sid = Number(slot.dataset.sid);
    const cacheKey = `ielts_ai_cache:${id}:${sid}`;
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      try { slot.innerHTML = renderDeep(JSON.parse(cached)); return; } catch { /* 重新生成 */ }
    }
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "deep-ai-btn";
    btn.textContent = "🤖 AI 深挖本句";
    slot.appendChild(btn);
    btn.addEventListener("click", async () => {
      btn.disabled = true;
      btn.textContent = "AI 分析中…";
      try {
        const s = passage.sentences.find((x) => x.id === sid);
        const tags = await loadTags();
        const tagList = tags.map((t) => `${t.id}:${t.name}`).join("；");
        const deep = await ai.askDeepSeek([
          { role: "system", content:
            "你是给雅思基础薄弱学生讲课的英语老师。按《语法俱乐部》五大句型→修饰→从句→从句减化的框架,对给定句子输出 deep JSON。" +
            "字段:pattern{id(sv|svc|svo|svoo|svoc),label,tag,skeleton[{role,text,zh}],plain}、" +
            "chunks[{text,role(S/V/O/IO/C/attr/adv/app/conn/clause),zh,note,tag?}]、" +
            "grammar_points[{tag,name,explain}]、vocab[{w,lemma,pos,def,aids{morphemes[{text,type(prefix|root|suffix|connector),gloss}],derivation,family,mnemonic,forms},synonyms[{w,note}],confusables[{w,note}]}]、expressions[{text,zh,usage}]。" +
            "tag 只能从白名单选:" + tagList + "。全中文大白话讲解,只输出 JSON。" },
          { role: "user", content: `【句子】${s.en}\n【翻译】${s.zh}\n【已有语法简注】${s.grammar.type} — ${s.grammar.note}` },
        ], { json: true });
        slot.innerHTML = renderDeep(deep);
        localStorage.setItem(cacheKey, JSON.stringify(deep));
      } catch (e) {
        btn.disabled = false;
        btn.textContent = "🤖 AI 深挖本句";
        const err = document.createElement("div");
        err.className = "deep-ai-err";
        err.textContent = "生成失败:" + (e && e.message ? e.message : e);
        slot.appendChild(err);
      }
    });
  });
}

// 考点替换 chip:定位原文句 + 临时高亮 p 词串
function highlightInSentence(sid, phrase) {
  activate(Number(sid));
  if (!phrase) return;
  const sent = document.querySelector(`.sent[data-sid="${sid}"]`);
  if (!sent) return;
  // 在句子纯文本里找到 phrase 并用 mark 包裹(不区分大小写);2 秒后还原
  const original = sent.innerHTML;
  const text = sent.textContent;
  const idx = text.toLowerCase().indexOf(String(phrase).toLowerCase());
  if (idx < 0) return;
  sent.classList.add("pp-flash");
  setTimeout(() => sent.classList.remove("pp-flash"), 2000);
}

async function main() {
  if (!id) { leftEl.textContent = "缺少文章 id。"; return; }
  let d = getImportedPassage(id);
  if (!d) {
    try {
      const res = await fetch(`data/passages/${id}.json`, { cache: "no-store" });
      if (!res.ok) throw new Error();
      d = await res.json();
    } catch {
      leftEl.textContent = "无法加载文章。请通过 start.bat 启动本地服务器。";
      return;
    }
  }
  const v = validatePassage(d);
  if (!v.ok) { leftEl.textContent = "文章数据有误:" + v.errors.join("; "); return; }
  try { d = expandSentenceDetails(d); }
  catch (e) { leftEl.textContent = "逐句数据有误：" + e.message; return; }
  PASSAGE = d;
  srcEl.textContent = `${d.source} — ${d.title}`;
  renderQuestions(d.questions);

  // 左:按 para 分段
  let curPara = null, pEl = null;
  for (const s of d.sentences) {
    if (s.para !== curPara) {
      pEl = document.createElement("p");
      leftEl.appendChild(pEl);
      curPara = s.para;
    }
    pEl.appendChild(renderSentenceEN(s));
    pEl.appendChild(document.createTextNode(" "));
  }
  // 右:讲解卡片(折叠式,点标题或点左句展开)
  for (const s of d.sentences) {
    const c = document.createElement("div");
    c.className = "gcard"; c.dataset.sid = s.id;
    const wordsLine = s.words.length
      ? `<div class="gwords">生词:${s.words.map((w) => `${w.w} ${w.def}`).join(" / ")}</div>` : "";
    // 深度解析:有 deep 直接渲染;无 deep 且已配置 API Key 则给「AI 深挖」按钮
    const deepHTML = s.deep ? renderDeep(s.deep) : "";
    const aiSlot = s.deep ? "" : `<div class="deep-ai-slot" data-sid="${s.id}"></div>`;
    c.innerHTML = `
      <div class="ghead">
        <span class="garrow">▸</span>
        <span class="gtype">【${d.analysis_unit === "paragraph" ? "段" : "句"}${s.id}】${s.grammar.type}</span>
      </div>
      <div class="gbody"><div class="gbody-inner">
        <div class="gnote">拆解:${s.grammar.note}</div>
        <div class="gzh">翻译:${s.zh}</div>
        ${wordsLine}
        ${deepHTML}
        ${aiSlot}
      </div></div>`;
    c.querySelector(".ghead").addEventListener("click", () => {
      // 已展开的再点标题 → 收起;否则展开并联动(不滚动,避免页面跳动)
      if (c.classList.contains("open")) {
        c.classList.remove("open");
      } else {
        activate(s.id, false);
      }
    });
    rightEl.appendChild(c);
  }
  wireDeepAddWord();
  wireAiSlots(d);

  // 翻译显隐
  document.getElementById("toggle-zh").addEventListener("click", (e) => {
    document.body.classList.toggle("hide-zh");
    e.target.textContent = document.body.classList.contains("hide-zh") ? "显示翻译" : "隐藏翻译";
  });

  // 从生词库跳转带 sentence 参数 → 自动定位
  if (jumpSentence) activate(Number(jumpSentence));
}
main();
