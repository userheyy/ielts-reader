// 生词库存储层。浏览器用 localStorage;无 localStorage(如 Node)时退回内存,便于测试。
import { schedule } from "./srs.js?v=1";

const KEY = "ielts_vocab";

const mem = { v: null }; // Node 退回存储(模块级共享;测试文件开头需调用 __resetMem() 隔离)
function backend() {
  if (typeof localStorage !== "undefined") return localStorage;
  return {
    getItem: () => mem.v,
    setItem: (_k, val) => { mem.v = val; },
  };
}

export function loadAll() {
  const raw = backend().getItem(KEY);
  if (!raw) return [];
  try { return JSON.parse(raw); } catch { return []; }
}

function saveAll(list) {
  backend().setItem(KEY, JSON.stringify(list));
}

function localDateKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function reviewState(entry) {
  const r = entry.review || {};
  return {
    level: Number(r.level) || 0,
    next_due: r.next_due || null,
    history: Array.isArray(r.history) ? r.history : [],
    correct: Number(r.correct) || 0,
    wrong: Number(r.wrong) || 0,
    fuzzy: Number(r.fuzzy) || 0,
    streak: Number(r.streak) || 0,
    lapses: Number(r.lapses) || 0,
  };
}

// 判断某词是否已入库(按小写去重)
export function has(word) {
  const w = word.toLowerCase();
  return loadAll().some((e) => e.word.toLowerCase() === w);
}

// 新增或更新一个生词。entry 至少含 word/def;其余可选。
// 返回 { added: boolean }。已存在则更新出处/例句,不新增。
export function addWord(entry) {
  const list = loadAll();
  const w = entry.word.toLowerCase();
  const idx = list.findIndex((e) => e.word.toLowerCase() === w);
  const record = {
    word: entry.word,
    def: entry.def || "",
    pos: entry.pos || "",
    sentence_en: entry.sentence_en || "",
    sentence_zh: entry.sentence_zh || "",
    source: entry.source || "",
    passage_id: entry.passage_id || "",
    sentence_id: entry.sentence_id || null,
    added_at: entry.added_at || new Date().toISOString().slice(0, 10),
    status: "new",
    aids: entry.aids || null, // 记忆法数据;入库时通常为 null,之后备份→回填补上
    review: { level: 0, next_due: null, history: [] },
  };
  if (idx >= 0) {
    // 保留原 added_at/status/review/aids,更新语境与释义
    record.added_at = list[idx].added_at;
    record.status = list[idx].status;
    record.review = list[idx].review;
    // aids:新传入的优先(回填场景);否则保留已有的,不被清空
    record.aids = entry.aids || list[idx].aids || null;
    list[idx] = record;
    saveAll(list);
    return { added: false };
  }
  list.push(record);
  saveAll(list);
  return { added: true };
}

export function removeWord(word) {
  const w = word.toLowerCase();
  const list = loadAll().filter((e) => e.word.toLowerCase() !== w);
  saveAll(list);
}

// 轻量记忆曲线：到期、新词、错误率和遗忘次数共同决定抽取优先级。
export function reviewWeight(entry, now = new Date()) {
  const r = reviewState(entry);
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const due = r.next_due ? new Date(`${r.next_due}T00:00:00`) : null;
  const days = due ? Math.round((today - due) / 86400000) : 0;
  const total = r.correct + r.wrong + r.fuzzy;
  const errorRate = (r.wrong + r.fuzzy * 0.55) / Math.max(1, total);
  const dueScore = !due ? 5 : days >= 0 ? 3 + Math.min(8, days) : 0.35 / (1 + Math.abs(days));
  const newScore = total === 0 ? 4 : 0;
  const difficultyScore = errorRate * 9 + Math.min(5, r.lapses * 0.8);
  const levelScore = Math.max(0, 3 - r.level * 0.45);
  return Math.max(0.15, dueScore + newScore + difficultyScore + levelScore);
}

export function pickReviewWord(excludeWord = "", random = Math.random) {
  const list = loadAll();
  if (!list.length) return null;
  const pool = list.length > 1
    ? list.filter((e) => e.word.toLowerCase() !== excludeWord.toLowerCase())
    : list;
  const weighted = pool.map((entry) => ({ entry, weight: reviewWeight(entry) }));
  const total = weighted.reduce((n, x) => n + x.weight, 0);
  let cursor = random() * total;
  for (const item of weighted) {
    cursor -= item.weight;
    if (cursor <= 0) return item.entry;
  }
  return weighted[weighted.length - 1].entry;
}

export function gradeReview(word, rating, now = new Date()) {
  const list = loadAll();
  const idx = list.findIndex((e) => e.word.toLowerCase() === word.toLowerCase());
  if (idx < 0) throw new Error("生词不存在");
  // 调度交给共享 SRS(默认 FSRS,可设置回退梯度);next_due/level/统计等由其维护。
  const { review, interval } = schedule(list[idx].review, rating, now);
  list[idx].review = review;
  list[idx].status = review.level >= 5 && review.streak >= 3 ? "mastered" : "learning";
  saveAll(list);
  return { review, interval, status: list[idx].status };
}

export function getReviewStats() {
  const list = loadAll();
  const today = localDateKey();
  return {
    total: list.length,
    due: list.filter((e) => !reviewState(e).next_due || reviewState(e).next_due <= today).length,
    difficult: list.filter((e) => {
      const r = reviewState(e); const n = r.correct + r.wrong + r.fuzzy;
      return n >= 2 && (r.wrong + r.fuzzy * 0.55) / n >= 0.45;
    }).length,
  };
}

// 导出为可下载 JSON 字符串
export function exportJSON() {
  return JSON.stringify(loadAll(), null, 2);
}

// 从 JSON 字符串导入(合并,按 word 去重,导入项覆盖同名)
export function importJSON(text) {
  let incoming;
  try {
    incoming = JSON.parse(text);
  } catch {
    throw new Error("导入文件不是合法的 JSON");
  }
  if (!Array.isArray(incoming)) throw new Error("导入文件应为数组");
  const list = loadAll();
  const byWord = new Map(list.map((e) => [e.word.toLowerCase(), e]));
  // 注:导入文件假定为本模块 exportJSON 的产物(字段完整);不对外部残缺记录做补全。
  for (const e of incoming) {
    if (e && e.word) byWord.set(e.word.toLowerCase(), e);
  }
  const merged = [...byWord.values()];
  saveAll(merged);
  return { total: merged.length };
}

// 供测试重置内存后端
export function __resetMem() { mem.v = null; }
