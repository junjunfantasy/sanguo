/* Hash 路由 */
import { resolvePageId, searchPages } from './registry.js';
import { renderHome, renderPage, renderCategory, renderAll, renderSearchResults } from './renderer.js';

export function setupRouter(core) {
  window.addEventListener('hashchange', () => route(core));
  route(core);
}

async function route(core) {
  const rawHash = location.hash.slice(1) || '';

  // 页内锚点（脚注等）不触发页面路由
  if (rawHash && !rawHash.startsWith('?') && !rawHash.startsWith('!')) {
    const el = document.getElementById(decodeURIComponent(rawHash));
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setStatus('');
      return;
    }
  }

  setStatus('载入…');

  if (!rawHash) {
    // 首页
    renderHome(core);
    setStatus('');
    return;
  }

  // 特殊页面
  if (rawHash.startsWith('?')) {
    const params = new URLSearchParams(rawHash.slice(1));
    const query = params.get('q');
    const type = params.get('type');

    if (query) {
      const results = searchPages(query, core.registry);
      renderSearchResults(core, query, results);
      setStatus('');
      return;
    }
    if (type) {
      renderCategory(core, type);
      setStatus('');
      return;
    }
    // Fallback: 浏览所有 Special:All
    renderAll(core);
    setStatus('');
    return;
  }

  // 特殊命令
  if (rawHash.startsWith('!')) {
    const cmd = rawHash.slice(1);
    if (cmd === 'Special:All' || cmd === 'all') {
      renderAll(core);
      setStatus('');
      return;
    }
  }

  // 正常页面路由
  const decoded = decodeURIComponent(rawHash);
  const resolved = resolvePageId(decoded, core.registry);
  if (resolved) {
    const [pid] = resolved;
    await renderPage(core, pid);
  } else {
    // 尝试直接加载 .md 文件
    await renderPage(core, decoded);
  }

  setStatus('');
}

function setStatus(msg) {
  const el = document.getElementById('status');
  if (el) el.textContent = msg;
}
