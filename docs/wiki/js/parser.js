/* Markdown 解析流水线 */
import { resolvePageId } from './registry.js';

export function createMarkdownIt() {
  if (!window.markdownit) {
    throw new Error('markdown-it 未加载');
  }
  const md = window.markdownit({
    html: true,
    linkify: true,
    typographer: true,
    breaks: false,
  });

  // 图片点击在新窗口打开
  const defaultImageRender = md.renderer.rules.image || function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };
  md.renderer.rules.image = function(tokens, idx, options, env, self) {
    const token = tokens[idx];
    const src = token.attrGet('src') || '';
    const alt = token.content || '';
    return `<a href="${src}" target="_blank" rel="noopener">${defaultImageRender(tokens, idx, options, env, self)}</a>`;
  };

  return md;
}

/**
 * 正则提取 [[Wikilink]] 和目标文本
 * 支持 [[target]]、[[target|label]]、[[target:text]]
 */
const WIKILINK_RE = /\[\[([^\]|]+)(?:\|([^\]|]+))?\]\]/g;

/**
 * 解析 Markdown 内容:
 * 1. 分割 frontmatter
 * 2. 渲染 Markdown
 * 3. 展开 Wikilink
 */
export async function parseMarkdown(core, mdText, ctx = {}) {
  const { pid, meta } = ctx;

  // 提取 frontmatter
  const { front, body } = splitFrontmatter(mdText);

  // 渲染 Markdown (先临时替换 Wikilink 避免冲突)
  const { protectedText, tokens } = protectWikilinks(body);

  // MD → HTML
  let html = core.md.render(protectedText);

  // 展开 Wikilink 占位符为 <a>
  const broken = [];
  html = expandWikilinks(html, tokens, {
    selfId: pid,
    resolve: (target) => resolvePageId(target, core.registry),
    onBroken: (t) => broken.push(t),
  });

  return { front, html, broken };
}

function splitFrontmatter(text) {
  if (!text.startsWith('---')) return { front: {}, body: text };

  const end = text.indexOf('---', 3);
  if (end === -1) return { front: {}, body: text };

  const yamlText = text.slice(3, end).trim();
  const body = text.slice(end + 3).trim();

  // 简易 YAML 解析
  const front = {};
  for (const line of yamlText.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const colon = trimmed.indexOf(':');
    if (colon === -1) continue;
    const key = trimmed.slice(0, colon).trim();
    let val = trimmed.slice(colon + 1).trim();

    if (val.startsWith('[') && val.endsWith(']')) {
      front[key] = val.slice(1, -1).split(',').map(v => v.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
    } else if (val === 'true' || val === 'false') {
      front[key] = val === 'true';
    } else if (val === '' || val === 'null') {
      // 忽略或设为 null
    } else {
      front[key] = val.replace(/^["']|["']$/g, '');
    }
  }

  return { front, body };
}

/** 保护 Wikilink 语法，替换为唯一占位符 */
function protectWikilinks(text) {
  const tokens = [];
  let idx = 0;
  const protectedText = text.replace(WIKILINK_RE, (match, target, label) => {
    const placeholder = `__WIKILINK_${idx}__`;
    tokens.push({
      target: target.trim(),
      label: label ? label.trim() : target.trim(),
      placeholder,
    });
    idx++;
    return placeholder;
  });

  return { protectedText, tokens };
}

/** 展开 Wikilink 占位符为 <a> */
function expandWikilinks(html, tokens, { selfId, resolve, onBroken }) {
  for (const token of tokens) {
    const resolved = resolve(token.target);

    let linkHtml;
    if (resolved) {
      const [pid, entry] = resolved;
      const icon = (entry && entry.icon) || '';
      linkHtml = `<a href="#${encodeURIComponent(pid)}" class="wiki-link">${icon ? icon + ' ' : ''}${escapeHtml(token.label)}</a>`;
    } else {
      linkHtml = `<a href="#${encodeURIComponent(token.target)}" class="wiki-link broken">${escapeHtml(token.label)}</a>`;
      if (onBroken) onBroken(token.target);
    }

    html = html.replace(token.placeholder, linkHtml);
  }

  return html;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
