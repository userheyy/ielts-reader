// 每日单词的逻辑层:ielts_daily 读写 + 今日任务生成(复习优先+新词补足) +
// 游标推进 + 热力图数据聚合 + 连续打卡计数。纯逻辑,不碰 DOM,便于测试。
//
// 依赖:
//   - store.js 的生词库(loadAll)与 SRS 结构
//   - seed.js 的内置词加载/内置词SRS(loadSeed / getSeedReview)
//   - tools/seed_wordlist.json 通过 fetch 加载(3575词按词频排序,新词来源)
//
// 关键约束:新词只放"已在 vocab-seed.json 生成了 aids 的词"(当前批次),
// 游标不越过已生成边界;未生成 aids 的词不放出(等后续批次)。

import { loadAll as loadVocab } from "./store.js?v=7";
import { loadSeed, getSeedReview } from "./seed.js?v=3";

const KEY = "ielts_daily";
const WORDLIST_URL = "tools/seed_wordlist.json";

const DEFAULTS = { new_per_day: 30, review_cap: null };

let _wordlistCache = null;   // [{word, freq_rank, ...}] 按词频升序
let _seedIndexCache = null;  // Map<wordLower, seedEntry>

// ---------- 基础存储 ----------
function backend() {
  if (typeof localStorage !== "undefined") return localStorage;
  // Node 退回内存(测试用)
  if (!backend._mem) backend._mem = { v: null };
  return { getItem: () => backend._mem.v, setItem: (_k, val) => { backend._mem.v = val; } };
}

export function loadDaily() {
  const raw = backend().getItem(KEY);
  let d = null;
  if (raw) { try { d = JSON.parse(raw); } catch { d = null; } }
  if (!d || typeof d !== "object") d = {};
  return {
    settings: { ...DEFAULTS, ...(d.settings || {}) },
    new_word_cursor: Number(d.new_word_cursor) || 0,
    days: d.days && typeof d.days === "object" ? d.days : {},
  };
}

function saveDaily(d) {
  backend().setItem(KEY, JSON.stringify(d));
}

// ---------- 日期工具 ----------
export function dateKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${dd}`;
}

function daysAgoKey(n, from = new Date()) {
  const d = new Date(from.getFullYear(), from.getMonth(), from.getDate());
  d.setDate(d.getDate() - n);
  return dateKey(d);
}

// ---------- 设置 ----------
export function getSettings() {
  return loadDaily().settings;
}
export function updateSettings(patch) {
  const d = loadDaily();
  d.settings = { ...d.settings, ...patch };
  // 规范化:new_per_day 至少 0;review_cap null 或正整数
  d.settings.new_per_day = Math.max(0, Number(d.settings.new_per_day) || 0);
  if (d.settings.review_cap != null) {
    d.settings.review_cap = Math.max(0, Number(d.settings.review_cap) || 0);
  }
  saveDaily(d);
  return d.settings;
}

// ---------- 数据加载(词表 + 内置词索引) ----------
async function getWordlist() {
  if (_wordlistCache) return _wordlistCache;
  try {
    const res = await fetch(WORDLIST_URL, { cache: "no-cache" });
    const arr = res.ok ? await res.json() : [];
    _wordlistCache = Array.isArray(arr)
      ? arr.slice().sort((a, b) => (a.freq_rank || 1e9) - (b.freq_rank || 1e9))
      : [];
  } catch { _wordlistCache = []; }
  return _wordlistCache;
}

async function getSeedIndex() {
  if (_seedIndexCache) return _seedIndexCache;
  const seed = await loadSeed();
  _seedIndexCache = new Map();
  for (const w of seed.words || []) {
    if (w && w.word) _seedIndexCache.set(w.word.toLowerCase(), w);
  }
  return _seedIndexCache;
}

// ---------- 复习词:扫描所有已学词,挑到期的 ----------
// 返回 [{word, origin:'vocab'|'seed', due}]
// 同一个词可能同时存在于生词库和内置词 SRS(先读文章加了生词,后来又在今日学到
// 同名内置词)——只出一条,生词记录优先裁决(对齐 seed.js 复习池"同名去重,生词优先"),
// 否则同词双计:planned 多算一个、一天要过两遍。
function reviewDue(seedIndex, todayKey) {
  const out = [];
  const vocabOwned = new Set(); // 有复习历史的生词(小写):这些词以生词记录为准
  // 生词库
  for (const v of loadVocab()) {
    const r = v.review || {};
    const total = (Number(r.correct) || 0) + (Number(r.wrong) || 0) + (Number(r.fuzzy) || 0);
    if (total === 0) continue; // 从没复习过的生词不算"到期复习"(它们靠阅读入库,另计)
    vocabOwned.add(String(v.word || "").toLowerCase());
    if (!r.next_due || r.next_due <= todayKey) {
      out.push({ word: v.word, origin: "vocab", due: r.next_due || todayKey });
    }
  }
  // 内置词(已学过的,即有 seed_review 记录);生词已接管的同名词跳过
  for (const [wl, s] of seedIndex) {
    if (vocabOwned.has(wl)) continue;
    const r = getSeedReview(s.word);
    if (!r) continue; // 没学过的内置词由"新词"部分放出,不在这
    if (!r.next_due || r.next_due <= todayKey) {
      out.push({ word: s.word, origin: "seed", due: r.next_due || todayKey });
    }
  }
  // 越早到期越靠前
  out.sort((a, b) => (a.due || "").localeCompare(b.due || ""));
  return out;
}

// 已经"学过/见过"的内置词集合(用于新词跳过)
function learnedSeedSet(seedIndex) {
  const s = new Set();
  for (const [wl, entry] of seedIndex) {
    if (getSeedReview(entry.word)) s.add(wl);
  }
  return s;
}

// 过去各天(不含今天)new_words 的并集(小写),用于避免同一新词被重复放出。
// 排除今天是因为今天还没生成;若今天已生成会走上面的"复原"分支不到这里。
function queuedNewWords(d, todayKey) {
  const s = new Set();
  for (const key of Object.keys(d.days || {})) {
    if (key === todayKey) continue;
    for (const w of d.days[key].new_words || []) s.add(String(w).toLowerCase());
  }
  return s;
}

// review_cap 归一化:null/非法 → null(不限);否则非负整数
function normalizedReviewCap(settings) {
  if (settings.review_cap == null) return null;
  const n = Number(settings.review_cap);
  return Number.isFinite(n) ? Math.max(0, Math.floor(n)) : null;
}

// ---------- 今日任务生成 ----------
// 复原已存在的当天任务:词表用当天存的 new_words + 当前到期复习。
// 复习也要按"剩余额度"(cap - 已复习)截断,与 generateDay 的 cap 语义一致——
// 否则设了 cap 后刷新一次页面就能超量复习。
function restoreDay(d, seedIndex, todayKey) {
  const rec = d.days[todayKey];
  let review = reviewDue(seedIndex, todayKey);
  const cap = normalizedReviewCap(d.settings);
  if (cap != null) review = review.slice(0, Math.max(0, cap - (Number(rec.reviewed_done) || 0)));
  const newWords = (rec.new_words || [])
    .map((w) => seedIndex.get(w.toLowerCase()))
    .filter(Boolean);
  return { date: todayKey, review, newWords, day: rec };
}

// 生成(或重排)当天任务:按当前 settings 现取现排复习词与新词,落盘并返回。
// 调用前请确保这是"该重排"的时机(新建当天,或未开始时套用新配额)。
function generateDay(d, seedIndex, wordlist, todayKey) {
  const review = reviewDue(seedIndex, todayKey);
  const reviewCap = normalizedReviewCap(d.settings);
  const reviewList = reviewCap != null ? review.slice(0, reviewCap) : review;

  // 新词选取(纯过滤,不用游标——因 aids 词在词频序里稀疏散布,游标会错):
  // 取词频最高的、满足以下全部条件的词,补足新词配额:
  //   (a) 已在 vocab-seed.json 生成了 aids(在 seedIndex 中)
  //   (b) 没学过(无 seed_review 记录)
  // 注意:过去放出过但没评分的词【必须】能再次放出(设计§5"不重不漏")——
  // 它们没有 seed_review、也不在复习列表,若跳过就永久丢失(曾是真 bug)。
  // 因词表按词频排序,昨天没学完的词天然排最前,今天自动"接着学"。
  // 同一天内不重复靠 ensureTodayTask 的复原分支,与此处无关。
  const learned = learnedSeedSet(seedIndex);
  const quota = Math.max(0, Number(d.settings.new_per_day) || 0); // 防损坏配额放出无限词
  const newWords = [];
  for (const cand of wordlist) {
    if (newWords.length >= quota) break;
    const wl = (cand.word || "").toLowerCase();
    const seedEntry = seedIndex.get(wl);
    if (!seedEntry) continue;        // 还没生成 aids
    if (learned.has(wl)) continue;   // 已学过
    newWords.push(seedEntry);
  }
  // new_word_cursor 保留为"已学过 ∪ 曾放出"的去重计数,仅作展示/进度参考(不驱动选词)
  const cursorUnion = new Set([...learned, ...queuedNewWords(d, todayKey)]);
  for (const w of newWords) cursorUnion.add(w.word.toLowerCase());
  const cursorCount = cursorUnion.size;

  const rec = {
    planned: reviewList.length + newWords.length,
    reviewed_done: 0,
    new_done: 0,
    new_words: newWords.map((w) => w.word),
    completed: false,
  };
  d.days[todayKey] = rec;
  d.new_word_cursor = cursorCount;
  saveDaily(d);
  return { date: todayKey, review: reviewList, newWords, day: rec };
}

// 幂等:同一天重复调用返回已缓存的当天任务(不重排、不换词)。
// 返回 { date, review:[...], newWords:[...], day: <days[date] 记录> }
export async function ensureTodayTask(now = new Date()) {
  const todayKey = dateKey(now);
  const d = loadDaily();
  const seedIndex = await getSeedIndex();
  const wordlist = await getWordlist();

  if (d.days[todayKey]) return restoreDay(d, seedIndex, todayKey);
  return generateDay(d, seedIndex, wordlist, todayKey);
}

// 重排当天任务以套用最新设置(new_per_day 等)。
// 仅当今天"还没开始"(reviewed_done + new_done === 0)时才真正重排——避免把
// 用户已过的词/进度冲掉;已开始则原样复原(等价于 ensureTodayTask)。
export async function rebuildTodayTask(now = new Date()) {
  const todayKey = dateKey(now);
  const d = loadDaily();
  const seedIndex = await getSeedIndex();
  const wordlist = await getWordlist();

  const rec = d.days[todayKey];
  const started = rec && (rec.reviewed_done + rec.new_done) > 0;
  if (rec && started) return restoreDay(d, seedIndex, todayKey);
  return generateDay(d, seedIndex, wordlist, todayKey);
}

// 记录一次"过词"完成(复习或新词),更新当天进度与完成态。
// kind: 'review' | 'new'
export function markWordDone(kind, now = new Date()) {
  const todayKey = dateKey(now);
  const d = loadDaily();
  const rec = d.days[todayKey];
  if (!rec) return null;
  if (kind === "review") rec.reviewed_done += 1;
  else if (kind === "new") rec.new_done += 1;
  if (rec.reviewed_done + rec.new_done >= rec.planned) rec.completed = true;
  saveDaily(d);
  return rec;
}

// ---------- 热力图 / 统计 ----------
// 返回最近 weeks*7 天的格子数组(旧→新),每格 {date, count, completed, isToday}
export function heatmapCells(weeks = 18, now = new Date()) {
  const d = loadDaily();
  const total = weeks * 7;
  const todayKey = dateKey(now);
  const cells = [];
  for (let i = total - 1; i >= 0; i--) {
    const key = daysAgoKey(i, now);
    const rec = d.days[key];
    const count = rec ? (rec.reviewed_done + rec.new_done) : 0;
    cells.push({ date: key, count, completed: rec ? !!rec.completed : false, isToday: key === todayKey });
  }
  return cells;
}

// 连续打卡:从今天(或昨天)往回数连续"有完成记录(count>0)"的天数。
export function currentStreak(now = new Date()) {
  const d = loadDaily();
  let streak = 0;
  // 允许今天还没做:若今天无记录,从昨天起算
  let startOffset = 0;
  const todayRec = d.days[dateKey(now)];
  if (!todayRec || (todayRec.reviewed_done + todayRec.new_done) === 0) startOffset = 1;
  for (let i = startOffset; ; i++) {
    const rec = d.days[daysAgoKey(i, now)];
    if (rec && (rec.reviewed_done + rec.new_done) > 0) streak += 1;
    else break;
  }
  return streak;
}

// 累计学习词数(所有天 done 之和)
export function totalWordsDone() {
  const d = loadDaily();
  let n = 0;
  for (const key of Object.keys(d.days)) {
    const rec = d.days[key];
    n += (rec.reviewed_done || 0) + (rec.new_done || 0);
  }
  return n;
}

// 供测试重置
export function __reset() { if (backend._mem) backend._mem.v = null; _wordlistCache = null; _seedIndexCache = null; }

// 供测试注入词表 / 内置词索引,绕过 fetch(Node 下相对路径 fetch 拿不到文件)。
export function __setCachesForTest({ wordlist, seedIndex } = {}) {
  if (wordlist) _wordlistCache = wordlist;
  if (seedIndex) _seedIndexCache = seedIndex;
}
