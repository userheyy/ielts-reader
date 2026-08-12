// 每日单词的逻辑层:ielts_daily 读写 + 今日任务生成(复习优先+新词补足) +
// 游标推进 + 热力图数据聚合 + 连续打卡计数。纯逻辑,不碰 DOM,便于测试。
//
// 依赖:
//   - store.js 的生词库(loadAll)与 SRS 结构
//   - seed.js 的内置词加载/内置词SRS(loadSeed / getSeedReview)
//   - tools/seed_wordlist-basic.json 通过 fetch 加载(仅含单词和词频,新词来源)
//
// 关键约束:新词只放"已在 vocab-seed.json 生成了 aids 的词"(当前批次),
// 游标不越过已生成边界;未生成 aids 的词不放出(等后续批次)。

import { loadAll as loadVocab } from "./store.js?v=7";
import { loadSeedBasic, getSeedReviews } from "./seed.js?v=5";

const KEY = "ielts_daily";
const WORDLIST_URL = "tools/seed_wordlist-basic.json";

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
    excluded_words: d.excluded_words && typeof d.excluded_words === "object" && !Array.isArray(d.excluded_words)
      ? d.excluded_words : {},
  };
}

function saveDaily(d) {
  backend().setItem(KEY, JSON.stringify(d));
}

function wordKey(word) {
  return String(word || "").trim().toLowerCase();
}

function completedAfterEdit(rec) {
  const done = (Number(rec.reviewed_done) || 0) + (Number(rec.new_done) || 0);
  rec.planned = Math.max(done, Number(rec.planned) || 0);
  rec.completed = done > 0 && done >= rec.planned;
}

// ---------- 记忆队列排除 / 恢复 ----------
// “移出记忆队列”只暂停每日安排，不删除生词或内置词本身。
// 元数据同时记录本次对今日 planned 的调整，便于当天从设置里无损恢复。
export function getExcludedWords() {
  return Object.values(loadDaily().excluded_words)
    .filter((item) => item && item.word)
    .sort((a, b) => String(b.removed_at || "").localeCompare(String(a.removed_at || "")));
}

export function removeWordFromMemoryQueue(word, kind = "review", now = new Date()) {
  const key = wordKey(word);
  if (!key) return null;

  const d = loadDaily();
  if (d.excluded_words[key]) return { day: d.days[dateKey(now)] || null, item: d.excluded_words[key] };

  const todayKey = dateKey(now);
  const rec = d.days[todayKey];
  const normalizedKind = kind === "new" ? "new" : "review";
  let adjustedToday = false;

  if (rec) {
    if (normalizedKind === "new") {
      const index = (rec.new_words || []).findIndex((item) => wordKey(item) === key);
      const done = Number(rec.new_done) || 0;
      if (index >= done) {
        rec.new_words.splice(index, 1);
        rec.planned = Math.max(0, (Number(rec.planned) || 0) - 1);
        adjustedToday = true;
      }
    } else {
      const done = (Number(rec.reviewed_done) || 0) + (Number(rec.new_done) || 0);
      if ((Number(rec.planned) || 0) > done) {
        rec.planned -= 1;
        adjustedToday = true;
      }
    }
    completedAfterEdit(rec);
  }

  const item = {
    word: String(word).trim(),
    kind: normalizedKind,
    removed_on: todayKey,
    removed_at: now.toISOString(),
    adjusted_today: adjustedToday,
  };
  d.excluded_words[key] = item;
  saveDaily(d);
  return { day: rec || null, item };
}

export function restoreWordToMemoryQueue(word, now = new Date()) {
  const key = wordKey(word);
  if (!key) return null;

  const d = loadDaily();
  const item = d.excluded_words[key];
  if (!item) return { day: d.days[dateKey(now)] || null, item: null };

  const todayKey = dateKey(now);
  const rec = d.days[todayKey];
  if (rec && item.removed_on === todayKey && item.adjusted_today) {
    if (item.kind === "new") {
      if (!Array.isArray(rec.new_words)) rec.new_words = [];
      const exists = rec.new_words.some((queued) => wordKey(queued) === key);
      if (!exists) rec.new_words.push(item.word);
    }
    rec.planned = (Number(rec.planned) || 0) + 1;
    completedAfterEdit(rec);
  }

  delete d.excluded_words[key];
  saveDaily(d);
  return { day: rec || null, item };
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
    // 词表是静态文件,交给浏览器按 HTTP 缓存头处理。
    const res = await fetch(WORDLIST_URL);
    const payload = res.ok ? await res.json() : [];
    const arr = Array.isArray(payload) ? payload : (Array.isArray(payload.words) ? payload.words : []);
    _wordlistCache = Array.isArray(arr)
      ? arr.slice().sort((a, b) => (a.freq_rank || 1e9) - (b.freq_rank || 1e9))
      : [];
  } catch { _wordlistCache = []; }
  return _wordlistCache;
}

async function getSeedIndex() {
  if (_seedIndexCache) return _seedIndexCache;
  const seed = await loadSeedBasic();
  _seedIndexCache = new Map();
  for (const w of seed.words || []) {
    if (w && w.word) _seedIndexCache.set(w.word.toLowerCase(), w);
  }
  return _seedIndexCache;
}

// ---------- 复习词:扫描所有已学词,挑到期的 ----------
// 返回 [{word, origin:'vocab'|'seed', due}]
function reviewDue(seedIndex, todayKey, excluded = new Set(), seedReviews = getSeedReviews()) {
  const out = [];
  // 生词库
  for (const v of loadVocab()) {
    if (excluded.has(wordKey(v.word))) continue;
    const r = v.review || {};
    const total = (Number(r.correct) || 0) + (Number(r.wrong) || 0) + (Number(r.fuzzy) || 0);
    if (total === 0) continue; // 从没复习过的生词不算"到期复习"(它们靠阅读入库,另计)
    if (!r.next_due || r.next_due <= todayKey) {
      out.push({ word: v.word, origin: "vocab", due: r.next_due || todayKey });
    }
  }
  // 内置词(已学过的,即有 seed_review 记录)
  for (const [wl, s] of seedIndex) {
    if (excluded.has(wl)) continue;
    const r = seedReviews[wl] || null;
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
function learnedSeedSet(seedIndex, seedReviews = getSeedReviews()) {
  const s = new Set();
  for (const [wl, entry] of seedIndex) {
    if (seedReviews[wl]) s.add(wl);
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

// ---------- 今日任务生成 ----------
// 复原已存在的当天任务:词表用当天存的 new_words + 当前到期复习。
function restoreDay(d, seedIndex, todayKey, seedReviews = getSeedReviews()) {
  const rec = d.days[todayKey];
  const excluded = new Set(Object.keys(d.excluded_words || {}));
  const review = reviewDue(seedIndex, todayKey, excluded, seedReviews);
  const newWords = (rec.new_words || [])
    .filter((w) => !excluded.has(wordKey(w)))
    .map((w) => seedIndex.get(w.toLowerCase()))
    .filter(Boolean);
  return { date: todayKey, review, newWords, day: rec };
}

// 生成(或重排)当天任务:按当前 settings 现取现排复习词与新词,落盘并返回。
// 调用前请确保这是"该重排"的时机(新建当天,或未开始时套用新配额)。
function generateDay(d, seedIndex, wordlist, todayKey, seedReviews = getSeedReviews()) {
  const excluded = new Set(Object.keys(d.excluded_words || {}));
  const review = reviewDue(seedIndex, todayKey, excluded, seedReviews);
  const reviewCap = d.settings.review_cap;
  const reviewList = reviewCap != null ? review.slice(0, reviewCap) : review;

  // 新词选取(纯过滤,不用游标——因 aids 词在词频序里稀疏散布,游标会错):
  // 取词频最高的、满足以下全部条件的词,补足新词配额:
  //   (a) 已在 vocab-seed.json 生成了 aids(在 seedIndex 中)
  //   (b) 没学过(无 seed_review 记录)
  //   (c) 没在过去某天已放出过但还没评分(new_words 里出现过——防重复放出)
  const learned = learnedSeedSet(seedIndex, seedReviews);
  const alreadyQueued = queuedNewWords(d, todayKey); // 过去各天 new_words 的并集(小写)
  const quota = d.settings.new_per_day;
  const newWords = [];
  for (const cand of wordlist) {
    if (newWords.length >= quota) break;
    const wl = (cand.word || "").toLowerCase();
    const seedEntry = seedIndex.get(wl);
    if (!seedEntry) continue;        // 还没生成 aids
    if (excluded.has(wl)) continue;  // 用户已移出记忆队列
    if (learned.has(wl)) continue;   // 已学过
    if (alreadyQueued.has(wl)) continue; // 之前放出过、待评分,避免今天重复
    newWords.push(seedEntry);
  }
  // new_word_cursor 保留为"已学过+已放出"的计数,仅作展示/进度参考(不再驱动选词)
  const cursorCount = learned.size + alreadyQueued.size + newWords.length;

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
  const seedIndexPromise = getSeedIndex();

  // 已有当天任务时只需恢复,不再额外请求词频表。
  if (d.days[todayKey]) {
    const seedIndex = await seedIndexPromise;
    return restoreDay(d, seedIndex, todayKey, getSeedReviews());
  }

  // 新建任务时并行取轻量词条和词频表,避免两个请求串行等待。
  const [seedIndex, wordlist] = await Promise.all([seedIndexPromise, getWordlist()]);
  return generateDay(d, seedIndex, wordlist, todayKey, getSeedReviews());
}

// 今天已经开始后调整新词配额:保留已完成的新词,按新配额截断或补足未完成的新词。
// 降低配额时不需要重新下载词表;提高配额时才按需加载词表。
async function adjustStartedDay(d, seedIndex, todayKey, seedReviews = getSeedReviews()) {
  const rec = d.days[todayKey];
  const oldWords = Array.isArray(rec.new_words) ? rec.new_words.slice() : [];
  const newDone = Math.max(0, Number(rec.new_done) || 0);
  const target = Math.max(newDone, Number(d.settings.new_per_day) || 0);
  const reviewBase = Math.max(0, (Number(rec.planned) || 0) - oldWords.length);
  const excluded = new Set(Object.keys(d.excluded_words || {}));
  const nextWords = oldWords.slice(0, target);

  if (target > nextWords.length) {
    const wordlist = await getWordlist();
    const learned = learnedSeedSet(seedIndex, seedReviews);
    const alreadyQueued = queuedNewWords(d, todayKey);
    const existing = new Set(nextWords.map(wordKey));
    for (const cand of wordlist) {
      if (nextWords.length >= target) break;
      const wl = wordKey(cand.word);
      if (!wl || existing.has(wl) || excluded.has(wl) || learned.has(wl) || alreadyQueued.has(wl)) continue;
      if (!seedIndex.has(wl)) continue;
      nextWords.push(seedIndex.get(wl).word);
      existing.add(wl);
    }
  }

  rec.new_words = nextWords;
  rec.planned = Math.max(newDone + (Number(rec.reviewed_done) || 0), reviewBase + nextWords.length);
  d.new_word_cursor = Math.max(Number(d.new_word_cursor) || 0, nextWords.length);
  saveDaily(d);
  return restoreDay(d, seedIndex, todayKey, seedReviews);
}

// 重排当天任务以套用最新设置(new_per_day 等)。
// 未开始时按新配额重新生成;已开始时保留已完成进度,只截断或补足未完成的新词。
export async function rebuildTodayTask(now = new Date()) {
  const todayKey = dateKey(now);
  const d = loadDaily();
  const rec = d.days[todayKey];
  const started = rec && (rec.reviewed_done + rec.new_done) > 0;
  const seedIndexPromise = getSeedIndex();

  if (rec && started) {
    const seedIndex = await seedIndexPromise;
    return adjustStartedDay(d, seedIndex, todayKey, getSeedReviews());
  }

  const [seedIndex, wordlist] = await Promise.all([seedIndexPromise, getWordlist()]);
  return generateDay(d, seedIndex, wordlist, todayKey, getSeedReviews());
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
