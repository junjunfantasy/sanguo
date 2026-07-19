#!/usr/bin/env python3
"""
三国知识库 KG 人物数据构建脚本
从 sanguo-knowledge/characters/*.md 提取所有人物数据，生成 kg/entities/characters.json

输出:
  - kg/entities/characters.json: 完整结构化的 KG 人物数据（v2 优化版）
  - kg/entities/characters_stats.json: 人物统计

用法:
  python scripts/build_kg_characters.py
"""

import os
import re
import json
import sys
import yaml
from collections import defaultdict, OrderedDict

# === 路径配置 ===
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAR_DIR = os.path.join(REPO_DIR, "sanguo-knowledge", "characters")
OUTPUT_JSON = os.path.join(REPO_DIR, "kg", "entities", "characters.json")
STATS_JSON = os.path.join(REPO_DIR, "kg", "entities", "characters_stats.json")

# 势力归一化映射
FACTION_MAP = {
    '魏': '魏', '曹魏': '魏', '魏国': '魏',
    '蜀': '蜀', '蜀汉': '蜀', '季汉': '蜀',
    '吴': '吴', '东吴': '吴', '孙吴': '吴',
    '群': '群', '群雄': '群',
    '汉': '汉',
    '晋': '晋', '西晋': '晋',
    '袁绍': '群', '袁术': '群', '吕布': '群', '董卓': '群',
    '公孙瓒': '群', '刘表': '群', '刘璋': '群',
    '张角': '群', '张鲁': '群',
    '': '群',
}

# 三国杀技能映射
SKILL_MAP = {
    '曹操': ['奸雄', '护驾'], '司马懿': ['反馈', '鬼才'], '郭嘉': ['天妒', '遗计'],
    '荀彧': ['驱虎', '节命'], '贾诩': ['完杀', '乱武', '帷幕'], '程昱': ['设伏', '贲育'],
    '张辽': ['突袭', '威风'], '夏侯惇': ['刚烈', '清俭'], '许褚': ['裸衣', '虎贲'],
    '曹丕': ['行殇', '放逐', '颂威'], '曹植': ['落英', '酒诗'], '曹冲': ['称象', '仁心'],
    '刘备': ['仁德', '激将'], '诸葛亮': ['观星', '空城'], '关羽': ['武圣', '义绝'],
    '张飞': ['咆哮', '探囊'], '赵云': ['龙胆', '救主'], '马超': ['马术', '铁骑'],
    '黄忠': ['弓骑', '烈弓'], '庞统': ['连环', '涅槃'], '法正': ['恩怨', '眩惑'],
    '魏延': ['狂骨', '奇谋'], '姜维': ['挑衅', '志继'], '黄月英': ['集智', '奇才'],
    '徐庶': ['举荐', '无言'],
    '孙权': ['制衡', '救援'], '周瑜': ['英姿', '反间'], '鲁肃': ['好施', '缔盟'],
    '吕蒙': ['克己', '涉猎'], '陆逊': ['谦逊', '连营'], '黄盖': ['苦肉', '诈降'],
    '甘宁': ['奇袭', '威风'],
    '吕布': ['无双'], '袁绍': ['乱击', '血裔'], '董卓': ['暴虐', '酒池'],
    '公孙瓒': ['白马', '义从'], '袁术': ['妄尊', '同疾'], '华佗': ['青囊', '急救'],
    '左慈': ['化身', '新生'], '于吉': ['蛊惑', '缠怨'],
    '曹叡': ['明鉴', '兴衰'], '曹仁': ['据守', '励战'], '夏侯渊': ['设伏', '奔袭'],
    '张郃': ['巧变', '破军'], '徐晃': ['断粮', '长驱'], '于禁': ['节钺', '毅重'],
    '乐进': ['骁果', '先登'],
    '刘禅': ['享乐', '放权'], '王平': ['镇军', '严整'], '严颜': ['据守', '不屈'],
    '关平': ['孝义', '护父'], '张苞': ['咆哮', '骁勇'], '孟获': ['获缚', '蛮力'],
    '祝融夫人': ['烈刃', '飞刀'], '刘表': ['自守', '宗室'],
    '孙策': ['激昂', '英魂'], '孙坚': ['英魂', '破虏'], '太史慈': ['天义', '信义'],
    '程普': ['醇醪', '厉战'], '韩当': ['弓骑', '水战'], '凌统': ['旋风', '勇决'],
    '貂蝉': ['离间', '闭月'], '张角': ['雷击', '鬼道'], '陈宫': ['明策', '智迟'],
    '廖化': ['当先', '伏枥'], '马谡': ['心战', '挥泪'], '蒋琬': ['镇守', '聚势'],
    '费祎': ['调和', '应变'], '蔡邕': ['书卷', '辨声'],
    '荀攸': ['奇策', '智囊'], '曹洪': ['援护', '让马'], '曹真': ['督军', '坚守'],
    '李典': ['儒雅', '谦让'], '臧霸': ['威震', '啸聚'], '高顺': ['陷阵', '忠烈'],
    '文丑': ['骁锐', '争先'], '颜良': ['雄毅', '先登'], '田丰': ['刚直', '死谏'],
    '马良': ['白眉', '联营'], '诸葛瑾': ['弘雅', '通达'], '张翼': ['持重', '稳进'],
    '张嶷': ['抚远', '效节'], '马岱': ['斩逆', '追袭'], '李严': ['督运', '托孤'],
    '刘封': ['刚猛', '离间'],
    '诸葛恪': ['才捷', '骄矜'], '周泰': ['护主', '创痕'], '丁奉': ['奋短', '突袭'],
    '徐盛': ['筑城', '火计'], '朱桓': ['奋励', '濡须'], '顾雍': ['持重', '默言'],
    '张昭': ['直谏', '托孤'], '陆抗': ['协守', '毁盟'],
    '刘协': ['天命', '禅让'], '何进': ['外戚', '召乱'], '王允': ['连环', '殉汉'],
    '李儒': ['鸩杀', '迁都'], '贾充': ['弑君', '谄附'], '邓艾': ['阴平', '屯田'],
    '钟会': ['奇袭', '谋逆'], '羊祜': ['怀远', '不战'], '杜预': ['武库', '灭吴'],

    '全琮': ['邀名', '矜功'],
    '公孙度': ['辽东', '裂土'],
    '公孙渊': ['绝盟', '称燕'],
    '关兴': ['武继', '奋锐'],
    '刘宏': ['卖官', '昏政'],
    '刘巴': ['锻币', '通市'],
    '刘晔': ['奇佐', '霹雳'],
    '刘焉': ['牧州', '立威'],
    '刘璋': ['暗弱', '引狼'],
    '刘谌': ['战绝', '死节'],
    '刘辩': ['废立', '鸩酒'],
    '华歆': ['望归', '息兵'],
    '华雄': ['耀武', '斩将'],
    '卢植': ['通经', '督学'],
    '司马孚': ['守正', '全节'],
    '司马师': ['刚厉', '景略'],
    '司马昭': ['筹策', '睥睨'],
    '司马朗': ['郡望', '施仁'],
    '司马炎': ['受禅', '一统'],
    '向朗': ['藏书', '好学'],
    '吕岱': ['平南', '清厉'],
    '吴懿': ['奔袭', '邀战'],
    '吴班': ['摧锋', '先登'],
    '周鲂': ['断发', '诱敌'],
    '大乔': ['国色', '流离'],
    '孔融': ['让梨', '名士'],
    '孙尚香': ['弓腰', '联姻'],
    '审配': ['刚直', '死守'],
    '小乔': ['天香', '红颜'],
    '张华': ['博物', '推贤'],
    '张杨': ['护友', '中立'],
    '张松': ['献图', '强识'],
    '张绍': ['承爵', '求和'],
    '张让': ['弄权', '十侍'],
    '张鲁': ['义舍', '布施'],
    '文鸯': ['骁勇', '单骑'],
    '曹休': ['千驹', '倾袭'],
    '曹彰': ['虎骑', '将才'],
    '曹昂': ['慷慨', '护主'],
    '曹爽': ['托孤', '擅权'],
    '曹纯': ['虎豹', '缮甲'],
    '朱儁': ['讨逆', '平乱'],
    '朱然': ['胆守', '奋战'],
    '李傕': ['凶暴', '劫掠'],
    '杨仪': ['筹度', '怨望'],
    '杨修': ['鸡肋', '才露'],
    '步骘': ['弘德', '定叛'],
    '淳于琼': ['守仓', '醉酒'],
    '满宠': ['御策', '峻法'],
    '潘璋': ['擒龙', '夺刀'],
    '王基': ['奇制', '进趋'],
    '王昶': ['持重', '固边'],
    '王朗': ['鼓舌', '激词'],
    '王濬': ['楼船', '破吴'],
    '田豫': ['安疆', '奋守'],
    '皇甫嵩': ['火攻', '整军'],
    '祢衡': ['击鼓', '裸衣'],
    '秦宓': ['天辩', '谏征'],
    '简雍': ['巧说', '纵适'],
    '糜竺': ['资援', '巨贾'],
    '糜芳': ['背刺', '怯战'],
    '臧洪': ['义烈', '杀妾'],
    '董袭': ['断后', '殉船'],
    '蒋济': ['谏诤', '催粮'],
    '蔡琰': ['归汉', '悲歌'],
    '虞翻': ['直言', '易理'],
    '袁尚': ['恃宠', '争嗣'],
    '袁谭': ['骄兵', '求盟'],
    '袁隗': ['门阀', '灭族'],
    '许攸': ['成略', '恃才'],
    '诸葛绪': ['阴平', '失守'],
    '诸葛靓': ['全节', '不仕'],
    '谯周': ['劝降', '仇国'],
    '贺齐': ['讨逆', '奋威'],
    '贾逵': ['忠谏', '通漕'],
    '赵忠': ['谗言', '敛财'],
    '辛毗': ['谏诤', '持节'],
    '邓芝': ['修好', '殒命'],
    '郝昭': ['镇骨', '拒降'],
    '郭汜': ['乱京', '纵兵'],
    '郭淮': ['精策', '御敌'],
    '钟离牧': ['抚夷', '辟土'],
    '钟繇': ['活墨', '佐定'],
    '陆凯': ['直谏', '贞良'],
    '陈到': ['白毦', '护主'],
    '陈寿': ['秉笔', '直书'],
    '陈群': ['定品', '法恩'],
    '陶谦': ['让贤', '仁政'],
    '霍峻': ['镇关', '守城'],
    '韩遂': ['羌合', '叛离'],
    '马忠': ['抚南', '诚抚'],
    '马腾': ['西征', '奉召'],
    '鲍信': ['识鉴', '赴义'],
    '麴义': ['先登', '强弩'],
    '黄权': ['远见', '北望'],
    '黄祖': ['阻江', '强射'],
}

# 拼音 ID 映射（完整覆盖 100 人）
PINYIN_MAP = {
    '丁奉': 'dingfeng', '严颜': 'yanyan', '乐进': 'yuejin', '于吉': 'yuji',
    '于禁': 'yujin', '何进': 'hejin', '关平': 'guanping', '关羽': 'guanyu',
    '典韦': 'dianwei', '凌统': 'lingtong', '刘协': 'liuxie', '刘备': 'liubei',
    '刘封': 'liufeng', '刘禅': 'liuchan', '刘表': 'liubiao', '华佗': 'huatuo',
    '司马懿': 'simayi', '吕布': 'lübu', '吕蒙': 'lvmeng',
    '周仓': 'zhoucang', '周泰': 'zhoutai', '周瑜': 'zhouyu',
    '夏侯惇': 'xiahoudun', '夏侯渊': 'xiahouyuan', '太史慈': 'taishici',
    '姜维': 'jiangwei', '孙坚': 'sunjian', '孙权': 'sunquan', '孙策': 'sunce',
    '孟获': 'menghuo', '左慈': 'zuoci', '庞统': 'pangtong', '廖化': 'liaohua',
    '张嶷': 'zhangni', '张昭': 'zhangzhao', '张翼': 'zhangyi', '张苞': 'zhangbao',
    '张角': 'zhangjue', '张辽': 'zhangliao', '张郃': 'zhanghe', '张飞': 'zhangfei',
    '徐庶': 'xushu', '徐晃': 'xuhuang', '徐盛': 'xusheng', '文丑': 'wenchou',
    '曹丕': 'caopi', '曹仁': 'caoren', '曹冲': 'caochong', '曹叡': 'caorui',
    '曹操': 'caocao', '曹植': 'caozhi', '曹洪': 'caohong', '曹真': 'caozhen',
    '朱桓': 'zhuhuan', '李严': 'liyan', '李儒': 'liru', '李典': 'lidian',
    '杜预': 'duyu', '法正': 'fazheng', '王允': 'wangyun', '王平': 'wangping',
    '甘宁': 'ganning', '田丰': 'tianfeng', '祝融夫人': 'zhurongfuren',
    '程昱': 'chengyu', '程普': 'chengpu', '羊祜': 'yanghu', '臧霸': 'zangba',
    '荀彧': 'xunyu', '荀攸': 'xunyou', '蒋琬': 'jiangwan', '蔡邕': 'caiyong',
    '许褚': 'xuchu', '诸葛亮': 'zhugeliang', '诸葛恪': 'zhugeke',
    '诸葛瑾': 'zhugejin', '貂蝉': 'diaochan', '费祎': 'feiyi', '贾充': 'jiachong',
    '贾诩': 'jiaxu', '赵云': 'zhaoyun', '邓艾': 'dengai', '郭嘉': 'guojia',
    '钟会': 'zhonghui', '陆抗': 'lukang', '陆逊': 'luxun', '陈宫': 'chengong',
    '韩当': 'handang', '顾雍': 'guyong', '颜良': 'yanliang', '马岱': 'madai',
    '马良': 'maliang', '马谡': 'masu', '马超': 'machao', '高顺': 'gaoshun',
    '魏延': 'weiyan', '鲁肃': 'lusu', '黄月英': 'huangyueying', '黄盖': 'huanggai',
    '黄忠': 'huangzhong', '黄权': 'huangquan', '黄祖': 'huangzu',
    '诸葛瞻': 'zhugezhan', '司马昭': 'simazhao', '司马师': 'simashi',
    '司马防': 'simafang', '刘谌': 'liuchen', '刘永': 'liuyong', '刘理': 'liuli',
    '孙尚香': 'sunshangxiang', '大乔': 'daqiao', '小乔': 'xiaoqiao',
    '公孙瓒': 'gongsunzan',
}


def make_entity_id(name):
    """将中文名转为 Latin 字母 ID"""
    if name in PINYIN_MAP:
        return PINYIN_MAP[name].replace(' ', '').lower()
    # fallback: 取前两个字的拼音首字母
    code = str(ord(name[0]))[:3] if name else '000'
    return f'char_{code}'


# 关系上下文关键词映射（按优先级排序）
RELATION_PATTERNS = [
    ('relatives', ['父', '母', '子', '女', '妻', '夫', '兄', '弟', '姐', '妹',
                   '家族', '亲戚', '亲属', '儿子', '女儿', '父亲', '母亲',
                   '妻子', '夫人', '哥哥', '弟弟', '姐姐', '妹妹', '堂',
                   '叔', '伯', '舅', '姑', '姨', '侄', '甥', '孙']),
    ('brothers', ['结义', '义兄', '义弟', '异姓兄弟', '桃园', '拜把']),
    ('liege', ['君主', '主公', '主上', '皇帝', '大王', '陛下', '王爷',
               '帝', '王', '皇']),
    ('subordinates', ['部下', '部将', '下属', '手下', '大将', '将领',
                      '统帅', '都督', '麾下', '帐下', '参军', '先锋']),
    ('colleagues', ['同僚', '同事', '共事', '一起', '同道', '并肩',
                    '合作', '共同']),
    ('rivals', ['对手', '敌人', '打败', '击败', '对抗', '对阵', '敌方',
                '敌对', '仇', '战', '攻', '伐', '讨']),
    ('recommended', ['推荐', '举荐', '推荐人', '引荐', '荐']),
    ('mentor', ['师从', '学生', '弟子', '师父', '老师', '教导', '师生', '师']),
    ('friends', ['朋友', '好友', '故交', '故人', '至交', '知己', '交好']),
]


def is_location_or_abstract(link):
    """判断 wiki 链接是否是地点或抽象概念（不是人物）"""
    known_locations = {'洛阳', '长安', '成都', '许都', '建业', '荆州', '益州',
                       '徐州', '兖州', '冀州', '青州', '并州', '凉州', '雍州',
                       '司隶', '扬州', '交州', '幽州', '豫州', '赤壁', '官渡',
                       '街亭', '五丈原', '汉中', '夷陵', '樊城', '合肥',
                       '隆中', '南中', '江东', '中原', '西凉', '河北',
                       '虎牢关', '定军山', '逍遥津', '白帝城', '麦城',
                       '陈留', '谯郡', '颍川', '南阳', '襄阳',
                       '益州', '江陵', '长沙', '零陵', '桂阳',
                       '武陵', '巴郡', '蜀郡', '汉中郡',
                       '庐江', '会稽', '吴郡', '丹阳', '豫章',
                       '南郡', '巴东', '巴西',
                       }
    known_concepts = {'武将', '文臣', '谋士', '军师', '君主', '皇帝', '汉室',
                      '奸雄', '忠义', '勇猛', '仁德',
                      '步兵', '骑兵', '水军', '弓兵', '连弩', '虎豹骑',
                      '丹阳兵', '白毦兵', '藤甲兵', '锦帆贼',
                      '五虎上将', '五子良将', '八虎骑', '建安七子',
                      '三公', '九卿', '刺史', '州牧', '太守', '丞相',
                      '大将军', '太尉', '司徒', '司空',
                      '屯田', '青州兵',
                      }
    return link in known_locations or link in known_concepts


def extract_wiki_links(text):
    """从文本中提取 [[链接]] 格式的 wiki 链接，返回去重有序列表"""
    links = re.findall(r'\[\[([^\]]+?)\]\]', text)
    # 去重但保持顺序
    seen = set()
    result = []
    for link in links:
        # 去掉链接中的 | 管道符（如 [[曹操|曹孟德]] -> 曹操）
        link = link.split('|')[0].strip()
        if link not in seen:
            seen.add(link)
            result.append(link)
    return result


def normalize_faction(faction_val):
    """归一化势力值"""
    if isinstance(faction_val, list):
        faction_val = faction_val[0] if faction_val else ''
    if isinstance(faction_val, str):
        return FACTION_MAP.get(faction_val.strip(), faction_val.strip())
    return '群'


def categorize_relations(wiki_links, body_text):
    """根据上下文对 wiki 链接进行分类，过滤非人物链接"""
    relations = defaultdict(list)
    seen = set()

    lines = body_text.split('\n')
    # 构建行号索引
    link_contexts = {}  # link -> list of nearby lines
    for i, line in enumerate(lines):
        found_links = re.findall(r'\[\[([^\]]+?)\]\]', line)
        for link in found_links:
            link = link.split('|')[0].strip()
            if link not in link_contexts:
                link_contexts[link] = []
            # 取上下文（前后各2行）
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            context_text = '\n'.join(lines[start:end]).lower()
            link_contexts[link].append(context_text)

    for link in wiki_links:
        # 跳过地点和抽象概念
        if is_location_or_abstract(link):
            continue
        if link in seen:
            continue
        seen.add(link)

        # 合并所有上下文
        contexts = link_contexts.get(link, [])
        context = '\n'.join(contexts)

        classified = False
        for rel_type, keywords in RELATION_PATTERNS:
            for kw in keywords:
                if kw in context:
                    # 避免误分类：如果同时匹配多个，选优先级最高的
                    relations[rel_type].append(link)
                    classified = True
                    break
            if classified:
                break

        if not classified:
            relations['related'].append(link)

    # 去重
    cleaned = {}
    for k, v in relations.items():
        cleaned[k] = list(OrderedDict.fromkeys(v))
    return cleaned


def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return {}, content
    try:
        fm = yaml.safe_load(fm_match.group(1))
    except:
        return {}, content
    body = content[fm_match.end():].strip()
    return fm if isinstance(fm, dict) else {}, body


def extract_summary(body_text):
    """从正文提取摘要（从 性格特点 节取第一段）"""
    # 找 ## 性格特点 下的内容
    lines = body_text.split('\n')
    in_summary = False
    summary_parts = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## 性格特点'):
            in_summary = True
            continue
        if in_summary:
            if stripped.startswith('## '):
                break
            if stripped and not stripped.startswith('-') and not stripped.startswith('*'):
                # Clean wiki links and markdown
                clean = re.sub(r'\[\[([^\]]+?)(\|[^\]]+)?\]\]', r'\1', stripped)
                clean = re.sub(r'\*\*', '', clean)
                clean = re.sub(r'^#+\s*', '', clean)
                if clean:
                    summary_parts.append(clean)

    summary = ''.join(summary_parts)
    if len(summary) > 150:
        summary = summary[:147] + '…'
    elif not summary:
        # fallback: first meaningful line
        for line in lines:
            s = line.strip()
            if s and not s.startswith('#') and not s.startswith('-') and not s.startswith('*') and not s.startswith('|'):
                clean = re.sub(r'\[\[([^\]]+?)\]\]', r'\1', s)
                summary = clean[:150]
                break
    return summary.strip()


def process_all_characters():
    """处理所有角色 markdown 文件"""
    characters = []
    stats = {
        'total': 0,
        'by_faction': defaultdict(int),
        'by_era': defaultdict(int),
        'by_tags': defaultdict(int),
        'total_relations': 0,
        'errors': [],
    }

    if not os.path.isdir(CHAR_DIR):
        print(f"❌ 目录不存在: {CHAR_DIR}")
        return [], stats

    files = sorted([f for f in os.listdir(CHAR_DIR) if f.endswith('.md') and not f.startswith('._')])
    errors = []

    for fname in files:
        filepath = os.path.join(CHAR_DIR, fname)
        name_from_file = fname[:-3]

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"⚠️  读取失败: {fname} - {e}")
            continue

        # 解析 YAML frontmatter
        fm, body = parse_frontmatter(content)
        if not fm or 'name' not in fm:
            errors.append(f"⚠️  无效 frontmatter: {fname}")
            continue

        cname = fm.get('name', name_from_file)
        aliases = fm.get('aliases', [])
        if isinstance(aliases, str):
            aliases = [aliases]

        faction = normalize_faction(fm.get('faction', ['群']))
        birth_year = fm.get('birth_year')
        death_year = fm.get('death_year')
        era = fm.get('era', [])
        if isinstance(era, str):
            era = [era]

        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]

        # 生成实体 ID
        entity_id = make_entity_id(cname)

        # 提取 wiki 链接和关系
        wiki_links = extract_wiki_links(body)
        relations = categorize_relations(wiki_links, body)
        stats['total_relations'] += len(wiki_links)

        # 提取摘要
        summary = extract_summary(body)

        # 获取三国杀技能
        skills = SKILL_MAP.get(cname, [])

        # 构建人物条目
        entity = OrderedDict([
            ('id', entity_id),
            ('name', cname),
            ('aliases', aliases),
            ('faction', faction),
            ('birth_year', birth_year if birth_year else None),
            ('death_year', death_year if death_year else None),
            ('era', era),
            ('tags', tags),
            ('skills', skills),
            ('summary', summary),
        ])

        # 添加关系（只保留非空）
        cleaned_rels = {k: v for k, v in relations.items() if v}
        if cleaned_rels:
            entity['related_entities'] = cleaned_rels

        characters.append(entity)

        # 统计
        stats['by_faction'][faction] += 1
        for e in era:
            stats['by_era'][e] += 1
        for t in tags:
            stats['by_tags'][t] += 1

    stats['total'] = len(characters)
    stats['errors'] = errors
    stats['faction_counts'] = dict(stats['by_faction'])
    stats['era_counts'] = dict(stats['by_era'])
    stats['top_tags'] = dict(sorted(stats['by_tags'].items(), key=lambda x: -x[1])[:20])

    return characters, stats


def main():
    print("=" * 60)
    print("  三国知识库 KG 人物数据构建工具 v2")
    print("=" * 60)
    print(f"  人物目录: {CHAR_DIR}")
    print(f"  输出: {OUTPUT_JSON}")
    print()

    print("[1/3] 扫描人物 Markdown 文件...")
    characters, stats = process_all_characters()

    print(f"  ✅ 成功处理 {stats['total']} 个人物")
    total_rels = stats.get('total_relations', 0)
    print(f"  📎 提取 {total_rels} 条 wiki 链接关系")

    if stats['errors']:
        print(f"  ⚠️  {len(stats['errors'])} 个警告:")
        for e in stats['errors'][:3]:
            print(f"    {e}")

    print()
    print("[2/3] 势力分布:")
    for faction, count in sorted(stats['faction_counts'].items(), key=lambda x: -x[1]):
        bar = '█' * (count * 2)
        print(f"    {faction}: {count:2d}人 {bar}")

    print(f"  标签 Top 10:")
    for tag, count in sorted(stats['top_tags'].items(), key=lambda x: -x[1])[:10]:
        print(f"    {tag}: {count}人")

    # 写入 JSON
    print()
    print("[3/3] 写入 characters.json...")
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    output = OrderedDict([
        ('meta', OrderedDict([
            ('generated_by', 'build_kg_characters.py'),
            ('version', '2.0'),
            ('total_characters', stats['total']),
            ('total_relations', total_rels),
        ])),
        ('characters', characters),
    ])

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    json_size = os.path.getsize(OUTPUT_JSON)
    print(f"  ✅ 已写入: {OUTPUT_JSON} ({json_size:,} bytes)")

    stats_path = STATS_JSON
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✅ 已写入: {stats_path}")

    print()
    print("=" * 60)
    print(f"  完成! 共处理 {stats['total']} 个人物，{total_rels} 条关系")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
