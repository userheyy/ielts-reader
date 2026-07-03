import assert from "node:assert";

const spoken = [];
const fakeSynth = {
  speaking: false, pending: false, paused: false,
  getVoices: () => [
    { name: "Unstable Online UK", lang: "en-GB", localService: false },
    { name: "Reliable Local", lang: "en-US", localService: true },
  ],
  addEventListener: () => {},
  cancel() { this.speaking = false; this.pending = false; },
  resume() { this.paused = false; },
  speak(u) {
    spoken.push({ text: u.text, voice: u.voice?.name }); this.speaking = true;
    setTimeout(() => u.onstart?.(), 1);
    setTimeout(() => { this.speaking = false; u.onend?.(); }, 15);
  },
};
globalThis.window = { speechSynthesis: fakeSynth };
globalThis.localStorage = { getItem: () => null, setItem: () => {} };
globalThis.SpeechSynthesisUtterance = class { constructor(text) { this.text = text; } };

const { speakEnglish } = await import("./speech.js?test=1");
speakEnglish("sentence one");
await new Promise((r) => setTimeout(r, 30));
speakEnglish("New Zealand");
await new Promise((r) => setTimeout(r, 3));
speakEnglish("sentence two");
await new Promise((r) => setTimeout(r, 180));
assert.deepEqual(spoken.map((x) => x.text), ["sentence one", "New Zealand", "sentence two"]);
assert.ok(spoken.every((x) => x.voice === undefined), "默认应交给系统选择，不绑定在线音色");
console.log("speech.js 连续播放测试通过 ✅");
