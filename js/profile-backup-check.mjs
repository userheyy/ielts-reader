import assert from "node:assert/strict";
import { exportProfileJSON, restoreProfileBackup } from "./profile-backup.js";

const bag = new Map();
globalThis.localStorage = {
  getItem: (key) => bag.has(key) ? bag.get(key) : null,
  setItem: (key, value) => bag.set(key, String(value)),
};

const passage = {
  id: "tmp-p1",
  source: "Agent",
  title: "Temporary Passage",
  sentences: [{
    id: 1,
    para: 1,
    en: "New Zealand is beautiful.",
    zh: "新西兰很美。",
    grammar: { type: "主系表", note: "is 连接主语和表语" },
    words: [{ word: "New Zealand", pos: "n.", def: "新西兰" }],
  }],
};

bag.set("ielts_vocab", JSON.stringify([{ word: "delta", def: "三角洲", review: { level: 2 } }]));
bag.set("ielts_imported_passages", JSON.stringify({ "tmp-p1": passage }));
bag.set("ielts_speech_voice", "Microsoft Ada Multilingual Online");
bag.set("ielts_speech_rate", "0.9");

const exported = exportProfileJSON();
const parsed = JSON.parse(exported);
assert.equal(parsed.summary.vocab_count, 1);
assert.equal(parsed.summary.imported_passage_count, 1);

bag.clear();
bag.set("ielts_vocab", JSON.stringify([{ word: "airport", def: "机场" }]));
const result = restoreProfileBackup(exported);
assert.equal(result.total_vocab, 2);
assert.equal(result.total_imported_passages, 1);
assert.equal(bag.get("ielts_speech_voice"), "Microsoft Ada Multilingual Online");

const vocab = JSON.parse(bag.get("ielts_vocab"));
assert.ok(vocab.some((entry) => entry.word === "delta"));
assert.ok(vocab.some((entry) => entry.word === "airport"));

const passages = JSON.parse(bag.get("ielts_imported_passages"));
assert.equal(passages["tmp-p1"].title, "Temporary Passage");

const legacy = restoreProfileBackup(JSON.stringify([{ word: "legacy", def: "旧版生词文件" }]));
assert.equal(legacy.legacy, true);
assert.ok(JSON.parse(bag.get("ielts_vocab")).some((entry) => entry.word === "legacy"));
