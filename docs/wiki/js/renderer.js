/* 页面渲染器 */
import { resolvePageId } from './registry.js';

/** 渲染首页 */
export function renderHome(core) {
  const article = document.getElementById('article');
  document.getElementById('crumb').textContent = '';

  const registry = core.registry;
  const pages = registry.pages;

  // 统计
  const typeCounts = {};
  for (const entry of Object.values(pages)) {
    const label = entry.label || '其他';
    typeCounts[label] = (typeCounts[label] || 0) + 1;
  }
  const typeList = Object.entries(typeCounts).sort((a, b) => b[1] - a[1]);

  // 按类别分组
  const sections = [
    { label: '人物', icon: '👤', count: typeCounts['人物'] || 0, type: '人物' },
    { label: '典故', icon: '📖', count: typeCounts['典故'] || 0, type: '典故' },
    { label: '文献', icon: '📜', count: typeCounts['文献'] || 0, type: '文献' },
    { label: '三国杀技能', icon: '🃏', count: typeCounts['三国杀技能'] || 0, type: '三国杀技能' },
    { label: '战役', icon: '⚔️', count: typeCounts['战役'] || 0, type: '战役' },
    { label: '事件', icon: '📅', count: typeCounts['事件'] || 0, type: '事件' },
    { label: '势力', icon: '🏛️', count: typeCounts['势力'] || 0, type: '势力' },
    { label: '兵器', icon: '🗡️', count: typeCounts['兵器'] || 0, type: '兵器' },
    { label: '计策', icon: '🎯', count: typeCounts['计策'] || 0, type: '计策' },
  ];

  article.innerHTML = `
    <div class="home-hero fade-in">
      <h1>🏯 三国知识库 Wiki</h1>
      <p>基于 Obsidian 笔记的深度阅读平台 · 三国的历史、文学与文化</p>
      <div class="home-stats">
        <div class="home-stat"><div class="home-stat-num">${Object.keys(pages).length}</div><div class="home-stat-label">总条目</div></div>
        ${sections.filter(s => s.count > 0).slice(0, 5).map(s =>
          `<div class="home-stat"><div class="home-stat-num">${s.count}</div><div class="home-stat-label">${s.icon} ${s.label}</div></div>`
        ).join('')}
      </div>
    </div>
    <div class="home-sections fade-in">
      ${sections.filter(s => s.count > 0).map(s =>
        `<div class="home-section" onclick="location.hash='?type=${encodeURIComponent(s.label)}'">
          <h3>${s.icon} ${s.label}</h3>
          <p>共 ${s.count} 个条目</p>
        </div>`
      ).join('')}
    </div>
  `;

  document.getElementById('status').textContent = '';
}

/** 渲染单页 */
export async function renderPage(core, pid) {
  const article = document.getElementById('article');
  const crumb = document.getElementById('crumb');

  const entry = core.registry.pages[pid];
  if (!entry) {
    renderNotFound(core, pid);
    return;
  }

  crumb.textContent = `› ${entry.icon || ''} ${entry.name || pid}`;

  article.innerHTML = `<p class="loading">载入中…</p>`;
  document.getElementById('status').textContent = '载入…';

  try {
    const bust = `?v=${Math.floor(Date.now() / 30000)}`;
    const mdUrl = `pages/${encodeURIComponent(pid)}.md${bust}`;
    const r = await fetch(mdUrl);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);

    const mdText = await r.text();
    const { front, html, broken } = await parseMarkdown(core, mdText, { pid, meta: entry });

    const icon = entry.icon || '📄';
    const title = entry.name || pid;

    // 渲染正文 + 侧边栏
    article.innerHTML = `
      <div class="fade-in">
        <h1>${icon} ${escapeHtml(title)}</h1>
        <div class="article-body">${html}</div>
      </div>
    `;

    // 渲染侧边栏 infobox
    const sidebar = document.getElementById('sidebar');
    const infobox = document.getElementById('infobox');
    const sidebarPortrait = document.getElementById('sidebar-portrait');

    sidebar.removeAttribute('hidden');
    infobox.removeAttribute('hidden');
    sidebarPortrait.setAttribute('hidden', '');

    // 构建 infobox 表格
    const rows = [];
    if (entry.label) rows.push(['类型', entry.label]);
    if (entry.type === 'character') {
      if (entry.faction) rows.push(['势力', entry.faction]);
      if (entry.birth !== undefined && entry.birth !== '?') rows.push(['生年', entry.birth]);
      if (entry.death !== undefined && entry.death !== '?') rows.push(['卒年', entry.death]);
    }
    if (front.era) rows.push(['时期', front.era]);
    if (front.source) rows.push(['出处', front.source]);
    if (front.author) rows.push(['作者', front.author]);
    if (entry.aliases && entry.aliases.length > 0) {
      rows.push(['别名', entry.aliases.join('、')]);
    }

    infobox.innerHTML = `
      <h3>${icon} ${escapeHtml(title)}</h3>
      <table>
        ${rows.map(r => `<tr><td>${r[0]}</td><td>${escapeHtml(r[1])}</td></tr>`).join('')}
      </table>
      ${(entry.tags && entry.tags.length > 0) ? `
        <div class="infobox-tags">
          ${entry.tags.map(t => `<span class="infobox-tag">${escapeHtml(t)}</span>`).join('')}
        </div>
      ` : ''}
    `;

    // 渲染侧边栏链接（同类型页面）
    const sidebarLinks = document.getElementById('sidebar-links');
    const sameType = Object.values(core.registry.pages)
      .filter(e => e.type === entry.type && e.id !== pid)
      .slice(0, 20);
    if (sameType.length > 0) {
      sidebarLinks.removeAttribute('hidden');
      sidebarLinks.innerHTML = `
        <h3>同类型条目</h3>
        <ul>
          ${sameType.map(e =>
            `<li><a href="#${encodeURIComponent(e.id)}">${e.icon || ''} ${escapeHtml(e.name || e.id)}</a></li>`
          ).join('')}
        </ul>
      `;
    } else {
      sidebarLinks.setAttribute('hidden', '');
    }

    document.getElementById('status').textContent = '';
  } catch (e) {
    article.innerHTML = `<div class="error-page"><h2>加载失败</h2><p>无法加载页面「${escapeHtml(pid)}」: ${e.message}</p></div>`;
    document.getElementById('status').textContent = '加载失败';
  }
}

/** 渲染分类页面 */
export function renderCategory(core, typeLabel) {
  const article = document.getElementById('article');
  document.getElementById('crumb').textContent = `› ${typeLabel}`;

  const pages = Object.values(core.registry.pages)
    .filter(e => e.label === typeLabel)
    .sort((a, b) => (a.name || a.id).localeCompare(b.name || b.id, 'zh'));

  const icon = pages.length > 0 ? (pages[0].icon || '📄') : '📄';

  article.innerHTML = `
    <div class="category-header fade-in">
      <h1>${icon} ${escapeHtml(typeLabel)}</h1>
      <p class="cat-desc">共 ${pages.length} 个条目</p>
    </div>
    <div class="category-grid fade-in">
      ${pages.map(p => `
        <div class="cat-card" onclick="location.hash='${encodeURIComponent(p.id)}'">
          <div><span class="cat-icon">${p.icon || '📄'}</span><span class="cat-name">${escapeHtml(p.name || p.id)}</span></div>
          ${p.faction ? `<div class="cat-meta">${p.faction}</div>` : ''}
          ${(p.tags && p.tags.length > 0) ? `
            <div class="cat-tags">
              ${p.tags.slice(0, 5).map(t => `<span class="cat-tag">${escapeHtml(t)}</span>`).join('')}
            </div>
          ` : ''}
        </div>
      `).join('')}
    </div>
  `;

  document.getElementById('status').textContent = '';
}

/** 渲染全部页面 */
export function renderAll(core) {
  const article = document.getElementById('article');
  document.getElementById('crumb').textContent = '› 全部页面';

  const sorted = Object.values(core.registry.pages)
    .sort((a, b) => (a.name || a.id).localeCompare(b.name || b.id, 'zh'));

  // 按类型分组
  const byType = {};
  for (const p of sorted) {
    const label = p.label || '其他';
    if (!byType[label]) byType[label] = [];
    byType[label].push(p);
  }

  const typeKeys = Object.keys(byType).sort();

  article.innerHTML = `
    <div class="category-header fade-in">
      <h1>全部页面</h1>
      <p class="cat-desc">共 ${sorted.length} 个条目</p>
    </div>
    ${typeKeys.map(type => `
      <h2 style="margin-top:1.5em;font-size:1.1em;color:var(--accent);border-bottom:1px solid var(--border);padding-bottom:0.2em;">${byType[type][0].icon || '📄'} ${escapeHtml(type)} (${byType[type].length})</h2>
      <div class="category-grid" style="margin-top:0.5em;">
        ${byType[type].map(p => `
          <div class="cat-card" onclick="location.hash='${encodeURIComponent(p.id)}'">
            <div><span class="cat-name">${escapeHtml(p.name || p.id)}</span></div>
            <div class="cat-meta">${p.faction ? p.faction : ''}</div>
          </div>
        `).join('')}
      </div>
    `).join('')}
  `;

  document.getElementById('status').textContent = '';
}

/** 渲染搜索页 */
export function renderSearchResults(core, query, results) {
  const article = document.getElementById('article');
  document.getElementById('crumb').textContent = '› 搜索';

  const matchLabels = { name: '名称', alias: '别名', tag: '标签', id: 'ID' };

  article.innerHTML = `
    <div class="category-header fade-in">
      <h1>🔍 搜索结果</h1>
      <p class="cat-desc">「${escapeHtml(query)}」共找到 ${results.length} 个结果</p>
    </div>
    <div class="category-grid fade-in">
      ${results.map(r => `
        <div class="cat-card" onclick="location.hash='${encodeURIComponent(r.pid)}'">
          <div><span class="cat-icon">${r.entry.icon || '📄'}</span><span class="cat-name">${escapeHtml(r.entry.name || r.pid)}</span>
            <span style="font-size:11px;color:var(--fg-dim);margin-left:6px;">(${matchLabels[r.match] || r.match})</span>
          </div>
          <div class="cat-meta">${r.entry.label || ''} ${r.entry.faction ? '· ' + r.entry.faction : ''}</div>
        </div>
      `).join('')}
    </div>
  `;

  document.getElementById('status').textContent = '';
}

/** 渲染 404 */
export function renderNotFound(core, pid) {
  const article = document.getElementById('article');
  article.innerHTML = `
    <div class="error-page fade-in">
      <h2>页面未找到</h2>
      <p>「${escapeHtml(pid)}」在知识库中尚未收录。</p>
      <p style="margin-top:1em;"><a href="#Special:All" style="color:var(--link);">浏览全部页面</a></p>
    </div>
  `;
  document.getElementById('status').textContent = '未找到';
  document.getElementById('crumb').textContent = '› 未找到';
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
