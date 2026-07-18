#!/usr/bin/env python3
"""
WikiLink 增强脚本: 自动给人物 markdown 文件中未链接的已知实体添加 [[]]
读取 KG 实体库，扫描人物文件，补全缺失的 WikiLinks。

用法:
  python scripts/enhance_wikilinks.py

效果:
  - 为人名、地点、事件、概念等添加 [[]] 链接
  - 跳过 frontmatter / 已有链接 / 自身引用 / 泛词
  - 最长匹配优先（避免 "曹操" 被 "曹操起兵" 覆盖）
"""

import os
import re
import json
import sys
from collections import defaultdict

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAR_DIR = os.path.join(REPO_DIR, "sanguo-knowledge", "characters")
KG_CHARS = os.path.join(REPO_DIR, "kg", "entities", "characters.json")
KG_EVENTS = os.path.join(REPO_DIR, "kg", "events", "events.json")

# 泛词黑名单 — 这些词即使出现在 KG 里也不应自动链接
STOP_WORDS = {
    '技能', '武将', '文臣', '谋士', '军师', '君主', '皇帝', '人物',
    '地点', '势力', '身份', '姓名', '别名', '生卒', '时期',
    '类型', '标签', '主公', '太守', '刺史', '州牧', '丞相',
    '大将军', '都督', '刺史', '县令', '将军', '校尉', '都尉',
    '步兵', '骑兵', '水军', '弓兵', '连弩',
    '忠义', '勇猛', '仁德', '奸雄', '刚烈', '傲慢', '忠诚',
    '义气', '谋略', '武艺', '才智', '胆识', '武勇',
}

# 地点列表（已知的州郡关隘）
LOCATIONS = {
    '洛阳', '长安', '成都', '许都', '建业', '荆州', '益州', '徐州',
    '兖州', '冀州', '青州', '并州', '凉州', '雍州', '司隶', '扬州',
    '交州', '幽州', '豫州', '赤壁', '官渡', '街亭', '五丈原', '汉中',
    '夷陵', '樊城', '合肥', '隆中', '南中', '江东', '中原', '西凉',
    '河北', '虎牢关', '定军山', '逍遥津', '白帝城', '麦城', '陈留',
    '颍川', '南阳', '襄阳', '江陵', '长沙', '庐江', '会稽', '吴郡',
    '丹阳', '南郡', '下邳', '小沛', '新野', '许昌', '邺城',
    '涪城', '绵竹', '剑阁', '祁山', '子午谷', '陈仓', '潼关', '函谷关',
    '上庸', '柴桑', '皖城', '濮阳', '徐州', '寿春',
}


def load_entities():
    """加载所有已知实体，生成 (名称, 类型) 映射，按长度降序"""
    entities = {}  # name -> type

    # 1. 人物（从 kg/entities/characters.json）
    try:
        with open(KG_CHARS, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for c in data.get('characters', []):
            entities[c['name']] = 'character'
            for a in c.get('aliases', []):
                if a and a not in entities:
                    entities[a] = 'character'
            for t in c.get('tags', []):
                if t and len(t) >= 2 and t not in STOP_WORDS and t not in entities:
                    entities[t] = 'concept'
    except Exception as e:
        print(f"⚠️  无法加载 KG 人物: {e}")

    # 2. 地点
    for loc in LOCATIONS:
        if loc not in entities:
            entities[loc] = 'location'

    # 3. 事件（从 kg/events/events.json）
    try:
        with open(KG_EVENTS, 'r', encoding='utf-8') as f:
            events = json.load(f)
        for e in events:
            name = e.get('name', '')
            if name and len(name) >= 2:
                entities[name] = 'event'
    except Exception as e:
        print(f"⚠️  无法加载 KG 事件: {e}")

    # 按名称长度降序排列（最长匹配优先）
    sorted_entities = sorted(entities.items(), key=lambda x: -len(x[0]))
    print(f"📚 已加载 {len(entities)} 个已知实体:")
    type_counts = defaultdict(int)
    for _, t in sorted_entities:
        type_counts[t] += 1
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"    {t}: {c}")
    return sorted_entities


def enhance_wikilinks_in_file(filepath, sorted_entities):
    """增强单个文件的 wikilink"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取文件名（用于跳过自引用）
    fname = os.path.basename(filepath).replace('.md', '')
    # 尝试从 frontmatter 读取 name
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    char_name = fname
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.split('\n'):
            if line.startswith('name:'):
                char_name = line.split(':', 1)[1].strip().strip('"').strip("'")
                break

    # 分段：frontmatter 不处理，只处理 body
    if fm_match:
        front_end = fm_match.end()
        frontmatter = content[:front_end]
        body = content[front_end:]
    else:
        frontmatter = ''
        body = content

    # 保护已有 wiki 链接和 markdown 链接
    protected_spans = []

    # 找到所有 [[...]] 的区间
    for m in re.finditer(r'\[\[([^\]]+)\]\]', body):
        protected_spans.append((m.start(), m.end()))

    # 找到所有 [![]()] 图片和 [txt]() 链接
    for m in re.finditer(r'\[([^\]]*)\]\([^\)]+\)', body):
        protected_spans.append((m.start(), m.end()))

    # 找到所有 ```代码块```
    for m in re.finditer(r'```[\s\S]*?```', body):
        protected_spans.append((m.start(), m.end()))

    # 找到所有行内代码 `code`
    for m in re.finditer(r'`[^`]+`', body):
        protected_spans.append((m.start(), m.end()))

    # 找到所有 # 标题行（不处理标题中的文本）
    for m in re.finditer(r'^#+\s+.*$', body, re.MULTILINE):
        protected_spans.append((m.start(), m.end()))

    # 合并重叠区间
    protected_spans.sort()
    merged = []
    for start, end in protected_spans:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    protected_spans = merged

    def is_protected(pos):
        return any(start <= pos < end for start, end in protected_spans)

    # 按最长匹配优先，扫描 body
    replacements = []  # (start, end, new_text)

    for entity_name, entity_type in sorted_entities:
        if len(entity_name) < 2:
            continue
        # 跳过自身引用
        if entity_name == char_name or entity_name == fname:
            continue
        # 跳过泛词
        if entity_name in STOP_WORDS:
            continue

        # 在 body 中查找所有出现
        search_from = 0
        while True:
            idx = body.find(entity_name, search_from)
            if idx == -1:
                break

            # 检查是否在保护区内
            if is_protected(idx):
                search_from = idx + 1
                continue

            # 检查是否已经是 [[entity]] 的一部分
            # 往前看是否有 [[
            before = body[max(0, idx - 2):idx]
            after = body[idx + len(entity_name):idx + len(entity_name) + 2]
            if before == '[[' or before.endswith('[[') or after.startswith(']]'):
                search_from = idx + 1
                continue

            # 检查字符边界（不是中文词的一部分）
            prev_char = body[idx - 1] if idx > 0 else ''
            next_char = body[idx + len(entity_name)] if idx + len(entity_name) < len(body) else ''

            # 中文语境：左边是中文或英文标点/空格/行首，右边同理
            if (prev_char and re.match(r'[\u4e00-\u9fff]', prev_char) and
                not re.match(r'[\u4e00-\u9fff]', entity_name[0])):
                # 词边界不匹配
                search_from = idx + 1
                continue

            # 检查是否已经被其他更长的替换覆盖
            overlapping = False
            for r_start, r_end, _ in replacements:
                if r_start <= idx < r_end or r_start < idx + len(entity_name) <= r_end:
                    overlapping = True
                    break
            if overlapping:
                search_from = idx + 1
                continue

            # ✅ 可以替换
            new_text = f'[[{entity_name}]]'
            replacements.append((idx, idx + len(entity_name), new_text))
            search_from = idx + len(new_text)

    # 按位置从后往前替换（避免偏移）
    replacements.sort(key=lambda x: -x[0])
    body_list = list(body)
    added = 0
    for start, end, new_text in replacements:
        # 重新检查是否被保护（可能在前面替换后变成了保护状态）
        body_list[start:end] = list(new_text)
        added += 1

    new_body = ''.join(body_list)
    new_content = frontmatter + new_body

    return new_content, added


def main():
    print("=" * 60)
    print("  三国知识库 WikiLink 增强工具")
    print("=" * 60)
    print()

    # 加载实体
    sorted_entities = load_entities()
    print()

    # 扫描所有人物文件
    files = sorted([f for f in os.listdir(CHAR_DIR) if f.endswith('.md') and not f.startswith('._')])
    print(f"📁 共 {len(files)} 个人物文件")

    total_added = 0
    stats = []
    errors = []

    for fname in files:
        filepath = os.path.join(CHAR_DIR, fname)
        try:
            new_content, added = enhance_wikilinks_in_file(filepath, sorted_entities)
            if added > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            stats.append((fname, added))
            total_added += added
        except Exception as e:
            errors.append(f"{fname}: {e}")

    # 统计
    print()
    print(f"✅ 共添加 {total_added} 个 WikiLink")
    top = sorted(stats, key=lambda x: -x[1])[:10]
    print(f"\nTop 10 增强最多的文件:")
    for fname, added in top:
        print(f"  +{added:3d}  {fname}")

    if errors:
        print(f"\n⚠️  {len(errors)} 个错误:")
        for e in errors[:5]:
            print(f"  {e}")

    print()
    print("=" * 60)
    print(f"  完成! 共处理 {len(files)} 个文件，添加 {total_added} 个链接")
    print("=" * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
