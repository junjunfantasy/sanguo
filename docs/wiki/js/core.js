/* Wiki SPA 入口 */
import { createMarkdownIt, parseMarkdown } from './parser.js';
import { loadRegistry, resolvePageId, searchPages } from './registry.js';
import { setupRouter } from './router.js';

async function boot() {
  const core = {
    md: null,
    registry: null,
  };

  // 检查依赖
  if (!window.markdownit) {
    showFatal('依赖未加载：markdown-it');
    return;
  }

  // 初始化 markdown-it
  core.md = createMarkdownIt();

  // 加载注册表
  try {
    core.registry = await loadRegistry();
  } catch (e) {
    showFatal('无法加载 pages.json：' + e.message);
    return;
  }

  // 暴露给全局，方便调试
  window.__wiki = core;

  // 设置搜索建议
  setupSearchSuggestions(core);

  // 启动路由器
  setupRouter(core);
}

function setupSearchSuggestions(core) {
  const input = document.getElementById('topnav-q');
  const suggestions = document.getElementById('search-suggestions');
  const searchForm = document.getElementById('topnav-search-form');

  if (!input || !suggestions) return;

  let timeout = null;

  input.addEventListener('input', () => {
    clearTimeout(timeout);
    const q = input.value.trim();
    if (!q) {
      suggestions.classList.remove('active');
      suggestions.innerHTML = '';
      return;
    }

    timeout = setTimeout(() => {
      const results = searchPages(q, core.registry);
      if (results.length === 0) {
        suggestions.classList.remove('active');
        return;
      }

      suggestions.innerHTML = results.slice(0, 10).map(r => {
        const label = r.entry.label || '';
        const name = r.entry.name || r.pid;
        const icon = r.entry.icon || '📄';
        return `<div class="search-suggestion" onclick="location.hash='${encodeURIComponent(r.pid)}'; document.getElementById('topnav-q').blur(); suggestions.classList.remove('active');">
          <span>${icon}</span>
          <span class="sug-name">${escapeHtml(name)}</span>
          <span class="sug-label">${label}</span>
        </div>`;
      }).join('');
      suggestions.classList.add('active');
    }, 150);
  });

  input.addEventListener('blur', () => {
    setTimeout(() => suggestions.classList.remove('active'), 200);
  });

  input.addEventListener('focus', () => {
    if (suggestions.children.length > 0) {
      suggestions.classList.add('active');
    }
  });

  // 回车：跳转到搜索页面
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (q) {
      location.hash = `?q=${encodeURIComponent(q)}`;
      suggestions.classList.remove('active');
      input.blur();
    }
  });
}

function showFatal(msg) {
  const article = document.getElementById('article');
  if (article) {
    article.innerHTML = `<div class="error-page"><h2>错误</h2><p>${escapeHtml(msg)}</p></div>`;
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

boot();
