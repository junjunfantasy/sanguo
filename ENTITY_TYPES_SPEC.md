# Three Kingdoms Knowledge Base - Entity Types Specification

## Overview
This specification defines the entity types for the Three Kingdoms knowledge base, combining historical sources (Records of Three Kingdoms), literary sources (Romance of Three Kingdoms), and card game mechanics (三国杀).

## Core Entity Types (20 categories)

### 1. 人物
- **Subtypes**: 历史人物, 文学人物, 虚构人物
- **Attributes**: 
  - 姓名, 字, 号, 谥号
  - 生卒年份, 籍贯
  - 所属势力, 官职
  - 武力值, 智力值, 政治值, 魅力值
  - 典故, 评价
- **Examples**: 刘备, 曹操, 孙权, 诸葛亮, 关羽, 吕布

### 2. 势力
- **Subtypes**: 主要势力, 地方势力, 短期势力
- **Attributes**:
  - 势力名称, 统治者
  - 存续时间, 首都
  - 疆域范围, 人口
  - 旗帜颜色, 图腾
- **Examples**: 蜀汉, 曹魏, 东吴, 袁绍, 董卓

### 3. 地点
- **Subtypes**: 城市, 郡县, 关隘, 战场, 地形
- **Attributes**:
  - 名称, 古名, 今名
  - 地理位置, 坐标
  - 所属势力, 战略价值
  - 相关战役, 历史事件
- **Examples**: 洛阳, 长安, 赤壁, 虎牢关, 荆州

### 4. 官职
- **Subtypes**: 中央官职, 地方官职, 军职, 虚衔
- **Attributes**:
  - 官职名称, 品级
  - 职权范围, 设置时间
  - 著名担任者, 废除时间
- **Examples**: 丞相, 大将军, 太守, 刺史, 都督

### 5. 兵种
- **Subtypes**: 步兵 骑兵, 水军, 攻城器械
- **Attributes**:
  - 兵种名称, 特点
  - 装备, 战术用途
  - 代表战役, 著名将领
- **Examples**: 虎豹骑, 丹阳兵, 白毦兵, 连弩

### 6. 武器
- **Subtypes**: 冷兵器, 攻城器械, 防御装备
- **Attributes**:
  - 武器名称, 类型
  - 持有者, 传说
  - 威力, 特殊能力
- **Examples**: 青龙偃月刀, 方天画戟, 丈八蛇矛, 倚天剑

### 7. 战役
- **Subtypes**: 大型战役, 小规模战斗, 围城战, 水战
- **Attributes**:
  - 战役名称, 时间
  - 交战双方, 地点
  - 参战兵力, 战果
  - 战术特点, 历史影响
- **Examples**: 官渡之战, 赤壁之战, 夷陵之战, 淝水之战

### 8. 策略
- **Subtypes**: 军事策略, 政治策略, 外交策略
- **Attributes**:
  - 策略名称, 类型
  - 提出者, 使用场合
  - 执行过程, 效果
  - 相关典故
- **Examples**: 空城计, 苦肉计, 连环计, 远交近攻

### 9. 典故
- **Subtypes**: 成语典故, 历史典故, 文学典故
- **Attributes**:
  - 典故名称, 出处
  - 相关人物, 事件
  - 含义, 现代用法
- **Examples**: 三顾茅庐, 草船借箭, 桃园结义, 乐不思蜀

### 10. 文献
- **Subtypes**: 史书, 小说, 诗歌, 评论
- **Attributes**:
  - 文献名称, 作者
  - 成书时间, 版本
  - 内容概述, 价值
- **Examples**: 三国志, 三国演义, 三国志平话, 曹操集

### 11. 年号
- **Subtypes**: 皇帝年号, 地方势力年号
- **Attributes**:
  - 年号名称, 使用者
  - 起止时间, 改元原因
  - 公元对应
- **Examples**: 建安, 黄初, 章武, 嘉禾

### 12. 制度
- **Subtypes**: 政治制度, 经济制度, 军事制度, 文化制度
- **Attributes**:
  - 制度名称, 类型
  - 制定者, 实施时间
  - 内容, 影响
- **Examples**: 屯田制, 九品中正制, 世兵制

### 13. 建筑
- **Subtypes**: 宫殿, 城池, 陵墓, 寺庙
- **Attributes**:
  - 建筑名称, 类型
  - 位置, 建造时间
  - 建筑特点, 现状
- **Examples**: 铜雀台, 许都宫殿, 成都皇宫, 孙权陵

### 14. 物品
- **Subtypes**: 日常用品, 礼仪用品, 艺术品
- **Attributes**:
  - 物品名称, 用途
  - 持有者, 相关事件
  - 文化意义
- **Examples**: 传国玉玺, 七星灯, 赤兔马, 的卢马

### 15. 组织
- **Subtypes**: 政治集团, 军事集团, 学术团体
- **Attributes**:
  - 组织名称, 性质
  - 成员, 活动
  - 影响力
- **Examples**: 二十八路诸侯, 江东集团, 荆州集团

### 16. 技能
- **Subtypes**: 武将技能, 谋士技能, 特殊技能
- **Attributes**:
  - 技能名称, 类型
  - 拥有者, 效果
  - 发动条件, 历史依据
- **Examples**: 仁德, 奸雄, 诸葛连弩, 借刀杀人

### 17. 卡牌
- **Subtypes**: 武将卡, 基本牌, 锦囊牌, 装备牌
- **Attributes**:
  - 卡牌名称, 类型
  - 效果, 使用条件
  - 设计来源, 平衡性
- **Examples**: 杀, 闪, 桃, 无中生有, 万箭齐发

### 18. 关系
- **Subtypes**: 血缘关系, 政治关系, 军事关系, 个人关系
- **Attributes**:
  - 关系类型, 双方
  - 关系性质, 开始时间
  - 变化过程, 结束时间
- **Examples**: 君臣, 父子, 兄弟, 师徒, 敌对, 盟友

### 19. 时间
- **Subtypes**: 年份, 季节, 月份, 具体日期
- **Attributes**:
  - 时间描述, 公元对应
  - 农历对应, 相关事件
  - 历法系统
- **Examples**: 建安十三年, 冬十月, 公元208年

### 20. 评价
- **Subtypes**: 历史评价, 文学评价, 现代评价
- **Attributes**:
  - 评价内容, 评价者
  - 评价对象, 评价角度
  - 出处, 影响力
- **Examples**: "治世之能臣，乱世之奸雄", "千古良相"

## Entity Relationships

### Character Relationships
- **血缘**: 父子, 母子, 兄弟, 姐妹, 夫妻
- **政治**: 君臣, 同僚, 上下级
- **军事**: 统帅, 部将, 同袍
- **个人**: 朋友, 敌人, 师徒, 恩人

### Spatial Relationships
- **隶属**: 城市→郡国→州
- **相邻**: 边界接壤
- **距离**: 里程, 行军时间

### Temporal Relationships
- **先后**: 时间顺序
- **重叠**: 同期存在
- **因果**: 事件因果关系

### Faction Relationships
- **从属**: 个人→势力
- **联盟**: 势力间合作
- **敌对**: 势力间冲突
- **臣服**: 势力间依附

## Data Sources Integration

### Historical Sources (三国志)
- 优先级: 高
- 可信度: 高
- 覆盖: 魏书, 蜀书, 吴书

### Literary Sources (三国演义)
- 优先级: 中
- 可信度: 中 (文学加工)
- 覆盖: 全书120回

### Card Game Sources (三国杀)
- 优先级: 中
- 可信度: 游戏平衡性
- 覆盖: 标准版, 扩展包

## Annotation Guidelines

### Entity Identification
- 历史人物优先使用史书记载姓名
- 文学虚构人物标注"虚构"属性
- 同一人物不同名称建立别名映射

### Attribute Extraction
- 数值属性(武力/智力)以史书为基准
- 文学描述作为补充标注
- 卡牌数值作为游戏化参考

### Relationship Validation
- 历史关系以正史为准
- 文学关系标注出处
- 游戏关系标注"游戏设定"

## Quality Control

### Consistency Rules
- 同一实体在不同文献中保持统一ID
- 时间属性统一转换为公元纪年
- 地理属性标注古今对照

### Completeness Standards
- 核心人物100%属性覆盖
- 重要事件90%关系覆盖
- 主要势力80%数据覆盖

### Accuracy Validation
- 历史数据交叉验证
- 文学数据标注来源
- 游戏数据标注版本
