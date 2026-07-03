// 单词测试的错题本 / 统计存储层。
// 独立 localStorage 键，和背单词 SRS(store.js/seed.js)完全隔离。
// 每个词一条统计：{ word, seen, correct, wrong, wrong_open, last_result, last_at }
//   - seen/correct/wrong：累计考过、答对、答错次数
//   - wrong_open：是否在错题本里(答错即置 true；错题模式下连续答对 2 次移出)
//   - streak_right_in_wrong：错题模式下的连续答对计数(用于 2 连对移出)
//   - last_result: 'correct' | 'wrong'
// 无 localStorage(如 Node 测试)时退回内存。

const KEY = "ielts_quiz_stats";

const mem = { v: null };
function backend() {
  if (typeof localStorage !== "undefined") return localStorage;
  return { getItem: () => mem.v, setItem: (_k, val) => { mem.v = val; } };
}

function loadMap() {
  const raw = backend().getItem(KEY);
  if (!raw) return {};
  try { return JSON.parse(raw) || {}; } catch { return {}; }
}
function saveMap(map) {
  backend().setItem(KEY, JSON.stringify(map));
}

function blank(word) {
  return {
    word,
    seen: 0,
    correct: 0,
    wrong: 0,
    wrong_open: false,
    streak_right_in_wrong: 0,
    last_result: null,
    last_at: null,
  };
}

function nowStamp() {
  // 允许在没有真实时间的测试环境退化为 null
  try { return new Date().toISOString(); } catch { return null; }
}

// 记录一次作答结果。
//   word: 目标词
//   isCorrect: 是否答对
//   fromWrongMode: 本题是否来自「错题模式」(影响移出逻辑)
// 返回该词更新后的统计对象。
export function recordResult(word, isCorrect, fromWrongMode = false) {
  const map = loadMap();
  const w = word.toLowerCase();
  const rec = map[w] || blank(word);
  rec.word = word; // 保留原始大小写
  rec.seen += 1;
  rec.last_at = nowStamp();
  if (isCorrect) {
    rec.correct += 1;
    rec.last_result = "correct";
    if (fromWrongMode && rec.wrong_open) {
      rec.streak_right_in_wrong += 1;
      // 错题模式下连续答对 2 次 → 移出错题本
      if (rec.streak_right_in_wrong >= 2) {
        rec.wrong_open = false;
        rec.streak_right_in_wrong = 0;
      }
    }
  } else {
    rec.wrong += 1;
    rec.last_result = "wrong";
    rec.wrong_open = true;           // 答错即进错题本
    rec.streak_right_in_wrong = 0;   // 连对清零
  }
  map[w] = rec;
  saveMap(map);
  return rec;
}

// 错题本里的所有词(word 数组，原始大小写)
export function wrongWords() {
  const map = loadMap();
  return Object.values(map).filter((r) => r.wrong_open).map((r) => r.word);
}

export function wrongCount() {
  return wrongWords().length;
}

// 单词的统计(不存在返回 null)
export function getStat(word) {
  const map = loadMap();
  return map[word.toLowerCase()] || null;
}

// 汇总统计：{ testedWords, totalSeen, totalCorrect, accuracy(0-1|null), wrongCount }
export function summary() {
  const map = loadMap();
  const recs = Object.values(map);
  const totalSeen = recs.reduce((a, r) => a + r.seen, 0);
  const totalCorrect = recs.reduce((a, r) => a + r.correct, 0);
  return {
    testedWords: recs.length,
    totalSeen,
    totalCorrect,
    accuracy: totalSeen ? totalCorrect / totalSeen : null,
    wrongCount: recs.filter((r) => r.wrong_open).length,
  };
}

// 手动清空错题本(把所有 wrong_open 置 false，保留历史计数)
export function clearWrongBook() {
  const map = loadMap();
  for (const r of Object.values(map)) { r.wrong_open = false; r.streak_right_in_wrong = 0; }
  saveMap(map);
}

// 测试用：重置内存后端
export function __resetMem() { mem.v = null; }
