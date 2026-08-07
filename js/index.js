import { listImportedPassages } from "./passage-store.js";

// 从 id(如 c14-test3-p2)解析册号/Test/Passage,用于分组与排序。
// 解析不出册号的(如本地导入的自定义 id)归到 book=null。
function parseId(id) {
  const m = /^c(\d+)-test(\d+)-p(\d+)/i.exec(id || "");
  if (!m) return { book: null, test: 0, passage: 0 };
  return { book: Number(m[1]), test: Number(m[2]), passage: Number(m[3]) };
}

function renderCard(p) {
  const meta = parseId(p.id);
  const a = document.createElement("a");
  a.className = "card";
  a.href = `reader.html?id=${encodeURIComponent(p.id)}`;
  a.dataset.search = `${p.source || ""} ${p.title || ""}`.toLowerCase();
  const q = p.question_count ? `<span>${p.question_count} 题</span>` : "";
  const order = meta.book == null ? "本地文章" : `TEST ${meta.test} · PASSAGE ${meta.passage}`;
  a.innerHTML = `
    <div class="card-topline"><span class="card-order">${order}</span><span class="card-arrow">↗</span></div>
    <div class="src">${p.source}${p.imported ? " · 本地导入" : ""}</div>
    <div class="title">${p.title}</div>
    <div class="count"><span>${p.sentence_count} 个精读单元</span>${q}</div>`;
  return a;
}

// 把文章按册归为多个组,册号从小到大,组内按 Test/Passage 原书顺序。
// 本地导入(book=null)单独归到最上面一组。
function groupPassages(passages) {
  const byBook = new Map();
  for (const p of passages) {
    const meta = parseId(p.id);
    const key = meta.book == null ? "imported" : meta.book;
    if (!byBook.has(key)) byBook.set(key, []);
    byBook.get(key).push({ p, meta });
  }
  const groups = [];
  // 本地导入组排最前
  if (byBook.has("imported")) {
    groups.push({ book: null, title: "本地导入", items: byBook.get("imported") });
    byBook.delete("imported");
  }
  // 其余按册号升序
  const books = [...byBook.keys()].sort((a, b) => a - b);
  for (const book of books) {
    const items = byBook.get(book).sort((a, b) =>
      a.meta.test - b.meta.test || a.meta.passage - b.meta.passage);
    groups.push({ book, title: `剑桥雅思${book}`, items });
  }
  return groups;
}

function renderGroups(listEl, groups) {
  groups.forEach((g, index) => {
    const section = document.createElement("section");
    section.className = "book-group collapsed"; // 默认收起
    section.dataset.search = `${g.title} ${g.items.map(({ p }) => p.title).join(" ")}`.toLowerCase();
    const head = document.createElement("button");
    head.type = "button";
    head.className = "book-head";
    head.setAttribute("aria-expanded", "false");
    const number = g.book == null ? "LOCAL" : String(g.book).padStart(2, "0");
    head.innerHTML = `
      <span class="book-number">${number}</span>
      <span class="book-title-block"><small>CAMBRIDGE IELTS</small><h2>${g.title}</h2></span>
      <span class="book-count"><strong>${g.items.length}</strong><small>篇文章</small></span>
      <span class="book-action"><span>查看篇目</span><b class="book-caret" aria-hidden="true">↘</b></span>`;
    head.addEventListener("click", () => {
      const willOpen = section.classList.contains("collapsed");
      listEl.querySelectorAll(".book-group:not(.collapsed)").forEach((open) => {
        if (open !== section) {
          open.classList.add("collapsed");
          open.querySelector(".book-head").setAttribute("aria-expanded", "false");
        }
      });
      section.classList.toggle("collapsed", !willOpen);
      const collapsed = !willOpen;
      head.setAttribute("aria-expanded", collapsed ? "false" : "true");
    });
    section.appendChild(head);
    const grid = document.createElement("div");
    grid.className = "card-grid";
    for (const { p } of g.items) grid.appendChild(renderCard(p));
    section.appendChild(grid);
    section.style.setProperty("--book-order", index);
    listEl.appendChild(section);
  });
}

function bindSearch(listEl, emptyEl) {
  const input = document.getElementById("library-search");
  if (!input) return;
  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    let visibleGroups = 0;
    listEl.querySelectorAll(".book-group").forEach((section) => {
      const groupMatch = section.querySelector(".book-title-block h2").textContent.toLowerCase().includes(query);
      let visibleCards = 0;
      section.querySelectorAll(".card").forEach((card) => {
        const show = !query || groupMatch || card.dataset.search.includes(query);
        card.hidden = !show;
        if (show) visibleCards++;
      });
      section.hidden = visibleCards === 0;
      if (!section.hidden) visibleGroups++;
      if (query && !section.hidden) {
        section.classList.remove("collapsed");
        section.querySelector(".book-head").setAttribute("aria-expanded", "true");
      } else if (!query) {
        section.classList.add("collapsed");
        section.querySelector(".book-head").setAttribute("aria-expanded", "false");
      }
    });
    emptyEl.textContent = "没有找到匹配的书或文章。";
    emptyEl.style.display = query && visibleGroups === 0 ? "block" : "none";
  });
}

async function main() {
  const listEl = document.getElementById("list");
  const emptyEl = document.getElementById("empty");
  let idx;
  try {
    const res = await fetch("data/index.json", { cache: "no-store" });
    idx = await res.json();
  } catch (e) {
    emptyEl.textContent = "无法加载文章索引。请通过 start.bat 启动本地服务器后再打开。";
    emptyEl.style.display = "block";
    return;
  }
  const imported = listImportedPassages();
  const importedIds = new Set(imported.map((p) => p.id));
  const builtIn = idx.passages || [];
  const passages = [...imported, ...builtIn.filter((p) => !importedIds.has(p.id))];
  if (passages.length === 0) { emptyEl.style.display = "block"; return; }
  const groups = groupPassages(passages);
  document.getElementById("book-total").textContent = groups.filter((g) => g.book != null).length;
  document.getElementById("passage-total").textContent = passages.length;
  renderGroups(listEl, groups);
  bindSearch(listEl, emptyEl);
}
main().catch((error) => {
  console.error("阅读首页加载失败", error);
  const emptyEl = document.getElementById("empty");
  emptyEl.textContent = "文章列表加载失败，请刷新页面重试。";
  emptyEl.style.display = "block";
});
