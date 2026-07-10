// 内置雅思词库加载 + 复习池合并。
// - 从 data/vocab-seed.json 读内置词(只读的知识源,永不写回该文件)。
// - 用户可把内置词"加入复习",其加入状态与 SRS 状态存 localStorage(独立键),
//   避免污染 seed 文件,也避免与生词库互相干扰。
// - 复习池 = localStorage 生词 ∪ 已加入复习的内置词;同名去重,生词优先(见 spec §5.4)。

import { loadAll as loadVocab } from "./store.js?v=7";

const SEED_URL = "data/vocab-seed.json";
const ADDED_KEY = "ielts_vocab_seed_added";   // 已加入复习的内置词: { [word]: true }
const SEED_REVIEW_KEY = "ielts_vocab_seed_review"; // 内置词的 SRS 状态: { [word]: reviewObj }

let _seedCache = null; // { meta, words: [...] }

function readJSON(key, fallback) {
  if (typeof localStorage === "undefined") return fallback;
  const raw = localStorage.getItem(key);
  if (!raw) return fallback;
  try { return JSON.parse(raw); } catch { return fallback; }
}
function writeJSON(key, val) {
  if (typeof localStorage === "undefined") return;
  localStorage.setItem(key, JSON.stringify(val));
}

// 加载内置词库(带缓存)。失败(文件不存在/空)时返回空结构,不抛错。
export async function loadSeed() {
  if (_seedCache) return _seedCache;
  try {
    const res = await fetch(SEED_URL, { cache: "no-cache" });
    if (!res.ok) throw new Error("seed not found");
    const data = await res.json();
    _seedCache = data && Array.isArray(data.words) ? data : { meta: {}, words: [] };
  } catch {
    _seedCache = { meta: {}, words: [] };
  }
  return _seedCache;
}

export function getSeedMeta() {
  return _seedCache ? (_seedCache.meta || {}) : {};
}

// 某内置词是否已加入复习
export function isSeedAdded(word) {
  const added = readJSON(ADDED_KEY, {});
  return !!added[word.toLowerCase()];
}

// 加入/移出复习
export function setSeedAdded(word, on = true) {
  const added = readJSON(ADDED_KEY, {});
  const w = word.toLowerCase();
  if (on) added[w] = true; else delete added[w];
  writeJSON(ADDED_KEY, added);
}

export function seedAddedCount() {
  return Object.keys(readJSON(ADDED_KEY, {})).length;
}

// 内置词的 SRS 状态读写(结构与 store.js 的 review 对象一致)
export function getSeedReview(word) {
  const all = readJSON(SEED_REVIEW_KEY, {});
  return all[word.toLowerCase()] || null;
}
export function setSeedReview(word, review) {
  const all = readJSON(SEED_REVIEW_KEY, {});
  all[word.toLowerCase()] = review;
  writeJSON(SEED_REVIEW_KEY, all);
}

// 复习池:把内置词(已加入的)包装成与生词记录同构的对象,
// 再与 localStorage 生词合并,同名去重(生词优先;生词 aids 为空则借用 seed 的 aids)。
// 返回数组,元素形如生词记录 + { _origin:'vocab'|'seed' }。
export async function buildReviewPool() {
  const seed = await loadSeed();
  const added = readJSON(ADDED_KEY, {});
  const vocab = loadVocab();
  const byWord = new Map();

  // 先放内置词(已加入的)
  for (const s of seed.words) {
    const w = (s.word || "").toLowerCase();
    if (!w || !added[w]) continue;
    byWord.set(w, {
      word: s.word,
      def: s.def || "",
      pos: s.pos || "",
      sentence_en: s.sentence_en || "",
      sentence_zh: s.sentence_zh || "",
      source: "雅思核心词库",
      passage_id: "",
      sentence_id: null,
      aids: s.aids || null,
      collocations: s.collocations || null,
      review: getSeedReview(s.word) || { level: 0, next_due: null, history: [] },
      _origin: "seed",
    });
  }
  // 再放生词,同名覆盖(生词优先);若生词 aids/搭配 空而 seed 有,则借用
  for (const v of vocab) {
    const w = (v.word || "").toLowerCase();
    const seedHit = byWord.get(w);
    const merged = { ...v, _origin: "vocab" };
    if ((!merged.aids || !hasAids(merged.aids)) && seedHit && seedHit.aids) {
      merged.aids = seedHit.aids;
    }
    if ((!merged.collocations || !merged.collocations.length) && seedHit && seedHit.collocations) {
      merged.collocations = seedHit.collocations;
    }
    byWord.set(w, merged);
  }
  return [...byWord.values()];
}

function hasAids(a) {
  if (!a || typeof a !== "object") return false;
  return (
    (Array.isArray(a.morphemes) && a.morphemes.length) ||
    (a.derivation && a.derivation.trim()) ||
    (a.family && Array.isArray(a.family.words) && a.family.words.length) ||
    (a.mnemonic && a.mnemonic.trim()) ||
    (Array.isArray(a.forms) && a.forms.length)
  );
}

// 按词根分组内置词(供词库页"按词根成组"视图)。无词根的词归到 "__misc__"。
export function groupSeedByRoot(words) {
  const groups = new Map();
  for (const w of words) {
    let key = "__misc__", gloss = "";
    const fam = w.aids && w.aids.family;
    const rootM = w.aids && Array.isArray(w.aids.morphemes)
      ? w.aids.morphemes.find((m) => m.type === "root")
      : null;
    if (fam && fam.root) { key = fam.root; gloss = fam.gloss || ""; }
    else if (rootM) { key = rootM.text; gloss = rootM.gloss || ""; }
    if (!groups.has(key)) groups.set(key, { root: key, gloss, words: [] });
    groups.get(key).words.push(w);
  }
  // 词多的词根排前面;__misc__ 垫底
  return [...groups.values()].sort((a, b) => {
    if (a.root === "__misc__") return 1;
    if (b.root === "__misc__") return -1;
    return b.words.length - a.words.length;
  });
}
