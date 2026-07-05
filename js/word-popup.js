// 通用"点词/短语 → 弹窗查释义 + 入生词库"组件。
// 阅读页(reader.js)和听力页(listening.js)复用同一份。
//
// 用法:
//   import { openWordPopup } from "./word-popup.js?v=1";
//   openWordPopup({
//     event,      // MouseEvent(用于定位弹窗)
//     word,       // 点的词或短语,如 "predicted" / "New Zealand"
//     wordDefs,   // Map<lowercase, {w, pos, def}> — 本句/本段的精选词表(可空 Map)
//     sentence,   // { id, en, zh } — 例句上下文
//     source,     // "剑桥雅思14 · Test 1 · Passage 1" — 入库时的 source 字段
//     passageId,  // "c14-test1-p1" — 入库时的 passage_id
//     onSaved,    // 可选:入库成功后回调(参数 = 词形还原候选数组);默认高亮页面里所有 .word 元素
//   });
//
// 依赖:store.js(addWord/has)、speech.js(speakEnglish/speechSupported)、data/dict.json(内置词典)

import { addWord, has } from "./store.js";
import { speakEnglish, speechSupported } from "./speech.js?v=6";

// ---- 内置词典单例(懒加载,多页共享) ----
let DICT = null;
let dictPromise = null;
function ensureDict() {
  if (dictPromise) return dictPromise;
  dictPromise = fetch("data/dict.json")
    .then((r) => r.json())
    .then((d) => { DICT = d; })
    .catch(() => { DICT = {}; });
  return dictPromise;
}

// ---- 词形还原(makers→maker, studies→study, running→run, moved→move ...) ----
export function lemmaCandidates(word) {
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

// ---- 三级降级查词:本句精选 → 内置词典(均带词形还原)。返回 {w, pos, def, phonetic} 或 null ----
function lookupWord(word, wordDefs) {
  const exact = wordDefs && wordDefs.get(word.toLowerCase());
  if (exact) return { w: exact.w, pos: exact.pos, def: exact.def, phonetic: "" };
  // 多词短语不做词形还原,避免 "New Zealand" 被拆成 new / zealand
  if (/\s/.test(word)) return null;
  if (wordDefs) {
    for (const c of lemmaCandidates(word)) {
      const d = wordDefs.get(c);
      if (d) return { w: d.w, pos: d.pos, def: d.def, phonetic: "" };
    }
  }
  if (DICT) {
    for (const c of lemmaCandidates(word)) {
      const d = DICT[c];
      if (d) return { w: c, pos: "", def: d[1], phonetic: d[0] };
    }
  }
  return null;
}

// ---- 弹窗单例 ----
let popup = null;
function closePopup() { if (popup) { popup.remove(); popup = null; } }
// 页面级"点空白关闭":只注册一次(多页 import 时也只注册一次,因为模块是 singleton)
document.addEventListener("click", (e) => {
  if (!popup) return;
  if (popup.contains(e.target)) return;
  // 不关闭若点在触发词元素上(避免立刻关掉刚打开的弹窗;各页触发元素 class 不同,用宽松判定)
  const t = e.target;
  if (t.classList && (t.classList.contains("word") || t.classList.contains("wtip"))) return;
  closePopup();
});

// ---- 主入口 ----
export async function openWordPopup({ event, word, wordDefs, sentence, source, passageId, onSaved }) {
  closePopup();
  await ensureDict(); // 首次点击时词典可能还没加载完
  const def = lookupWord(word, wordDefs || new Map());
  popup = document.createElement("div");
  popup.className = "popup";
  const defHtml = def
    ? `<div><span class="pw">${escapeHtml(def.w)}</span><span class="ppos">${escapeHtml(def.pos || def.phonetic)}</span></div><div class="pdef">${escapeHtml(def.def)}</div>`
    : `<div><span class="pw">${escapeHtml(word)}</span></div><div style="color:#999">未收录释义</div>`;
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

  const saveBtn = document.createElement("button");
  const saveWord = def ? def.w : word;
  const already = has(saveWord) || has(word);
  saveBtn.textContent = already ? "已入库" : "+ 入库";
  saveBtn.disabled = already;
  saveBtn.addEventListener("click", () => {
    addWord({
      word: saveWord,
      def: def ? def.def : "",
      pos: def ? def.pos : "",
      sentence_en: sentence ? sentence.en : "",
      sentence_zh: sentence ? sentence.zh : "",
      source: source || "",
      passage_id: passageId || "",
      sentence_id: sentence ? sentence.id : null,
    });
    saveBtn.textContent = "已入库";
    saveBtn.disabled = true;
    const cands = lemmaCandidates(word);
    if (typeof onSaved === "function") {
      onSaved(cands);
    } else {
      // 默认行为:高亮页面里所有 .word / .wtip 元素中 lemma 匹配的
      document.querySelectorAll(".word, .wtip").forEach((el) => {
        const raw = el.dataset && el.dataset.word ? el.dataset.word : el.textContent;
        if (lemmaCandidates(raw).some((c) => cands.includes(c))) {
          el.classList.add("saved");
        }
      });
    }
  });

  actions.append(speakBtn, saveBtn);
  popup.appendChild(actions);
  document.body.appendChild(popup);
  const r = event.target.getBoundingClientRect();
  popup.style.left = Math.min(
    window.scrollX + r.left,
    window.scrollX + document.documentElement.clientWidth - 280,
  ) + "px";
  popup.style.top = (window.scrollY + r.bottom + 4) + "px";
}

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
