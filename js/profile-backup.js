import { validatePassage } from "./schema.js";

const VOCAB_KEY = "ielts_vocab";
const PASSAGE_KEY = "ielts_imported_passages";
const VOICE_KEY = "ielts_speech_voice";
const RATE_KEY = "ielts_speech_rate";

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
  return {
    app: "ielts-reading-helper",
    version: 1,
    exported_at: new Date().toISOString(),
    data: {
      vocab,
      imported_passages: importedPassages,
      speech: {
        voice: storage().getItem(VOICE_KEY) || "",
        rate: storage().getItem(RATE_KEY) || "",
      },
    },
    summary: {
      vocab_count: vocab.length,
      imported_passage_count: Object.keys(importedPassages).length,
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

  return {
    legacy: Boolean(backup.legacy),
    vocab_added_or_updated: incomingVocab.length,
    imported_passages_added_or_updated: Object.keys(incomingPassages).length,
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
