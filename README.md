# 雅思备考平台（阅读精读器 + 语法书 + 听力精听 + 词汇联想）

一个纯静态的本地雅思备考工具。核心是阅读精读：左边剑桥雅思原文，右边逐句语法拆解 + 中文翻译，点单词可入生词库，配套真题题目与答案。在此之上还有：

- **深度句子解析**：按《语法俱乐部》(旋元佑) 框架，逐句给出五大句型主干、成分拆解、语法点、词汇词根词缀 + 同义替换、表达积累（面向基础薄弱的考生，大白话讲解）。
- **同义替换考点**：每道题标注「题干 ⇄ 原文」的替换映射——雅思阅读/听力的核心考点。
- **语法书**：内置《语法俱乐部》知识库，句子里的语法标签可点击跳转到书中对应章节。
- **听力精听**：逐句遮罩精听 + 变速 + AB 复读 + 听写判分（剑桥真题音频）。
- **词汇联想**：词根词缀色块、同根词族、近义词延伸、间隔重复复习。
- **AI 深挖**（可选）：配置 DeepSeek API Key 后，可对任意句子实时生成深度解析。

无需框架、无需构建；预生成内容为本地数据，AI 与部分版权资源为可选的本地增强。

## 在线使用（推荐）

直接打开网址即可，任何电脑、手机浏览器都能用，无需安装任何东西：

**👉 https://userheyy.github.io/ielts-reader/**

> 部署在 GitHub Pages 上。作者 `git push` 更新后，刷新页面就是最新内容。

## 本地运行

想在本地离线用，或者自己改代码：

1. 安装 **Python 3**（Windows 安装时勾选 “Add Python to PATH”）
2. 下载本仓库（`git clone` 或点绿色 **Code → Download ZIP** 解压）
3. **Windows**：双击 `start.bat`，浏览器会自动打开
   **Mac / Linux**：在项目目录执行 `python3 -m http.server 8000`，再浏览器打开 `http://127.0.0.1:8000`

> 必须通过本地服务器打开，不能直接双击 `index.html`（浏览器的 `file://` 安全限制会导致文章数据加载失败）。

## 目前收录

- **24 篇**精读文章，全部为「老师精修」质量（逐句语法 + 地道翻译 + 生词 + 真题答案）
  - 剑桥雅思 17：Test 1–4，共 12 篇
  - 剑桥雅思 19（A类）：Test 1–4，共 12 篇

## 功能

- 左右对照：原文 ↔ 逐句精讲，点句子/点单词左右联动
- 语法拆解：每句标注句式类型 + 主干与修饰关系；有深度解析的句子额外展开「句型主干/成分拆解/语法点/词汇深挖/同义替换/表达积累」
- 同义替换：题目核对后展示「题干 ⇄ 原文」考点替换 chips，点击定位原文并高亮
- 语法书（`grammar.html`）：《语法俱乐部》知识库，语法标签可跳转
- 听力精听（`listening.html`）：逐句遮罩、变速 0.5–1.5×、单句循环、AB 复读、逐句听写判分、打点模式
- 生词库：点原文单词入库，`vocab.html` 复习（间隔重复）；`library.html` 浏览内置词库
- 真题题目：录入原题与标准答案，可自测、可「定位原文」跳转
- 朗读：浏览器语音朗读单句 / 单词
- 设置（`settings.html`）：配置 DeepSeek API Key（仅存本浏览器），启用「AI 深挖本句」
- 全量备份：导出/导入你的生词库与学习记录

## 本地专属增强（可选，不影响在线基础功能）

以下三类资源涉及版权或密钥，**只存在于你本地、不会提交到仓库**（已在 `.gitignore` 屏蔽）。线上/未配置时相关页面会优雅降级，给出安装提示，不会报错。

1. **DeepSeek AI 深挖**
   - 复制 `tools/config.local.json.example` 为 `tools/config.local.json`，填入你的 API Key（用于 `tools/` 批量生成脚本）
   - 或直接在网页「设置」页填入 Key（存浏览器 localStorage，用于「AI 深挖本句」按钮）
   - ⚠️ Key 绝不要写进任何会提交的文件；若曾泄露请到 DeepSeek 后台重置
2. **《语法俱乐部》语法书**
   - `py tools/extract_grammar_book.py --epub "你的 语法俱乐部.epub 路径"`
   - 生成 `data/local/grammar-book.json`（版权内容，仅本地）
3. **剑桥听力音频 + 转写**
   - 音频按 `media/audio/{册}-{test}-part{n}.mp3` 命名放入（见 `media/audio/README.md`）
   - 逐句转写 `data/listening/*.json`（版权内容，仅本地；`index.json` 除外）
   - 时间戳可用 `listening.html?id=...&annotate=1` 打点模式边听边补

## 目录结构

```
ielts-reader/
├── index.html          文章列表首页
├── reader.html         精读页（左右对照 + 深度解析）
├── listening.html      听力精听
├── grammar.html        语法书（语法俱乐部）
├── vocab.html / library.html / daily.html / test.html   词汇复习/词库/打卡/测试
├── settings.html       设置（DeepSeek API Key）
├── start.bat           Windows 一键启动本地服务器
├── data/
│   ├── index.json          文章索引
│   ├── dict.json           内置词典
│   ├── grammar-tags.json   语法标签白名单（三方共享契约）
│   ├── passages/           每篇文章一个 JSON（原文+讲解+deep+题目）
│   ├── listening/          听力：index.json 可提交，转写 *.json 仅本地
│   └── local/              语法书提取产物（仅本地，gitignore）
├── media/audio/        剑桥听力音频（仅本地，gitignore）
├── js/                 前端逻辑（reader/deep/aids/listening/grammar/ai …）
├── css/                样式
└── tools/              数据生成脚本（Python：DeepSeek 生成、语法书提取、校验）
```

## 更新文章

作者更新流程：编辑 / 新增 `data/passages/*.json` 与 `data/index.json` → `git commit` → `git push`。
在线版会自动更新；本地版重新 `git pull` 即可。**其他人无需再拷整个文件夹。**

## 版权说明

文章原文出自剑桥大学出版社《剑桥雅思官方真题集》，版权归原出版社所有；语法讲解框架参考旋元佑《英语魔法师之语法俱乐部》。本仓库仅供个人学习使用。**听力音频、听力逐句转写、语法书提取内容均为版权材料，只保存在本地、不随仓库分发**（已在 `.gitignore` 屏蔽）。
