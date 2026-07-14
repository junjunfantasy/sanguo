/* 页面注册表加载与 ID 解析 */
export async function loadRegistry(url = 'pages.json') {
  const bust = `?v=${Math.floor(Date.now() / 60000)}`;
  const r = await fetch(url + bust);
  if (!r.ok) throw new Error(`pages.json HTTP ${r.status}`);
  return r.json();
}

/**
 * Hash 路由 / WikiLink 的 ID 解析:
 * 1. 精确匹配 pages[raw]
 * 2. 别名 alias_index[raw]
 * 3. 直接文件名匹配
 */
export function resolvePageId(raw, registry) {
  if (!raw) return null;
  if (raw in registry.pages) return [raw, registry.pages[raw]];
  if (raw in registry.alias_index) {
    const pid = registry.alias_index[raw];
    return [pid, registry.pages[pid]];
  }
  // 尝试带 .md 后缀
  const withMd = raw + '.md';
  if (withMd in registry.pages) return [withMd, registry.pages[withMd]];
  return null;
}

/** 按条件搜索页面 */
export function searchPages(query, registry) {
  if (!query || !query.trim()) return [];
  const q = query.trim().toLowerCase();
  const results = [];
  const seen = new Set();

  for (const [pid, entry] of Object.entries(registry.pages)) {
    if (seen.has(pid)) continue;

    // 搜索 name
    if (entry.name && entry.name.toLowerCase().includes(q)) {
      results.push({ pid, entry, match: 'name' });
      seen.add(pid);
      continue;
    }
    // 搜索别名
    if (entry.aliases && entry.aliases.some(a => a.toLowerCase().includes(q))) {
      results.push({ pid, entry, match: 'alias' });
      seen.add(pid);
      continue;
    }
    // 搜索标签
    if (entry.tags && entry.tags.some(t => t.toLowerCase().includes(q))) {
      results.push({ pid, entry, match: 'tag' });
      seen.add(pid);
      continue;
    }
    // 搜索 ID
    if (pid.toLowerCase().includes(q)) {
      results.push({ pid, entry, match: 'id' });
      seen.add(pid);
    }
  }

  return results;
}
