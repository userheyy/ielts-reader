# 题库生成状态

## 当前策略

题库生成不采用“PDF/OCR 直接导入即完成”的方式，而是分两层：

### 第一层：识别底稿

OCR、PDF 文字层或多模态识图只作为底稿来源，用来获得：

- 原文切句
- 题目
- 标准答案
- 原文定位

### 第二层：老师精修

每篇文章必须由雅思老师视角把关：

- 校对原文顺序，尤其是双栏 PDF、跨页、表格题
- 核对答案与定位依据
- 补逐句中文翻译
- 补句法/语法拆解
- 补固定短语和高频词，避免短语被拆词误译

只有完成第二层，状态才标记为 `teacher_refined`。

## 已归档旧文章

旧的剑雅 2 / 剑雅 13 示例文章已移到：

`data/passages_archive/pre_c14_19_seed/`

首页索引已清空旧文章，只显示新题库。

## 已入库

| 书 | Test | Passage | 标题 | 状态 |
|---|---:|---:|---|---|
| 剑雅 17 | 1 | 1 | The development of the London underground railway | 老师精修已完成 |
| 剑雅 17 | 1 | 2 | Stadiums: past, present and future | 老师精修已完成 |
| 剑雅 17 | 1 | 3 | To catch a king | 老师精修已完成 |
| 剑雅 17 | 2 | 1 | The Dead Sea Scrolls | 老师精修已完成 |
| 剑雅 17 | 2 | 2 | A second attempt at domesticating the tomato | 老师精修已完成 |
| 剑雅 17 | 2 | 3 | Insight or evolution? | 老师精修已完成 |
| 剑雅 17 | 3 | 1 | The thylacine | 老师精修已完成 |
| 剑雅 17 | 3 | 2 | Palm oil | 老师精修已完成 |
| 剑雅 17 | 3 | 3 | Building the Skyline: The Birth and Growth of Manhattan’s Skyscrapers | 老师精修已完成 |
| 剑雅 17 | 4 | 1 | Bats to the rescue | 老师精修已完成 |
| 剑雅 17 | 4 | 2 | Does education fuel economic growth? | 老师精修已完成 |
| 剑雅 17 | 4 | 3 | Timur Gareyev – blindfold chess champion | 老师精修已完成；正文建议后续 OCR 二刷 |

当前首页索引文章数：12 篇。

当前质量分布：

- `teacher_refined`: 12 篇
- `draft_raw`: 0 篇

## PDF 可抽取性审计

审计脚本：

`tools/audit_cambridge_pdfs.py`

审计结果：

| 书 | 文字层状态 | 处理方式 |
|---|---|---|
| 剑雅 14 | 几乎无文字层 | 需要 OCR |
| 剑雅 15 | 文字层不稳定 | 建议 OCR |
| 剑雅 16 | 几乎无文字层 | 需要 OCR |
| 剑雅 17 | 文字层可用 | 可直接抽取 |
| 剑雅 18 | 几乎无文字层 / 有水印文字 | 需要 OCR |
| 剑雅 19 | 文字层不稳定 | 建议 OCR |

审计 JSON：

`tmp/cambridge_pdf_audit.json`

## 下一步

1. 剑雅 17 的 12 篇已全部进入可学习版题库。
2. Test 4 Passage 3 因 PDF 文字层/双栏顺序异常，已修正标题、题目、答案、短语和语法，但正文建议后续用 OCR 单篇二刷。
3. 下一批建议从剑雅 14 或 18 开始 OCR 产底稿，再按同样流程逐篇精修。
