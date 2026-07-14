# Three Kingdoms Knowledge Base - Event Types Specification

## Overview
This specification defines the event types and relationship schemas for the Three Kingdoms knowledge base, covering the period from 184 AD (Yellow Turban Rebellion) to 280 AD (Fall of Wu).

## Event Types (12 categories)

### 1. 军事事件
- **Subtypes**: 战役, 战斗, 围城, 水战, 骚扰, 伏击
- **Core Attributes**:
  - 事件名称, 时间, 地点
  - 交战双方, 指挥官
  - 参战兵力, 伤亡情况
  - 战术特点, 战略意义
  - 史料来源, 文学描述
- **Examples**: 官渡之战, 赤壁之战, 五丈原之战, 樊城之战

### 2. 政治事件
- **Subtypes**: 政变, 禅让, 册封, 废立, 朝议, 结盟
- **Core Attributes**:
  - 事件名称, 时间, 地点
  - 主要参与者, 决策过程
  - 政治背景, 影响范围
  - 历史评价, 后续发展
- **Examples**: 董卓之乱, 曹丕篡汉, 夷陵之战后的政治重组

### 3. 人事事件
- **Subtypes**: 任命, 免职, 投奔, 叛变, 被俘, 死亡
- **Core Attributes**:
  - 人物, 事件类型
  - 时间, 地点
  - 相关人物, 原因
  - 影响后果
- **Examples**: 诸葛亮出山, 关羽投降曹操, 马谡失街亭被斩

### 4. 外交事件
- **Subtypes**: 结盟, 毁盟, 联姻, 质子, 使节, 条约
- **Core Attributes**:
  - 事件名称, 时间
  - 参与势力/人物
  - 协议内容, 期限
  - 执行情况, 破坏原因
- **Examples**: 孙刘联盟, 魏吴联盟, 蜀吴联姻

### 5. 经济事件
- **Subtypes**: 屯田, 赋税, 贸易, 饥荒, 迁民, 兴修水利
- **Core Attributes**:
  - 事件类型, 时间
  - 实施者, 受影响地区
  - 具体措施, 效果
  - 经济影响
- **Examples**: 曹操屯田制, 诸葛亮治蜀, 蜀汉南中开发

### 6. 文化事件
- **Subtypes**: 著述, 教育, 艺术, 宗教, 科技发明
- **Core Attributes**:
  - 事件类型, 时间
  - 主要人物, 成果
  - 影响范围, 传承
- **Examples**: 曹操建安文学, 诸葛亮木牛流马, 华佗医学

### 7. 自然灾害
- **Subtypes**: 水灾, 旱灾, 疫病, 地震, 蝗灾
- **Core Attributes**:
  - 灾害类型, 时间
  - 受灾地区, 程度
  - 应对措施, 影响
- **Examples**: 建安大瘟疫, 荆州水灾

### 8. 社会事件
- **Subtypes**: 起义, 暴动, 迁徙, 流民, 民变
- **Core Attributes**:
  - 事件类型, 时间
  - 参与者, 规模
  - 原因, 结果
- **Examples**: 黄巾起义, 五溪蛮夷叛乱

### 9. 工程事件
- **Subtypes**: 城池建设, 道路修建, 运河开凿, 防御工事
- **Core Attributes**:
  - 工程名称, 时间
  - 主持者, 地点
  - 规模, 用途
  - 现状
- **Examples**: 铜雀台修建, 成都城墙建设

### 10. 宗教事件
- **Subtypes**: 佛教传播, 道教活动, 祭祀, 占卜
- **Core Attributes**:
  - 事件类型, 时间
  - 参与者, 内容
  - 影响范围
- **Examples**: 张角太平道, 于吉道教活动

### 11. 法律事件
- **Subtypes**: 立法, 司法, 赦免, 刑罚
- **Core Attributes**:
  - 事件类型, 时间
  - 制定者/执行者
  - 内容, 对象
  - 影响
- **Examples**: 曹操制定新法, 诸葛亮治蜀法度

### 12. 情报事件
- **Subtypes**: 间谍, 侦察, 反间, 密信, 谍报
- **Core Attributes**:
  - 事件类型, 时间
  - 执行者, 目标
  - 内容, 结果
- **Examples**: 蒋干盗书, 周瑜反间计

## Relationship Types (9 categories)

### 1. 血缘关系
- **Types**: 父子, 母子, 夫妻, 兄弟, 姐妹, 祖孙, 叔侄, 姻亲
- **Attributes**: 关系类型, 开始时间, 结束时间(如死亡), 性质
- **Examples**: 刘备-刘禅(父子), 孙权-孙尚香(兄妹)

### 2. 政治关系
- **Types**: 君臣, 同僚, 上下级, 政敌, 盟友
- **Attributes**: 关系类型, 开始时间, 结束时间, 权力结构
- **Examples**: 曹操-荀彧(君臣), 诸葛亮-李严(同僚)

### 3. 军事关系
- **Types**: 统帅-部将, 同袍, 敌对, 投降, 救援
- **Attributes**: 关系类型, 开始时间, 结束时间, 军事层级
- **Examples**: 周瑜-黄盖(统帅-部将), 关羽-张飞(同袍)

### 4. 个人关系
- **Types**: 朋友, 师徒, 恩人, 仇敌, 知己
- **Attributes**: 关系类型, 开始时间, 结束时间, 情感性质
- **Examples**: 刘备-诸葛亮(君臣+知己), 庞统-诸葛亮(同僚)

### 5. 地理关系
- **Types**: 隶属, 相邻, 包含, 距离, 交通
- **Attributes**: 关系类型, 具体描述, 战略意义
- **Examples**: 荆州-襄阳(隶属), 许昌-洛阳(相邻)

### 6. 时间关系
- **Types**: 先后, 同期, 重叠, 因果
- **Attributes**: 关系类型, 时间差, 逻辑联系
- **Examples**: 官渡之战(先)-赤壁之战(后), 诸葛亮-司马懿(同期)

### 7. 势力关系
- **Types**: 从属, 联盟, 敌对, 臣服, 竞争
- **Attributes**: 关系类型, 开始时间, 结束时间, 力量对比
- **Examples**: 蜀汉-东吴(联盟), 曹魏-蜀汉(敌对)

### 8. 文献关系
- **Types**: 记载, 引用, 补充, 矛盾, 评价
- **Attributes**: 关系类型, 具体内容, 可信度
- **Examples**: 三国志-三国演义(记载与文学化)

### 9. 游戏关系
- **Types**: 技能关联, 卡牌配合, 阵营归属, 平衡关系
- **Attributes**: 关系类型, 游戏机制, 设计意图
- **Examples**: 诸葛亮-空城计(技能关联), 刘备-仁德(技能设计)

## Event Relationship Schema

### Cross-Chapter References (跨章互见)
- **共人**: 同一人物在不同章节/文献中出现
- **共地**: 同一地点在不同事件中出现
- **同期**: 同一时期发生的不同事件
- **因果**: 事件间的因果关系
- **对比**: 类似事件的对比分析

### Event Chains (事件链)
- **时间链**: 按时间顺序的事件序列
- **因果链**: 因果关系的事件序列
- **人物链**: 同一人物相关的事件序列
- **地域链**: 同一地区相关的事件序列

## Temporal System

### Era Conversion (年号转换)
- **黄巾起义**: 184年 (中平元年)
- **董卓之乱**: 189-192年 (初平-永汉)
- **群雄割据**: 192-208年 (初平-建安十三年)
- **三国鼎立**: 208-280年 (建安十三年-太康元年)

### Calendar Systems
- **公元纪年**: 标准时间系统
- **年号纪年**: 历史文献使用
- **干支纪年**: 传统历法系统
- **节气纪年**: 农事相关事件

## Spatial System

### Administrative Divisions
- **州**: 最高行政单位 (13州)
- **郡国**: 次级行政单位
- **县**: 基层行政单位
- **特殊区域**: 都城, 军事重镇

### Geographic Features
- **平原**: 中原地区
- **山地**: 秦岭, 巴山
- **水系**: 长江, 黄河, 淮水
- **关隘**: 战略要地

## Data Integration Rules

### Historical Priority (史料优先级)
1. **三国志**: 最高优先级, 陈寿原著
2. **三国志注**: 裴松之注, 补充说明
3. **后汉书**: 范晔著作, 补充史料
4. **资治通鉴**: 司马光编年, 综合史料

### Literary Integration (文学整合)
- **三国演义**: 标注"文学加工"
- **三国志平话**: 标注"民间传说"
- **戏曲小说**: 标注"艺术创作"

### Game Mechanics Integration (游戏机制整合)
- **三国杀标准版**: 基础卡牌数据
- **三国杀扩展包**: 扩展卡牌数据
- **三国杀OL**: 线上版本特色

## Annotation Standards

### Event Identification
- 历史事件以史书记载为准
- 文学事件标注出处章节
- 游戏事件标注卡牌/技能

### Relationship Validation
- 历史关系需史料支撑
- 文学关系标注"虚构"
- 游戏关系标注"游戏设定"

### Temporal Precision
- 精确到月日的优先标注
- 仅能确定年份的标注年份
- 时间有争议的标注"约"

### Spatial Precision
- 精确地点标注古今对照
- 大致区域标注范围
- 地点有争议的标注"疑似"

## Quality Control

### Consistency Rules
- 同一事件在不同文献中保持统一ID
- 时间统一转换为公元纪年
- 地点统一标注古今对照

### Completeness Standards
- 重大战役100%数据覆盖
- 重要政治事件90%数据覆盖
- 主要人物事件80%数据覆盖

### Accuracy Validation
- 历史数据交叉验证
- 文学数据标注来源
- 游戏数据标注版本
