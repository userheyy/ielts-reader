// 语法书页:渲染《语法俱乐部》(data/local/grammar-book.json,已 gitignore),
// 并把阅读器里的语法 tag 链接(grammar.html#ch16.relative)路由到对应书中小节。
// 本地书缺失(线上或未提取)时优雅降级:用 data/grammar-tags.json 渲染 54 个语法点骨架。

const tocEl = document.getElementById("toc");
const contentEl = document.getElementById("content");
const noticeEl = document.getElementById("grammar-notice");
const crumbEl = document.getElementById("grammar-crumb");

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

let BOOK = null;   // grammar-book.json
let TAGS = [];     // grammar-tags.json 的 tags[]
let TAG_BY_ID = {};

async function loadJSON(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(String(r.status));
  return r.json();
}

// 把任意锚点(tag id 如 ch16.relative,或书内 section anchor 如 ch1.s12)解析成 section anchor
function resolveAnchor(hash) {
  const key = (hash || "").replace(/^#/, "");
  if (!key) return null;
  if (TAG_BY_ID[key] && TAG_BY_ID[key].book_anchor) return TAG_BY_ID[key].book_anchor;
  return key; // 可能本身就是 section anchor
}

function renderToc() {
  if (!BOOK) return;
  tocEl.innerHTML = BOOK.parts.map((p) => `
    <div class="toc-part">
      <div class="toc-part-title">${esc(p.title)}</div>
      ${p.chapters.map((c) => `
        <details class="toc-ch">
          <summary>${esc(c.title)}</summary>
          <ul>${c.sections.map((s) =>
            `<li><a href="#${esc(s.anchor)}" data-anchor="${esc(s.anchor)}">${esc(s.title)}</a></li>`).join("")}</ul>
        </details>`).join("")}
    </div>`).join("");
}

function sectionHTML(section, chapter) {
  const blocks = (section.blocks || []).map((b) => {
    if (b.t === "ex") {
      return `<div class="g-ex"><div class="g-ex-en">${esc(b.en)}</div>${b.zh ? `<div class="g-ex-zh">${esc(b.zh)}</div>` : ""}${b.note ? `<div class="g-ex-note">${esc(b.note)}</div>` : ""}</div>`;
    }
    return `<p class="g-p">${esc(b.zh || b.en || "")}</p>`;
  }).join("");
  const concepts = (section.concepts && section.concepts.length)
    ? `<div class="g-concepts">${section.concepts.map((c) => `<span class="g-concept">${esc(c)}</span>`).join("")}</div>` : "";
  return `<section class="g-section" id="${esc(section.anchor)}" data-anchor="${esc(section.anchor)}">
    <h3 class="g-section-title">${esc(section.title)} <small>${esc(chapter.title)}</small></h3>
    ${concepts}${blocks}</section>`;
}

// 渲染某一章的全部小节(右侧内容区),并可滚动定位到某个 anchor
function renderChapter(chapter, part, focusAnchor) {
  crumbEl.textContent = `${part.title.replace(/^第.篇\s*/, "")} · ${chapter.title}`;
  contentEl.innerHTML = `<div class="g-chapter-head"><span class="g-part-tag">${esc(part.title)}</span><h2>${esc(chapter.title)}</h2></div>`
    + chapter.sections.map((s) => sectionHTML(s, chapter)).join("");
  if (focusAnchor) {
    const el = contentEl.querySelector(`[id="${CSS.escape(focusAnchor)}"]`);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      el.classList.add("g-flash");
      setTimeout(() => el.classList.remove("g-flash"), 1600);
    }
  } else {
    contentEl.scrollTo({ top: 0 });
  }
  // 高亮目录当前章
  tocEl.querySelectorAll(".toc-ch").forEach((d) => {
    const on = d.querySelector("summary").textContent === chapter.title;
    if (on) d.open = true;
  });
}

function findByAnchor(anchor) {
  if (!BOOK || !anchor) return null;
  // anchor 可能是 section anchor(ch1.s12)或 chapter anchor(ch1)
  for (const part of BOOK.parts) {
    for (const chapter of part.chapters) {
      if (chapter.anchor === anchor) return { part, chapter, section: null };
      const section = chapter.sections.find((s) => s.anchor === anchor);
      if (section) return { part, chapter, section };
    }
  }
  return null;
}

function route() {
  if (!BOOK) return;
  const resolved = resolveAnchor(location.hash);
  let hit = resolved && findByAnchor(resolved);
  if (!hit) {
    // 若解析到的是 chXX(无 .sYY),尝试定位到该章
    const chOnly = (resolved || "").split(".")[0];
    hit = findByAnchor(chOnly);
  }
  if (!hit) {
    const p0 = BOOK.parts[0];
    hit = { part: p0, chapter: p0.chapters[0], section: null };
  }
  renderChapter(hit.chapter, hit.part, hit.section ? hit.section.anchor : null);
}

// ---- 降级:本地书缺失时,用 taxonomy 渲染语法点骨架 ----
function renderFallback() {
  noticeEl.innerHTML = `<div class="g-notice">
    <b>📖 本地未提取《语法俱乐部》完整内容</b>
    <p>下面是语法点索引骨架。要看每个语法点的书内详解,请在本地运行:</p>
    <code>py tools/extract_grammar_book.py --epub "你的语法俱乐部.epub 路径"</code>
    <p class="g-notice-sub">(该书受版权保护,提取内容仅存本地、不会上传;音频同理。)</p>
  </div>`;
  // 按 ch 分组
  const byCh = {};
  for (const t of TAGS) { (byCh[t.ch] = byCh[t.ch] || []).push(t); }
  const chs = Object.keys(byCh).map(Number).sort((a, b) => a - b);
  tocEl.innerHTML = chs.map((ch) =>
    `<div class="toc-part"><div class="toc-part-title">第 ${ch} 章</div>
      <ul>${byCh[ch].map((t) => `<li><a href="#${esc(t.id)}" data-anchor="${esc(t.id)}">${esc(t.name)}</a></li>`).join("")}</ul>
    </div>`).join("");
  contentEl.innerHTML = chs.map((ch) => `<section class="g-section">
    <h3 class="g-section-title">第 ${ch} 章</h3>
    ${byCh[ch].map((t) => `<div class="g-tag-skel" id="${esc(t.id)}"><b>${esc(t.name)}</b><span>${esc(t.brief)}</span></div>`).join("")}
  </section>`).join("");
  const key = (location.hash || "").replace(/^#/, "");
  if (key) {
    const el = document.getElementById(key);
    if (el) { el.scrollIntoView({ block: "center" }); el.classList.add("g-flash"); }
  }
}

async function main() {
  // taxonomy 一定要有(已提交,线上也在)
  try {
    const tagData = await loadJSON("data/grammar-tags.json");
    TAGS = tagData.tags || [];
    TAG_BY_ID = Object.fromEntries(TAGS.map((t) => [t.id, t]));
  } catch { TAGS = []; }

  try {
    BOOK = await loadJSON("data/local/grammar-book.json");
  } catch {
    BOOK = null;
  }

  if (!BOOK) { renderFallback(); return; }

  renderToc();
  route();
  window.addEventListener("hashchange", route);
  tocEl.addEventListener("click", (ev) => {
    if (ev.target.closest("a[data-anchor]")) {
      // 窄屏点完目录自动收起
      document.body.classList.remove("toc-open");
    }
  });
}

document.getElementById("toc-toggle").addEventListener("click", () => {
  document.body.classList.toggle("toc-open");
});

main();
