// 口语陪练。3 tab(Part 1 / Part 2 / Part 3),浏览器 MediaRecorder 录音 →
// POST /whisper(本地 speaking_server.py + faster-whisper)→ DeepSeek 按四项评分。
//
// 依赖:tools/speaking_server.py 必须运行在同域名端口(替代 python -m http.server)。
// 若 POST /whisper 返回 404,提示用户改用 speaking_server.py 启动。

import { askDeepSeek, hasKey } from "./ai.js?v=1";

const TASKS = { part1: [], part2: [], part3: [] };
const state = {
  part1: { recorder: null, chunks: [], startTs: 0, timerId: null, qIdx: 0 },
  part2: { recorder: null, chunks: [], startTs: 0, timerId: null },
  part3: { recorder: null, chunks: [], startTs: 0, timerId: null, qIdx: 0 },
};

function esc(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${String(s).padStart(2, "0")}`;
}

// ---- 加载题库 ----
async function loadTasks() {
  const r = await fetch("data/speaking/tasks.json");
  const d = await r.json();
  TASKS.part1 = d.part1 || [];
  TASKS.part2 = d.part2 || [];
  TASKS.part3 = d.part3 || [];
  fillPicker("part1", (t) => t.topic);
  fillPicker("part2", (t) => t.topic);
  fillPicker("part3", (t) => t.topic);
  renderTask("part1");
  renderTask("part2");
  renderTask("part3");
}

function fillPicker(kind, label) {
  const sel = document.getElementById(`${kind}-pick`);
  sel.innerHTML = "";
  for (const t of TASKS[kind]) {
    const opt = document.createElement("option");
    opt.value = t.id;
    opt.textContent = label(t);
    sel.appendChild(opt);
  }
  sel.addEventListener("change", () => renderTask(kind));
}

function currentTask(kind) {
  const id = document.getElementById(`${kind}-pick`).value;
  return TASKS[kind].find((t) => t.id === id) || TASKS[kind][0];
}

function renderTask(kind) {
  const t = currentTask(kind);
  if (!t) return;
  document.getElementById(`${kind}-topic`).textContent = t.topic || "";
  document.getElementById(`${kind}-transcript`).style.display = "none";
  document.getElementById(`${kind}-transcript-text`).textContent = "";
  document.getElementById(`${kind}-result`).innerHTML = "";

  if (kind === "part1" || kind === "part3") {
    const listEl = document.getElementById(`${kind}-questions`);
    listEl.innerHTML = (t.questions || [])
      .map((q, i) => `<li data-idx="${i}">${esc(q)}</li>`).join("");
    listEl.querySelectorAll("li").forEach((li) =>
      li.addEventListener("click", () => setQuestion(kind, Number(li.dataset.idx))));
    setQuestion(kind, 0);
    if (kind === "part3") {
      const rel = TASKS.part2.find((p2) => p2.id === t.related_to);
      document.getElementById("part3-related").textContent =
        rel ? `(承接 Part 2:${rel.topic})` : "";
    }
  }
  if (kind === "part2") {
    document.getElementById("part2-cue").textContent = t.cue || "";
  }
}

function setQuestion(kind, idx) {
  const t = currentTask(kind);
  if (!t || !t.questions) return;
  state[kind].qIdx = idx;
  const q = t.questions[idx] || "";
  document.getElementById(`${kind}-current`).textContent = `▶ 现在回答:${q}`;
  document.querySelectorAll(`#${kind}-questions li`).forEach((li, i) =>
    li.style.fontWeight = i === idx ? "700" : "");
}

// ---- 录音 ----
async function startRecording(kind) {
  if (state[kind].recorder && state[kind].recorder.state === "recording") return;
  let stream;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (e) {
    document.getElementById(`${kind}-status`).textContent = `麦克风被拒绝: ${e.message || e}`;
    return;
  }
  const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
    ? "audio/webm;codecs=opus"
    : "audio/webm";
  const rec = new MediaRecorder(stream, { mimeType });
  state[kind].chunks = [];
  rec.addEventListener("dataavailable", (e) => {
    if (e.data && e.data.size > 0) state[kind].chunks.push(e.data);
  });
  rec.addEventListener("stop", () => {
    stream.getTracks().forEach((tr) => tr.stop());
    const blob = new Blob(state[kind].chunks, { type: mimeType });
    handleRecordingDone(kind, blob);
  });
  rec.start();
  state[kind].recorder = rec;
  state[kind].startTs = Date.now();
  document.getElementById(`${kind}-recorder`).classList.add("recording");
  document.getElementById(`${kind}-rec`).classList.add("recording");
  document.getElementById(`${kind}-rec`).textContent = "⏹";
  document.getElementById(`${kind}-status`).textContent = "录音中…再点按钮结束";
  state[kind].timerId = setInterval(() => {
    const sec = (Date.now() - state[kind].startTs) / 1000;
    document.getElementById(`${kind}-timer`).textContent = fmtTime(sec);
  }, 200);
}

function stopRecording(kind) {
  const rec = state[kind].recorder;
  if (!rec || rec.state !== "recording") return;
  rec.stop();
  clearInterval(state[kind].timerId);
  document.getElementById(`${kind}-recorder`).classList.remove("recording");
  document.getElementById(`${kind}-rec`).classList.remove("recording");
  document.getElementById(`${kind}-rec`).textContent = "🎙️";
  document.getElementById(`${kind}-status`).textContent = "转写中(本地 whisper)…";
}

async function handleRecordingDone(kind, blob) {
  const statusEl = document.getElementById(`${kind}-status`);
  const transEl = document.getElementById(`${kind}-transcript`);
  const transText = document.getElementById(`${kind}-transcript-text`);
  const resultEl = document.getElementById(`${kind}-result`);

  // 1) 上传到 speaking_server.py POST /whisper
  const form = new FormData();
  form.append("audio", blob, "recording.webm");
  let transcript = "", duration = 0;
  try {
    const r = await fetch("/whisper", { method: "POST", body: form });
    if (r.status === 404) {
      resultEl.innerHTML = `<div class="banner">
        <b>找不到 /whisper 端点。</b>请用 <code>py tools/speaking_server.py</code> 启动服务(替代 python -m http.server),
        它同时提供静态文件 + 音频转写。当前 <code>start.bat</code> 也已改成启这个服务。
      </div>`;
      statusEl.textContent = "转写端点未启用";
      return;
    }
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const j = await r.json();
    if (j.error) throw new Error(j.error);
    transcript = j.transcript || "";
    duration = j.duration_sec || 0;
  } catch (e) {
    resultEl.innerHTML = `<div class="banner">转写失败:${esc(e.message || e)}</div>`;
    statusEl.textContent = "转写失败";
    return;
  }

  transEl.style.display = "block";
  transText.textContent = transcript;
  statusEl.textContent = `转写 ${duration.toFixed(1)}s 音频完成`;

  if (!transcript.trim()) {
    resultEl.innerHTML = `<div class="banner">转写文本为空(可能没检测到语音或麦克风静音)。</div>`;
    return;
  }

  // 2) DeepSeek 评分
  if (!hasKey()) {
    resultEl.innerHTML = `<div class="banner">尚未配置 DeepSeek API Key。到 <a href="settings.html">设置</a> 页填 Key 后再试。</div>`;
    return;
  }
  resultEl.innerHTML = `<div class="loading">DeepSeek 正在评分,通常 15-30 秒…</div>`;
  try {
    const t = currentTask(kind);
    const q = (kind === "part1" || kind === "part3")
      ? (t.questions || [])[state[kind].qIdx] : t.cue;
    const feedback = await askDeepSeek([
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: buildUserPrompt(kind, t.topic, q, transcript, duration) },
    ], { json: true, maxTokens: 2048, temperature: 0.3 });
    if (!feedback || !feedback.scores) throw new Error("返回结构不合规范");
    renderFeedback(resultEl, feedback);
  } catch (e) {
    resultEl.innerHTML = `<div class="banner">评分失败:${esc(e.message || e)}</div>`;
  }
}

const SYSTEM_PROMPT = `你是雅思 8 分口语 examiner。根据学生朗读/回答的转写文本,按 IELTS Speaking Band Descriptors 四项打分:
- FC(Fluency & Coherence):语流是否连贯,有无过多重复、犹豫填充词
- LR(Lexical Resource):词汇丰富度、准确性、地道搭配
- GRA(Grammatical Range & Accuracy):句式多样性、语法正确率
- PR(Pronunciation):**基于文本节奏 heuristic(转写有无明显重复/断句/单词层面不完整),精评仍需真人**,给个参考分即可
- overall:综合分(可取 0.5 精度)

给出短评 note(全中文,一句话讲这一项弱在哪 / 强在哪),再给出 3-5 条具体改进建议 tips。

输出严格 JSON(不要 markdown 代码块):
{
  "scores": {"FC": 6.5, "LR": 6.0, "GRA": 6.0, "PR": 6.0, "overall": 6.0},
  "notes": {"FC": "…", "LR": "…", "GRA": "…", "PR": "…"},
  "tips": ["…", "…", "…"],
  "summary": "全中文一句话优劣势 + 一句下一步建议"
}

学生水平以 4.5-6.5 分为主。评分严格但公正。全中文 note/tips/summary。`;

function buildUserPrompt(kind, topic, question, transcript, duration) {
  const partLabel = { part1: "Part 1 常见话题", part2: "Part 2 长回答(1-2 分钟)", part3: "Part 3 深入讨论" }[kind];
  return `【题型】${partLabel} · ${topic}
【问题】${question}
【学生答语音时长】${duration.toFixed(1)} 秒
【学生回答(whisper 转写)】
${transcript}`;
}

function renderFeedback(el, fb) {
  const s = fb.scores || {};
  const n = fb.notes || {};
  const tipsHtml = (fb.tips || []).map((t) => `<div class="sp-note">${esc(t)}</div>`).join("");
  el.innerHTML = `
    <div class="score-grid">
      ${["FC", "LR", "GRA", "PR"].map((k) =>
        `<div class="score-cell"><div class="label">${k}</div><div class="val">${esc(s[k] ?? "-")}</div></div>`).join("")}
      <div class="score-cell overall"><div class="label">Overall</div><div class="val">${esc(s.overall ?? "-")}</div></div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:6px;margin:8px 0;">
      ${["FC", "LR", "GRA", "PR"].map((k) =>
        `<div class="sp-note"><b>${k}:</b> ${esc(n[k] || "-")}</div>`).join("")}
    </div>
    <h4 style="margin: 12px 0 6px;">改进建议</h4>
    ${tipsHtml}
    <h4 style="margin: 12px 0 6px;">总评</h4>
    <div class="sp-note" style="border-left-color:#ef4444;background:#fef2f2;">${esc(fb.summary || "")}</div>
  `;
}

// ---- 绑定 ----
document.querySelectorAll(".speaking-tabs .tab").forEach((btn) =>
  btn.addEventListener("click", () => {
    const kind = btn.dataset.tab;
    document.querySelectorAll(".speaking-tabs .tab").forEach((b) =>
      b.classList.toggle("active", b === btn));
    document.querySelectorAll(".sp-section").forEach((s) =>
      s.classList.toggle("hidden", s.dataset.section !== kind));
  }));

for (const kind of ["part1", "part2", "part3"]) {
  document.getElementById(`${kind}-rec`).addEventListener("click", () => {
    const rec = state[kind].recorder;
    if (rec && rec.state === "recording") stopRecording(kind);
    else startRecording(kind);
  });
}

loadTasks().catch((e) => console.error("[speaking] loadTasks failed", e));
