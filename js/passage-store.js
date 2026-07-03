import { validatePassage } from "./schema.js";

const KEY = "ielts_imported_passages";

function loadMap() {
  try { return JSON.parse(localStorage.getItem(KEY) || "{}"); }
  catch { return {}; }
}

function saveMap(map) {
  localStorage.setItem(KEY, JSON.stringify(map));
}

export function listImportedPassages() {
  return Object.values(loadMap()).map((p) => ({
    id: p.id,
    source: p.source,
    title: p.title,
    sentence_count: p.sentences.length,
    question_count: (p.questions || []).reduce((n, g) => n + g.items.length, 0),
    imported: true,
  }));
}

export function getImportedPassage(id) {
  return loadMap()[id] || null;
}

export function importPassageJSON(text) {
  let passage;
  try { passage = JSON.parse(text); }
  catch { throw new Error("文件不是合法的 JSON"); }
  const result = validatePassage(passage);
  if (!result.ok) throw new Error(result.errors.join("；"));
  const map = loadMap();
  const replaced = Boolean(map[passage.id]);
  map[passage.id] = passage;
  saveMap(map);
  return { passage, replaced };
}
