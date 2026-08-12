import { loadSeed } from "./seed.js?v=5";
import { renderMorphemes } from "./aids.js?v=5";

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const requestedRoot = (params.get("root") || "").trim().toLowerCase();
const requestedWord = (params.get("word") || "").trim().toLowerCase();
const requestedBack = params.get("back") || "";
const returnTo = /^vocab\.html#(?:daily|review|library)$/.test(requestedBack)
  ? requestedBack
  : "vocab.html#review";

const FALLBACKS = {
  disappoint: {
    morphemes: [
      { text: "dis", type: "prefix", gloss: "否定、相反" },
      { text: "appoint", type: "root", gloss: "指定、约定" },
    ],
    derivation: "dis-（没有按原定安排发生）+ appoint（指定、约定）→ 没有达到原来的期待 → 使失望",
  },
  puncture: {
    morphemes: [
      { text: "punct", type: "root", gloss: "点、刺" },
      { text: "ure", type: "suffix", gloss: "名词后缀" },
    ],
    derivation: "punct（刺）+ -ure（名词后缀）→ 刺出的孔 → 刺穿、刺破",
  },
  punctuate: {
    morphemes: [
      { text: "punct", type: "root", gloss: "点、刺" },
      { text: "uate", type: "suffix", gloss: "动词后缀" },
    ],
    derivation: "punct（点）+ -uate（动词后缀）→ 在句子中加点作标记 → 加标点",
  },
};

const PREFIX_GLOSSES = {
  contra: "相反、对立", trans: "跨越、转变", inter: "在……之间", pre: "预先",
  post: "之后", sub: "在下、次级", dis: "否定、相反", de: "去除、向下",
  re: "再次、重新", ex: "向外", in: "向内、进入", im: "进入；不",
  ir: "不", il: "不", ad: "朝向、加强", ap: "朝向（ad 变体）",
  ac: "朝向（ad 变体）", con: "共同、一起", com: "共同、一起", per: "彻底、贯穿",
  uni: "一", bi: "二", tri: "三", auto: "自己", geo: "地球",
  photo: "光", tele: "远",
};

const SUFFIX_GLOSSES = {
  ization: "名词后缀", ation: "名词后缀", tion: "名词后缀", sion: "名词后缀",
  ment: "名词后缀", ness: "名词后缀", ity: "名词后缀", al: "形容词后缀",
  able: "能够……的", ible: "能够……的", ous: "具有……的", ive: "具有……性质的",
  er: "人或物", or: "人或物", ist: "……者", ism: "状态或体系", ing: "行为或状态",
  ed: "……的", ure: "行为或结果", ual: "形容词后缀", ate: "动词后缀",
  ize: "使……", ify: "使……", ary: "与……有关的", y: "词形后缀",
};

function esc(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function wordKey(value) {
  return String(value || "").trim().toLowerCase();
}

function rootTokens(value) {
  return String(value || "")
    .toLowerCase()
    .split(/[\s/+,|·-]+/)
    .map((x) => x.trim())
    .filter((x) => x.length >= 2);
}

function buildFamilyGroups(words) {
  const refs = new Map();
  const ensureRef = (name, def = "") => {
    const key = wordKey(name);
    if (!key) return;
    if (!refs.has(key)) refs.set(key, { word: String(name).trim(), def: def || "", seed: null });
    else if (def && !refs.get(key).def) refs.get(key).def = def;
  };

  for (const entry of words) {
    const key = wordKey(entry.word);
    if (!key) continue;
    ensureRef(entry.word, entry.def);
    refs.get(key).seed = entry;
    const family = entry.aids && entry.aids.family;
    const fallbackRoots = entry.aids && Array.isArray(entry.aids.morphemes)
      ? entry.aids.morphemes.filter((m) => m && m.type === "root" && m.text).map((m) => m.text).join("/")
      : "";
    refs.get(key).roots = new Set(rootTokens((family && family.root) || fallbackRoots));
    for (const member of (family && Array.isArray(family.words) ? family.words : [])) {
      const memberKey = wordKey(member && member.word);
      if (!memberKey) continue;
      ensureRef(member.word, member.def);
    }
  }

  return { refs };
}

function rootsKey(roots) {
  return [...(roots || [])].sort().join("/");
}

function inferDetails(ref, group) {
  const word = wordKey(ref.word);
  const rootCandidates = [...new Set([
    ...(group.roots || []),
    ...group.words.flatMap((item) => [...(item.roots || [])]),
  ])].sort((a, b) => b.length - a.length);
  const root = rootCandidates.find((candidate) => candidate && word.includes(candidate));
  const def = ref.def || "同词根关联词";
  if (!root) {
    return {
      morphemes: [],
      derivation: `与 ${group.roots.join(" / ")} 同词根，核心含义保持关联 → ${def}`,
    };
  }

  const rootGloss = group.gloss || "核心含义";
  const start = word.indexOf(root);
  const before = word.slice(0, start);
  const after = word.slice(start + root.length);
  const morphemes = [];
  let derivation = "";
  if (before) {
    const prefix = Object.keys(PREFIX_GLOSSES).sort((a, b) => b.length - a.length).find((item) => before === item);
    morphemes.push({ text: before, type: "prefix", gloss: prefix ? PREFIX_GLOSSES[prefix] : "前置成分" });
    derivation += `${before}（${prefix ? PREFIX_GLOSSES[prefix] : "前置成分"}）+ `;
  }
  morphemes.push({ text: root, type: "root", gloss: rootGloss });
  derivation += `${root}（${rootGloss}）`;
  if (after) {
    const suffix = Object.keys(SUFFIX_GLOSSES).sort((a, b) => b.length - a.length).find((item) => after === item);
    morphemes.push({ text: after, type: "suffix", gloss: suffix ? SUFFIX_GLOSSES[suffix] : "词形后缀" });
    derivation += ` + ${after}（${suffix ? SUFFIX_GLOSSES[suffix] : "词形后缀"}）`;
  }
  derivation += ` → ${def}`;
  return { morphemes, derivation };
}

function findGroup(index) {
  const refs = index.refs;
  const requestedRef = requestedWord ? refs.get(requestedWord) : null;
  const queryTokens = rootTokens(requestedRoot);
  // 有真实词条时，以该词条声明的完整词根组合为锚点。
  // 例如 point 的 punct/point 只匹配同组的 appoint/appointment，
  // 不会因为都含有 punct 就把 punch、acupuncture 等旁支带进来。
  const requestedTokens = requestedRef && requestedRef.seed && requestedRef.roots && requestedRef.roots.size
    ? [...requestedRef.roots]
    : queryTokens;
  const anchorKey = rootsKey(requestedTokens);

  // 按当前页面的词根筛选，而不是把所有词族声明递归合并成一个巨型连通图。
  // 这样 point 页面会聚焦 point/punct 相关词，同时保留显式声明的缺失词条。
  const selected = new Set();
  let exactHits = 0;
  for (const [key, ref] of refs) {
    if (!ref.seed) continue;
    const roots = ref.roots || new Set();
    if (!requestedTokens.length || rootsKey(roots) === anchorKey) {
      selected.add(key);
      exactHits += 1;
    }
  }
  // 老数据可能只标了部分词根；完整组合没有命中时再退回交集匹配。
  if (requestedTokens.length && !exactHits) {
    for (const [key, ref] of refs) {
      if (!ref.seed) continue;
      const roots = ref.roots || new Set();
      if (requestedTokens.some((token) => roots.has(token))) selected.add(key);
    }
  }
  if (requestedRef) {
    selected.add(requestedWord);
    const family = requestedRef.seed && requestedRef.seed.aids && requestedRef.seed.aids.family;
    for (const member of (family && Array.isArray(family.words) ? family.words : [])) {
      const key = wordKey(member && member.word);
      if (key && refs.has(key)) selected.add(key);
    }
  }

  // 只补入已选词条明确提到、但当前词库尚未收录的词，避免把另一个大词族递归带进来。
  for (const key of [...selected]) {
    const ref = refs.get(key);
    if (!ref || !ref.seed) continue;
    const family = ref.seed.aids && ref.seed.aids.family;
    for (const member of (family && Array.isArray(family.words) ? family.words : [])) {
      const memberKey = wordKey(member && member.word);
      if (memberKey && refs.has(memberKey) && !refs.get(memberKey).seed) selected.add(memberKey);
    }
  }
  if (!selected.size) return null;

  const words = [...selected].map((key) => refs.get(key)).filter(Boolean).sort((a, b) => {
    if (a.seed && !b.seed) return -1;
    if (!a.seed && b.seed) return 1;
    return (a.seed?.freq_rank || 1e9) - (b.seed?.freq_rank || 1e9);
  });
  const roots = requestedTokens.length
    ? requestedTokens
    : [...new Set(words.flatMap((ref) => [...(ref.roots || [])]))];
  const glosses = [];
  for (const ref of words) {
    const family = ref.seed && ref.seed.aids && ref.seed.aids.family;
    if (!family || !family.gloss) continue;
    if (!requestedTokens.length || requestedTokens.some((token) => (ref.roots || new Set()).has(token))) {
      if (!glosses.includes(family.gloss)) glosses.push(family.gloss);
    }
  }
  return { words, roots, gloss: glosses[0] || "" };
}

function detailsFor(ref, group) {
  const fallback = FALLBACKS[wordKey(ref.word)] || {};
  const aids = ref.seed && ref.seed.aids ? ref.seed.aids : {};
  const inferred = inferDetails(ref, group);
  return {
    morphemes: aids.morphemes && aids.morphemes.length ? aids.morphemes : fallback.morphemes || inferred.morphemes || [],
    derivation: aids.derivation || fallback.derivation || inferred.derivation,
  };
}

function renderCard(ref, activeWord, group) {
  const seed = ref.seed;
  const details = detailsFor(ref, group);
  const active = wordKey(ref.word) === activeWord;
  const root = (seed && seed.aids && seed.aids.family && seed.aids.family.root) || requestedRoot || "";
  const href = `family.html?${new URLSearchParams({ root, word: ref.word, back: returnTo }).toString()}`;
  const morph = details.morphemes.length
    ? `<div class="family-morphemes">${renderMorphemes({ morphemes: details.morphemes })}</div>`
    : "";
  return `<article class="family-word-card${active ? " active" : ""}">
    <div class="family-word-top">
      <a class="family-word" href="${esc(href)}">${esc(ref.word)}</a>
      ${active ? '<span class="family-current">当前词</span>' : ""}
      ${seed && seed.pos ? `<span class="family-pos">${esc(seed.pos)}</span>` : ""}
    </div>
    <div class="family-def">${esc((seed && seed.def) || ref.def || "词库关联词")}</div>
    ${morph}
    ${details.derivation ? `<div class="family-derivation"><b>词义变化</b>${esc(details.derivation)}</div>` : ""}
  </article>`;
}

function renderPage(group) {
  const back = $("family-back");
  if (back) {
    back.href = returnTo;
    back.textContent = returnTo.endsWith("#daily") ? "← 返回今日记单词" : returnTo.endsWith("#library") ? "← 返回词库" : "← 返回记单词";
  }
  const activeWord = group.words.some((w) => wordKey(w.word) === requestedWord)
    ? requestedWord
    : wordKey(group.words[0] && group.words[0].word);
  const rootLabel = group.roots.length ? group.roots.join(" / ") : "词族";
  $("family-hero").hidden = false;
  $("family-title").textContent = `${rootLabel} · 词根词族`;
  $("family-subtitle").textContent = group.gloss
    ? `共同含义：${group.gloss}。先看词根，再看前缀和后缀如何改变方向。`
    : "先看共同词根，再看前缀和后缀如何改变词义。";
  $("family-root-line").innerHTML = group.roots.map((root) => `<span>${esc(root)}</span>`).join('<i>＋</i>');
  $("family-explainer").hidden = false;
  $("family-explainer-text").textContent = "词根保留核心意思，前缀通常改变方向，后缀通常改变词性。把同一组词放在一起看，比单独背释义更容易记住词义之间的关系。";
  $("family-toolbar").hidden = false;
  $("family-count").textContent = `共 ${group.words.length} 个词条`;
  $("family-grid").innerHTML = group.words.map((ref) => renderCard(ref, activeWord, group)).join("");
}

const seed = await loadSeed();
const group = findGroup(buildFamilyGroups(seed.words || []));
if (group) renderPage(group);
else $("family-empty").hidden = false;
