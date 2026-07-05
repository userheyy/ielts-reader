// 设置页逻辑:DeepSeek API Key / 模型名 + 全站朗读(voice/rate)统一入口。
// key 存 localStorage 'ielts_ds_key',模型存 'ielts_ds_model'(与 js/ai.js 约定一致)。
// 朗读 voice/rate 存 localStorage 'ielts_speech_voice' / 'ielts_speech_rate'(见 js/speech.js)。
import { initSpeechControls, speakEnglish, stopSpeaking } from "./speech.js?v=6";

// ---- 朗读控件挂载(voice/rate 存 localStorage,全站朗读读同一份) ----
initSpeechControls(
  document.getElementById("speech-voice"),
  document.getElementById("speech-rate"),
  document.getElementById("speech-stop"),
);
document.getElementById("speech-test").addEventListener("click", () => {
  speakEnglish("The quick brown fox jumps over the lazy dog. IELTS is a test of English proficiency.");
});

const KEY_LS = "ielts_ds_key";
const MODEL_LS = "ielts_ds_model";
const DEFAULT_MODEL = "deepseek-chat";

const keyEl = document.getElementById("ds-key");
const toggleEl = document.getElementById("ds-key-toggle");
const modelEl = document.getElementById("ds-model");
const saveEl = document.getElementById("ds-save");
const clearEl = document.getElementById("ds-clear");
const testEl = document.getElementById("ds-test");
const statusEl = document.getElementById("ds-status");
const testResultEl = document.getElementById("ds-test-result");

function lsGet(name) {
  try {
    return (localStorage.getItem(name) || "").trim();
  } catch {
    return ""; // 隐私模式等场景拿不到 localStorage
  }
}

// 只显示前 5 位和后 4 位,避免完整 Key 出现在屏幕上被偷看/截图
function mask(k) {
  if (k.length <= 9) return k.slice(0, 2) + "***";
  return k.slice(0, 5) + "……" + k.slice(-4);
}

function setStatus(el, msg, kind) {
  el.textContent = msg;
  el.className = "set-status" + (kind ? " " + kind : "");
}

function refreshKeyHint() {
  const saved = lsGet(KEY_LS);
  keyEl.placeholder = saved ? "已保存(输入新 Key 可覆盖)" : "sk-...";
  if (saved) setStatus(statusEl, "当前已保存 Key:" + mask(saved), "ok");
  else setStatus(statusEl, "还没有保存 Key,AI 功能暂时用不了", "");
}

// 显示/隐藏 Key 明文
toggleEl.addEventListener("click", () => {
  const show = keyEl.type === "password";
  keyEl.type = show ? "text" : "password";
  toggleEl.textContent = show ? "隐藏" : "显示";
});

// 保存:输入框里有 Key 就覆盖保存;模型名一起保存(空则回落默认)
saveEl.addEventListener("click", () => {
  const k = keyEl.value.trim();
  const m = modelEl.value.trim() || DEFAULT_MODEL;
  try {
    if (k) localStorage.setItem(KEY_LS, k);
    localStorage.setItem(MODEL_LS, m);
  } catch {
    setStatus(statusEl, "保存失败:浏览器不允许写入本地存储(可能开了隐私/无痕模式)", "err");
    return;
  }
  modelEl.value = m;
  const saved = lsGet(KEY_LS);
  if (!saved) {
    setStatus(statusEl, "模型名已保存,但 API Key 还没填,AI 功能暂时用不了", "err");
    return;
  }
  // 保存成功后清空输入框并恢复密文状态,避免 Key 留在屏幕上
  keyEl.value = "";
  keyEl.type = "password";
  toggleEl.textContent = "显示";
  refreshKeyHint();
  setStatus(statusEl, (k ? "Key 和模型已保存:" : "模型已保存(Key 未变动):") + mask(saved), "ok");
});

// 清除:只删 Key,模型名保留
clearEl.addEventListener("click", () => {
  try {
    localStorage.removeItem(KEY_LS);
  } catch {}
  keyEl.value = "";
  keyEl.type = "password";
  toggleEl.textContent = "显示";
  setStatus(testResultEl, "", "");
  refreshKeyHint();
  setStatus(statusEl, "已清除本浏览器保存的 Key", "ok");
});

// 测试连接:用保存好的 Key 发一条最小请求,显示往返毫秒和模型回复
testEl.addEventListener("click", async () => {
  const typed = keyEl.value.trim();
  if (typed && typed !== lsGet(KEY_LS)) {
    setStatus(testResultEl, "输入框里有还没保存的 Key,请先点「保存」再测试", "err");
    return;
  }
  testEl.disabled = true;
  setStatus(testResultEl, "测试中,请稍等……", "");
  const t0 = performance.now();
  try {
    const mod = await import("./ai.js"); // 动态引入,页面本身不因 ai.js 出问题而白屏
    const reply = await mod.askDeepSeek(
      [{ role: "user", content: "回复:在线" }],
      { maxTokens: 5 },
    );
    const ms = Math.round(performance.now() - t0);
    setStatus(testResultEl, "连接成功,往返 " + ms + " 毫秒,模型回复:" + reply, "ok");
  } catch (e) {
    const ms = Math.round(performance.now() - t0);
    setStatus(testResultEl, "连接失败(" + ms + " 毫秒):" + (e && e.message ? e.message : e), "err");
  } finally {
    testEl.disabled = false;
  }
});

// 初始化
modelEl.value = lsGet(MODEL_LS) || DEFAULT_MODEL;
refreshKeyHint();
