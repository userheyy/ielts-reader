// 间隔重复调度器 —— 复习/今日/生词库三处共用同一份逻辑(此前在 store.js / vocab.js /
// daily.js 各抄了一份梯度算法,现收敛到这里)。
//
// 默认用 FSRS-6(自适应记忆模型:难度 D + 稳定度 S + 可提取度 R);可在设置里切回旧梯度算法。
// 公式与默认权重取自 open-spaced-repetition/ts-fsrs(MIT)。本项目三档评分映射到 FSRS:
//   forgot → Again(1) · fuzzy → Hard(2) · remembered → Good(3)。
//
// review 对象在原有字段(level/next_due/history/correct/wrong/fuzzy/streak/lapses)基础上
// 增补 FSRS 状态 stability / difficulty / last_review;旧字段继续维护,供抽词权重与统计复用。

// FSRS-6 默认权重(21 个;w[20] 为 decay)
const DEFAULT_W = [
  0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001, 1.8722, 0.1666,
  0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542,
];
const S_MIN = 0.001, S_MAX = 36500, MAX_INTERVAL = 36500;
const DEFAULT_RETENTION = 0.9;
const LADDER = [0, 1, 3, 7, 14, 30, 60, 120]; // 旧梯度间隔(按 level):迁移播种 + 回退用
const RATING_TO_G = { forgot: 1, fuzzy: 2, remembered: 3 };

// ---------- 设置(localStorage,可被 settings 页读写) ----------
const SET_KEY = "ielts_srs_settings";
function clampNum(v, lo, hi, dflt) {
  v = Number(v);
  return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : dflt;
}
export function getSrsSettings() {
  let s = {};
  try { s = JSON.parse((typeof localStorage !== "undefined" && localStorage.getItem(SET_KEY)) || "{}") || {}; } catch { s = {}; }
  return {
    algo: s.algo === "ladder" ? "ladder" : "fsrs",           // 默认 FSRS
    retention: clampNum(s.retention, 0.80, 0.97, DEFAULT_RETENTION),
  };
}
export function setSrsSettings(patch) {
  const next = { ...getSrsSettings(), ...patch };
  next.retention = clampNum(next.retention, 0.80, 0.97, DEFAULT_RETENTION);
  next.algo = next.algo === "ladder" ? "ladder" : "fsrs";
  try { localStorage.setItem(SET_KEY, JSON.stringify(next)); } catch { /* ignore */ }
  return next;
}

// ---------- 日期工具 ----------
function startOfDay(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
export function dayKey(d = new Date()) {
  const y = d.getFullYear(), m = String(d.getMonth() + 1).padStart(2, "0"), dd = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${dd}`;
}
function daysBetween(fromKey, toDate) {
  if (!fromKey) return 0;
  const [y, m, d] = String(fromKey).slice(0, 10).split("-").map(Number);
  if (!y) return 0;
  const from = new Date(y, (m || 1) - 1, d || 1);
  return Math.max(0, Math.round((startOfDay(toDate) - from) / 86400000));
}
function round8(x) { return Math.round(x * 1e8) / 1e8; }

// ---------- FSRS 数学 ----------
function decayFactor(w) {
  const decay = -w[20];
  const factor = Math.exp(Math.log(0.9) / decay) - 1;
  return { decay, factor };
}
function retrievability(w, t, s) {
  const { decay, factor } = decayFactor(w);
  return Math.pow(1 + (factor * t) / s, decay);
}
function intervalModifier(w, retention) {
  const { decay, factor } = decayFactor(w);
  return (Math.pow(retention, 1 / decay) - 1) / factor;
}
function initStability(w, g) { return Math.max(w[g - 1], 0.1); }
function initDifficulty(w, g) { return clampNum(w[4] - Math.exp((g - 1) * w[5]) + 1, 1, 10, 5); }
function nextDifficulty(w, d, g) {
  const deltaD = -w[6] * (g - 3);
  const nextD = d + (deltaD * (10 - d)) / 9;          // linear damping
  const reverted = w[7] * initDifficulty(w, 4) + (1 - w[7]) * nextD; // mean reversion → Easy anchor
  return clampNum(reverted, 1, 10, 5);
}
function nextRecallStability(w, d, s, r, g) {
  const hard = g === 2 ? w[15] : 1;
  const easy = g === 4 ? w[16] : 1;
  const val = s * (1 + Math.exp(w[8]) * (11 - d) * Math.pow(s, -w[9]) * (Math.exp((1 - r) * w[10]) - 1) * hard * easy);
  return Math.min(S_MAX, Math.max(S_MIN, val));
}
function nextForgetStability(w, d, s, r) {
  const val = w[11] * Math.pow(d, -w[12]) * (Math.pow(s + 1, w[13]) - 1) * Math.exp((1 - r) * w[14]);
  return Math.min(S_MAX, Math.max(S_MIN, val));
}
function stabilityOnFail(w, d, s, r) {
  const sAfterFail = nextForgetStability(w, d, s, r);
  const nextSMin = s / Math.exp(w[17] * w[18]);
  return Math.min(sAfterFail, Math.max(S_MIN, nextSMin));
}
function fsrsInterval(w, s, retention) {
  const ivl = Math.round(s * intervalModifier(w, retention));
  return Math.min(MAX_INTERVAL, Math.max(1, ivl));
}

// ---------- 归一化 review ----------
function normalize(review) {
  const r = review || {};
  return {
    level: Number(r.level) || 0,
    next_due: r.next_due || null,
    history: Array.isArray(r.history) ? r.history.slice() : [],
    correct: Number(r.correct) || 0,
    wrong: Number(r.wrong) || 0,
    fuzzy: Number(r.fuzzy) || 0,
    streak: Number(r.streak) || 0,
    lapses: Number(r.lapses) || 0,
    stability: Number(r.stability) || 0,
    difficulty: Number(r.difficulty) || 0,
    last_review: r.last_review || null,
  };
}

// ---------- 核心:根据评分推进一个 review ----------
// 返回 { review, interval } —— review 为新状态,interval 为下次间隔(天)。
export function schedule(review, rating, now = new Date()) {
  const g = RATING_TO_G[rating];
  if (!g) throw new Error("未知评分: " + rating);
  const r = normalize(review);
  const settings = getSrsSettings();
  const today = startOfDay(now);

  // 旧统计(抽词权重 / mastered 状态仍在用)
  if (rating === "forgot") { r.wrong += 1; r.lapses += 1; r.streak = 0; r.level = Math.max(0, r.level - 2); }
  else if (rating === "fuzzy") { r.fuzzy += 1; r.streak = 0; r.level = Math.max(0, r.level - 1); }
  else { r.correct += 1; r.streak += 1; r.level = Math.min(7, r.level + 1); }

  let interval;
  if (settings.algo === "ladder") {
    interval = rating === "forgot" ? 0 : rating === "fuzzy" ? 1 : LADDER[r.level];
  } else {
    const w = DEFAULT_W;
    const d = r.difficulty, s = r.stability, hasState = d >= 1 && s >= S_MIN;
    let ns, nd;
    if (hasState) {
      // 已有 FSRS 状态:按“距上次复习的天数”算可提取度,再推进
      const t = r.last_review ? daysBetween(r.last_review, today)
        : Math.round(s * intervalModifier(w, settings.retention)); // 无 last_review 时视为“刚到期”
      const rr = retrievability(w, Math.max(0, t), s);
      ns = g === 1 ? stabilityOnFail(w, d, s, rr) : nextRecallStability(w, d, s, rr, g);
      nd = nextDifficulty(w, d, g);
    } else {
      // 无 FSRS 状态(全新词,或从旧梯度算法迁移的词):按本次评分初始化。
      // 迁移采用“重新起步”而非猜测稳定度——本项目复习历史很浅,重启无害且避免过冲。
      nd = initDifficulty(w, g);
      ns = initStability(w, g);
    }
    r.stability = round8(ns);
    r.difficulty = round8(nd);
    interval = fsrsInterval(w, ns, settings.retention);
    r.last_review = dayKey(today);
  }

  const due = new Date(today);
  due.setDate(due.getDate() + interval);
  r.next_due = dayKey(due);
  r.history.push({ date: now.toISOString(), rating, level: r.level, interval });
  if (r.history.length > 100) r.history = r.history.slice(-100);
  return { review: r, interval };
}

// 供测试/校验:导出内部数学
export const _internals = { DEFAULT_W, decayFactor, retrievability, intervalModifier, initStability, initDifficulty, nextDifficulty, nextRecallStability, stabilityOnFail, fsrsInterval };
