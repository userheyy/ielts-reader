# 听力音频目录

本目录存放剑桥雅思听力的 mp3 音频,**仅限本地个人学习使用**。

## 版权提醒(重要)

剑桥雅思真题音频受版权保护。本目录已在 `.gitignore` 里用
`media/audio/**`(仅保留本 README)整体屏蔽——**任何 mp3 都绝不会、也绝不允许提交到
git 仓库或推送到 GitHub**。请自行从正版渠道(剑桥官方出版物附带音频)获取文件放入本目录。

## 命名约定

统一命名为:`{book}-{test}-part{n}.mp3`

- `{book}`:册号,如 `c14`(剑桥雅思 14)
- `{test}`:测试号,如 `test1`
- `{n}`:部分号 1–4(即 Part 1 / Section 1 到 Part 4 / Section 4)

例:剑 14 音频目录里的 `T1S1.mp3`(Test 1 Section 1)应改名为:

```
c14-test1-part1.mp3
```

完整一套(剑 14 Test 1)如下:

| 原始文件 | 放入本目录后的文件名 |
| --- | --- |
| T1S1.mp3 | c14-test1-part1.mp3 |
| T1S2.mp3 | c14-test1-part2.mp3 |
| T1S3.mp3 | c14-test1-part3.mp3 |
| T1S4.mp3 | c14-test1-part4.mp3 |

## 和页面的对应关系

`data/listening/{id}.json` 里的 `audio` 字段指向本目录,例如
`"audio": "media/audio/c14-test1-part1.mp3"`。文件缺失时,listening.html
会在顶部提示,并保留"文本精读"功能(揭示句子、做题不需要音频)。
