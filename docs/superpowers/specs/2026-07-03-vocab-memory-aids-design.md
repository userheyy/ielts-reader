# 记忆法背单词系统 — 设计文档

> 雅思学习平台的第二个子系统。在现有生词库(SRS)之上，增加"多种记忆法"（词根词缀 / 词族 / 联想助记 / 词形变化），并内置一批雅思词库供系统化记忆。
> 日期：2026-07-03　状态：设计已与用户逐段确认，待用户 review 后进入实施计划。

---

## 1. 背景与范围

### 用户目标
- 2026 年 9 月左右考雅思 6.5，需要高效记单词。
- 现有背单词只按记忆曲线抽词，用户希望**用更多方法帮助记忆**：联想记忆法、词根词缀法、助记法、词族串联等。
- 这是**内容/助记层**的增强，**不是** SRS 引擎层的改动。

### 本次范围
1. **记忆法数据层**：为单词增加 `aids`（词根词缀拆解 / 词族 / 联想助记 / 词形变化），由 Claude 预生成为本地 JSON，运行时不接 API。
2. **内置雅思词库**：预生成雅思词的 `aids`，存 `data/vocab-seed.json`，随项目内置。**全量目标 = engra `IELTS.json` 的 3575 词**，分批滚动生产（先规范 + 第一批 40 词样板验收，再每批约 40 词做到全覆盖）。
3. **生词库增强**：现有 localStorage 生词库，动态生词通过"备份→回填→恢复"补 `aids`。
4. **三处 UI**：复习抽词卡改造（词根先做提示）、生词库列表可展开记忆法、新增「词库」页承载内置词。

### 明确不在本次范围
- 不改现有 SRS 权重/间隔算法（`store.js` 的 `reviewWeight`/`gradeReview` 原样复用）。
- 不接任何运行时 API（词典/翻译/TTS 之外的外部服务）。
- ④"例句小故事"记忆法——**用户明确否决，不做**。
- 内置词库的展示页做，但不做多设备云同步、不做社交/PK 等。

### 关键决策记录（用户在头脑风暴中逐一拍板）
| 决策点 | 选择 |
|---|---|
| 功能定位 | C：先做生词库增强，schema/UI 面向未来大词库；**并内置一批雅思词** |
| 卡片放哪些记忆法 | ①词根词缀 ②词族串联 ③联想助记 ⑤词形变化（**不要**④小故事） |
| 复习交互 | B：词根当"提示"先给 → 用户靠词根推词义 → 翻面补全其余记忆法 |
| 数据从哪来 | B：Claude 预生成高质量 JSON，开源库当参考原料，不接运行时 API |
| 生词库回填桥 | A：复用现有「备份生词 / 恢复生词备份」按钮，零新增基建 |
| 内置词库范围 | 先 A（高频优先的第一批）→ 后 C（全量 3575 分批滚动） |
| 生产方式 | A：先出规范 + 第一批 40 词样板，验收后每批约 40 词滚动至 3575 |

---

## 2. 关键前提与已验证事实

### 参考项目（已 down 到 `C:\Users\11386\Desktop\单词\`，浅 clone，独立于主项目）
| 仓库 | 许可 | 用途 | 关键文件 |
|---|---|---|---|
| `word-root-workshop` | MIT | **UX 蓝本 + schema**（纯原生无构建，架构孪生） | `js/wordData.js`（`examples[].breakdown:{prefix,root,suffix}`）、`css/minimal.css`（色块） |
| `generated-english-roots-list` | MIT | 词根→释义查表（1061 词根） | `english.roots.list.build.json` |
| `engra` | MIT | 雅思词表 + CEFR/词频分层 | `dict/glossaries/IELTS.json`(3575)、CEFR-A1..C2 等 |
| `ECDICT` | MIT | 词频(`frq`/`bnc`)、词形(`exchange`) | `ecdict.csv` |
| `DictionaryByGPT4` | **CC-BY-SA** | 联想句参考（仅启发，文字重写） | `gptwords.json`（JSONL，8715 词） |

### 已核实的数据现实（决定生成策略）
- `IELTS.json` = **3575 词**（是"全部雅思词汇"，非"高频子集"）。
- 其中 **73%(2629)** 在 DictionaryByGPT4 有现成联想可参考。
- 仅 **29%(1041)** 能自动查到词根拆解 → **词根拆解必须 Claude 逐词判断，不能纯靠查表**。
- `DictionaryByGPT4` 是 **JSONL**（每行一个 `{word, content}`），content 为 markdown，标题含 `### 词根分析 / ### 词缀分析 / ### 记忆辅助` 等；文件是合法 UTF-8（终端乱码只是 codepage 显示问题）。
- **Windows 坑**：`engra` 含 `dict/roots/con.yml`，`con` 是 Windows 保留名，导致 `git checkout` 失败——已用 sparse-checkout 排除该文件成功 clone。

### 本方案的代价（用户已知情）
- 全量 3575 词逐词精做，密度≈精修一篇文章。**每批约 40 词**（一次会话能装下、能保质的粒度），全量约 **70–100 批**滚动完成，非一次性。
- 强行按每批数百词会触发上下文溢出 + 后半批质量崩坏（文章精修已有前车之鉴：超长任务子 agent 易 API stall / 幻觉）——故锁定小批次。

---

## 3. 整体架构

```
                         ┌─────────────────────────────┐
  预处理（离线，Claude）    │  开源库(参考原料，桌面\单词\)   │
                         │  roots-list · ECDICT · GPT4  │
                         └──────────────┬──────────────┘
                                        │ Claude 逐词生成 aids（核对事实 + 写联想）
                                        ▼
   内置词库： data/vocab-seed.json  ◄─── tools/gen_seed_aids.py（+ validate）
   动态生词： localStorage(ielts_vocab) ◄─ 备份→回填(tools/backfill_aids.py)→恢复
                                        │
                                        ▼ 运行时只读，不接 API
                         ┌─────────────────────────────┐
                         │  静态网页（无框架原生 JS）      │
                         │  vocab.html（复习+列表）       │
                         │  library.html（内置词库，新）  │
                         └─────────────────────────────┘
```

### 技术选型
- 与主项目一致：纯静态、无框架、无构建、ES module（`js/*.js`）、本地 `python -m http.server`。
- 复用现有：`store.js`(SRS)、`speech.js`(TTS)、`profile-backup.js`(备份)。
- 新增 JS 模块：`js/aids.js`（渲染 `aids` 的卡片组件，供复习/列表/词库三处共用）、`js/library.js`（词库页逻辑）、`js/seed.js`（加载 `vocab-seed.json` 并与 localStorage 生词合并进复习池）。

### 为什么这么选
- 记忆法数据是"静态知识"，正好落在项目已验证的"Claude 预生成 JSON、网页只展示"方法论上。
- 内置词与生词共用 `aids` 结构 + 同一套 `aids.js` 渲染 + 同一套 SRS，零重复、面向未来大词库零重构。

---

## 4. 数据结构（系统核心）

### 4.1 `aids` 对象（挂在每条单词记录上）
```jsonc
"aids": {
  "morphemes": [                              // ①词根词缀：有序词素
    { "text": "pre",  "type": "prefix", "gloss": "在前面" },
    { "text": "dict", "type": "root",   "gloss": "说" }
    // type ∈ prefix | root | suffix | connector
  ],
  "derivation": "pre(在前)+dict(说) → 事先说出 → 预测",   // 一句话推导（可为空）
  "family": {                                 // ②词族串联（可为空）
    "root": "dict",
    "gloss": "说",
    "words": [
      { "word": "dictate",    "def": "口述/命令" },
      { "word": "contradict", "def": "反驳（对着说）" }
    ]
  },
  "mnemonic": "开口说话前就已知道结果，即预言",            // ③联想助记（宁缺毋滥，可为空）
  "forms": [                                  // ⑤词形变化（可为空）
    { "word": "prediction",  "pos": "n.",   "def": "预测" },
    { "word": "predictable", "pos": "adj.", "def": "可预测的" }
  ]
}
```
**字段规则**
- 所有子字段**允许为空/缺省**：`morphemes: []`、`family: null`、`mnemonic: ""`、`forms: []` 均合法。
- 不规则词（无有意义词根，如 `abandon`）：`morphemes` 留空、`derivation` 留空，靠 `mnemonic` 记；**不强拆**。
- `mnemonic` **宁缺毋滥**：只有能给出有画面感、不牵强的联想时才写，否则留空。禁模板套话。

### 4.2 内置词库 `data/vocab-seed.json`
```jsonc
{
  "meta": {
    "source": "engra IELTS.json (3575) 分批滚动",
    "generated_batches": 1,          // 已生产批次数
    "total_target": 3575,
    "attribution": "词根参考 generated-english-roots-list(MIT)、词形参考 ECDICT(MIT)、联想参考 DictionaryByGPT4(CC-BY-SA，文字经重写)"
  },
  "words": [
    {
      "word": "predict",
      "phonetic": "prɪˈdɪkt",
      "pos": "v.",
      "def": "预测、预言",
      "sentence_en": "Economists predict that house prices will rise.",
      "sentence_zh": "经济学家预测房价将上涨。",
      "cefr": "B2",
      "freq_rank": 1234,             // 供选词排序与"高频优先"
      "aids": { /* 见 4.1 */ }
    }
  ]
}
```
- 追加式：后续批次往 `words` 里加，`generated_batches` 递增。**按 `freq_rank` 从高频到低频推进**。
- 校验：`tools/validate_seed.py`（仿现有 `validate_data.py`），保证字段完整/类型正确/无重复 word。

### 4.3 生词库记录（localStorage，向后兼容扩展）
- 在现有 `store.js` 记录结构上新增可选 `aids` 字段（初始 `null`）。
- **向后兼容**：老生词无 `aids` 时，复习/列表退回原始行为，不报错。`store.js` 的 `addWord` 增加透传 `aids`（默认 `null`），其余 SRS 逻辑不动。

---

## 5. 界面与交互

### 5.1 复习抽词卡（`vocab.html` 改造，采用 B 交互）
1. 抽到词 → **仅显示单词 + 词根色块提示**（`pre🔴 + dict🔵` 带含义小字），引导靠词根推词义。
2. 点「显示完整释义 + 记忆法」→ 亮出：释义 + 词族 + 联想 + 词形（完整 `aids`）。
3. 三档评分（忘记/模糊/记住）→ 调用现有 `gradeReview`，SRS 不变。
4. **降级**：`aids` 为空的词，跳过步骤 1 的词根提示，直接走原"显示释义"行为。
- 配色（取自 word-root-workshop）：前缀 `#EF4444` / 词根 `#3B82F6`(粗边框) / 后缀 `#F59E0B`。

### 5.2 生词库列表（`vocab.html` 表格增强）
- 每行加展开按钮，点开在行下方用 `aids.js` 完整渲染记忆法卡。
- 无 `aids` 的词：按钮显示灰态「+ 补记忆法」，提示该词待备份回填。
- 现有搜索/朗读/删除/出处跳转全部保留。

### 5.3 新增「词库」页 `library.html`（承载内置高频词）
- 顶部导航加第三入口：文章库 · 我的生词库 · **词库**。
- 两种浏览：**按词根成组**（学一个词根解锁一串词，仿 workshop）+ **按词频/字母列表**。
- 每词一张完整 `aids` 卡（复用 `aids.js`）；可"加入复习"把内置词纳入 SRS 抽词池。
- 顶部显示生产进度（`generated_batches`/`total_target`）。

### 5.4 复习池合并（`js/seed.js`）
- 复习抽词时，池 = localStorage 生词 ∪ 用户"加入复习"的内置词；两者共用 `store.js` 的 SRS 权重。
- 内置词的 SRS 状态也存 localStorage（键区分，如 `ielts_vocab_seed_review`），避免污染 `vocab-seed.json`（该文件保持只读的知识源）。
- **去重规则**：若某词同时是内置词又被用户点成生词，以 localStorage 生词库为准（生词记录优先，其 `aids` 若为空则回退用 seed 的 `aids` 展示），同一词在复习池中只出现一次，避免双重计数。

---

## 6. 数据生成工作流（Claude 预生成）

### 6.1 内置词库（分批滚动）
1. **选词与排序**：从 `engra/IELTS.json` 取全 3575 词，用 `ECDICT` 的 `frq`/`bnc` 排序、附 CEFR，产出 `tools/seed_wordlist.json`（含 `freq_rank`/`cefr`），**高频在前**。
2. **逐词生成**：`tools/gen_seed_aids.py`（结构仿 `refine_c17_*.py`：一个手写 `SEED` 批次字典 + 落盘 + 校验）。每词生成 `aids`，生成时读三个开源库做参考：
   - 词根拆解 → `generated-english-roots-list` + workshop，**不规则词 Claude 判断，不强拆**。
   - 词形 → `ECDICT.exchange`（可靠事实）。
   - 词族 → 词根库 examples + Claude 补充。
   - 联想 → `DictionaryByGPT4` 的「记忆辅助」启发，**牵强则重写，宁缺毋滥**。
3. **批次粒度**：每批约 40 词。**第一批 40 词作为质量样板**回填 `vocab-seed.json`，用户在真实网页验收 → 定稿后每批约 40 词滚动至 3575。
4. **进度追踪**：`docs/superpowers/SEED_PROGRESS.md` 记录已完成批次/词数/下一批起点。
5. **校验**：每批跑 `tools/validate_seed.py` 全绿方算完成。

### 6.2 动态生词回填（A 方案，用户日常）
1. 用户点 `vocab.html`「备份生词」→ 导出 `ielts-vocab.json`。
2. 交给 Claude → `tools/backfill_aids.py` 识别 `aids==null` 的词 → 逐词生成 → 写回同一 JSON。
3. 用户点「恢复生词备份」导入 → 生词带上记忆法。**零新增基建**。

### 6.3 质量红线（固化为 `docs/superpowers/AIDS_SPEC.md`）
- 事实字段（词形/词族/词根）尽量全、须核对开源库。
- 联想只在**不牵强**时给，禁模板套话（同文章精修的 `REFINE_SPEC` 标准）。
- 许可证：DictionaryByGPT4(CC-BY-SA) 仅作参考启发、文字重写，不整段复制；产物为原创衍生数据，项目内注明 attribution。

---

## 7. 项目结构与约定（新增/改动）
```
ielts-app/
  data/
    vocab-seed.json          # 新：内置词库(分批追加)
  js/
    aids.js                  # 新：aids 卡片渲染(三处共用)
    library.js               # 新：词库页逻辑
    seed.js                  # 新：加载 seed + 合并复习池
    store.js                 # 改：addWord 透传 aids(默认 null)，SRS 逻辑不动
    vocab.js                 # 改：复习卡 B 交互 + 列表可展开
  library.html               # 新：词库页
  vocab.html                 # 改：导航加"词库"入口
  tools/
    seed_wordlist.json       # 新：选词+排序结果
    gen_seed_aids.py         # 新：逐批生成 aids
    backfill_aids.py         # 新：生词回填
    validate_seed.py         # 新：seed 校验
  docs/superpowers/
    AIDS_SPEC.md             # 新：aids 生成规范+质量红线
    SEED_PROGRESS.md         # 新：分批进度
```

## 8. 测试策略
- `aids.js` 渲染：对"全字段/仅词根/仅联想/全空"四种 `aids` 形态各测一遍，确保无字段时不崩、降级正确。
- `store.js`：新增 `aids` 透传与"老记录无 aids"回归测试（复用现有 Node 测试方式）。
- `seed.js`：复习池合并去重、内置词 SRS 状态独立存储不污染 seed 文件。
- 数据：`validate_seed.py` 每批全绿；抽查若干词人工核对词根/词形正确性。

## 9. 里程碑（供实施计划展开）
1. `aids` schema + `aids.js` 渲染组件（含四形态降级）。
2. `store.js`/`vocab.js` 改造（B 交互复习 + 列表展开）。
3. `seed.js` + `library.html` 词库页 + 复习池合并。
4. 选词排序 `seed_wordlist.json` + `gen_seed_aids.py` + `validate_seed.py`。
5. **第一批 40 词样板生成 → 用户网页验收 → 规范定稿**。
6. 滚动生产后续批次至 3575（每批约 40 词，进度入 `SEED_PROGRESS.md`）。
