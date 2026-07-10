// 词库页:展示内置雅思核心词,支持"按词根成组 / 按词频列表"两视图、搜索、加入复习、朗读。
// 渲染方式:分组成一个个「List」(每组固定词数),配翻页器。每页整块渲染,不做无限滚动懒加载
// —— 规避之前 IntersectionObserver 哨兵在 iframe 内滚到中途卡住、不再追加的问题。
import { renderAids, aidsHasContent, renderCollocations } from "./aids.js?v=2";
import { loadSeed, getSeedMeta, isSeedAdded, setSeedAdded, seedAddedCount, groupSeedByRoot } from "./seed.js?v=3";
import {speakEnglish, speechSupported} from "./speech.js?v=6";

const bodyEl = document.getElementById("lib-body");
const emptyEl = document.getElementById("lib-empty");
const progressEl = document.getElementById("lib-progress");
const searchEl = document.getElementById("lib-search");
const pagerTopEl = document.getElementById("lib-pager-top");
const pagerBotEl = document.getElementById("lib-pager-bottom");
const cefrFilterEl = document.getElementById("lib-cefr-filter");

const PAGE_SIZE = 20;   // 每个 List 20 个词:一次可消化的学习量;词卡含完整记忆法较高,20 个滚动长度适中
const CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"];

let allWords = [];
let view = "root"; // 'root' | 'list'
let cefrFilter = ""; // "" = 全部难度;否则某个 CEFR 级别(按水平学)
let page = 0;      // 当前 List 序号(0 起)
// 当前视图+搜索过滤后的渲染序列:
//   sequence[i] = 词对象;groupInfo[i] = 该词所属词根组信息(仅成组视图,列表视图为 null)
let sequence = [];
let groupInfo = null;

/* 朗读控件已迁移到 settings.html(F5) */

function esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function wordCardHTML(w) {
  const added = isSeedAdded(w.word);
  const speakBtn = speechSupported()
    ? `<button class="lib-speak" data-word="${esc(w.word)}" title="朗读">🔊</button>` : "";
  const addBtn = added
    ? `<button class="lib-add-btn added" data-word="${esc(w.word)}" data-on="0">✓ 已加入复习</button>`
    : `<button class="lib-add-btn" data-word="${esc(w.word)}" data-on="1">+ 加入复习</button>`;
  const cefr = w.cefr ? `<span class="lib-cefr">${esc(w.cefr)}</span>` : "";
  return `
    <div class="lib-word-card" data-word="${esc(w.word)}">
      <div class="lib-word-head">
        ${speakBtn}
        <span class="lib-word">${esc(w.word)}</span>
        <span class="lib-phon">${w.phonetic ? "/" + esc(w.phonetic) + "/" : ""}</span>
        <span class="lib-pos">${esc(w.pos || "")}</span>
        ${cefr}
      </div>
      <div class="lib-def">${esc(w.def || "")}</div>
      ${aidsHasContent(w.aids) ? renderAids(w.aids) : '<div class="aid-block" style="color:#9aa39c">（记忆法生成中）</div>'}
      ${renderCollocations(w.collocations)}
      <div style="margin-top:11px">${addBtn}</div>
    </div>`;
}

function rootHeaderHTML(g) {
  return g.root === "__misc__"
    ? `<div class="lib-root-title"><span class="rg-gloss">其他（暂无明确词根）</span><span class="rg-count">${g.count} 词</span></div>`
    : `<div class="lib-root-title"><span class="rg-root">${esc(g.root)}</span><span class="rg-gloss">${esc(g.gloss || "")}</span><span class="rg-count">${g.count} 词</span></div>`;
}

function applyFilters(list) {
  let out = list;
  if (cefrFilter) out = out.filter((w) => (w.cefr || "") === cefrFilter);
  const f = searchEl.value.trim().toLowerCase();
  if (f) out = out.filter((w) =>
    w.word.toLowerCase().includes(f) || (w.def || "").toLowerCase().includes(f));
  return out;
}

// 渲染 CEFR 难度筛选 chips(全部 + 数据里实际存在的级别 + 各自词数)
function renderCefrChips() {
  const counts = {};
  for (const w of allWords) { const c = w.cefr || ""; if (c) counts[c] = (counts[c] || 0) + 1; }
  const present = CEFR_ORDER.filter((l) => counts[l]);
  const chip = (val, label, n) =>
    `<button class="lib-cefr-chip${cefrFilter === val ? " active" : ""}" data-cefr="${val}">${label}<span>${n}</span></button>`;
  cefrFilterEl.innerHTML = chip("", "全部", allWords.length) + present.map((l) => chip(l, l, counts[l])).join("");
}

// 依据当前视图 + 搜索,重建渲染序列(词的线性数组)。成组视图额外记录每个词的词根组信息。
function rebuildSequence() {
  const list = applyFilters(allWords);
  if (view === "root") {
    const groups = groupSeedByRoot(list);
    sequence = [];
    groupInfo = [];
    for (const g of groups) {
      for (const w of g.words) {
        sequence.push(w);
        groupInfo.push({ root: g.root, gloss: g.gloss, count: g.words.length });
      }
    }
  } else {
    sequence = list;
    groupInfo = null;
  }
}

function pageCount() {
  return Math.max(1, Math.ceil(sequence.length / PAGE_SIZE));
}

// 渲染当前 List(page)。scrollTop=true 时(用户翻页)回到词库顶部。
function renderPage(scrollTop = false) {
  const total = sequence.length;
  if (!total) {
    bodyEl.innerHTML = searchEl.value.trim()
      ? '<p class="lib-empty">没有匹配的词。</p>'
      : "";
    pagerTopEl.innerHTML = "";
    pagerBotEl.innerHTML = "";
    return;
  }
  const pc = pageCount();
  if (page > pc - 1) page = pc - 1;
  if (page < 0) page = 0;

  const start = page * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, total);

  let html = `<div class="lib-list-banner">List ${page + 1} <span class="llb-range">第 ${start + 1}–${end} 词 · 共 ${total} 词</span></div>`;
  for (let i = start; i < end; i++) {
    if (groupInfo) {
      // 页首、或词根组发生变化时,插入词根组标题(组跨页时页首会重复显示当前组标题)
      if (i === start || groupInfo[i].root !== groupInfo[i - 1].root) {
        html += rootHeaderHTML(groupInfo[i]);
      }
    }
    html += wordCardHTML(sequence[i]);
  }
  bodyEl.innerHTML = html;

  renderPager(pagerTopEl, pc, "top");
  renderPager(pagerBotEl, pc, "bottom");

  if (scrollTop) window.scrollTo(0, 0);
}

function renderPager(el, pc, where) {
  if (pc <= 1) { el.innerHTML = ""; return; }
  let opts = "";
  for (let i = 0; i < pc; i++) {
    const lo = i * PAGE_SIZE + 1;
    const hi = Math.min((i + 1) * PAGE_SIZE, sequence.length);
    opts += `<option value="${i}"${i === page ? " selected" : ""}>List ${i + 1}（${lo}–${hi} 词）</option>`;
  }
  el.innerHTML =
    `<button class="lib-page-prev" ${page === 0 ? "disabled" : ""}>‹ 上一组</button>` +
    `<select class="lib-page-select" aria-label="选择 List">${opts}</select>` +
    `<button class="lib-page-next" ${page >= pc - 1 ? "disabled" : ""}>下一组 ›</button>` +
    `<span class="lib-page-info">List ${page + 1} / ${pc}</span>`;
}

function gotoPage(p) {
  const pc = pageCount();
  const np = Math.max(0, Math.min(pc - 1, p));
  if (np === page) return;
  page = np;
  renderPage(true);
}

// 翻页器事件(顶/底两处共用委托)
function wirePager(el) {
  el.addEventListener("click", (ev) => {
    if (ev.target.closest(".lib-page-prev")) gotoPage(page - 1);
    else if (ev.target.closest(".lib-page-next")) gotoPage(page + 1);
  });
  el.addEventListener("change", (ev) => {
    const sel = ev.target.closest(".lib-page-select");
    if (sel) gotoPage(parseInt(sel.value, 10) || 0);
  });
}
wirePager(pagerTopEl);
wirePager(pagerBotEl);

function rerender(resetPage = true) {
  if (!allWords.length) {
    bodyEl.innerHTML = "";
    pagerTopEl.innerHTML = "";
    pagerBotEl.innerHTML = "";
    emptyEl.hidden = false;
    return;
  }
  emptyEl.hidden = true;
  if (resetPage) page = 0;
  rebuildSequence();
  renderPage(false);
}

function updateProgress() {
  const meta = getSeedMeta();
  const target = meta.total_target || allWords.length;
  const added = seedAddedCount();
  const n = allWords.length;
  // 重新措辞:1127 指「已配好记忆法(词根词缀+联想+例句)的词」,3575 是雅思核心词总目标。
  // 之前写「已收录 1127 / 3575」易被误读成"词丢了",这里点明是记忆法生成进度。
  progressEl.innerHTML =
    `记忆法 <b>${n}</b> / ${target} 词` +
    (added ? ` · 已加入复习 <b>${added}</b>` : "");
  progressEl.title =
    `雅思核心词共 ${target} 个;其中 ${n} 个已配好「词根词缀 + 联想助记 + 例句」记忆法,` +
    `正按词频从高到低逐批扩充。不是词变少了,是记忆法还在陆续生成。`;
}

// 事件委托:朗读 / 加入复习
bodyEl.addEventListener("click", (ev) => {
  const speak = ev.target.closest(".lib-speak");
  if (speak) {
    speakEnglish(speak.dataset.word, {
      onstart: () => speak.classList.add("speaking"),
      onend: () => speak.classList.remove("speaking"),
      onerror: () => speak.classList.remove("speaking"),
    });
    return;
  }
  const add = ev.target.closest(".lib-add-btn");
  if (add) {
    const on = add.dataset.on === "1";
    setSeedAdded(add.dataset.word, on);
    if (on) { add.classList.add("added"); add.textContent = "✓ 已加入复习"; add.dataset.on = "0"; }
    else { add.classList.remove("added"); add.textContent = "+ 加入复习"; add.dataset.on = "1"; }
    updateProgress();
  }
});

document.querySelectorAll(".lib-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".lib-tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    view = tab.dataset.view;
    rerender(true);
  });
});

// 搜索:防抖不必要(数据量小),直接重建;每次搜索回到 List 1。
searchEl.addEventListener("input", () => rerender(true));

// CEFR 难度筛选:点 chip → 只看该级别的词(回到 List 1)
cefrFilterEl.addEventListener("click", (ev) => {
  const b = ev.target.closest(".lib-cefr-chip");
  if (!b) return;
  cefrFilter = b.dataset.cefr;
  cefrFilterEl.querySelectorAll(".lib-cefr-chip").forEach((c) => c.classList.toggle("active", c.dataset.cefr === cefrFilter));
  rerender(true);
});

(async function init() {
  const seed = await loadSeed();
  allWords = (seed.words || []).slice().sort((a, b) => (a.freq_rank || 1e9) - (b.freq_rank || 1e9));
  renderCefrChips();
  updateProgress();
  rerender(true);
})();
