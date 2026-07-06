// 听力精听页。三种形态:
//   listening.html                    → 落地页:读 data/listening/index.json 渲染测试卡列表
//   listening.html?id=xxx             → 三栏精听:逐句转写(遮罩揭示)/ 题目 / 播放器+听写
//   listening.html?id=xxx&annotate=1  → 打点模式:边听边给每句记 start 时间,可导出 JSON
// 四条降级路径:①无 id → 落地页;②part 数据缺失 → 提示卡+回落地页;
// ③音频 404 → 提示卡,转写/做题当文本精读用;④句子未打点(start 全 null)→ 顺序列表模式。
import { scoreDictation } from "./dictation.js?v=1";
import { has as wordStoreHas } from "./store.js";
import { openWordPopup } from "./word-popup.js?v=1";

const params = new URLSearchParams(location.search);
const partId = params.get("id");
const ANNOTATE = params.get("annotate") === "1";

const noticeEl = document.getElementById("notice");
const landingEl = document.getElementById("landing");
const landingListEl = document.getElementById("landing-list");
const viewEl = document.getElementById("player-view");
const srcEl = document.getElementById("lsn-src");
const annotateLinkEl = document.getElementById("annotate-link");
const transcriptEl = document.getElementById("transcript");
const questionsEl = document.getElementById("lsn-questions");
const sideEl = document.getElementById("lsn-side");
const playerBarEl = document.getElementById("lsn-player-bar");

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function fmtTime(t) {
  if (t == null || !isFinite(t)) return "--:--";
  const m = Math.floor(t / 60);
  const s = Math.floor(t % 60);
  return m + ":" + String(s).padStart(2, "0");
}

function notice(html, type = "warn") {
  const div = document.createElement("div");
  div.className = "lsn-note" + (type === "err" ? " err" : "");
  div.innerHTML = html;
  noticeEl.appendChild(div);
  return div;
}

// ============================================================
// 落地页
// ============================================================
async function renderLanding() {
  landingEl.hidden = false;
  let idx;
  try {
    const res = await fetch("data/listening/index.json", { cache: "no-store" });
    if (!res.ok) throw new Error();
    idx = await res.json();
  } catch {
    notice("无法加载 <code>data/listening/index.json</code>。请通过 start.bat 启动本地服务器后再试。", "err");
    return;
  }
  const tests = idx.tests || [];
  if (!tests.length) {
    notice("听力库还没有测试数据。");
    return;
  }
  landingListEl.innerHTML = tests.map((t) => `
    <section class="book-group">
      <div class="book-head"><h2>${esc(t.source || t.id)}</h2><span class="book-note">逐句精听 · 听写 · 真题演练</span></div>
      <div class="card-grid">
        ${(t.parts || []).map((p) => `
          <a class="card" href="listening.html?id=${encodeURIComponent(p.id)}">
            <div class="src">Part ${esc(p.part)} · 第 ${esc(p.question_range || "")} 题</div>
            <div class="title">${esc(p.title || "Part " + p.part)}</div>
            <div class="count lsn-card-foot">
              <span>精听 / 听写 / 做题</span>
            </div>
          </a>`).join("")}
      </div>
    </section>`).join("");
  // 卡片右下角的「打点」是卡片(<a>)里的小入口,单独拦截跳转
  landingListEl.addEventListener("click", (ev) => {
    const ann = ev.target.closest(".lsn-ann");
    if (ann) {
      ev.preventDefault();
      location.href = ann.dataset.ann;
    }
  });
}

// ============================================================
// 精听页状态
// ============================================================
let PART = null;
let segs = [];          // 全部句子(契约顺序)
let timed = [];         // 有 start 的句子,按 start 升序
let allItems = [];      // 拍平的所有题目 item
let revealed = new Set();     // 兼容别名:hintLevels[sid] >= 3 时 revealed.has(sid) === true
                              // 保留供 dictation / jumpToSegment 等旧逻辑用
let hintLevels = new Map();   // sid → 0|1|2|3|4:每句的渐进提示级数(N2)
                              // 0=锁定 / 1=首字母 / 2=前5词+首字母 / 3=完整英文 / 4=完整英文+中文
let followScroll = true;      // 列表是否跟随播放

let audio = null;
let audioFailed = false;
let duration = NaN;
let seekDragging = false;

let mode = "normal";    // normal | sentence | ab | dictation
let repeatN = 2;        // 单句循环次数(1-5)
let repeatDone = 0;
let loopIdx = -1;       // sentence 模式正在循环的 timed 下标
let abA = null;
let abB = null;
let dictEndTime = null; // 听写模式:播完本句自动停的时间点
let curTimedIdx = -1;   // 当前播放到的 timed 下标
let curSegId = null;    // 当前播放句的 id(用于渲染高亮)

// 听写状态(进度按句存 localStorage)
const DICT_KEY = "ielts_dict:" + partId;
let dictIdx = 0;
let dictBest = {};      // segId → 最好成绩(percent)

// 打点状态
let annStarts = [];     // 每句的已打时间(秒,1 位小数)或 null,下标对齐 segs
let annIdx = 0;         // 当前待打点句(segs 下标),依次推进
let annLast = -1;       // 最近一次打点的下标(±0.2s 微调对象)

// ============================================================
// 数据加载
// ============================================================
async function renderPart(id) {
  let d;
  try {
    const res = await fetch(`data/listening/${id}.json`, { cache: "no-store" });
    if (!res.ok) throw new Error();
    d = await res.json();
  } catch {
    notice(`这一篇(<b>${esc(id)}</b>)的转写数据还没录入。数据文件应在 ` +
      `<code>data/listening/${esc(id)}.json</code>,录好后刷新本页即可。下面是已有的听力列表:`);
    renderLanding();
    return;
  }
  PART = d;
  segs = Array.isArray(d.segments) ? d.segments : [];
  timed = segs.filter((s) => typeof s.start === "number").slice().sort((a, b) => a.start - b.start);
  allItems = [];
  for (const g of d.questions || []) {
    for (const it of g.items || []) allItems.push(it);
  }

  viewEl.hidden = false;
  srcEl.textContent = `${d.source || ""}${d.title ? " — " + d.title : ""}`;
  document.title = (d.title || id) + " · 听力精听";
  // 打点入口只在 ?annotate=1 时可见(N4:普通用户看不到)
  if (ANNOTATE) {
    annotateLinkEl.hidden = false;
    annotateLinkEl.textContent = "退出打点";
    annotateLinkEl.href = `listening.html?id=${encodeURIComponent(id)}`;
    annStarts = segs.map((s) => (typeof s.start === "number" ? s.start : null));
    annIdx = annStarts.indexOf(null);
    if (annIdx < 0) annIdx = 0; // 全部已打 → 从头开始重打
  } else {
    annotateLinkEl.hidden = true;
  }

  loadDictProgress();
  initAudio();
  renderTranscript();
  renderQuestions(d.questions);
  renderSide();
  bindKeyboard();
}

// ============================================================
// 播放器
// ============================================================
function initAudio() {
  if (!PART.audio) { showAudioMissing(); return; }
  audio = new Audio(PART.audio);
  audio.preload = "metadata";
  audio.addEventListener("error", () => {
    audioFailed = true;
    showAudioMissing();
    refreshPlayBtn();
    if (ANNOTATE) refreshAnnPanel(); // 让打点按钮从"启用"变"disabled"
  });
  audio.addEventListener("loadedmetadata", () => {
    duration = audio.duration;
    const durEl = document.getElementById("pl-dur");
    const seek = document.getElementById("pl-seek");
    if (durEl) durEl.textContent = fmtTime(duration);
    if (seek) seek.max = duration;
  });
  audio.addEventListener("timeupdate", onTick);
  audio.addEventListener("play", () => { refreshPlayBtn(); if (ANNOTATE) refreshAnnPanel(); });
  audio.addEventListener("pause", () => { refreshPlayBtn(); if (ANNOTATE) refreshAnnPanel(); });
  audio.addEventListener("ended", refreshPlayBtn);
}

function showAudioMissing() {
  if (document.getElementById("audio-missing-note")) return;
  const n = notice(`未找到音频文件。请把对应 mp3 命名为 <code>${esc(PART.audio || "media/audio/….mp3")}</code> ` +
    `放入项目后刷新本页。在此之前,转写和题目仍可当<b>文本精读</b>用:揭示句子、看同义替换、做题核对都不需要音频。`, "err");
  n.id = "audio-missing-note";
}

function canPlay() { return !!audio && !audioFailed; }

function togglePlay() {
  if (!canPlay()) return;
  if (audio.paused) audio.play();
  else audio.pause();
}

function refreshPlayBtn() {
  const btn = document.getElementById("pl-toggle");
  if (!btn) return;
  if (!canPlay()) {
    btn.disabled = true;
    btn.textContent = "音频缺失";
    return;
  }
  btn.textContent = audio.paused ? "▶ 播放" : "⏸ 暂停";
}

// 二分查当前句:timed 里最后一个 start ≤ t 的下标;没有则 -1
function findTimedIndex(t) {
  let lo = 0, hi = timed.length - 1, ans = -1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (timed[mid].start <= t + 0.05) { ans = mid; lo = mid + 1; }
    else hi = mid - 1;
  }
  return ans;
}

function segEnd(ti) {
  if (ti < 0) return Infinity;
  return ti + 1 < timed.length ? timed[ti + 1].start : (isFinite(duration) ? duration : Infinity);
}

function timedIndexOfSeg(s) {
  return timed.findIndex((x) => x.id === s.id);
}

function onTick() {
  const t = audio.currentTime;
  const curEl = document.getElementById("pl-cur");
  const seek = document.getElementById("pl-seek");
  if (curEl) curEl.textContent = fmtTime(t);
  if (seek && !seekDragging) seek.value = t;
  if (ANNOTATE) return; // 打点模式不做跟随/循环

  // 各模式的边界回跳
  if (mode === "sentence" && loopIdx >= 0) {
    if (t >= segEnd(loopIdx) - 0.02) {
      repeatDone += 1;
      if (repeatDone < repeatN) {
        audio.currentTime = timed[loopIdx].start;
      } else if (loopIdx + 1 < timed.length) {
        loopIdx += 1;
        repeatDone = 0;
        audio.currentTime = timed[loopIdx].start;
        refreshModePanel();
      } else {
        audio.pause();
      }
    }
  } else if (mode === "ab" && abA != null && abB != null) {
    if (t >= abB - 0.02) audio.currentTime = abA;
  } else if (dictEndTime != null) {
    // normal / dictation:playSegment 设了 dictEndTime,到时间自动 pause,不流到下句
    if (t >= dictEndTime - 0.02) {
      audio.pause();
      dictEndTime = null;
      if (mode === "dictation") {
        const inp = document.getElementById("dict-input");
        if (inp) inp.focus();
      }
    }
  }

  // 列表高亮跟随
  const ti = findTimedIndex(t);
  if (ti !== curTimedIdx) {
    curTimedIdx = ti;
    setPlayingSeg(ti >= 0 ? timed[ti].id : null);
  }
}

function setPlayingSeg(segId) {
  if (curSegId === segId) return;
  const prev = curSegId;
  curSegId = segId;
  if (prev != null) {
    const el = transcriptEl.querySelector(`.seg[data-sid="${prev}"]`);
    if (el) el.classList.remove("playing");
  }
  if (segId != null) {
    const el = transcriptEl.querySelector(`.seg[data-sid="${segId}"]`);
    if (el) {
      el.classList.add("playing");
      if (followScroll && mode !== "dictation") el.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }
}

// 跳播某句。默认播完本句自动暂停(用户预期"点哪句只播那句,不往下流")。
// 例外:sentence 模式由自己的循环边界 handle;ab 模式在 [A,B] 内循环。
function playSegment(s, forDictation = false) {
  if (!canPlay() || !s || typeof s.start !== "number") return false;
  const ti = timedIndexOfSeg(s);
  if (mode === "sentence" && !forDictation) { loopIdx = ti; repeatDone = 0; refreshModePanel(); }
  // sentence / ab 由 onTick 里的 mode 分支自己 handle 边界,dictEndTime 保持 null
  if (mode === "sentence" || mode === "ab") dictEndTime = null;
  else dictEndTime = segEnd(ti); // normal / dictation:播完该句自动 pause
  audio.currentTime = s.start;
  audio.play();
  return true;
}

function stepSentence(d) {
  if (!timed.length || !canPlay()) return;
  let i = curTimedIdx < 0 ? 0 : curTimedIdx + d;
  i = Math.max(0, Math.min(timed.length - 1, i));
  playSegment(timed[i]);
}

function repeatCurrent() {
  if (curTimedIdx >= 0) playSegment(timed[curTimedIdx]);
}

// ============================================================
// 左栏:逐句转写
// ============================================================
// 收集会命中该句的题目(按 evidence_segment 或 segment.answers 关联)
function itemsForSeg(s) {
  const ans = Array.isArray(s.answers) ? s.answers : [];
  return allItems.filter((it) => it.evidence_segment === s.id || ans.includes(it.number));
}

// 在 text 里找出若干 needle 的首次命中区间(忽略大小写,去重叠)
function findRanges(text, needles) {
  const lower = text.toLowerCase();
  const out = [];
  for (const nd of needles) {
    const f = String(nd.find || "").toLowerCase();
    if (!f) continue;
    const i = lower.indexOf(f);
    if (i >= 0) out.push({ ...nd, a: i, b: i + f.length });
  }
  out.sort((x, y) => x.a - y.a || y.b - x.b);
  const res = [];
  for (const r of out) {
    if (!res.length || r.a >= res[res.length - 1].b) res.push(r);
  }
  return res;
}

// 给一段纯文本包生词气泡(点击可弹 word-popup 入生词库)
function wrapWords(text, words) {
  if (!text) return "";
  if (!Array.isArray(words) || !words.length) return esc(text);
  const needles = words.map((w) => ({
    find: w.w,
    title: `${w.pos ? w.pos + " " : ""}${w.def || ""}`.trim(),
    word: w.w,
    pos: w.pos || "",
    def: w.def || "",
    cls: "wtip",
  }));
  const ranges = findRanges(text, needles);
  let html = "";
  let pos = 0;
  for (const r of ranges) {
    html += esc(text.slice(pos, r.a));
    const savedCls = wordSavedInStore(r.word) ? " saved" : "";
    html += `<span class="wtip${savedCls}" title="${esc(r.title)}" data-word="${esc(r.word || "")}" data-pos="${esc(r.pos || "")}" data-def="${esc(r.def || "")}">${esc(text.slice(r.a, r.b))}</span>`;
    pos = r.b;
  }
  return html + esc(text.slice(pos));
}

function wordSavedInStore(w) {
  try { return !!(w && wordStoreHas(w)); } catch { return false; }
}

// 句子英文 HTML:同义替换(paraphrase.p)波浪线在外层,生词气泡在内层
function renderEnHTML(s) {
  const paraNeedles = [];
  for (const it of itemsForSeg(s)) {
    for (const pair of (it.paraphrase && it.paraphrase.pairs) || []) {
      if (!pair || !pair.p) continue;
      paraNeedles.push({
        find: pair.p,
        title: `第${it.number}题:${pair.q} ⇄ ${pair.p}${pair.note ? "(" + pair.note + ")" : ""}`,
      });
    }
  }
  const pr = findRanges(s.en, paraNeedles);
  let html = "";
  let pos = 0;
  for (const r of pr) {
    html += wrapWords(s.en.slice(pos, r.a), s.words);
    html += `<span class="para-hl" title="${esc(r.title)}">${wrapWords(s.en.slice(r.a, r.b), s.words)}</span>`;
    pos = r.b;
  }
  return html + wrapWords(s.en.slice(pos), s.words);
}

// 首字母模板:把英文文本变成 "T__ p___" 形式(前 keepFirstN 个词完整,其余打码)
// 标点保留原样,数字保留原样;字母词按 "首字母 + 剩余长度个 _" 打码。
function maskEn(en, keepFirstN) {
  const parts = String(en || "").split(/([A-Za-z][A-Za-z'\-]*)/);
  let wordCount = 0;
  return parts.map((tok) => {
    if (!/^[A-Za-z]/.test(tok)) return tok;
    wordCount++;
    if (wordCount <= keepFirstN) return tok;
    const rest = Math.max(1, tok.replace(/['\-]/g, "").length - 1);
    return tok[0] + "_".repeat(rest);
  }).join("");
}

function segRowHTML(s) {
  const i = segs.indexOf(s);
  if (ANNOTATE) {
    const st = annStarts[i];
    const tHtml = st != null
      ? `<span class="seg-time">${fmtTime(st)}(${st.toFixed(1)}s)</span>`
      : `<span class="seg-time unset">未打点</span>`;
    return `<div class="seg ann${i === annIdx ? " ann-cur" : ""}" data-sid="${s.id}">
      <div class="seg-meta"><span class="seg-no">${s.id}</span>${tHtml}
        ${s.speaker ? `<span class="seg-spk">${esc(s.speaker)}</span>` : ""}</div>
      <div class="seg-en">${esc(s.en)}</div>
      <div class="seg-zh">${esc(s.zh || "")}</div>
    </div>`;
  }
  const t = typeof s.start === "number" ? fmtTime(s.start) : "--:--";
  const ansBadge = Array.isArray(s.answers) && s.answers.length
    ? `<span class="seg-ans">题${s.answers.join(",")}</span>` : "";
  const playing = s.id === curSegId ? " playing" : "";
  const level = hintLevels.get(s.id) || 0;

  // Level 0:锁定,只显示句号 + 时间 + 提示按钮
  if (level === 0) {
    return `<div class="seg locked${playing}" data-sid="${s.id}">
      <span class="seg-no">${s.id}</span><span class="seg-time">${t}</span>
      <span class="seg-lock">🔒 点击提示 + 跳播</span>${ansBadge}
    </div>`;
  }

  // Level 1-4:根据 level 决定英文渲染 + 是否显示中文
  let enHtml;
  if (level === 1) {
    enHtml = esc(maskEn(s.en, 0));                              // 全首字母
  } else if (level === 2) {
    enHtml = esc(maskEn(s.en, 5));                              // 前 5 词 + 首字母
  } else {
    enHtml = renderEnHTML(s);                                    // Level 3/4:完整英文(带 wtip + para-hl)
  }
  const showZh = level >= 4;

  const nextTip = level < 4
    ? `<span class="seg-hint-lv">💡 提示 ${level}/4 · 再点${["", "关键词", "完整英文", "中文", ""][level]}</span>`
    : `<span class="seg-hint-lv">✓ 全部揭示 · 再点跳播</span>`;

  return `<div class="seg open lv${level}${playing}" data-sid="${s.id}">
    <div class="seg-meta"><span class="seg-no">${s.id}</span><span class="seg-time">${t}</span>
      ${s.speaker ? `<span class="seg-spk">${esc(s.speaker)}</span>` : ""}${ansBadge}
      ${nextTip}</div>
    <div class="seg-en">${enHtml}</div>
    ${showZh ? `<div class="seg-zh">${esc(s.zh || "")}</div>` : ""}
  </div>`;
}

function renderTranscript() {
  if (!segs.length) {
    transcriptEl.innerHTML = '<p style="color:var(--muted)">这一篇没有句子数据。</p>';
    return;
  }
  const bar = ANNOTATE
    ? `<div class="tr-bar"><span>打点模式:点句可选中重打(共 ${segs.length} 句)</span></div>`
    : `<div class="tr-bar">
        <span>逐句转写 · 共 ${segs.length} 句</span>
        <span>
          <label class="tr-follow"><input type="checkbox" id="tr-follow" ${followScroll ? "checked" : ""}>跟随播放</label>
          <button type="button" id="tr-all">${allFullyRevealed() ? "全部收起" : "全部揭示"}</button>
        </span>
      </div>`;
  transcriptEl.innerHTML = bar + segs.map(segRowHTML).join("");
}

function rerenderRow(sid) {
  const el = transcriptEl.querySelector(`.seg[data-sid="${sid}"]`);
  const s = segs.find((x) => x.id === sid);
  if (!el || !s) return;
  const tmp = document.createElement("div");
  tmp.innerHTML = segRowHTML(s);
  el.replaceWith(tmp.firstElementChild);
}

function jumpToSegment(sid) {
  // 从题目跳过来 → 直接推到 Level 4(完整英文 + 中文)方便看答案
  if (!ANNOTATE) {
    const cur = hintLevels.get(sid) || 0;
    if (cur < 4) {
      hintLevels.set(sid, 4);
      revealed.add(sid);
      rerenderRow(sid);
      refreshTrAllBtn();
    }
  }
  const row = transcriptEl.querySelector(`.seg[data-sid="${sid}"]`);
  if (!row) return;
  row.scrollIntoView({ behavior: "smooth", block: "center" });
  row.classList.remove("pulse");
  requestAnimationFrame(() => row.classList.add("pulse"));
}

function allFullyRevealed() {
  return segs.length > 0 && segs.every((s) => (hintLevels.get(s.id) || 0) >= 4);
}

function refreshTrAllBtn() {
  const btn = document.getElementById("tr-all");
  if (btn) btn.textContent = allFullyRevealed() ? "全部收起" : "全部揭示";
}

transcriptEl.addEventListener("click", (ev) => {
  if (ev.target.id === "tr-all") {
    if (allFullyRevealed()) {
      hintLevels.clear();
      revealed.clear();
    } else {
      segs.forEach((s) => {
        hintLevels.set(s.id, 4);
        revealed.add(s.id);
      });
    }
    renderTranscript();
    return;
  }
  if (ev.target.id === "tr-follow") {
    followScroll = ev.target.checked;
    return;
  }
  // 点 .wtip 生词 → 弹词汇 popup 入生词库(不触发揭示/跳播);annotate 模式跳过
  if (!ANNOTATE) {
    const wtip = ev.target.closest(".wtip");
    if (wtip) {
      ev.stopPropagation();
      const parentSeg = wtip.closest(".seg");
      const s = parentSeg && segs.find((x) => x.id === Number(parentSeg.dataset.sid));
      if (s) {
        const wordText = wtip.dataset.word || wtip.textContent;
        const wordDefs = new Map(
          (s.words || []).map((w) => [w.w.toLowerCase(), w]),
        );
        openWordPopup({
          event: ev, word: wordText, wordDefs, sentence: s,
          source: PART.source, passageId: PART.id,
        });
      }
      return;
    }
  }
  const row = ev.target.closest(".seg");
  if (!row) return;
  const sid = Number(row.dataset.sid);
  const s = segs.find((x) => x.id === sid);
  if (!s) return;
  if (ANNOTATE) { // 打点模式:点句 = 选中该句为"当前待打点"(重打)
    annIdx = segs.indexOf(s);
    renderTranscript();
    refreshAnnPanel();
    return;
  }
  // N2:4 级渐进提示。每次点句:hintLevel 累加 (0→1→2→3→4) + 跳播。
  // Level ≥ 3 时同步维护 revealed set 兼容旧代码(dictation 判分等)。
  const cur = hintLevels.get(sid) || 0;
  const next = Math.min(4, cur + 1);
  hintLevels.set(sid, next);
  if (next >= 3) revealed.add(sid); else revealed.delete(sid);
  rerenderRow(sid);
  refreshTrAllBtn();
  playSegment(s);
});

// ============================================================
// 中栏:题目(填空复用 style.css 的 question-* 样式)
// ============================================================
function normalizeAnswer(v) {
  return String(v || "").trim().toLowerCase().replace(/\s+/g, " ");
}

// 标准答案支持 "a/b" 写法(任一都算对)
function answerAccepts(answer) {
  return String(answer).split("/").map(normalizeAnswer).filter(Boolean);
}

function normalizeOption(opt, i) {
  if (opt && typeof opt === "object") {
    return {
      val: String(opt.label || opt.value || String.fromCharCode(65 + i)).trim(),
      text: String(opt.text || opt.content || ""),
    };
  }
  const s = String(opt == null ? "" : opt).trim();
  const m = s.match(/^([A-H])[.)]?\s+(.+)$/);
  if (m) return { val: m[1], text: m[2] };
  return { val: String.fromCharCode(65 + i), text: s };
}

function evidenceBtnHTML(item) {
  return item.dataset.evidence
    ? ` <button type="button" class="evidence-jump" data-sid="${item.dataset.evidence}">答案句</button>`
    : "";
}

function showAnswer(item, m = "check") {
  const note = item.querySelector(".answer-note");
  const answer = item.dataset.answer || "";
  if (!answer) {
    item.classList.remove("correct", "wrong");
    item.classList.add("unanswered");
    note.textContent = "这题还没有录入标准答案。";
    return false;
  }
  const input = item.querySelector("input");
  const user = item.classList.contains("mc")
    ? normalizeAnswer(item.dataset.user || "")
    : normalizeAnswer(input ? input.value : "");
  item.classList.remove("unanswered", "answer-only");
  if (m === "reveal") {
    item.classList.remove("correct", "wrong");
    item.classList.add("answer-only");
    note.innerHTML = `答案:<strong>${esc(answer)}</strong>${evidenceBtnHTML(item)}`;
    return null;
  }
  const ok = !!user && answerAccepts(answer).includes(user);
  item.classList.toggle("correct", ok);
  item.classList.toggle("wrong", !ok);
  note.innerHTML = ok
    ? `正确 ✓${evidenceBtnHTML(item)}`
    : `${user ? "不对" : "未作答"}｜答案:<strong>${esc(answer)}</strong>${evidenceBtnHTML(item)}`;
  return ok;
}

function checkScope(scope) {
  let total = 0, correct = 0;
  scope.querySelectorAll(".question-item").forEach((item) => {
    if (!item.dataset.answer) return;
    total += 1;
    if (showAnswer(item, "check")) correct += 1;
  });
  return { total, correct };
}

function questionItemEl(group, q) {
  const item = document.createElement("div");
  const isMC = group.type === "multiple_choice" || Array.isArray(q.options);
  item.className = "question-item" + (isMC ? " mc" : "");
  item.dataset.answer = q.answer || "";
  if (q.evidence_segment != null) item.dataset.evidence = q.evidence_segment;
  const label = `<label><b>${esc(q.number)}</b><span>${esc(q.prompt || "")}</span></label>`;
  if (isMC) {
    const opts = (q.options || []).map((o, i) => {
      const { val, text } = normalizeOption(o, i);
      return `<button type="button" class="mc-opt" data-val="${esc(val)}"><b>${esc(val)}</b>${esc(text)}</button>`;
    }).join("");
    item.innerHTML = `${label}<div class="mc-opts">${opts}</div><div class="answer-note" aria-live="polite"></div>`;
  } else {
    item.innerHTML = `${label}<input type="text" autocomplete="off" aria-label="第 ${esc(q.number)} 题答案">
      <div class="answer-note" aria-live="polite"></div>`;
  }
  if (q.evidence_segment != null) {
    item.querySelector("label").addEventListener("click", () => jumpToSegment(Number(q.evidence_segment)));
  }
  return item;
}

function renderQuestions(groups) {
  questionsEl.innerHTML = `<div class="questions-title">
    <span>Questions</span>
    <div class="question-actions">
      <small id="lsn-score">先作答,再核对</small>
      <button type="button" id="lsn-check-all">核对全部</button>
      <button type="button" id="lsn-reveal-all">显示答案</button>
    </div>
  </div>`;
  if (!groups || !groups.length) {
    questionsEl.innerHTML += '<p class="question-empty">这一篇暂未录入题目。</p>';
    return;
  }
  for (const group of groups) {
    const section = document.createElement("section");
    section.className = "question-group";
    section.innerHTML = `<h2>${esc(group.title || "")}</h2>
      ${(group.instructions || []).map((l) => `<p class="instruction">${esc(l)}</p>`).join("")}`;
    for (const q of group.items || []) section.appendChild(questionItemEl(group, q));
    const check = document.createElement("button");
    check.className = "check-answers";
    check.textContent = "核对本组答案";
    check.addEventListener("click", () => {
      const { total, correct } = checkScope(section);
      const sc = document.getElementById("lsn-score");
      if (sc) sc.textContent = `本组 ${correct}/${total}`;
    });
    section.appendChild(check);
    questionsEl.appendChild(section);
  }
  questionsEl.addEventListener("click", (ev) => {
    const opt = ev.target.closest(".mc-opt");
    if (opt) { // 多选题点选
      const item = opt.closest(".question-item");
      item.dataset.user = opt.dataset.val;
      item.querySelectorAll(".mc-opt").forEach((o) => o.classList.toggle("sel", o === opt));
      return;
    }
    const evd = ev.target.closest(".evidence-jump");
    if (evd) { jumpToSegment(Number(evd.dataset.sid)); return; }
    if (ev.target.id === "lsn-check-all") {
      const { total, correct } = checkScope(questionsEl);
      document.getElementById("lsn-score").textContent = `总分 ${correct}/${total}`;
      return;
    }
    if (ev.target.id === "lsn-reveal-all") {
      const reveal = ev.target.textContent === "显示答案";
      questionsEl.querySelectorAll(".question-item").forEach((item) => {
        if (reveal) showAnswer(item, "reveal");
        else {
          item.classList.remove("correct", "wrong", "unanswered", "answer-only");
          item.querySelector(".answer-note").textContent = "";
        }
      });
      ev.target.textContent = reveal ? "隐藏答案" : "显示答案";
      document.getElementById("lsn-score").textContent = reveal ? "已显示标准答案" : "先作答,再核对";
    }
  });
}

// ============================================================
// 右栏:播放器 + 模式面板 + 听写 + 打点
// ============================================================
const SPEEDS = [0.5, 0.75, 0.9, 1, 1.25, 1.5];
const MODES = [
  ["normal", "顺序"],
  ["sentence", "单句循环"],
  ["ab", "AB复读"],
  ["dictation", "听写"],
];

function renderSide() {
  const speedChips = SPEEDS.map((v) =>
    `<button type="button" class="chip${v === 1 ? " on" : ""}" data-speed="${v}">${v}×</button>`).join("");
  const modeChips = MODES.map(([v, label]) => {
    const needTimed = v !== "normal" && v !== "dictation";
    const dis = needTimed && !timed.length ? " disabled title=\"本篇未对齐时间戳,不能按句循环\"" : "";
    return `<button type="button" class="chip${v === mode ? " on" : ""}" data-mode="${v}"${dis}>${label}</button>`;
  }).join("");
  // 播放器条(sticky top,不占用侧栏空间;annotate 时不显示模式 chip)
  playerBarEl.innerHTML = `
    <div class="pl-main">
      <button type="button" id="pl-back" title="后退 5 秒">−5s</button>
      <button type="button" id="pl-toggle" class="pl-play">▶ 播放</button>
      <button type="button" id="pl-fwd" title="前进 5 秒">+5s</button>
    </div>
    <div class="pl-time-inline">
      <span id="pl-cur">0:00</span>
      <input type="range" id="pl-seek" min="0" max="100" step="0.1" value="0" aria-label="播放进度">
      <span id="pl-dur">--:--</span>
    </div>
    <div class="pl-inline-row"><span class="pl-label">语速</span><div class="chiprow" id="pl-speeds">${speedChips}</div></div>
    ${ANNOTATE ? "" : `<div class="pl-inline-row"><span class="pl-label">模式</span><div class="chiprow" id="pl-modes">${modeChips}</div></div>`}
  `;
  // 侧栏(题目下方):模式面板 + 听写卡 +(annotate 时)打点面板
  sideEl.innerHTML = `
    ${ANNOTATE ? "" : `<div class="pl-card mode-panel-card" id="mode-panel-wrap"><div class="mode-panel" id="mode-panel"></div>
      <div class="pl-kbd">快捷键:Space 播/停 · ← → 上/下句 · R 重复本句(输入框内不生效)</div></div>`}
    ${ANNOTATE ? annPanelHTML() : ""}
    ${ANNOTATE ? `<div class="pl-card"><div class="pl-kbd">快捷键:Space 给当前句打点 · P 播/停</div></div>` : ""}
    <div class="pl-card dict-card" id="dict-panel" hidden></div>`;

  // 事件监听器:播放器条上的点击(seek/speed/mode)+ 侧栏点击(模式面板 detail)
  playerBarEl.addEventListener("click", onSideClick);
  sideEl.addEventListener("click", onSideClick);
  const seek = document.getElementById("pl-seek");
  seek.addEventListener("input", () => {
    if (!canPlay()) return;
    seekDragging = true;
    audio.currentTime = Number(seek.value);
  });
  seek.addEventListener("change", () => { seekDragging = false; });
  if (isFinite(duration)) {
    document.getElementById("pl-dur").textContent = fmtTime(duration);
    seek.max = duration;
  }
  refreshPlayBtn();
  if (!ANNOTATE) refreshModePanel();
  else refreshAnnPanel();
}

function onSideClick(ev) {
  const t = ev.target;
  if (t.id === "pl-toggle") { togglePlay(); return; }
  if (t.id === "pl-back" || t.id === "pl-fwd") {
    if (canPlay()) audio.currentTime = Math.max(0, audio.currentTime + (t.id === "pl-back" ? -5 : 5));
    return;
  }
  if (t.dataset.speed) {
    if (audio) audio.playbackRate = Number(t.dataset.speed);
    document.querySelectorAll("#pl-speeds .chip").forEach((c) => c.classList.toggle("on", c === t));
    return;
  }
  if (t.dataset.mode) { switchMode(t.dataset.mode); return; }
  if (t.id === "rep-count") return; // select 交给 change
  // 模式面板里的按钮
  if (t.id === "ab-mark") { abMark(); return; }
  if (t.id === "ab-clear") { abA = null; abB = null; refreshModePanel(); return; }
  // 听写
  if (t.id === "dict-play") { playSegment(segs[dictIdx], true); return; }
  if (t.id === "dict-prev") { dictGo(dictIdx - 1); return; }
  if (t.id === "dict-next") { dictGo(dictIdx + 1); return; }
  // 打点
  if (t.id === "ann-mark") { annMark(); return; }
  if (t.id === "ann-minus") { annAdjust(-0.2); return; }
  if (t.id === "ann-plus") { annAdjust(0.2); return; }
  if (t.id === "ann-export") { annExport(); return; }
}

function switchMode(m) {
  mode = m;
  loopIdx = -1;
  repeatDone = 0;
  dictEndTime = null;
  document.querySelectorAll("#pl-modes .chip").forEach((c) =>
    c.classList.toggle("on", c.dataset.mode === m));
  if (m === "sentence" && timed.length) {
    loopIdx = curTimedIdx >= 0 ? curTimedIdx : 0;
  }
  const dictPanel = document.getElementById("dict-panel");
  if (dictPanel) {
    dictPanel.hidden = m !== "dictation";
    if (m === "dictation") renderDictPanel();
  }
  refreshModePanel();
}

function refreshModePanel() {
  const panel = document.getElementById("mode-panel");
  if (!panel) return;
  if (mode === "normal") {
    panel.innerHTML = '<div class="hint">顺序播放。点击左侧已揭示的句子可跳播。</div>';
  } else if (mode === "sentence") {
    const opts = [1, 2, 3, 4, 5].map((n) =>
      `<option value="${n}"${n === repeatN ? " selected" : ""}>${n} 次</option>`).join("");
    const cur = loopIdx >= 0 ? `当前循环第 <b>${timed[loopIdx].id}</b> 句` : "点左侧句子开始循环";
    panel.innerHTML = `每句重复 <select id="rep-count">${opts}</select> 遍后自动进下一句 · ${cur}
      <div class="hint">播完设定遍数自动切到下一句继续循环,适合逐句磨耳朵。</div>`;
    panel.querySelector("#rep-count").addEventListener("change", (e) => {
      repeatN = Number(e.target.value);
      repeatDone = 0;
    });
  } else if (mode === "ab") {
    const a = abA != null ? fmtTime(abA) : "未标";
    const b = abB != null ? fmtTime(abB) : "未标";
    const next = abA == null ? "标记 A 点" : (abB == null ? "标记 B 点" : "重新标 A 点");
    panel.innerHTML = `<span class="ab-times">A:${a} · B:${b}</span>
      <div class="ann-btns" style="margin-top:6px">
        <button type="button" id="ab-mark">${next}</button>
        <button type="button" id="ab-clear">清除</button>
      </div>
      <div class="hint">播放中点两次按钮分别标 A、B 点,到 B 点自动跳回 A 点循环。</div>`;
  } else if (mode === "dictation") {
    panel.innerHTML = '<div class="hint">听写模式:在下方卡片逐句「播放→默写→回车判分」,≥90 分自动进下一句。</div>';
  }
}

function abMark() {
  if (!canPlay()) return;
  const t = audio.currentTime;
  if (abA == null) abA = t;
  else if (abB == null) {
    abB = t;
    if (abB < abA) { const x = abA; abA = abB; abB = x; }
  } else { abA = t; abB = null; }
  refreshModePanel();
}

// ---------------- 听写 ----------------
function loadDictProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(DICT_KEY) || "{}");
    dictBest = saved.best || {};
    dictIdx = Math.min(Math.max(0, saved.idx || 0), Math.max(0, segs.length - 1));
  } catch {
    dictBest = {};
    dictIdx = 0;
  }
}

function saveDictProgress() {
  try {
    localStorage.setItem(DICT_KEY, JSON.stringify({ best: dictBest, idx: dictIdx }));
  } catch { /* 存储满/隐私模式,忽略 */ }
}

function dictDoneCount() {
  return segs.filter((s) => (dictBest[s.id] || 0) >= 90).length;
}

function renderDictPanel() {
  const panel = document.getElementById("dict-panel");
  if (!panel || !segs.length) return;
  const s = segs[dictIdx];
  const canHear = canPlay() && typeof s.start === "number";
  panel.innerHTML = `
    <div class="dict-head">听写模式 <small id="dict-prog">已完成 ${dictDoneCount()}/${segs.length} 句(≥90 分算完成)</small></div>
    <div class="dict-nav">
      <span>第 <b>${dictIdx + 1}</b>/${segs.length} 句</span>
      <button type="button" id="dict-play" class="dict-playbtn"${canHear ? "" : ` disabled title="${canPlay() ? "这句还没打时间点" : "音频缺失"}"`}>▶ 播放本句</button>
      <button type="button" id="dict-prev"${dictIdx === 0 ? " disabled" : ""}>上一句</button>
      <button type="button" id="dict-next"${dictIdx >= segs.length - 1 ? " disabled" : ""}>下一句</button>
    </div>
    <textarea id="dict-input" rows="2" placeholder="听完把这句敲出来,回车判分"></textarea>
    <div class="dict-result" id="dict-result"></div>
    <div class="dict-best" id="dict-best">${dictBest[s.id] != null ? `本句最好成绩:${dictBest[s.id]} 分` : "本句还没写过"}</div>`;
  const input = panel.querySelector("#dict-input");
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      dictScore();
    }
  });
  input.focus();
}

function dictScore() {
  const s = segs[dictIdx];
  const input = document.getElementById("dict-input");
  const resultEl = document.getElementById("dict-result");
  if (!s || !input || !resultEl) return;
  const { percent, tokens } = scoreDictation(input.value, s.en);
  const toks = tokens.map((tk) => {
    const title = tk.status === "wrong" ? ` title="你写的是:${esc(tk.hint)}"` : "";
    return `<span class="dk-tok ${tk.status}"${title}>${esc(tk.t)}</span>`;
  }).join("");
  resultEl.innerHTML = `<span class="dict-score ${percent >= 90 ? "good" : "bad"}">${percent} 分</span>${toks}`;
  const prev = dictBest[s.id] || 0;
  if (percent > prev) dictBest[s.id] = percent;
  saveDictProgress();
  const prog = document.getElementById("dict-prog");
  if (prog) prog.textContent = `已完成 ${dictDoneCount()}/${segs.length} 句(≥90 分算完成)`;
  const bestEl = document.getElementById("dict-best");
  if (bestEl) bestEl.textContent = `本句最好成绩:${dictBest[s.id]} 分`;
  if (percent >= 90 && dictIdx < segs.length - 1) {
    setTimeout(() => dictGo(dictIdx + 1, true), 900); // 达标 → 稍停后自动下一句
  }
}

function dictGo(i, autoplay = false) {
  if (mode !== "dictation") return;
  dictIdx = Math.max(0, Math.min(segs.length - 1, i));
  saveDictProgress();
  renderDictPanel();
  if (autoplay) playSegment(segs[dictIdx], true);
}

// ---------------- 打点 ----------------
function annPanelHTML() {
  return '<div class="pl-card ann-card" id="ann-panel"></div>';
}

function flashAnnHint(msg) {
  const panel = document.getElementById("ann-panel");
  if (!panel) return;
  let hint = panel.querySelector(".ann-warn");
  if (!hint) {
    hint = document.createElement("div");
    hint.className = "ann-warn";
    panel.prepend(hint);
  }
  hint.textContent = msg;
  clearTimeout(hint._t);
  hint._t = setTimeout(() => hint.remove(), 2500);
}

function refreshAnnPanel() {
  const panel = document.getElementById("ann-panel");
  if (!panel) return;
  const done = annStarts.filter((x) => x != null).length;
  const cur = segs[annIdx];
  const last = annLast >= 0 ? segs[annLast] : null;
  const paused = !audio || audio.paused;
  const markLabel = !audio || audioFailed ? "音频缺失" : paused ? "先按 ▶ 播放" : "打点(Space)";
  const markCls = "ann-mark" + (paused ? " ann-mark-paused" : "");
  panel.innerHTML = `
    <div class="ann-prog">打点进度 ${done}/${segs.length}</div>
    <div class="ann-flow">第一步 <b>按 ▶ 播放音频</b>;第二步 听到"当前待打点句"开口的瞬间按 <b>Space</b>。</div>
    ${cur ? `<div class="ann-cur-en"><b>待打点 · 第 ${cur.id} 句</b><br>${esc(cur.en)}</div>`
          : '<div class="ann-cur-en">全部句子都打完点了,可以导出。</div>'}
    <div class="ann-btns">
      <button type="button" id="ann-mark" class="${markCls}"${audio && !audioFailed ? "" : " disabled"}>${markLabel}</button>
      <button type="button" id="ann-minus"${last ? "" : " disabled"}>−0.2s</button>
      <button type="button" id="ann-plus"${last ? "" : " disabled"}>+0.2s</button>
      <button type="button" id="ann-export" class="ann-export">导出 JSON</button>
    </div>
    ${last ? `<div class="ann-hint">最近打点:第 ${last.id} 句 = ${annStarts[annLast].toFixed(1)}s(±0.2s 微调它并回跳试听)</div>` : ""}
    <div class="ann-hint">点左侧任意句可选中重打;导出的 JSON 覆盖 <code>data/listening/${esc(partId)}.json</code> 即完成打点。</div>`;
}

// 打点比普通播放宽松:audio 对象存在、没触发 error 就允许记录 currentTime。
// canPlay() 会额外要求 readyState≥HAVE_FUTURE_DATA(浏览器实现里近似),
// 一进 annotate 页(音频还没 loadedmetadata、用户还没按播放)就返回 false,
// 直接把第一次 Space/点按钮拦掉——这是 bug 的根因。
// 只用 audio && !audioFailed:currentTime 未加载好时为 0,后面 Math.round 也能安全处理;
// 用户按播放后 currentTime 才推进,打点值自然正常。
function annMark() {
  if (!audio || audioFailed || annIdx >= segs.length || annIdx < 0) return;
  const t = Number(audio.currentTime);
  // 音频没在播放且几乎在起点 → 用户还没开播,阻止把所有句子打成 0 秒
  if (audio.paused && (!isFinite(t) || t < 0.5)) {
    flashAnnHint("请先按 ▶ 播放音频,再按 Space 打点");
    return;
  }
  annStarts[annIdx] = Math.round((isFinite(t) ? t : 0) * 10) / 10;
  annLast = annIdx;
  // 依次推进:找下一个未打点的句;都打过就顺延+1
  let next = annIdx + 1;
  const firstUnset = annStarts.indexOf(null, next);
  annIdx = firstUnset >= 0 ? firstUnset : Math.min(next, segs.length);
  renderTranscript();
  const row = transcriptEl.querySelector(".seg.ann-cur");
  if (row) row.scrollIntoView({ behavior: "smooth", block: "center" });
  refreshAnnPanel();
}

function annAdjust(delta) {
  if (annLast < 0 || annStarts[annLast] == null) return;
  annStarts[annLast] = Math.max(0, Math.round((annStarts[annLast] + delta) * 10) / 10);
  if (canPlay()) { // 回跳试听调整后的入点
    audio.currentTime = annStarts[annLast];
    audio.play();
  }
  renderTranscript();
  refreshAnnPanel();
}

function annExport() {
  const out = {
    ...PART,
    segments: segs.map((s, i) => ({ ...s, start: annStarts[i] })),
  };
  const blob = new Blob([JSON.stringify(out, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `${partId}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

// ============================================================
// 快捷键(input/textarea/select 聚焦时不拦截)
// ============================================================
function bindKeyboard() {
  document.addEventListener("keydown", (e) => {
    const tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.target.isContentEditable) return;
    if (ANNOTATE) {
      if (e.code === "Space") { e.preventDefault(); if (!e.repeat) annMark(); }
      else if (e.key === "p" || e.key === "P") togglePlay();
      return;
    }
    if (e.code === "Space") { e.preventDefault(); togglePlay(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); stepSentence(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); stepSentence(1); }
    else if (e.key === "r" || e.key === "R") repeatCurrent();
  });
}

// ============================================================
// 入口
// ============================================================
if (!partId) renderLanding();
else renderPart(partId);
