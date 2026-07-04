// DeepSeek API 封装(AI_CONTRACT 的唯一实现)。其它页面这样用:
//   const { askDeepSeek, hasKey } = await import("./ai.js");  // 建议 try/catch
//   const text = await askDeepSeek([{role:"user",content:"..."}]);
//   const obj  = await askDeepSeek(msgs, { json:true });      // 返回解析好的对象
//
// key 存 localStorage 'ielts_ds_key',模型名存 'ielts_ds_model'(默认 deepseek-chat),
// 都在 settings.html 里配置。
// 已用 curl 对 api.deepseek.com 做过 OPTIONS 预检:任意 Origin 都会被回显进
// Access-Control-Allow-Origin,浏览器可直连,不需要本地代理服务器。

const API_URL = "https://api.deepseek.com/chat/completions";
const KEY_LS = "ielts_ds_key";
const MODEL_LS = "ielts_ds_model";
const DEFAULT_MODEL = "deepseek-chat";
const TIMEOUT_MS = 60000; // 单次请求最多等 60 秒,避免按钮永远转圈

// 是否已配置 API Key(不校验有效性,只看有没有存)
export function hasKey() {
  try {
    return !!(localStorage.getItem(KEY_LS) || "").trim();
  } catch {
    return false; // 隐私模式等拿不到 localStorage 时视为未配置
  }
}

function getKey() {
  let k = "";
  try {
    k = (localStorage.getItem(KEY_LS) || "").trim();
  } catch {}
  if (!k) throw new Error("尚未配置 DeepSeek API Key,请到「设置」页填写");
  return k;
}

function getModel() {
  try {
    return (localStorage.getItem(MODEL_LS) || "").trim() || DEFAULT_MODEL;
  } catch {
    return DEFAULT_MODEL;
  }
}

// 发一次请求,返回模型回复的纯文本;所有错误都转成中文 Error 抛出
async function callOnce(messages, { json, maxTokens, temperature }) {
  const key = getKey();
  const body = {
    model: getModel(),
    messages,
    max_tokens: maxTokens,
    temperature,
  };
  if (json) body.response_format = { type: "json_object" };

  const ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
  const timer = ctrl ? setTimeout(() => ctrl.abort(), TIMEOUT_MS) : null;

  let resp;
  try {
    resp = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + key,
      },
      body: JSON.stringify(body),
      signal: ctrl ? ctrl.signal : undefined,
    });
  } catch (e) {
    if (e && e.name === "AbortError") {
      throw new Error("请求超时(60 秒没有响应),请检查网络后重试");
    }
    // fetch 网络层失败是 TypeError:多半是断网,或请求被浏览器/插件拦截(CORS,
    // 即浏览器的跨域安全限制)。DeepSeek 官方接口本身允许跨域,正常情况下不会触发。
    throw new Error("网络请求失败:可能是断网,或请求被浏览器/插件拦截(CORS)。请检查网络连接后重试");
  } finally {
    if (timer) clearTimeout(timer);
  }

  if (!resp.ok) {
    if (resp.status === 401) throw new Error("API Key 无效或已被重置");
    if (resp.status === 429) throw new Error("请求过于频繁,请稍候");
    let detail = "";
    try {
      const j = await resp.json();
      detail = (j && j.error && j.error.message) || "";
    } catch {}
    throw new Error("DeepSeek 接口返回错误(HTTP " + resp.status + ")" + (detail ? ":" + detail : ""));
  }

  let data;
  try {
    data = await resp.json();
  } catch {
    throw new Error("DeepSeek 返回的数据不是合法 JSON,请稍后重试");
  }
  const content = data && data.choices && data.choices[0] && data.choices[0].message
    ? data.choices[0].message.content
    : null;
  if (typeof content !== "string") throw new Error("DeepSeek 返回格式异常:没有拿到回复内容");
  return content;
}

// 主入口。json=false 返回字符串;json=true 返回 JSON.parse 后的对象,
// 首次解析失败会把原文发回去让模型修一次,再失败才报错。
export async function askDeepSeek(messages, { json = false, maxTokens = 4096, temperature = 0.3 } = {}) {
  if (!Array.isArray(messages) || messages.length === 0) {
    throw new Error("askDeepSeek:messages 必须是非空数组");
  }
  const text = await callOnce(messages, { json, maxTokens, temperature });
  if (!json) return text;

  try {
    return JSON.parse(text);
  } catch {
    // 带原文重试一次:让模型自己把坏 JSON 修成合法 JSON
    const fixMessages = messages.concat([
      { role: "assistant", content: text },
      { role: "user", content: "你上面的输出不是合法 JSON,程序解析失败了。请只输出修正后的合法 JSON,不要带任何解释、注释或代码块标记。" },
    ]);
    const retry = await callOnce(fixMessages, { json: true, maxTokens, temperature });
    try {
      return JSON.parse(retry);
    } catch {
      throw new Error("DeepSeek 连续两次没有返回合法 JSON,请稍后重试");
    }
  }
}
