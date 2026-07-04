import { importPassageJSON, listImportedPassages } from "./passage-store.js";
import { bindProfileBackupUI } from "./profile-backup.js";

// 从 id(如 c14-test3-p2)解析册号/Test/Passage,用于分组与排序。
// 解析不出册号的(如本地导入的自定义 id)归到 book=null。
function parseId(id) {
  const m = /^c(\d+)-test(\d+)-p(\d+)/i.exec(id || "");
  if (!m) return { book: null, test: 0, passage: 0 };
  return { book: Number(m[1]), test: Number(m[2]), passage: Number(m[3]) };
}

function renderCard(p) {
  const a = document.createElement("a");
  a.className = "card";
  a.href = `reader.html?id=${encodeURIComponent(p.id)}`;
  const q = p.question_count ? `<span>${p.question_count} 题</span>` : "";
  const quality = p.quality === "teacher_refined"
    ? `<span class="quality refined">老师精修</span>`
    : p.quality === "draft_raw"
      ? `<span class="quality draft">待精修</span>`
      : "";
  a.innerHTML = `
    <div class="src">${p.source}${p.imported ? " · 本地导入" : ""}</div>
    <div class="title">${p.title}</div>
    <div class="count"><span>${p.sentence_count} 个精读单元</span>${q}${quality}</div>`;
  return a;
}

// 把文章按册归为多个组,册号从小到大(剑14→…→19→…),组内按 Test/Passage 原书顺序。
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
  for (const g of groups) {
    const section = document.createElement("section");
    section.className = "book-group collapsed"; // 默认收起
    const head = document.createElement("button");
    head.type = "button";
    head.className = "book-head";
    head.setAttribute("aria-expanded", "false");
    const refined = g.items.filter((x) => x.p.quality === "teacher_refined").length;
    const note = g.book == null
      ? `${g.items.length} 篇`
      : refined === g.items.length
        ? `${g.items.length} 篇 · 全部老师精修`
        : `${g.items.length} 篇`;
    head.innerHTML = `<span class="book-caret" aria-hidden="true">▶</span><h2>${g.title}</h2><span class="book-note">${note}</span>`;
    head.addEventListener("click", () => {
      const collapsed = section.classList.toggle("collapsed");
      head.setAttribute("aria-expanded", collapsed ? "false" : "true");
    });
    section.appendChild(head);
    const grid = document.createElement("div");
    grid.className = "card-grid";
    for (const { p } of g.items) grid.appendChild(renderCard(p));
    section.appendChild(grid);
    listEl.appendChild(section);
  }
}

async function main() {
  const listEl = document.getElementById("list");
  const emptyEl = document.getElementById("empty");
  const statsEl = document.getElementById("library-stats");
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
  if (statsEl) {
    statsEl.textContent = `当前显示 ${passages.length} 篇：内置 ${builtIn.length} 篇，本地导入 ${imported.length} 篇`;
  }
  if (passages.length === 0) { emptyEl.style.display = "block"; return; }
  renderGroups(listEl, groupPassages(passages));
}

document.getElementById("passage-import").addEventListener("change", async (ev) => {
  const file = ev.target.files[0];
  if (!file) return;
  try {
    const { passage, replaced } = importPassageJSON(await file.text());
    alert(`${replaced ? "已更新" : "已导入"}《${passage.title}》，即将打开。`);
    location.href = `reader.html?id=${encodeURIComponent(passage.id)}`;
  } catch (e) {
    alert("文章导入失败：" + e.message);
    ev.target.value = "";
  }
});
bindProfileBackupUI({
  exportButtonId: "profile-export",
  importInputId: "profile-import",
  onRestored: () => location.reload(),
});
main();
