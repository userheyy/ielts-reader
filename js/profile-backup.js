import { validatePassage } from "./schema.js";

const VOCAB_KEY = "ielts_vocab";
const PASSAGE_KEY = "ielts_imported_passages";
const VOICE_KEY = "ielts_speech_voice";
const RATE_KEY = "ielts_speech_rate";
// 背单词相关键:内置词的复习状态/加入状态、每日任务与打卡痕迹。
// 这些是不透明的 JSON,备份时整块存/恢复时整块覆盖(不做字段级校验)。
const SEED_REVIEW_KEY = "ielts_vocab_seed_review";
const SEED_ADDED_KEY = "ielts_vocab_seed_added";
const DAILY_KEY = "ielts_daily";

function storage() {
  if (typeof localStorage === "undefined") {
    throw new Error("当前环境不支持浏览器本地存储");
  }
  return localStorage;
}

function readJSON(key, fallback) {
  const raw = storage().getItem(key);
  if (!raw) return fallback;
  try { return JSON.parse(raw); } catch { return fallback; }
}

function normalizePassageMap(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  const valid = {};
  for (const [id, passage] of Object.entries(value)) {
    if (!passage || typeof passage !== "object") continue;
    const result = validatePassage(passage);
    if (result.ok) valid[id] = passage;
  }
  return valid;
}

function normalizeVocabList(value) {
  if (!Array.isArray(value)) return [];
  return value.filter((entry) => entry && typeof entry === "object" && entry.word);
}

export function collectProfileBackup() {
  const vocab = normalizeVocabList(readJSON(VOCAB_KEY, []));
  const importedPassages = normalizePassageMap(readJSON(PASSAGE_KEY, {}));
  const seedReview = readJSON(SEED_REVIEW_KEY, {});
  const seedAdded = readJSON(SEED_ADDED_KEY, {});
  const daily = readJSON(DAILY_KEY, null);
  return {
    app: "ielts-reading-helper",
    version: 2,
    exported_at: new Date().toISOString(),
    data: {
      vocab,
      imported_passages: importedPassages,
      seed_review: seedReview,
      seed_added: seedAdded,
      daily,
      speech: {
        voice: storage().getItem(VOICE_KEY) || "",
        rate: storage().getItem(RATE_KEY) || "",
      },
    },
    summary: {
      vocab_count: vocab.length,
      imported_passage_count: Object.keys(importedPassages).length,
      seed_learned_count: Object.keys(seedReview).length,
      daily_days: daily && daily.days ? Object.keys(daily.days).length : 0,
    },
  };
}

export function exportProfileJSON() {
  return JSON.stringify(collectProfileBackup(), null, 2);
}

function parseBackup(text) {
  let parsed;
  try { parsed = JSON.parse(text); }
  catch { throw new Error("备份文件不是合法的 JSON"); }

  // 兼容旧的“只备份生词”文件：恢复时只合并生词。
  if (Array.isArray(parsed)) {
    return {
      data: { vocab: parsed, imported_passages: {}, speech: {} },
      legacy: true,
    };
  }

  if (!parsed || typeof parsed !== "object" || !parsed.data) {
    throw new Error("这不是本应用的全量备份文件");
  }
  return parsed;
}

export function restoreProfileBackup(text) {
  const backup = parseBackup(text);
  const data = backup.data || {};
  const incomingVocab = normalizeVocabList(data.vocab);
  const incomingPassages = normalizePassageMap(data.imported_passages);
  const speech = data.speech && typeof data.speech === "object" ? data.speech : {};

  const currentVocab = normalizeVocabList(readJSON(VOCAB_KEY, []));
  const byWord = new Map(currentVocab.map((entry) => [entry.word.toLowerCase(), entry]));
  for (const entry of incomingVocab) byWord.set(entry.word.toLowerCase(), entry);
  const mergedVocab = [...byWord.values()];
  storage().setItem(VOCAB_KEY, JSON.stringify(mergedVocab));

  const currentPassages = normalizePassageMap(readJSON(PASSAGE_KEY, {}));
  const mergedPassages = { ...currentPassages, ...incomingPassages };
  storage().setItem(PASSAGE_KEY, JSON.stringify(mergedPassages));

  if (typeof speech.voice === "string") storage().setItem(VOICE_KEY, speech.voice);
  if (typeof speech.rate === "string" || typeof speech.rate === "number") {
    storage().setItem(RATE_KEY, String(speech.rate));
  }

  // 背单词状态:内置词复习/加入状态、每日打卡。整块合并/覆盖。
  // seed_review / seed_added:按 word 键合并,导入项覆盖同名。
  if (data.seed_review && typeof data.seed_review === "object") {
    const cur = readJSON(SEED_REVIEW_KEY, {});
    storage().setItem(SEED_REVIEW_KEY, JSON.stringify({ ...cur, ...data.seed_review }));
  }
  if (data.seed_added && typeof data.seed_added === "object") {
    const cur = readJSON(SEED_ADDED_KEY, {});
    storage().setItem(SEED_ADDED_KEY, JSON.stringify({ ...cur, ...data.seed_added }));
  }
  // daily:打卡痕迹以"天"为粒度合并(导入的天覆盖同名天);settings/cursor 取导入值。
  if (data.daily && typeof data.daily === "object") {
    const cur = readJSON(DAILY_KEY, {});
    const merged = {
      settings: { ...(cur.settings || {}), ...(data.daily.settings || {}) },
      new_word_cursor: Math.max(Number(cur.new_word_cursor) || 0, Number(data.daily.new_word_cursor) || 0),
      days: { ...(cur.days || {}), ...(data.daily.days || {}) },
    };
    storage().setItem(DAILY_KEY, JSON.stringify(merged));
  }

  const dailyDays = data.daily && data.daily.days ? Object.keys(data.daily.days).length : 0;
  return {
    legacy: Boolean(backup.legacy),
    vocab_added_or_updated: incomingVocab.length,
    imported_passages_added_or_updated: Object.keys(incomingPassages).length,
    seed_learned_restored: data.seed_review ? Object.keys(data.seed_review).length : 0,
    daily_days_restored: dailyDays,
    total_vocab: mergedVocab.length,
    total_imported_passages: Object.keys(mergedPassages).length,
  };
}

export function downloadProfileBackup() {
  const blob = new Blob([exportProfileJSON()], { type: "application/json" });
  const a = document.createElement("a");
  const date = new Date().toISOString().slice(0, 10);
  a.href = URL.createObjectURL(blob);
  a.download = `ielts-full-backup-${date}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
}

export function bindProfileBackupUI({ exportButtonId, importInputId, onRestored } = {}) {
  const exportButton = document.getElementById(exportButtonId);
  const importInput = document.getElementById(importInputId);
  if (exportButton) exportButton.addEventListener("click", downloadProfileBackup);
  if (!importInput) return;
  importInput.addEventListener("change", async (ev) => {
    const file = ev.target.files[0];
    if (!file) return;
    try {
      const result = restoreProfileBackup(await file.text());
      alert(
        `恢复完成：合并 ${result.vocab_added_or_updated} 个生词、` +
        `${result.imported_passages_added_or_updated} 篇临时导入文章。\n` +
        (result.seed_learned_restored ? `恢复 ${result.seed_learned_restored} 个内置词的学习记录。\n` : "") +
        (result.daily_days_restored ? `恢复 ${result.daily_days_restored} 天的打卡痕迹。\n` : "") +
        `当前共有 ${result.total_vocab} 个生词、${result.total_imported_passages} 篇临时导入文章。\n` +
        `注：项目自带的内置文章在 data 文件夹里，不需要放进浏览器备份。`
      );
      if (typeof onRestored === "function") onRestored(result);
    } catch (e) {
      alert("全量恢复失败：" + e.message);
    }
    ev.target.value = "";
  });
}
