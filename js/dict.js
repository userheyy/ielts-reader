// 共享内置词典查询。逻辑取自 reader.js 的词形还原 + 查词，供测试页题干悬停查词复用。
// 词典文件 data/dict.json 形如 { word: [phonetic, translation] }，约几万词，带常见变形。

let DICT = null;
let _ready = null;

// 按需加载词典(带缓存)。失败时退化为空词典，不抛错。
export function ensureDict() {
  if (_ready) return _ready;
  _ready = fetch("data/dict.json", { cache: "force-cache" })
    .then((r) => r.json())
    .then((d) => { DICT = d; return DICT; })
    .catch(() => { DICT = {}; return DICT; });
  return _ready;
}

// 词形还原候选：makers→maker, studies→study, running→run, moved→move...
function lemmaCandidates(word) {
  const w = word.toLowerCase().replace(/['’]s?$/, "");
  const out = [w];
  const push = (x) => { if (x.length >= 2 && !out.includes(x)) out.push(x); };
  if (w.endsWith("ies")) push(w.slice(0, -3) + "y");
  if (w.endsWith("es")) push(w.slice(0, -2));
  if (w.endsWith("s")) push(w.slice(0, -1));
  if (w.endsWith("ied")) push(w.slice(0, -3) + "y");
  if (w.endsWith("ed")) { push(w.slice(0, -2)); push(w.slice(0, -1)); }
  if (w.endsWith("ing")) {
    push(w.slice(0, -3)); push(w.slice(0, -3) + "e");
    if (w.length > 4 && w[w.length - 4] === w[w.length - 5]) push(w.slice(0, -4));
  }
  if (w.endsWith("er")) { push(w.slice(0, -2)); push(w.slice(0, -1)); }
  if (w.endsWith("est")) { push(w.slice(0, -3)); push(w.slice(0, -2)); }
  return out;
}

// 查一个词。返回 { w, phonetic, def } 或 null。词典未加载完时返回 null(调用方应先 await ensureDict)。
export function lookup(word) {
  if (!DICT) return null;
  if (/\s/.test(word)) return null; // 多词短语不还原
  for (const c of lemmaCandidates(word)) {
    const d = DICT[c];
    if (d) return { w: c, phonetic: d[0] || "", def: d[1] || "" };
  }
  return null;
}

export { lemmaCandidates };
