import { importPassageJSON, listImportedPassages } from "./passage-store.js";
import { bindProfileBackupUI } from "./profile-backup.js";

function renderCard(listEl, p) {
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
  listEl.appendChild(a);
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
  for (const p of passages) renderCard(listEl, p);
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
