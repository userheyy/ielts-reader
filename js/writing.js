// 雅思写作陪练。Task 1 + Task 2 tab,DeepSeek 按 IELTS Writing Band Descriptors
// 四项打分 + 逐段改写。历史批改存 localStorage。
//
// 依赖:js/ai.js(askDeepSeek);data/writing/tasks.json(题库)。

import { askDeepSeek, hasKey } from "./ai.js?v=1";
import { renderBandPanel, promptSnippet } from "./band-descriptors.js?v=1";

// Band Descriptors 面板挂到页面顶部
const bandPanelEl = document.getElementById("band-panel");
if (bandPanelEl) renderBandPanel(bandPanelEl, "writing");

const HISTORY_KEY = "ielts_writing_history";
const HISTORY_MAX = 50;
const TARGET_WC = { task1: 150, task2: 250 };

const TASKS = { task1: [], task2: [] };

function esc(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function countWords(text) {
  const m = (text || "").match(/[A-Za-z][A-Za-z'-]*/g);
  return m ? m.length : 0;
}

// ---- 题库加载 + 选题 ----
async function loadTasks() {
  const r = await fetch("data/writing/tasks.json", { cache: "no-store" });
  const d = await r.json();
  TASKS.task1 = d.task1 || [];
  TASKS.task2 = d.task2 || [];
  fillPicker("task1");
  fillPicker("task2");
  renderTask("task1");
  renderTask("task2");
}

function fillPicker(kind) {
  const sel = document.getElementById(`${kind}-pick`);
  const diffSel = document.getElementById(`${kind}-diff`);
  const diff = diffSel ? diffSel.value : "";
  const filtered = TASKS[kind].filter((t) => !diff || t.difficulty === diff);
  sel.innerHTML = "";
  if (!filtered.length) {
    const opt = document.createElement("option");
    opt.textContent = "(该难度下暂无题目)";
    opt.disabled = true;
    sel.appendChild(opt);
    return;
  }
  // 按 source 分组(optgroup),便于识别是热身题还是剑 xx 真题
  const byGroup = {};
  for (const t of filtered) {
    const g = t.source || "其他";
    (byGroup[g] = byGroup[g] || []).push(t);
  }
  for (const [group, arr] of Object.entries(byGroup)) {
    const og = document.createElement("optgroup");
    og.label = group;
    for (const t of arr) {
      const opt = document.createElement("option");
      opt.value = t.id;
      const diffTag = t.difficulty ? `[${t.difficulty}] ` : "";
      const typeTag = (t.type || t.topic || "").toUpperCase();
      opt.textContent = `${diffTag}${typeTag}`;
      og.appendChild(opt);
    }
    sel.appendChild(og);
  }
  if (!sel._pickBound) {
    sel.addEventListener("change", () => renderTask(kind));
    sel._pickBound = true;
  }
  if (diffSel && !diffSel._diffBound) {
    diffSel.addEventListener("change", () => { fillPicker(kind); renderTask(kind); });
    diffSel._diffBound = true;
  }
}

function currentTask(kind) {
  const id = document.getElementById(`${kind}-pick`).value;
  return TASKS[kind].find((t) => t.id === id) || TASKS[kind][0];
}

function renderTask(kind) {
  const t = currentTask(kind);
  if (!t) return;
  document.getElementById(`${kind}-prompt`).textContent = t.prompt || "";
  const hintEl = document.getElementById(`${kind}-hint`);
  hintEl.innerHTML = t.image_hint
    ? `<b>📊 数据要点(该真题原为图表,这里以文字描述数据代替,请按此写作):</b><br>${esc(t.image_hint)}`
    : "";
  // 切换选题时清空作文和结果,避免混淆
  document.getElementById(`${kind}-essay`).value = "";
  document.getElementById(`${kind}-result`).innerHTML = "";
  updateWc(kind);
}

// ---- 字数实时计数 ----
function updateWc(kind) {
  const text = document.getElementById(`${kind}-essay`).value;
  const wc = countWords(text);
  const target = TARGET_WC[kind];
  const el = document.getElementById(`${kind}-wc`);
  el.textContent = `${wc} words / 目标 ≥ ${target}`;
  el.classList.toggle("ok", wc >= target);
}

// ---- 批改 ----
const SYSTEM_PROMPT = promptSnippet("writing") + `

你是雅思 8 分 IELTS Writing examiner。给学生的作文按 IELTS Writing Band Descriptors 打分(严格对齐上面的锚点):
- TR(Task Response / Task Achievement):对题目要求的回应程度、观点清晰度、论据充分性
- CC(Coherence & Cohesion):段落结构、逻辑衔接、指代与替换手段
- LR(Lexical Resource):词汇丰富度、准确性、地道搭配
- GRA(Grammatical Range & Accuracy):句式多样性、语法正确率
- overall:综合分(可取 0.5 精度)

对每段给出 rewrite 建议:保留原意但语言升级到 6.5-7 分水准,并用一句话中文说明改动重点。

输出严格 JSON(不要 markdown 代码块):
{
  "scores": {"TR": 6.5, "CC": 6.0, "LR": 6.5, "GRA": 6.0, "overall": 6.5},
  "rewrite": [
    {"para": 1, "original": "…原段落…", "improved": "…改写…", "note": "中文说明改了什么"},
    …
  ],
  "summary": "一句话优劣势 + 一句下一步建议(全中文)"
}

评分要严格但公正。学生英文水平以 4.5-6.5 分为主。全中文 note/summary。`;

function buildUserPrompt(task, kind, essay) {
  const taskType = kind === "task1" ? `Task 1 · ${task.type || ""}` : `Task 2 · ${task.topic || ""}`;
  const parts = [`【题型】${taskType}`, `【题干】${task.prompt}`];
  if (task.image_hint) parts.push(`【图表数据要点】${task.image_hint}`);
  parts.push(`【学生作文】\n${essay}`);
  return parts.join("\n\n");
}

async function submitEssay(kind) {
  const t = currentTask(kind);
  const essay = document.getElementById(`${kind}-essay`).value.trim();
  const resultEl = document.getElementById(`${kind}-result`);
  const btn = document.getElementById(`${kind}-submit`);

  if (!essay) {
    resultEl.innerHTML = `<div class="banner">作文为空,请先写点内容再提交。</div>`;
    return;
  }
  if (!hasKey()) {
    resultEl.innerHTML = `<div class="banner">尚未配置 DeepSeek API Key。到 <a href="settings.html">设置</a> 页填入 Key 后再来。</div>`;
    return;
  }

  btn.disabled = true;
  btn.textContent = "批改中…";
  resultEl.innerHTML = `<div class="loading">DeepSeek 正在给你打分和改写,通常 20-40 秒…</div>`;

  try {
    const feedback = await askDeepSeek(
      [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: buildUserPrompt(t, kind, essay) },
      ],
      { json: true, maxTokens: 4096, temperature: 0.3 },
    );
    if (!feedback || typeof feedback !== "object" || !feedback.scores) {
      throw new Error("返回结果结构不合规范");
    }
    renderFeedback(resultEl, feedback);
    saveHistory({
      kind, taskId: t.id, taskSource: t.source, essay, feedback,
      at: new Date().toISOString(),
    });
    renderHistory();
  } catch (e) {
    resultEl.innerHTML = `<div class="banner">批改失败:${esc(e.message || e)}</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "提交批改";
  }
}

function renderFeedback(el, fb) {
  const s = fb.scores || {};
  const rewriteHtml = (fb.rewrite || []).map((r) => `
    <div class="rewrite-item">
      <div class="role">段 ${r.para || "?"}</div>
      ${r.original ? `<div class="orig">${esc(r.original)}</div>` : ""}
      <div class="imp">${esc(r.improved || "")}</div>
      ${r.note ? `<div class="note">${esc(r.note)}</div>` : ""}
    </div>`).join("");
  el.innerHTML = `
    <div class="score-grid">
      ${["TR", "CC", "LR", "GRA"].map((k) =>
        `<div class="score-cell"><div class="label">${k}</div><div class="val">${esc(s[k] ?? "-")}</div></div>`).join("")}
      <div class="score-cell overall"><div class="label">Overall</div><div class="val">${esc(s.overall ?? "-")}</div></div>
    </div>
    <h4 style="margin: 12px 0 6px;">逐段改写建议</h4>
    ${rewriteHtml || `<div class="loading">(无改写建议)</div>`}
    <h4 style="margin: 16px 0 6px;">总评</h4>
    <div class="summary-box">${esc(fb.summary || "")}</div>
  `;
}

// ---- 历史记录(localStorage) ----
function loadHistory() {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]"); } catch { return []; }
}
function saveHistory(entry) {
  const list = loadHistory();
  list.unshift(entry);
  if (list.length > HISTORY_MAX) list.length = HISTORY_MAX;
  localStorage.setItem(HISTORY_KEY, JSON.stringify(list));
}
function renderHistory() {
  const el = document.getElementById("history-list");
  const list = loadHistory();
  if (!list.length) { el.innerHTML = `<div class="loading">暂无历史。第一次批改后会存这里。</div>`; return; }
  el.innerHTML = list.map((h, i) => {
    const date = h.at ? h.at.slice(0, 16).replace("T", " ") : "";
    const overall = h.feedback?.scores?.overall ?? "-";
    return `<div class="history-item">
      <div class="meta"><b>[${h.kind === "task1" ? "T1" : "T2"} · ${overall}]</b> ${esc(h.taskSource)} · ${date}</div>
      <button data-idx="${i}" class="show-history">查看</button>
    </div>`;
  }).join("");
  el.querySelectorAll(".show-history").forEach((b) => b.addEventListener("click", (ev) => {
    const i = Number(ev.target.dataset.idx);
    const h = loadHistory()[i];
    if (!h) return;
    const kind = h.kind;
    // 恢复到对应 tab
    activateTab(kind);
    // 恢复作文和结果
    // 找到对应 task 并选中
    const sel = document.getElementById(`${kind}-pick`);
    if (sel && [...sel.options].some((o) => o.value === h.taskId)) {
      sel.value = h.taskId;
      renderTask(kind);
    }
    document.getElementById(`${kind}-essay`).value = h.essay || "";
    updateWc(kind);
    renderFeedback(document.getElementById(`${kind}-result`), h.feedback);
    document.getElementById(`${kind}-result`).scrollIntoView({ behavior: "smooth", block: "start" });
  }));
}

// ---- Tab 切换 ----
function activateTab(kind) {
  document.querySelectorAll(".writing-tabs .tab").forEach((b) =>
    b.classList.toggle("active", b.dataset.tab === kind));
  document.querySelectorAll(".task-section").forEach((s) =>
    s.classList.toggle("hidden", s.dataset.section !== kind));
}

// ---- 绑定 ----
document.querySelectorAll(".writing-tabs .tab").forEach((btn) =>
  btn.addEventListener("click", () => activateTab(btn.dataset.tab)));

for (const kind of ["task1", "task2"]) {
  document.getElementById(`${kind}-essay`).addEventListener("input", () => updateWc(kind));
  document.getElementById(`${kind}-submit`).addEventListener("click", () => submitEssay(kind));
}

loadTasks().then(renderHistory).catch((e) => {
  console.error("[writing] loadTasks failed", e);
});
