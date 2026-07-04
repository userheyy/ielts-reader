// 词库页:展示内置雅思核心词,支持"按词根成组 / 按词频列表"两视图、搜索、加入复习、朗读。
import { renderAids, aidsHasContent } from "./aids.js?v=1";
import { loadSeed, getSeedMeta, isSeedAdded, setSeedAdded, seedAddedCount, groupSeedByRoot } from "./seed.js?v=1";
import { initSpeechControls, speakEnglish, speechSupported } from "./speech.js?v=6";

const bodyEl = document.getElementById("lib-body");
const emptyEl = document.getElementById("lib-empty");
const progressEl = document.getElementById("lib-progress");
const searchEl = document.getElementById("lib-search");

let allWords = [];
let view = "root"; // 'root' | 'list'

initSpeechControls(
  document.getElementById("speech-voice"),
  document.getElementById("speech-rate"),
  document.getElementById("speech-stop"),
);

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
      <div style="margin-top:11px">${addBtn}</div>
    </div>`;
}

function applySearch(list) {
  const f = searchEl.value.trim().toLowerCase();
  if (!f) return list;
  return list.filter((w) =>
    w.word.toLowerCase().includes(f) || (w.def || "").toLowerCase().includes(f));
}

function rootGroupHTML(g) {
  const title = g.root === "__misc__"
    ? `<div class="lib-root-title"><span class="rg-gloss">其他（暂无明确词根）</span><span class="rg-count">${g.words.length} 词</span></div>`
    : `<div class="lib-root-title"><span class="rg-root">${esc(g.root)}</span><span class="rg-gloss">${esc(g.gloss || "")}</span><span class="rg-count">${g.words.length} 词</span></div>`;
  return `<div class="lib-root-group">${title}${g.words.map(wordCardHTML).join("")}</div>`;
}

// 懒加载:每次只把 units 里的一批渲染进 body,滚到底部再追加下一批。
// units 是当前视图的渲染单位数组(列表视图=词,成组视图=词根组);
// unitHTML 把一个单位转成 HTML;batchSize 是每批渲染多少个单位。
const LIST_BATCH = 60;   // 列表视图:每批 60 个词
const ROOT_BATCH = 8;    // 成组视图:每批 8 个词根组
const NEAR_PX = 600; // 哨兵进入视口下方 600px 内就预加载下一批
let units = [];
let unitHTML = wordCardHTML;
let batchSize = LIST_BATCH;
let cursor = 0;
let sentinel = null;
// 主触发:IntersectionObserver(高效);兜底:scroll/resize 监听(某些环境下 IO 不派发回调时仍可用)。
const observer = ("IntersectionObserver" in window)
  ? new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) fillWhileVisible();
    }, { rootMargin: NEAR_PX + "px 0px" })
  : null;

function renderNextBatch() {
  const batch = units.slice(cursor, cursor + batchSize);
  if (!batch.length) return false;
  const html = batch.map(unitHTML).join("");
  if (sentinel) sentinel.insertAdjacentHTML("beforebegin", html);
  else bodyEl.insertAdjacentHTML("beforeend", html);
  cursor += batch.length;
  if (cursor >= units.length) stopObserving(); // 全部渲染完,停止监听
  return true;
}

// 只要哨兵还在视口附近且没渲染完,就继续追加(处理首屏没填满、或一次滚很多的情况)。
function fillWhileVisible() {
  if (!sentinel) return;
  let guard = 0; // 防御性上限,避免异常情况死循环
  while (cursor < units.length && sentinelNear() && guard++ < 50) {
    if (!renderNextBatch()) break;
  }
}

function sentinelNear() {
  if (!sentinel) return false;
  const top = sentinel.getBoundingClientRect().top;
  return top <= window.innerHeight + NEAR_PX;
}

function stopObserving() {
  if (observer && sentinel) observer.unobserve(sentinel);
}

function onScrollOrResize() {
  if (cursor < units.length) fillWhileVisible();
}

// 重置并渲染首屏。之后靠 IntersectionObserver + scroll/resize 兜底继续追加;
// 若首屏没填满视口,fillWhileVisible 会在此处一次性把可见范围补齐。
function startLazyRender(nextUnits, nextUnitHTML, nextBatchSize) {
  units = nextUnits;
  unitHTML = nextUnitHTML;
  batchSize = nextBatchSize;
  cursor = 0;
  stopObserving();
  bodyEl.innerHTML = '<div id="lib-sentinel" aria-hidden="true"></div>';
  sentinel = document.getElementById("lib-sentinel");
  renderNextBatch();
  fillWhileVisible(); // 补满首屏可见区
  if (observer && sentinel && cursor < units.length) observer.observe(sentinel);
}

window.addEventListener("scroll", onScrollOrResize, { passive: true });
window.addEventListener("resize", onScrollOrResize, { passive: true });

function rerender() {
  if (!allWords.length) {
    stopObserving();
    sentinel = null;
    bodyEl.innerHTML = "";
    emptyEl.hidden = false;
    return;
  }
  emptyEl.hidden = true;
  const list = applySearch(allWords);
  if (!list.length) {
    stopObserving();
    sentinel = null;
    bodyEl.innerHTML = '<p class="lib-empty">没有匹配的词。</p>';
    return;
  }
  if (view === "root") startLazyRender(groupSeedByRoot(list), rootGroupHTML, ROOT_BATCH);
  else startLazyRender(list, wordCardHTML, LIST_BATCH);
}

function updateProgress() {
  const meta = getSeedMeta();
  const total = meta.total_target || allWords.length;
  const added = seedAddedCount();
  progressEl.innerHTML = `已收录 <b>${allWords.length}</b> / ${total} 词` +
    (added ? ` · 已加入复习 <b>${added}</b>` : "");
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
    rerender();
  });
});

searchEl.addEventListener("input", rerender);

(async function init() {
  const seed = await loadSeed();
  allWords = (seed.words || []).slice().sort((a, b) => (a.freq_rank || 1e9) - (b.freq_rank || 1e9));
  updateProgress();
  rerender();
})();
