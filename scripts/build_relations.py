#!/usr/bin/env python3
"""
从 KG 人物数据自动生成 docs/data/relations.js
覆盖全部 200 位人物，生成父子/兄弟/夫妻/君臣/敌对/同僚/盟友/宗亲关系
"""
import os, json, re

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_CHARS = os.path.join(REPO_DIR, "kg", "entities", "characters.json")
OUTPUT_JS = os.path.join(REPO_DIR, "docs", "data", "relations.js")

# 已知父子关系 (source=父亲, target=儿子)
FATHER_SON = [
    ('曹操','曹丕'),('曹操','曹植'),('曹操','曹彰'),('曹操','曹冲'),('曹操','曹昂'),
    ('曹丕','曹叡'),('孙坚','孙策'),('孙坚','孙权'),('刘备','刘禅'),('刘备','刘封'),
    ('关羽','关平'),('关羽','关兴'),('张飞','张苞'),('张飞','张绍'),
    ('诸葛亮','诸葛瞻'),('诸葛瑾','诸葛恪'),('陆逊','陆抗'),
    ('司马懿','司马师'),('司马懿','司马昭'),('司马昭','司马炎'),
    ('曹真','曹爽'),('孙权','孙亮'),('孙权','孙和'),('袁绍','袁谭'),('袁绍','袁尚'),
    ('刘焉','刘璋'),('公孙度','公孙康'),('公孙康','公孙渊'),
    ('马腾','马超'),('曹仁','曹泰'),('张昭','张承'),
    ('曹操','曹霖'),('刘表','刘琦'),('刘表','刘琮'),
    ('曹丕','曹霖'),('司马师','司马攸'),
]
# 已知兄弟关系
BROTHERS = [
    ('孙策','孙权'),('袁谭','袁尚'),('袁谭','袁熙'),('袁尚','袁熙'),
    ('曹丕','曹植'),('曹丕','曹彰'),('曹彰','曹植'),
    ('夏侯惇','夏侯渊'),('诸葛亮','诸葛瑾'),('马良','马谡'),
    ('司马师','司马昭'),('司马孚','司马懿'),
    ('张苞','张绍'),('刘琦','刘琮'),('全琮','全绪'),
]
# 已知夫妻关系
COUPLES = [
    ('刘备','孙尚香'),('孙策','大乔'),('周瑜','小乔'),
    ('诸葛亮','黄月英'),('孟获','祝融夫人'),('吕布','貂蝉'),
    ('蔡邕','蔡琰'),
]
# 已知师徒关系
MENTOR_STUDENT = [
    ('诸葛亮','姜维'),('诸葛亮','马谡'),('周瑜','吕蒙'),
    ('吕蒙','陆逊'),('陆逊','陆抗'),('刘备','卢植'),
    ('郑玄','卢植'),
]

def main():
    with open(KG_CHARS, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chars = data['characters']
    char_names = {c['name'] for c in chars}

    relations = []
    seen_pairs = {}  # pair -> index in relations list

    def add_rel(source, target, rtype):
        pair = tuple(sorted([source, target]))
        if pair not in seen_pairs and source in char_names and target in char_names:
            seen_pairs[pair] = len(relations)
            relations.append([source, target, rtype])
        elif pair in seen_pairs and source in char_names and target in char_names:
            # Overwrite with more specific type
            idx = seen_pairs[pair]
            old_type = relations[idx][2]
            # Priority: 父子 > 兄弟 > 夫妻 > 师徒 > 君臣 > 敌对 > 同僚 > 盟友 > 宗亲
            priority = {'父子':0,'兄弟':1,'夫妻':2,'师徒':3,'君臣':4,'敌对':5,'同僚':6,'盟友':7,'宗亲':8}
            if priority.get(rtype, 9) < priority.get(old_type, 9):
                relations[idx][2] = rtype

    # 1. 从 KG related_entities 提取
    REL_TYPE_MAP = {
        'relatives': '宗亲', 'brothers': '兄弟', 'liege': '君臣',
        'subordinates': '君臣', 'colleagues': '同僚', 'rivals': '敌对',
        'mentor': '师徒', 'friends': '盟友', 'recommended': '同僚',
    }
    for c in chars:
        source = c['name']
        for rel_key, targets in c.get('related_entities', {}).items():
            gtype = REL_TYPE_MAP.get(rel_key, '同僚')
            for target in targets:
                if target in char_names and target != source:
                    add_rel(source, target, gtype)

    # 2. 覆盖已知父子关系
    for father, son in FATHER_SON:
        add_rel(father, son, '父子')

    # 3. 覆盖已知兄弟关系
    for a, b in BROTHERS:
        add_rel(a, b, '兄弟')

    # 4. 覆盖已知夫妻关系
    for a, b in COUPLES:
        add_rel(a, b, '夫妻')

    # 5. 覆盖已知师徒关系
    for teacher, student in MENTOR_STUDENT:
        add_rel(teacher, student, '师徒')

    # 6. 已知敌对关系 (从 wiki 文本中提取的关键对抗)
    RIVALS = [
        ('曹操','刘备'),('曹操','孙权'),('曹操','袁绍'),('曹操','吕布'),('曹操','马超'),
        ('刘备','曹操'),('刘备','孙权'),('刘备','吕布'),
        ('孙权','曹操'),('孙权','刘备'),('孙权','张辽'),
        ('诸葛亮','司马懿'),('诸葛亮','曹真'),('关羽','吕蒙'),('关羽','曹仁'),
        ('周瑜','曹操'),('陆逊','刘备'),('吕布','曹操'),
        ('孙策','刘表'),('邓艾','姜维'),('钟会','姜维'),
        ('刘协','曹操'),('张辽','孙权'),('马超','曹操'),
        ('曹操','袁术'),('曹操','张绣'),('袁绍','公孙瓒'),
        ('诸葛亮','张郃'),('姜维','邓艾'),('姜维','钟会'),
        ('夏侯渊','黄忠'),('张郃','马谡'),
        ('司马懿','曹爽'),('司马师','毌丘俭'),('司马昭','诸葛诞'),
    ]
    for a, b in RIVALS:
        add_rel(a, b, '敌对')

    # 排序
    type_order = {'父子':0,'兄弟':1,'夫妻':2,'宗亲':3,'君臣':4,'师徒':5,'同僚':6,'敌对':7,'盟友':8}
    relations.sort(key=lambda r: (type_order.get(r[2],9), r[0], r[1]))

    # 生成 JS
    lines = ['// 三国人物关系数据 - 从KG自动生成', 'const SANGUO_RELATIONS = [']
    for source, target, rtype in relations:
        lines.append(f"  {{ source: '{source}', target: '{target}', type: '{rtype}' }},")
    lines.append('];')

    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # 统计
    char_in_rel = set()
    for s, t, _ in relations:
        char_in_rel.add(s); char_in_rel.add(t)

    type_counts = {}
    for _, _, rtype in relations:
        type_counts[rtype] = type_counts.get(rtype, 0) + 1

    print(f"✅ 生成完成: {OUTPUT_JS}")
    print(f"   共 {len(relations)} 条关系，覆盖 {len(char_in_rel)}/200 位人物")
    for t in ['父子','兄弟','夫妻','宗亲','君臣','师徒','同僚','敌对','盟友']:
        c = type_counts.get(t, 0)
        print(f"     {t}: {c}")

    # 更新 graph.html subtitle
    graph_html = os.path.join(REPO_DIR, 'docs', 'graph.html')
    with open(graph_html, 'r', encoding='utf-8') as f:
        html = f.read()
    new_sub = f'拖动缩放 · 悬停查看人物信息 · 颜色按势力区分 · <strong>{len(char_in_rel)}位人物 / {len(relations)}条关系</strong>'
    html = re.sub(r'拖动缩放.*?位人物 / \d+条关系', new_sub, html)
    with open(graph_html, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"   已更新 graph.html subtitle")

if __name__ == '__main__':
    main()
