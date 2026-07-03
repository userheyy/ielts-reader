const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
// 页面加载时清除之前 Online 音色可能遗留的浏览器级挂起任务。
if (synth) { synth.cancel(); synth.resume(); }
let selectedVoiceName = localStorage.getItem("ielts_speech_voice") || "";
let rate = Number(localStorage.getItem("ielts_speech_rate")) || 0.9;
let activeUtterance = null;
let activeCleanup = null;
let requestId = 0;

function englishVoices() {
  if (!synth) return [];
  return synth.getVoices().filter((v) => /^en[-_]/i.test(v.lang));
}

function selectableVoices() {
  return englishVoices().sort((a, b) => {
    const score = (v) => (/^en-GB$/i.test(v.lang) ? 100 : 0)
      + (/female|sonia|libby|serena/i.test(v.name) ? 15 : 0)
      + (v.localService ? 5 : 0);
    return score(b) - score(a) || a.name.localeCompare(b.name);
  });
}

function preferredVoice() {
  if (!selectedVoiceName) return null;
  return selectableVoices().find((v) => v.name === selectedVoiceName) || null;
}

export function speakEnglish(text, callbacks = {}) {
  if (!synth || !text) return false;
  if (activeCleanup) activeCleanup();
  const id = ++requestId;
  // 保持在用户点击的同步调用栈内，避免浏览器把延时播放判定为非用户触发。
  synth.cancel();
  synth.resume();
  const utterance = new SpeechSynthesisUtterance(text);
  activeUtterance = utterance;
  utterance.lang = "en-GB";
  utterance.rate = rate;
  utterance.pitch = 1;
  const voice = preferredVoice();
  if (voice) utterance.voice = voice;
  let finished = false;
  let watchdog = null;
  const finish = (isError = false) => {
    if (finished || id !== requestId) return;
    finished = true;
    activeUtterance = null;
    activeCleanup = null;
    if (watchdog) clearTimeout(watchdog);
    (isError ? callbacks.onerror : callbacks.onend)?.();
  };
  activeCleanup = () => finish(false);
  utterance.onstart = () => { if (id === requestId) callbacks.onstart?.(); };
  utterance.onend = () => finish(false);
  utterance.onerror = () => finish(true);
  synth.speak(utterance);
  const expectedMs = Math.max(3500, Math.min(25000, text.length * 105 / rate));
  watchdog = setTimeout(() => {
    if (id !== requestId || finished) return;
    synth.cancel(); synth.resume(); finish(false);
  }, expectedMs);
  return true;
}

export function stopSpeaking() {
  if (activeCleanup) activeCleanup();
  requestId += 1;
  activeUtterance = null;
  if (synth) { synth.cancel(); synth.resume(); }
}

export function speechSupported() {
  return Boolean(synth);
}

export function initSpeechControls(voiceSelect, rateSelect, stopButton) {
  if (!synth) {
    voiceSelect.innerHTML = '<option>浏览器不支持朗读</option>';
    voiceSelect.disabled = true;
    rateSelect.disabled = true;
    stopButton.disabled = true;
    return;
  }

  const renderVoices = () => {
    const voices = selectableVoices();
    voiceSelect.innerHTML = '<option value="">系统默认英语语音</option>';
    if (selectedVoiceName && !voices.some((v) => v.name === selectedVoiceName)) selectedVoiceName = "";
    if (!selectedVoiceName && voices.length) {
      selectedVoiceName = voices[0].name;
      localStorage.setItem("ielts_speech_voice", selectedVoiceName);
    }
    for (const voice of voices) {
      const option = document.createElement("option");
      option.value = voice.name;
      option.textContent = `${voice.name} · ${voice.lang} · ${voice.localService ? "本机" : "在线"}`;
      option.selected = voice.name === selectedVoiceName;
      voiceSelect.appendChild(option);
    }
    voiceSelect.value = selectedVoiceName;
  };
  renderVoices();
  synth.addEventListener("voiceschanged", renderVoices, { once: true });
  rateSelect.value = String(rate);
  voiceSelect.addEventListener("change", () => {
    selectedVoiceName = voiceSelect.value;
    localStorage.setItem("ielts_speech_voice", selectedVoiceName);
  });
  rateSelect.addEventListener("change", () => {
    rate = Number(rateSelect.value) || 0.9;
    localStorage.setItem("ielts_speech_rate", String(rate));
  });
  stopButton.addEventListener("click", stopSpeaking);
}
