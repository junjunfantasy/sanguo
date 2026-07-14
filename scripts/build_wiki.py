#!/usr/bin/env python3
"""
Build Wiki: 扫描 sanguo-knowledge/ 目录，生成 docs/wiki/pages.json 注册表，
并将所有 .md 文件复制到 docs/wiki/pages/ 目录下，供 Wiki SPA 使用。

执行: python3 scripts/build_wiki.py
依赖: Python 3 (标准库即可，不需要 pyyaml)
"""

import os
import re
import json
import sys

# === 路径配置 ===
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(REPO_DIR, "sanguo-knowledge")
WIKI_DIR = os.path.join(REPO_DIR, "docs", "wiki")
PAGES_DIR = os.path.join(WIKI_DIR, "pages")

# YAML frontmatter 提取 (纯 regex，不依赖 pyyaml)
FRONT_PATTERN = re.compile(r'^---\s*\n(.+?)\n---', re.DOTALL)

# 类型映射：将 frontmatter 中的 type 值归一化为显示用的中文分类
TYPE_LABELS = {
    'character': '人物',
    '典故': '典故',
    '成语典故': '典故',
    'book': '文献',
    'battle': '战役',
    'event': '事件',
    'faction': '势力',
    'skill': '三国杀技能',
    'methodology': '方法论',
    '州郡': '州郡',
    '古战场': '古战场',
    '都城': '都城',
    '冷兵器/剑': '兵器',
    '冷兵器/长矛': '兵器',
    '冷兵器/长柄刀': '兵器',
    '冷兵器/长柄戟': '兵器',
    '战马': '战马',
    '心理战术': '计策',
    '诈降计': '计策',
    '离间计': '计策',
    '借力计': '计策',
    '围点打援': '计策',
}

# 分类图标
TYPE_ICONS = {
    '人物': '👤',
    '典故': '📖',
    '文献': '📜',
    '战役': '⚔️',
    '事件': '📅',
    '势力': '🏛️',
    '三国杀技能': '🃏',
    '方法论': '🔧',
    '州郡': '🏘️',
    '古战场': '🏟️',
    '都城': '🏰',
    '兵器': '🗡️',
    '战马': '🐎',
    '计策': '🎯',
}


def parse_frontmatter(content):
    """从 Markdown 内容中提取 YAML frontmatter，返回 dict 和 body。"""
    m = FRONT_PATTERN.match(content)
    if not m:
        return {}, content

    yaml_text = m.group(1)
    body = content[m.end():].strip()

    # 简陋的 YAML 解析，只处理我们的数据结构
    result = {}
    for line in yaml_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        key = key.strip()
        val = val.strip()

        # 处理列表: [a, b, c] 或 - a\n- b 格式
        if val.startswith('[') and val.endswith(']'):
            items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(',') if v.strip()]
            result[key] = items
        elif val.startswith('- '):
            # 列表项在下一行处理，会合并
            pass
        elif val.lower() == 'true':
            result[key] = True
        elif val.lower() == 'false':
            result[key] = False
        else:
            result[key] = val.strip('"').strip("'")

    return result, body


def merge_yaml_lines(content):
    """将多行列表格式的 YAML 合并为单行，方便解析。"""
    lines = content.split('\n')
    merged = []
    in_front = False
    for line in lines:
        if line.strip() == '---':
            if not in_front:
                in_front = True
                merged.append(line)
                continue
            else:
                in_front = False
                merged.append(line)
                continue
        if in_front and line.strip().startswith('- '):
            # 找到上一个 key 所在行，追加
            if merged:
                prev = merged[-1]
                if ':' in prev and not prev.strip().startswith('- '):
                    # 追加到上一行
                    item = line.strip()[2:].strip().strip('"').strip("'")
                    merged[-1] = prev.rstrip() + f', {item}'
                    continue
        merged.append(line)
    return '\n'.join(merged)


def process_all_pages():
    """扫描整个 sanguo-knowledge 目录，生成 pages.json 数据。"""
    pages = {}
    alias_index = {}
    errors = []

    for root, dirs, files in os.walk(KNOWLEDGE_DIR):
        # 跳过 .obsidian 目录
        if '.obsidian' in root.split(os.sep):
            continue
        for fname in files:
            if not fname.endswith('.md') or fname.startswith('.'):
                continue

            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, KNOWLEDGE_DIR)

            # 去掉 .md 后缀作为 page_id
            page_id = fname[:-3]

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    raw = f.read()
            except Exception as e:
                errors.append(f"Read error: {rel_path} - {e}")
                continue

            # 合并 YAML 列表行
            merged = merge_yaml_lines(raw)
            front, body = parse_frontmatter(merged)

            page_type = front.get('type', 'unknown')
            label = TYPE_LABELS.get(page_type, page_type)
            icon = TYPE_ICONS.get(label, '📄')

            # 提取名称
            name = front.get('name') or front.get('title') or page_id

            # 提取别名
            aliases = []
            raw_aliases = front.get('aliases', front.get('alias', []))
            if isinstance(raw_aliases, str):
                raw_aliases = [raw_aliases]
            # 清理空值
            aliases = [a for a in raw_aliases if a]

            # 提取标签
            tags = front.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]

            # 提取 era 用于分类
            era = front.get('era', '')
            if isinstance(era, list):
                era = era[0] if era else ''

            page_entry = {
                'id': page_id,
                'name': name,
                'type': page_type,
                'label': label,
                'icon': icon,
                'file': rel_path.replace('\\', '/'),
                'tags': tags,
                'aliases': aliases,
                'era': era,
                'raw': raw,  # 嵌入原始 Markdown 内容，避免独立 .md fetch
            }

            # 人物特有字段
            if page_type == 'character':
                faction = front.get('faction', [''])
                if isinstance(faction, list):
                    faction_str = faction[0] if faction else ''
                else:
                    faction_str = faction
                page_entry['faction'] = faction_str
                page_entry['birth'] = front.get('birth_year', '?')
                page_entry['death'] = front.get('death_year', '?')

            pages[page_id] = page_entry

            # 别名索引
            for a in aliases:
                if a and a != name:
                    alias_index[a] = page_id

    return pages, alias_index, errors


def main():
    print(f"三国知识库 Wiki 构建工具")
    print(f"知识库目录: {KNOWLEDGE_DIR}")
    print(f"输出目录: {WIKI_DIR}")
    print()

    # Step 1: 扫描并生成 pages.json
    print("[1/3] 扫描知识库文件...")
    pages, alias_index, errors = process_all_pages()
    print(f"  发现 {len(pages)} 个页面")

    registry = {
        'pages': pages,
        'alias_index': alias_index,
        'total': len(pages),
        'generated_at': os.path.basename(__file__)
    }

    # 统计分类
    type_counts = {}
    for p in pages.values():
        label = p.get('label', '未知')
        type_counts[label] = type_counts.get(label, 0) + 1
    print(f"  分类统计:")
    for label, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        icon = TYPE_ICONS.get(label, '📄')
        print(f"    {icon} {label}: {count}")

    if errors:
        print(f"  ⚠️  {len(errors)} 个错误:")
        for e in errors[:5]:
            print(f"    {e}")

    # Step 2: 写入 pages.json
    print()
    print("[2/3] 写入 pages.json...")
    os.makedirs(WIKI_DIR, exist_ok=True)
    json_path = os.path.join(WIKI_DIR, 'pages.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    json_size = os.path.getsize(json_path)
    print(f"  已写入 {json_path} ({json_size:,} bytes)")

    # Step 3 (removed): 不再复制 .md 文件 — 内容已嵌入 pages.json

    print()
    print("✅ Wiki 构建完成!")
    print(f"  页面总数: {len(pages)}")
    print(f"  pages.json: {json_size:,} bytes")
    print()
    print(f"  请在浏览器访问: /wiki/ 查看效果 (需刷新 GitHub Pages)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
