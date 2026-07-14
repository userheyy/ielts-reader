// 今日过词队列构建 —— 纯逻辑,不碰 DOM,便于测试。
//
// 契约(见 docs/.../2026-07-03-daily-words-calendar-design.md §2):
//   队列 = 全部“当前仍到期”的复习词  ++  新词.slice(new_done)   (复习优先)
//
// 关键:复习词是每次进页现算的(reviewDue 只返回“今天仍到期”的词);过完一个
// 复习词后它的 next_due 被推到未来,自然从 task.review 消失 —— 复习“接着上次进度”
// 是自动的,不需要再按计数位移。只有新词是照当天存的 new_words 原样复原、不会自过滤,
// 所以只对新词按 new_done 跳过。
//
// 旧实现错在:q.slice(reviewed_done + new_done) 把已自过滤的复习进度又砍了一遍,
// 复习完成越多、砍得越狠,最终把未学的新词也砍空 → 点“继续今日任务”队列为空、
// 看起来没反应。这里对复习不做位移,根治该 bug。
//
// 参数:
//   task        { review:[{word, origin}], newWords:[seedEntry], day:{new_done, ...} }
//   wrapReview  (r) => 展示用词条 | null   —— 把复习项解析成完整词条(取不到则跳过)
// 返回:[{ entry, kind:'review'|'new', origin }]
export function buildQueue(task, wrapReview) {
  const rec = task.day;
  const q = [];
  // 复习项:全部当前到期的(已自过滤),逐个解析词条,取不到的跳过。
  for (const r of task.review) {
    const entry = wrapReview(r);
    if (entry) q.push({ entry, kind: "review", origin: r.origin });
  }
  // 新词项:照当天存的顺序,跳过已学的 new_done 个,其余入队。
  const newDone = Math.max(0, Number(rec.new_done) || 0);
  for (const s of task.newWords.slice(newDone)) {
    q.push({ entry: s, kind: "new", origin: "seed" });
  }
  return q;
}
