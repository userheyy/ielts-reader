# 雅思阅读精读器 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个本地纯静态网页:左边显示剑桥雅思阅读原文,右边逐句显示语法拆解+中文翻译,点词可入生词库;数据由 Claude 预处理(读 PDF 页图抄录+逐句讲解)生成为 JSON。

**Architecture:** 三页静态站点(首页/阅读器/生词库),原生 HTML+CSS+JS,无框架无构建。文章数据是本地 JSON(通过 `python -m http.server` 提供以绕过 file:// 的 fetch 限制),生词存 localStorage。预处理用 Python(pypdfium2 渲染 PDF 页为高清图)+ Claude 读图产出数据。

**Tech Stack:** HTML / CSS / 原生 JavaScript(ES modules)/ Python 3.13 + pypdfium2 + pdfplumber / localStorage。

**关键约定(所有任务共用):**
- 项目根:`C:\Users\11386\Desktop\雅思\ielts-app\`(下称 `ROOT`)。
- PDF 素材根:`C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19\`。
- Scratchpad(临时图):`C:\Users\11386\AppData\Local\Temp\claude\C--Users-11386-Desktop---\8ff3ffd7-779f-45d4-9c65-27d90695581f\scratchpad\`。
- **本项目不是 git 仓库**。计划中的"Commit"步骤改为"**验证产物存在并运行验证脚本**"(见每个 Commit 步骤的实际命令)。若用户后续要 git,可再 `git init`。
- 测试方式:纯静态无后端,用**数据校验脚本(Python/Node)**+**浏览器手测清单**。不引入 Jest/Pytest 框架,但每个数据/逻辑任务都给出可运行的校验命令与预期输出。

---

## 文件结构(先锁定分解)

| 文件 | 职责 |
|------|------|
| `ROOT/index.html` | 首页/文章库骨架 |
| `ROOT/reader.html` | 阅读器骨架(左右分栏容器) |
| `ROOT/vocab.html` | 生词库骨架 |
| `ROOT/css/style.css` | 全站样式(分栏、卡片、气泡、高亮、响应式) |
| `ROOT/js/store.js` | 生词 localStorage 读写(纯函数模块,三页共用) |
| `ROOT/js/schema.js` | passage JSON 的运行时校验函数(供页面与测试共用) |
| `ROOT/js/index.js` | 首页:读 `data/index.json` 渲染卡片列表 |
| `ROOT/js/reader.js` | 阅读器:读 passage JSON,渲染左原文/右讲解,点句联动,点词气泡,入库 |
| `ROOT/js/vocab.js` | 生词库:列表/搜索/删除/导入导出 |
| `ROOT/data/index.json` | 文章索引 |
| `ROOT/data/passages/<id>.json` | 单篇文章数据 |
| `ROOT/tools/find_page.py` | 按标题在 PDF 中定位页码 |
| `ROOT/tools/render_page.py` | 渲染 PDF 指定页为高清 PNG,可按 x 区间裁条 |
| `ROOT/tools/validate_data.py` | 校验所有 passage JSON 与 index.json 结构 |
| `ROOT/start.bat` | 双击启动 `python -m http.server 8000` |
| `ROOT/js/sample-check.mjs` | Node 端对 store.js 逻辑的最小校验脚本 |

每篇文章数据文件自成一体;JS 按职责拆分,单文件聚焦一件事。

---

## Task 1: 项目骨架 + 启动脚本 + 示例数据

**目的:** 先立起可运行的目录与最小示例数据,让后续 UI 有东西可读、可手测。

**Files:**
- Create: `ROOT/start.bat`
- Create: `ROOT/data/index.json`
- Create: `ROOT/data/passages/sample.json`
- Create: `ROOT/tools/validate_data.py`

- [ ] **Step 1: 写 `start.bat`(一键启动本地服务器)**

`ROOT/start.bat`:
```bat
@echo off
cd /d "%~dp0"
echo 正在启动雅思阅读器本地服务器...
echo 浏览器打开:  http://localhost:8000/index.html
echo 关闭本窗口即停止服务器。
python -m http.server 8000
```

- [ ] **Step 2: 写最小示例文章 `data/passages/sample.json`**

这是用于把 UI 跑通的假数据(2 句),真实文章后续任务生成。

`ROOT/data/passages/sample.json`:
```json
{
  "id": "sample",
  "source": "示例 · Test 0 · Passage 0",
  "title": "Sample Passage (UI 测试用)",
  "sentences": [
    {
      "id": 1,
      "para": 1,
      "en": "Why are some people right-handed and others left-handed?",
      "zh": "为什么有些人惯用右手,有些人惯用左手?",
      "grammar": {
        "type": "特殊疑问句(并列)",
        "note": "由 and 连接两个并列问句;后半句 others (are) left-handed 承前省略了 are。"
      },
      "words": [
        { "w": "right-handed", "pos": "adj.", "def": "惯用右手的" },
        { "w": "left-handed", "pos": "adj.", "def": "惯用左手的" }
      ]
    },
    {
      "id": 2,
      "para": 1,
      "en": "This has never been a straightforward question to answer.",
      "zh": "这从来都不是一个容易回答的问题。",
      "grammar": {
        "type": "主系表(现在完成时)",
        "note": "has never been 现在完成时表持续状态;to answer 为不定式作后置定语修饰 question。"
      },
      "words": [
        { "w": "straightforward", "pos": "adj.", "def": "简单明了的;直截了当的" }
      ]
    }
  ]
}
```

- [ ] **Step 3: 写文章索引 `data/index.json`**

`ROOT/data/index.json`:
```json
{
  "passages": [
    { "id": "sample", "source": "示例 · Test 0 · Passage 0", "title": "Sample Passage (UI 测试用)", "sentence_count": 2 }
  ]
}
```

- [ ] **Step 4: 写数据校验脚本 `tools/validate_data.py`**

`ROOT/tools/validate_data.py`:
```python
"""校验 data/index.json 与所有 data/passages/*.json 的结构完整性。
运行: python tools/validate_data.py
无错误则打印 OK 并以 0 退出;有问题打印每条错误并以 1 退出。
"""
import json, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

def check_passage(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for k in ("id", "source", "title", "sentences"):
        if k not in d:
            errors.append(f"{path}: 缺字段 {k}")
    sents = d.get("sentences", [])
    if not sents:
        errors.append(f"{path}: sentences 为空")
    prev_id, prev_para = 0, 1
    for s in sents:
        for k in ("id", "para", "en", "zh", "grammar", "words"):
            if k not in s:
                errors.append(f"{path} 句{s.get('id','?')}: 缺字段 {k}")
        if s.get("id") != prev_id + 1:
            errors.append(f"{path}: 句 id 不连续,期望 {prev_id+1} 得到 {s.get('id')}")
        prev_id = s.get("id", prev_id)
        if s.get("para", prev_para) < prev_para:
            errors.append(f"{path}: para 递减 (句{s.get('id')})")
        prev_para = s.get("para", prev_para)
        g = s.get("grammar", {})
        if not isinstance(g, dict) or "type" not in g or "note" not in g:
            errors.append(f"{path} 句{s.get('id')}: grammar 需含 type 与 note")
        for w in s.get("words", []):
            for k in ("w", "pos", "def"):
                if k not in w:
                    errors.append(f"{path} 句{s.get('id')}: 生词缺字段 {k}")
    return d

def main():
    idx_path = os.path.join(ROOT, "data", "index.json")
    with open(idx_path, encoding="utf-8") as f:
        idx = json.load(f)
    listed = {p["id"] for p in idx["passages"]}
    files = {}
    for path in glob.glob(os.path.join(ROOT, "data", "passages", "*.json")):
        d = check_passage(path)
        files[d["id"]] = len(d.get("sentences", []))
    # 交叉核对:index 里每篇都要有文件,句数一致
    for p in idx["passages"]:
        if p["id"] not in files:
            errors.append(f"index.json 列出 {p['id']} 但缺少 data/passages/{p['id']}.json")
        elif p.get("sentence_count") != files[p["id"]]:
            errors.append(f"{p['id']}: index 句数 {p.get('sentence_count')} != 文件句数 {files[p['id']]}")
    if errors:
        print("校验失败:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(files)} 篇文章,索引 {len(listed)} 条,全部通过。")

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 运行校验脚本,确认示例数据通过**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/validate_data.py
```
Expected: `OK: 1 篇文章,索引 1 条,全部通过。`

- [ ] **Step 6: 确认启动脚本可跑(手动)**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python -c "import http.server; print('http.server available')"
```
Expected: `http.server available`
(实际双击 `start.bat` 的验证放到 Task 6 与页面一起手测。)

---

## Task 2: 生词存储模块 store.js + Node 校验

**目的:** 先把生词库的数据层写好并验证(纯逻辑,不依赖 DOM),后续 UI 直接调用。

**Files:**
- Create: `ROOT/js/store.js`
- Create: `ROOT/js/sample-check.mjs`

- [ ] **Step 1: 写 `js/store.js`(生词读写,ES module)**

设计为可在浏览器与 Node 双环境用:localStorage 不存在时退回内存对象,便于 Node 测。

`ROOT/js/store.js`:
```javascript
// 生词库存储层。浏览器用 localStorage;无 localStorage(如 Node)时退回内存,便于测试。
const KEY = "ielts_vocab";

const mem = { v: null }; // Node 退回存储
function backend() {
  if (typeof localStorage !== "undefined") return localStorage;
  return {
    getItem: () => mem.v,
    setItem: (_k, val) => { mem.v = val; },
  };
}

export function loadAll() {
  const raw = backend().getItem(KEY);
  if (!raw) return [];
  try { return JSON.parse(raw); } catch { return []; }
}

function saveAll(list) {
  backend().setItem(KEY, JSON.stringify(list));
}

// 判断某词是否已入库(按小写去重)
export function has(word) {
  const w = word.toLowerCase();
  return loadAll().some((e) => e.word.toLowerCase() === w);
}

// 新增或更新一个生词。entry 至少含 word/def;其余可选。
// 返回 { added: boolean }。已存在则更新出处/例句,不新增。
export function addWord(entry) {
  const list = loadAll();
  const w = entry.word.toLowerCase();
  const idx = list.findIndex((e) => e.word.toLowerCase() === w);
  const record = {
    word: entry.word,
    def: entry.def || "",
    pos: entry.pos || "",
    sentence_en: entry.sentence_en || "",
    sentence_zh: entry.sentence_zh || "",
    source: entry.source || "",
    passage_id: entry.passage_id || "",
    sentence_id: entry.sentence_id || null,
    added_at: entry.added_at || new Date().toISOString().slice(0, 10),
    status: "new",
    review: { level: 0, next_due: null, history: [] },
  };
  if (idx >= 0) {
    // 保留原 added_at/status/review,更新语境与释义
    record.added_at = list[idx].added_at;
    record.status = list[idx].status;
    record.review = list[idx].review;
    list[idx] = record;
    saveAll(list);
    return { added: false };
  }
  list.push(record);
  saveAll(list);
  return { added: true };
}

export function removeWord(word) {
  const w = word.toLowerCase();
  const list = loadAll().filter((e) => e.word.toLowerCase() !== w);
  saveAll(list);
}

// 导出为可下载 JSON 字符串
export function exportJSON() {
  return JSON.stringify(loadAll(), null, 2);
}

// 从 JSON 字符串导入(合并,按 word 去重,导入项覆盖同名)
export function importJSON(text) {
  const incoming = JSON.parse(text);
  if (!Array.isArray(incoming)) throw new Error("导入文件应为数组");
  const list = loadAll();
  const byWord = new Map(list.map((e) => [e.word.toLowerCase(), e]));
  for (const e of incoming) {
    if (e && e.word) byWord.set(e.word.toLowerCase(), e);
  }
  const merged = [...byWord.values()];
  saveAll(merged);
  return { total: merged.length };
}

// 供测试重置内存后端
export function __resetMem() { mem.v = null; }
```

- [ ] **Step 2: 写 Node 校验脚本 `js/sample-check.mjs`(先失败)**

`ROOT/js/sample-check.mjs`:
```javascript
import { addWord, has, loadAll, removeWord, exportJSON, importJSON, __resetMem } from "./store.js";
import assert from "node:assert";

__resetMem();

// 1) 新增
let r = addWord({ word: "Practically", def: "实际上", source: "剑2·T1·P1" });
assert.equal(r.added, true, "首次应新增");
assert.equal(loadAll().length, 1);

// 2) 去重(大小写不敏感)
r = addWord({ word: "practically", def: "实际上(更新)", source: "剑2·T1·P2" });
assert.equal(r.added, false, "同词应更新而非新增");
assert.equal(loadAll().length, 1, "仍应只有 1 条");
assert.equal(has("PRACTICALLY"), true, "has 应大小写不敏感");
assert.equal(loadAll()[0].source, "剑2·T1·P2", "出处应被更新");

// 3) 预留字段存在
assert.ok(loadAll()[0].review && loadAll()[0].status === "new", "应含 status/review 预留字段");

// 4) 导出/导入往返
const dump = exportJSON();
__resetMem();
assert.equal(loadAll().length, 0, "重置后应为空");
const imp = importJSON(dump);
assert.equal(imp.total, 1, "导入后应有 1 条");
assert.equal(loadAll()[0].word, "practically");

// 5) 删除
removeWord("practically");
assert.equal(loadAll().length, 0, "删除后应为空");

console.log("store.js 全部断言通过 ✅");
```

- [ ] **Step 3: 运行,验证通过**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && node js/sample-check.mjs
```
Expected: `store.js 全部断言通过 ✅`
(若报错则修 store.js 直到通过。)

- [ ] **Step 4: 记录产物存在(代替 commit)**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && ls js/store.js js/sample-check.mjs && echo TASK2_DONE
```
Expected: 两文件路径 + `TASK2_DONE`

---

## Task 3: passage 运行时校验 schema.js

**目的:** UI 加载文章前先校验结构,避免坏数据导致页面崩;测试与页面共用同一函数。

**Files:**
- Create: `ROOT/js/schema.js`
- Modify: `ROOT/js/sample-check.mjs`(追加对 schema 的断言)

- [ ] **Step 1: 写 `js/schema.js`**

`ROOT/js/schema.js`:
```javascript
// passage JSON 运行时校验。返回 { ok: boolean, errors: string[] }。
export function validatePassage(d) {
  const errors = [];
  for (const k of ["id", "source", "title", "sentences"]) {
    if (!(k in d)) errors.push(`缺字段 ${k}`);
  }
  if (!Array.isArray(d.sentences) || d.sentences.length === 0) {
    errors.push("sentences 应为非空数组");
    return { ok: false, errors };
  }
  let prevId = 0, prevPara = 1;
  for (const s of d.sentences) {
    for (const k of ["id", "para", "en", "zh", "grammar", "words"]) {
      if (!(k in s)) errors.push(`句${s.id ?? "?"}: 缺字段 ${k}`);
    }
    if (s.id !== prevId + 1) errors.push(`句 id 不连续:期望 ${prevId + 1} 得 ${s.id}`);
    prevId = s.id;
    if (s.para < prevPara) errors.push(`句${s.id}: para 递减`);
    prevPara = s.para;
    if (!s.grammar || typeof s.grammar.type !== "string" || typeof s.grammar.note !== "string") {
      errors.push(`句${s.id}: grammar 需含 type 与 note 字符串`);
    }
    if (!Array.isArray(s.words)) errors.push(`句${s.id}: words 应为数组`);
  }
  return { ok: errors.length === 0, errors };
}
```

- [ ] **Step 2: 在 `js/sample-check.mjs` 追加 schema 断言**

在文件末尾 `console.log(...)` 之前插入:
```javascript
// --- schema.js 校验 ---
import { validatePassage } from "./schema.js";
const good = { id: "x", source: "s", title: "t", sentences: [
  { id: 1, para: 1, en: "a", zh: "啊", grammar: { type: "t", note: "n" }, words: [] },
] };
assert.equal(validatePassage(good).ok, true, "合法 passage 应通过");
const bad = { id: "x", source: "s", title: "t", sentences: [
  { id: 2, para: 1, en: "a", zh: "啊", grammar: { type: "t" }, words: [] },
] };
const res = validatePassage(bad);
assert.equal(res.ok, false, "非法 passage 应失败");
assert.ok(res.errors.length >= 2, "应报出 id 不连续与 grammar 缺 note");
```
(注:import 语句需提到文件顶部与其它 import 并列;若运行时报 import 位置错误,把这两个 import 移到文件最上方。)

- [ ] **Step 3: 运行验证**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && node js/sample-check.mjs
```
Expected: `store.js 全部断言通过 ✅`(且无 schema 断言报错)

- [ ] **Step 4: 记录产物**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && ls js/schema.js && echo TASK3_DONE
```
Expected: 路径 + `TASK3_DONE`

---

## Task 4: 首页 index.html + index.js

**目的:** 文章库列表页,读 index.json 渲染卡片,点卡片进阅读器。

**Files:**
- Create: `ROOT/index.html`
- Create: `ROOT/js/index.js`
- Create: `ROOT/css/style.css`(本任务先建基础样式,后续任务扩展)

- [ ] **Step 1: 写基础样式 `css/style.css`**

`ROOT/css/style.css`:
```css
:root {
  --green: #7bc47f;
  --green-dark: #4a9d5b;
  --bg: #f5f7f5;
  --card: #ffffff;
  --text: #222;
  --muted: #777;
  --hl: #d7f0d9;
}
* { box-sizing: border-box; }
body {
  margin: 0; font-family: "Segoe UI", "Microsoft YaHei", system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.6;
}
header.topbar {
  background: var(--green); color: #fff; padding: 12px 20px;
  display: flex; align-items: center; gap: 20px;
}
header.topbar a { color: #fff; text-decoration: none; font-weight: 600; }
header.topbar h1 { font-size: 18px; margin: 0; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.card {
  background: var(--card); border-radius: 10px; padding: 16px 18px;
  box-shadow: 0 1px 4px rgba(0,0,0,.08); text-decoration: none; color: inherit;
  display: block; transition: transform .1s, box-shadow .1s;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 3px 10px rgba(0,0,0,.12); }
.card .src { color: var(--muted); font-size: 13px; }
.card .title { font-size: 17px; font-weight: 600; margin: 6px 0; }
.card .count { color: var(--green-dark); font-size: 13px; }
```

- [ ] **Step 2: 写 `index.html`**

`ROOT/index.html`:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>雅思阅读精读器 · 文章库</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <header class="topbar">
    <h1>雅思阅读精读器</h1>
    <a href="index.html">文章库</a>
    <a href="vocab.html">生词库</a>
  </header>
  <div class="container">
    <div id="list" class="card-grid"></div>
    <p id="empty" style="display:none;color:var(--muted)">还没有文章。请先用预处理流程生成。</p>
  </div>
  <script type="module" src="js/index.js"></script>
</body>
</html>
```

- [ ] **Step 3: 写 `js/index.js`**

`ROOT/js/index.js`:
```javascript
async function main() {
  const listEl = document.getElementById("list");
  const emptyEl = document.getElementById("empty");
  let idx;
  try {
    const res = await fetch("data/index.json");
    idx = await res.json();
  } catch (e) {
    emptyEl.textContent = "无法加载文章索引。请通过 start.bat 启动本地服务器后再打开。";
    emptyEl.style.display = "block";
    return;
  }
  const passages = idx.passages || [];
  if (passages.length === 0) { emptyEl.style.display = "block"; return; }
  for (const p of passages) {
    const a = document.createElement("a");
    a.className = "card";
    a.href = `reader.html?id=${encodeURIComponent(p.id)}`;
    a.innerHTML = `
      <div class="src">${p.source}</div>
      <div class="title">${p.title}</div>
      <div class="count">${p.sentence_count} 句</div>`;
    listEl.appendChild(a);
  }
}
main();
```

- [ ] **Step 4: 手动验证(需先启动服务器)**

Run(启动服务器,后台):
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python -m http.server 8000
```
然后浏览器打开 `http://localhost:8000/index.html`。
Expected: 看到一张卡片"Sample Passage (UI 测试用)",出处"示例 · Test 0 · Passage 0",标注"2 句";点击跳转到 `reader.html?id=sample`(此时阅读器尚未实现,下个任务做)。

- [ ] **Step 5: 记录产物**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && ls index.html js/index.js css/style.css && echo TASK4_DONE
```
Expected: 三路径 + `TASK4_DONE`

---

## Task 5: 阅读器 reader.html + reader.js(核心)

**目的:** 左原文/右讲解、点句联动高亮、点词气泡、入库、翻译显隐。

**Files:**
- Create: `ROOT/reader.html`
- Create: `ROOT/js/reader.js`
- Modify: `ROOT/css/style.css`(追加阅读器样式)

- [ ] **Step 1: 追加阅读器样式到 `css/style.css`**

在 `style.css` 末尾追加:
```css
/* ---- 阅读器 ---- */
.reader-toolbar { display: flex; gap: 12px; align-items: center; margin-bottom: 12px; }
.reader-toolbar button {
  background: var(--green); color: #fff; border: none; border-radius: 6px;
  padding: 6px 12px; cursor: pointer; font-size: 14px;
}
.reader-toolbar .src { color: var(--muted); font-size: 14px; }
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start; }
.pane { background: var(--card); border-radius: 10px; padding: 18px 22px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
.pane.left { font-size: 17px; }
.pane.left p { margin: 0 0 12px; }
.sent { cursor: pointer; border-radius: 3px; }
.sent:hover { background: #eef7ef; }
.sent.active { background: var(--hl); }
.word { cursor: pointer; }
.word.saved { color: var(--green-dark); border-bottom: 2px solid var(--green); }
/* 右侧讲解卡片 */
.gcard { border-left: 3px solid transparent; padding: 8px 10px; margin-bottom: 14px; border-radius: 4px; }
.gcard.active { border-left-color: var(--green); background: #f3faf4; }
.gcard .gtype { font-weight: 600; color: var(--green-dark); font-size: 14px; }
.gcard .gnote { font-size: 14px; margin: 4px 0; }
.gcard .gzh { font-size: 15px; color: #333; }
.gcard .gwords { font-size: 13px; color: var(--muted); margin-top: 4px; }
.hide-zh .gzh { display: none; }
/* 生词气泡 */
.popup {
  position: absolute; z-index: 50; background: #fff; border: 1px solid #ddd;
  border-radius: 8px; box-shadow: 0 3px 12px rgba(0,0,0,.18); padding: 10px 12px;
  max-width: 260px; font-size: 14px;
}
.popup .pw { font-weight: 600; }
.popup .ppos { color: var(--muted); font-size: 12px; margin-left: 4px; }
.popup button {
  margin-top: 8px; background: var(--green); color: #fff; border: none;
  border-radius: 5px; padding: 4px 10px; cursor: pointer; font-size: 13px;
}
.popup button:disabled { background: #bbb; cursor: default; }
@media (max-width: 800px) { .split { grid-template-columns: 1fr; } }
```

- [ ] **Step 2: 写 `reader.html`**

`ROOT/reader.html`:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>阅读器</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <header class="topbar">
    <h1>雅思阅读精读器</h1>
    <a href="index.html">文章库</a>
    <a href="vocab.html">生词库</a>
  </header>
  <div class="container">
    <div class="reader-toolbar">
      <span class="src" id="src"></span>
      <button id="toggle-zh">隐藏翻译</button>
    </div>
    <div class="split">
      <div class="pane left" id="left"></div>
      <div class="pane right" id="right"></div>
    </div>
  </div>
  <script type="module" src="js/reader.js"></script>
</body>
</html>
```

- [ ] **Step 3: 写 `js/reader.js`(渲染 + 交互)**

`ROOT/js/reader.js`:
```javascript
import { validatePassage } from "./schema.js";
import { addWord, has } from "./store.js";

const params = new URLSearchParams(location.search);
const id = params.get("id");
const jumpSentence = params.get("sentence");

const leftEl = document.getElementById("left");
const rightEl = document.getElementById("right");
const srcEl = document.getElementById("src");

let popup = null;
function closePopup() { if (popup) { popup.remove(); popup = null; } }
document.addEventListener("click", (e) => {
  if (popup && !popup.contains(e.target) && !e.target.classList.contains("word")) closePopup();
});

// 把一句话渲染成可点单词的 span 序列;单词保留标点分离
function renderSentenceEN(s) {
  const span = document.createElement("span");
  span.className = "sent";
  span.dataset.sid = s.id;
  // 用正则切出单词与非单词,单词包 .word
  const wordDefs = new Map(s.words.map((w) => [w.w.toLowerCase(), w]));
  const parts = s.en.split(/(\b[A-Za-z][A-Za-z'-]*\b)/g);
  for (const part of parts) {
    if (/^[A-Za-z]/.test(part)) {
      const w = document.createElement("span");
      w.className = "word";
      w.textContent = part;
      if (has(part)) w.classList.add("saved");
      w.addEventListener("click", (ev) => {
        ev.stopPropagation();
        openWordPopup(ev, part, wordDefs.get(part.toLowerCase()), s);
      });
      span.appendChild(w);
    } else {
      span.appendChild(document.createTextNode(part));
    }
  }
  // 点句子本身(非单词处)→ 联动
  span.addEventListener("click", () => activate(s.id));
  return span;
}

function openWordPopup(ev, word, def, sentence) {
  closePopup();
  popup = document.createElement("div");
  popup.className = "popup";
  const defHtml = def
    ? `<div><span class="pw">${def.w}</span><span class="ppos">${def.pos}</span></div><div>${def.def}</div>`
    : `<div><span class="pw">${word}</span></div><div style="color:#999">未收录释义</div>`;
  popup.innerHTML = defHtml;
  const btn = document.createElement("button");
  const already = has(word);
  btn.textContent = already ? "已入库" : "+ 入库";
  btn.disabled = already;
  btn.addEventListener("click", () => {
    addWord({
      word: def ? def.w : word,
      def: def ? def.def : "",
      pos: def ? def.pos : "",
      sentence_en: sentence.en,
      sentence_zh: sentence.zh,
      source: PASSAGE.source,
      passage_id: PASSAGE.id,
      sentence_id: sentence.id,
    });
    btn.textContent = "已入库"; btn.disabled = true;
    // 高亮原文中所有该词
    document.querySelectorAll(".word").forEach((el) => {
      if (el.textContent.toLowerCase() === word.toLowerCase()) el.classList.add("saved");
    });
  });
  popup.appendChild(btn);
  document.body.appendChild(popup);
  const r = ev.target.getBoundingClientRect();
  popup.style.left = (window.scrollX + r.left) + "px";
  popup.style.top = (window.scrollY + r.bottom + 4) + "px";
}

function activate(sid) {
  document.querySelectorAll(".sent").forEach((el) =>
    el.classList.toggle("active", el.dataset.sid == sid));
  document.querySelectorAll(".gcard").forEach((el) =>
    el.classList.toggle("active", el.dataset.sid == sid));
  const g = document.querySelector(`.gcard[data-sid="${sid}"]`);
  if (g) g.scrollIntoView({ behavior: "smooth", block: "center" });
}

let PASSAGE = null;

async function main() {
  if (!id) { leftEl.textContent = "缺少文章 id。"; return; }
  let d;
  try {
    const res = await fetch(`data/passages/${id}.json`);
    d = await res.json();
  } catch {
    leftEl.textContent = "无法加载文章。请通过 start.bat 启动本地服务器。";
    return;
  }
  const v = validatePassage(d);
  if (!v.ok) { leftEl.textContent = "文章数据有误:" + v.errors.join("; "); return; }
  PASSAGE = d;
  srcEl.textContent = `${d.source} — ${d.title}`;

  // 左:按 para 分段
  let curPara = null, pEl = null;
  for (const s of d.sentences) {
    if (s.para !== curPara) {
      pEl = document.createElement("p");
      leftEl.appendChild(pEl);
      curPara = s.para;
    }
    pEl.appendChild(renderSentenceEN(s));
    pEl.appendChild(document.createTextNode(" "));
  }
  // 右:讲解卡片,全部展开
  for (const s of d.sentences) {
    const c = document.createElement("div");
    c.className = "gcard"; c.dataset.sid = s.id;
    const wordsLine = s.words.length
      ? `<div class="gwords">生词:${s.words.map((w) => `${w.w} ${w.def}`).join(" / ")}</div>` : "";
    c.innerHTML = `
      <div class="gtype">【句${s.id}】${s.grammar.type}</div>
      <div class="gnote">拆解:${s.grammar.note}</div>
      <div class="gzh">翻译:${s.zh}</div>
      ${wordsLine}`;
    c.addEventListener("click", () => activate(s.id));
    rightEl.appendChild(c);
  }

  // 翻译显隐
  document.getElementById("toggle-zh").addEventListener("click", (e) => {
    document.body.classList.toggle("hide-zh");
    e.target.textContent = document.body.classList.contains("hide-zh") ? "显示翻译" : "隐藏翻译";
  });

  // 从生词库跳转带 sentence 参数 → 自动定位
  if (jumpSentence) activate(Number(jumpSentence));
}
main();
```

- [ ] **Step 4: 手测(服务器需运行)**

浏览器打开 `http://localhost:8000/reader.html?id=sample`。逐项确认:
- 左侧显示 2 句英文,成段。
- 点句子空白处 → 该句左侧高亮(浅绿),右侧对应卡片高亮并滚动居中。
- 点单词 `right-handed` → 弹气泡显示"惯用右手的 / adj.",有"+ 入库"按钮。
- 点"+ 入库" → 按钮变"已入库",原文该词变绿色下划线。
- 刷新页面 → 该词仍为绿色(已持久化)。
- 点顶部"隐藏翻译" → 右侧"翻译:"行消失;再点恢复。
Expected: 全部符合。

- [ ] **Step 5: 记录产物**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && ls reader.html js/reader.js && echo TASK5_DONE
```
Expected: 路径 + `TASK5_DONE`

---

## Task 6: 生词库 vocab.html + vocab.js

**目的:** 查看/搜索/删除生词,导入导出,点出处跳回原文。

**Files:**
- Create: `ROOT/vocab.html`
- Create: `ROOT/js/vocab.js`
- Modify: `ROOT/css/style.css`(追加表格样式)

- [ ] **Step 1: 追加生词库样式到 `css/style.css`**

末尾追加:
```css
/* ---- 生词库 ---- */
.vocab-tools { display: flex; gap: 10px; align-items: center; margin-bottom: 14px; flex-wrap: wrap; }
.vocab-tools input[type=text] { padding: 6px 10px; border: 1px solid #ccc; border-radius: 6px; }
.vocab-tools button, .vocab-tools label.filebtn {
  background: var(--green); color: #fff; border: none; border-radius: 6px;
  padding: 6px 12px; cursor: pointer; font-size: 14px;
}
.vocab-count { color: var(--muted); margin-left: auto; }
table.vocab { width: 100%; border-collapse: collapse; background: var(--card); border-radius: 8px; overflow: hidden; }
table.vocab th, table.vocab td { padding: 8px 10px; border-bottom: 1px solid #eee; text-align: left; font-size: 14px; vertical-align: top; }
table.vocab th { background: #eef7ef; }
table.vocab .src-link { color: var(--green-dark); cursor: pointer; text-decoration: underline; }
table.vocab .del { color: #c0392b; cursor: pointer; }
```

- [ ] **Step 2: 写 `vocab.html`**

`ROOT/vocab.html`:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>生词库</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <header class="topbar">
    <h1>雅思阅读精读器</h1>
    <a href="index.html">文章库</a>
    <a href="vocab.html">生词库</a>
  </header>
  <div class="container">
    <div class="vocab-tools">
      <input type="text" id="search" placeholder="搜索单词或出处…" />
      <button id="export">导出 JSON</button>
      <label class="filebtn">导入 JSON<input type="file" id="import" accept="application/json" hidden /></label>
      <span class="vocab-count" id="count"></span>
    </div>
    <table class="vocab">
      <thead>
        <tr><th>单词</th><th>释义</th><th>例句</th><th>出处</th><th>时间</th><th></th></tr>
      </thead>
      <tbody id="rows"></tbody>
    </table>
    <p id="empty" style="display:none;color:var(--muted);margin-top:16px">生词库还是空的。去阅读文章时点单词入库吧。</p>
  </div>
  <script type="module" src="js/vocab.js"></script>
</body>
</html>
```

- [ ] **Step 3: 写 `js/vocab.js`**

`ROOT/js/vocab.js`:
```javascript
import { loadAll, removeWord, exportJSON, importJSON } from "./store.js";

const rowsEl = document.getElementById("rows");
const countEl = document.getElementById("count");
const emptyEl = document.getElementById("empty");
const searchEl = document.getElementById("search");

function render(filter = "") {
  const all = loadAll().slice().sort((a, b) => (b.added_at || "").localeCompare(a.added_at || ""));
  const f = filter.trim().toLowerCase();
  const list = f
    ? all.filter((e) => e.word.toLowerCase().includes(f) || (e.source || "").toLowerCase().includes(f))
    : all;
  rowsEl.innerHTML = "";
  emptyEl.style.display = all.length === 0 ? "block" : "none";
  for (const e of list) {
    const tr = document.createElement("tr");
    const srcCell = e.passage_id
      ? `<span class="src-link" data-pid="${e.passage_id}" data-sid="${e.sentence_id ?? ""}">${e.source}</span>`
      : (e.source || "");
    tr.innerHTML = `
      <td>${e.word} <span style="color:#999">${e.pos || ""}</span></td>
      <td>${e.def || ""}</td>
      <td>${e.sentence_en || ""}</td>
      <td>${srcCell}</td>
      <td>${e.added_at || ""}</td>
      <td><span class="del" data-word="${e.word}">删除</span></td>`;
    rowsEl.appendChild(tr);
  }
  countEl.textContent = `共 ${all.length} 个生词`;
}

rowsEl.addEventListener("click", (ev) => {
  const del = ev.target.closest(".del");
  if (del) { removeWord(del.dataset.word); render(searchEl.value); return; }
  const link = ev.target.closest(".src-link");
  if (link) {
    const pid = link.dataset.pid, sid = link.dataset.sid;
    location.href = `reader.html?id=${encodeURIComponent(pid)}${sid ? `&sentence=${sid}` : ""}`;
  }
});

searchEl.addEventListener("input", () => render(searchEl.value));

document.getElementById("export").addEventListener("click", () => {
  const blob = new Blob([exportJSON()], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ielts-vocab.json";
  a.click();
});

document.getElementById("import").addEventListener("change", async (ev) => {
  const file = ev.target.files[0];
  if (!file) return;
  const text = await file.text();
  try {
    const r = importJSON(text);
    alert(`导入成功,现共 ${r.total} 个生词。`);
    render(searchEl.value);
  } catch (e) {
    alert("导入失败:" + e.message);
  }
  ev.target.value = "";
});

render();
```

- [ ] **Step 4: 手测(服务器运行 + 先在阅读器入过词)**

浏览器打开 `http://localhost:8000/vocab.html`:
- 显示之前入库的词(如 right-handed),"共 N 个生词"。
- 搜索框输入词的一部分 → 列表实时过滤。
- 点"出处" → 跳到 `reader.html?id=sample&sentence=...` 并高亮该句。
- 点"导出 JSON" → 下载 `ielts-vocab.json`。
- 点"删除" → 该行消失,计数减一。
- 点"导入 JSON"选刚下载的文件 → 提示导入成功,词回来。
Expected: 全部符合。

- [ ] **Step 5: 记录产物**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && ls vocab.html js/vocab.js && echo TASK6_DONE
```
Expected: 路径 + `TASK6_DONE`

---

## Task 7: 预处理工具 find_page.py + render_page.py

**目的:** 把"定位文章页码"和"渲染页面为高清图(可裁栏)"固化成可复用脚本,供 Claude 读图抄录。

**Files:**
- Create: `ROOT/tools/find_page.py`
- Create: `ROOT/tools/render_page.py`

- [ ] **Step 1: 写 `tools/find_page.py`**

`ROOT/tools/find_page.py`:
```python
"""在 PDF 中按关键词(通常文章标题)定位页码(0基)。
用法: python tools/find_page.py "<pdf路径>" "AIRPORTS ON WATER"
输出匹配到的页码及该页字符数。
"""
import sys
import pdfplumber

def main():
    pdf_path, keyword = sys.argv[1], sys.argv[2]
    with pdfplumber.open(pdf_path) as pdf:
        hits = []
        for i, pg in enumerate(pdf.pages):
            t = pg.extract_text() or ""
            if keyword.lower() in t.lower():
                hits.append((i, len(t), round(pg.width), round(pg.height)))
        if not hits:
            print(f"未找到 '{keyword}'"); sys.exit(1)
        for i, n, w, h in hits:
            print(f"页码(0基)={i}  字符数={n}  页宽高={w}x{h}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 用剑2 验证 find_page**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/find_page.py "C:/Users/11386/Desktop/雅思/雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）/剑桥雅思真题1-19/【2】剑桥雅思真题2.pdf" "AIRPORTS ON WATER"
```
Expected: 输出含 `页码(0基)=5`(与探索一致)。

- [ ] **Step 3: 写 `tools/render_page.py`**

`ROOT/tools/render_page.py`:
```python
"""把 PDF 指定页高清渲染为 PNG,可选按 x 比例裁成竖条(便于读清多栏)。
用法:
  python tools/render_page.py "<pdf>" <page0based> <out_dir> [scale] [ncols]
- scale 默认 4.0
- ncols 默认 1(不切栏);>1 时把页面按等宽切成 ncols 张竖条图(仅用于"看清",抄录顺序由人判断)
输出: out_dir/page{page}_full.png,以及若 ncols>1 则 page{page}_col{k}.png
"""
import sys, os
import pypdfium2 as pdfium

def main():
    pdf_path = sys.argv[1]
    page_no = int(sys.argv[2])
    out_dir = sys.argv[3]
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    ncols = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    os.makedirs(out_dir, exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[page_no]
    img = page.render(scale=scale).to_pil()
    W, H = img.size
    full = os.path.join(out_dir, f"page{page_no}_full.png")
    img.save(full)
    print("saved", full, img.size)
    if ncols > 1:
        colw = W / ncols
        for k in range(ncols):
            crop = img.crop((int(k * colw), 0, int((k + 1) * colw), H))
            p = os.path.join(out_dir, f"page{page_no}_col{k+1}.png")
            crop.save(p)
            print("saved", p, crop.size)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 用剑2 P1 验证 render_page(渲染并裁 2 条)**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/render_page.py "C:/Users/11386/Desktop/雅思/雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）/剑桥雅思真题1-19/【2】剑桥雅思真题2.pdf" 5 "C:/Users/11386/AppData/Local/Temp/claude/C--Users-11386-Desktop---/8ff3ffd7-779f-45d4-9c65-27d90695581f/scratchpad/render_test" 4.0 2
```
Expected: 打印 `page5_full.png (3320, 2456)`、`page5_col1.png`、`page5_col2.png` 三行 saved。

- [ ] **Step 5: 记录产物**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && ls tools/find_page.py tools/render_page.py && echo TASK7_DONE
```
Expected: 路径 + `TASK7_DONE`

---

## Task 8: 生成第一篇真实文章 c2-test1-p1(读图抄录 + 逐句讲解)

**目的:** 用真实数据替换示例,验证端到端体验。这是 Claude 的模型工作,非纯脚本。

**Files:**
- Create: `ROOT/data/passages/c2-test1-p1.json`
- Modify: `ROOT/data/index.json`(加入该篇;可保留 sample 或移除)

- [ ] **Step 1: 渲染剑2 P1 页面图供抄录**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/render_page.py "C:/Users/11386/Desktop/雅思/雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）/剑桥雅思真题1-19/【2】剑桥雅思真题2.pdf" 5 "C:/Users/11386/AppData/Local/Temp/claude/C--Users-11386-Desktop---/8ff3ffd7-779f-45d4-9c65-27d90695581f/scratchpad/c2p1" 4.0 2
```
Expected: 生成 `c2p1/page5_col1.png` 与 `page5_col2.png`。

- [ ] **Step 2: 读图抄录正确原文(Claude 用 Read 读两张 col 图)**

用 Read 工具读 `page5_col1.png` 与 `page5_col2.png`,按栏顺序抄录 Passage 1 全文(约 2 段起,视文章而定)。**这是模型工作:确保语序连贯、无串栏、拼写与标点正确。** 抄录结果作为下一步逐句拆分的输入。
(注:文章可能跨到第 6 页的题目区之前结束;正文若跨页,追加渲染下一页并接续。)

- [ ] **Step 3: 逐句生成数据并写 `data/passages/c2-test1-p1.json`**

将抄录原文按句拆分,逐句写 en/zh/grammar(type+note)/words,遵循 Task 1 sample.json 的结构。段落用 `para` 标注。示例首句(实际以抄录为准):
```json
{
  "id": "c2-test1-p1",
  "source": "剑桥雅思2 · Test 1 · Passage 1",
  "title": "Airports on Water",
  "sentences": [
    {
      "id": 1, "para": 1,
      "en": "River deltas are difficult places for map makers.",
      "zh": "对于制图者来说,河流三角洲是很难处理的地方。",
      "grammar": {
        "type": "主系表(简单句)",
        "note": "主语 River deltas,系动词 are,表语 difficult places;for map makers 为介词短语作状语,说明'对谁而言难'。"
      },
      "words": [
        { "w": "delta", "pos": "n.", "def": "(河流)三角洲" }
      ]
    }
  ]
}
```

- [ ] **Step 4: 更新 `data/index.json`**

把 c2-test1-p1 加入 passages 数组(sentence_count 填实际句数)。是否保留 sample 由执行者决定(建议移除 sample,保持库干净):
```json
{
  "passages": [
    { "id": "c2-test1-p1", "source": "剑桥雅思2 · Test 1 · Passage 1", "title": "Airports on Water", "sentence_count": 0 }
  ]
}
```
(sentence_count 改为实际值。)

- [ ] **Step 5: 运行数据校验**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/validate_data.py
```
Expected: `OK: N 篇文章 … 全部通过。`(句数与 index 一致;若报 sentence_count 不符,回改 index。)

- [ ] **Step 6: 端到端手测**

服务器运行,打开 `http://localhost:8000/index.html` → 点"Airports on Water" → 阅读器逐句精读、点词入库、翻译显隐、生词库查看与跳回,全流程走一遍。
Expected: 与 sample 相同的交互,但内容为真实剑2 P1。

- [ ] **Step 7: 记录产物**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/validate_data.py && ls data/passages/c2-test1-p1.json && echo TASK8_DONE
```
Expected: 校验 OK + 路径 + `TASK8_DONE`

---

## Task 9: 补齐剑2 Test1 另外两篇 + 收尾

**目的:** 产出 Passage 2、Passage 3,凑齐一个完整 Test 的阅读,验证多篇场景。

**Files:**
- Create: `ROOT/data/passages/c2-test1-p2.json`
- Create: `ROOT/data/passages/c2-test1-p3.json`
- Modify: `ROOT/data/index.json`

- [ ] **Step 1: 定位并渲染 Passage 2 / 3 页面**

先用 find_page 找标题页码(Passage 2 标题可用其正文首个显著短语;Passage 3 标题同理),再 render_page 渲染:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/find_page.py "<剑2 pdf 路径>" "<Passage2 标志词>"
```
然后 `python tools/render_page.py "<剑2 pdf>" <页码> "<scratch>/c2p2" 4.0 2`(P3 同法)。
(注:Passage 3 常带 List of Headings 等题型说明,抄录时只取文章正文,跳过题目。)

- [ ] **Step 2: 读图抄录 + 逐句生成 c2-test1-p2.json**

同 Task 8 Step 2-3,产出 `data/passages/c2-test1-p2.json`。

- [ ] **Step 3: 读图抄录 + 逐句生成 c2-test1-p3.json**

同上,产出 `data/passages/c2-test1-p3.json`。

- [ ] **Step 4: 更新 index.json(三篇齐全)**

`data/index.json` 的 passages 含 c2-test1-p1/p2/p3,各自 sentence_count 为实际值。

- [ ] **Step 5: 全量校验 + 手测文章库**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/validate_data.py
```
Expected: `OK: 3 篇文章 … 全部通过。`
浏览器打开首页:三张卡片;逐篇点进可精读;生词跨文章入库、生词库出处正确跳回对应文章。

- [ ] **Step 6: 记录完成**

Run:
```bash
cd "C:/Users/11386/Desktop/雅思/ielts-app" && python tools/validate_data.py && ls data/passages/ && echo ALL_DONE
```
Expected: 校验 OK + 三个 json + `ALL_DONE`

---

## 完成标准(Definition of Done)
- `python tools/validate_data.py` 通过,3 篇剑2 Test1 阅读入库。
- 双击 `start.bat` 起服务器,首页/阅读器/生词库三页均正常。
- 阅读器:点句联动高亮、点词气泡+释义、入库标色去重、翻译显隐,均工作。
- 生词库:列表/搜索/删除/导入导出/出处跳回,均工作。
- `node js/sample-check.mjs` 全绿。
- 生词数据含 status/review 预留字段,为背单词子项目铺路。
