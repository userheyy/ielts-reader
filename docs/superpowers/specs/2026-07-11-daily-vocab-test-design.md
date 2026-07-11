# 每日单词 Test（从打卡词池现场组卷）设计

日期：2026-07-11

## 背景与目标

现有 `test.html`（生词页「测试」tab，iframe 嵌入 `test.html?embed=1`）是**完形填空**题型，题目来自**静态** `data/quiz-bank.json`（约 732 道固定题），与用户实际学过什么**脱节**，每组 10 题。

本次改造：把单词测试改成**从用户打卡过的词现场组卷**的「每日 test」，每次最多 **100 题**，**中英互选**题型。让 test 成为对「已打卡内容」的真实检验，词池随学习自动增长。

## 术语：什么是「打卡过的词」

一个词算「打卡过」= 它有 SRS 复习记录（用户通过每日任务 daily.html 学过 / 复习过）。两个来源：

1. **内置词**：`localStorage['ielts_vocab_seed_review']` 里出现的词（key 为小写词）。完整词条从 `data/vocab-seed.json`（3566 词，均带 `def`）取。
2. **阅读生词**：`localStorage['ielts_vocab']` 里 `review.correct + review.wrong + review.fuzzy > 0` 的词（真正复习过的，排除只收藏未复习的）。

两来源按小写去重，**生词优先**（与 `seed.js` 的 `buildReviewPool` 去重规则一致）。

> 注：仅当词条有非空中文 `def` 时才可入池（组卷需要中文释义）。seed 全 3566 词都有 def；生词 def 可能为空，为空则跳过。

## 7 项已定决策

| # | 决策点 | 选择 |
|---|---|---|
| 1 | 词池 | 只出打卡学过的词（seed_review ∪ 复习过的生词） |
| 2 | 词池不足 100 | 有多少考多少（上限 100），页面提示「打卡词库共 N 词」 |
| 3 | 每日机制 | 每次进重新随机抽（不绑日期、无「今日已完成」状态，纯刷题） |
| 4 | 题型 | 中英互选，4 选 1 |
| 5 | 方向 | 两个方向混合：一部分「看中文选英文」，一部分「看英文选中文」，逐题随机 |
| 6 | 干扰项 | 从打卡词池随机抽 3 个（不限词性，只来自打卡词） |
| 7 | 错题 | 沿用现有错题本 `test-store.js`（进错题本 / 只刷错题 / 连对 2 次移出） |

## 架构

### 新增模块 `js/test-pool.js`（纯逻辑，无 DOM，可 Node 测试）

职责一：**收集打卡词池**。

```
buildTestPool() -> [{ word, def, pos }]
  1. 从 vocab-seed.json 取 seedIndex（Map<wordLower, entry>）
  2. 遍历 ielts_vocab_seed_review 的 key：命中 seedIndex 且 def 非空 → 入池（origin: 'seed'）
  3. 遍历 ielts_vocab：review 计数和 > 0 且 def 非空 → 入池（origin: 'vocab'，覆盖同名 seed）
  4. 按 word 小写去重返回
```

职责二：**组卷**。

```
buildQuestions(pool, count = 100, opts?) -> [question]
  - 考点词 = 从 pool 随机抽 min(count, pool.length) 个（不重复）
  - 每个考点词生成一题 buildOneQuestion(word, pool)

buildOneQuestion(target, pool):
  - direction = 随机 'zh2en'（看中文选英文）或 'en2zh'（看英文选中文）
  - 干扰词 = 从 pool 里排除 target 后随机抽 3 个
  - zh2en：stem = target.def（中文）；选项文本 = [target, ...干扰].word（英文）
  - en2zh：stem = target.word（英文）；选项文本 = [target, ...干扰].def（中文）
  - 选项按「显示文本」去重（防同义 def 撞车）；不足 4 个则从 pool 继续补抽
  - 选项打乱，标出正确项
  - 返回 { word, direction, stem, options:[{text, correct}], target:{word,def,pos} }
```

组卷函数接受可注入的 `random`（默认 `Math.random`）与 `seedIndex`（默认 fetch），便于 Node 单测绕过随机与网络。

### 改造 `js/test.js`

- 删除 `loadBank() / BANK_URL / bankByWord` 及完形填空专用渲染（`renderStem` 挖空、题干悬停查词、`renderExplain` 的挖空回填）。
- `GROUP_SIZE` 10 → 常量 `TEST_SIZE = 100`。
- 初始化：`pool = await buildTestPool()`；首页统计加一行「当前打卡词库共 N 词」。
- `startSession('normal')`：`buildQuestions(pool, TEST_SIZE)`。
- `startSession('wrong')`：用 `wrongWords()` ∩ pool 的词，对每词 `buildOneQuestion`（错题也用相同题型/随机方向）。
- 渲染改为「题干 stem + 4 个纯文本选项」，支持两种方向：
  - 题干上方标注方向徽标（如「看中文选英文」/「看英文选中文」）。
  - 作答后解析区：显示 `word /音标/`、完整中文 def、词性、例句（有则显示 seed 的 `sentence_en/zh`）、🔊 读单词。不再做挖空回填。
- 错题本调用（`recordResult / wrongWords / wrongCount / summary`）保持不变。

### 入口（不改）

生词页 `vocab.html` 的「测试」tab 继续 iframe 嵌 `test.html?embed=1`。tab 名「测试」、iframe title、`?embed` 逻辑均不动。

### 不再需要的文件

`data/quiz-bank.json` 改造后不再被引用。**保留不删**（同事可能另有用途 / 避免破坏其分支），仅从 test.js 断开引用。

## 数据流

```
打开 test.html
  → test-pool.buildTestPool() 读 localStorage(seed_review + vocab) + fetch vocab-seed.json
  → 打卡词池 [{word, def, pos}]
  → 首页显示「打卡词库共 N 词」+ 错题数
  → 点「开始测试」→ buildQuestions(pool, 100)
      每题：随机方向 + 池内随机 3 干扰 + 选项文本去重/补足 + 打乱
  → 逐题作答 → recordResult 记错题本 → 结果页（分数 / 本轮错题）
  → 「只刷错题」用错题词重新组卷
```

## 边界情况

| 情况 | 表现 |
|---|---|
| 打卡词池为空 | 禁用「开始」，提示「还没有打卡过的词，先去『今日』学一些词再来测试」 |
| 打卡词 1~3 | 禁用「开始」，提示「打卡词不足 4 个，凑不齐四个选项」 |
| 打卡词 4~99 | 有多少考多少（N 词→N 题），首页提示词库共 N 词 |
| 打卡词 ≥ 100 | 随机抽 100 |
| 同题选项文本撞车 | 按显示文本去重，从池内继续补抽至 4 个；池太小补不齐则该题选项数 < 4（仅极端情况，池<4 已被拦截） |
| 只刷错题时错题词已很少 | 有几个考几个；错题本空时按钮禁用（现有逻辑） |

## 测试策略

- **Node 单测** `js/test-pool-check.mjs`（仿照现有 `*-check.mjs` 风格，注入内存 localStorage + 假 seedIndex + 固定 random）：
  - 空池 / 小池（<4）/ 正常池；
  - 组卷题数 = min(100, poolSize)；
  - 每题恰好 1 个正确项、选项文本不重复；
  - 两种方向都能生成且 stem/选项对应正确（zh2en 选项是英文、en2zh 选项是中文）；
  - 干扰项都来自池内。
- **浏览器验收**：用 Claude Preview 起本地静态服务器，手动注入若干 seed_review/vocab 记录，打开 test.html 走完一轮：核对方向混合、选项、解析、错题进本、只刷错题。

## 非目标（YAGNI）

- 不做「每日固定一套/今日已完成」日期状态（决策 3 选了纯随机）。
- 不做完形填空、拼写题、混合题型（决策 4 选了中英互选）。
- 不做同词性干扰（决策 6 选了随机干扰）。
- 不改 vocab.html、daily 流程、SRS、quiz-bank 生成工具。
- 不删 quiz-bank.json。
