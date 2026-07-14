# Three Kingdoms Knowledge Base (三国知识库)

## 项目概述
三国知识库是一个基于shiji-kb方法论的三国时期古籍知识工程项目。项目结合《三国志》、《三国演义》等历史文学资料，并整合三国杀卡牌游戏机制，构建结构化的三国知识图谱。

## 核心目标
1. 将三国时期相关文献转化为结构化知识
2. 建立三国人物、事件、地点、关系的完整知识图谱
3. 整合三国杀卡牌游戏数据，实现历史与游戏的结合
4. 提供可复用的知识提取方法论，适用于其他历史时期

## 项目结构
```
sanguo/
├── README.md                    # 项目说明
├── ENTITY_TYPES_SPEC.md         # 实体类型规范
├── EVENT_TYPES_SPEC.md          # 事件类型规范
├── skills/                      # 方法论技能文档
│   ├── 01-text-preprocessing.md
│   ├── 02-entity-extraction.md
│   ├── 03-event-extraction.md
│   └── ...
├── kg/                          # 知识图谱数据
│   ├── entities/                # 实体数据
│   │   ├── characters/          # 人物实体
│   │   ├── locations/           # 地点实体
│   │   ├── factions/            # 势力实体
│   │   └── ...
│   ├── events/                  # 事件数据
│   │   ├── battles/             # 战役事件
│   │   ├── political/           # 政治事件
│   │   └── ...
│   ├── relations/               # 关系数据
│   │   ├── character_relations/  # 人物关系
│   │   ├── event_relations/     # 事件关系
│   │   └── ...
│   ├── chronology/              # 编年数据
│   ├── genealogy/               # 世系数据
│   └── ontology/                # 本体定义
├── data/                        # 原始数据
│   ├── historical/              # 历史文献
│   │   ├── sanguozhi/           # 三国志
│   │   ├── houshu/              # 后汉书
│   │   └── zizhitongjian/       # 资治通鉴
│   ├── literary/               # 文学作品
│   │   ├── sanguoyanyi/         # 三国演义
│   │   └── pinghua/             # 三国志平话
│   └── game/                    # 游戏数据
│       ├── sanguosha/           # 三国杀数据
│       └── cards/               # 卡牌数据
├── scripts/                     # 处理脚本
│   ├── text_processing/         # 文本处理
│   ├── entity_extraction/       # 实体提取
│   ├── event_extraction/        # 事件提取
│   └── data_validation/         # 数据验证
├── app/                         # 应用界面
│   ├── web/                     # Web界面
│   └── game/                    # 策略游戏
├── docs/                        # 文档
│   ├── methodology/             # 方法论文档
│   ├── api/                     # API文档
│   └── user_guide/              # 用户指南
└── tests/                       # 测试
    ├── data_tests/              # 数据测试
    └── api_tests/               # API测试
```

## 数据来源
1. **历史文献**: 《三国志》(陈寿)、《后汉书》(范晔)、《资治通鉴》(司马光)
2. **文学作品**: 《三国演义》(罗贯中)、《三国志平话》
3. **游戏数据**: 三国杀卡牌游戏(标准版、扩展包)

## 核心特性
- **20类实体**: 人物、势力、地点、官职、兵种、武器、战役、策略、典故等
- **12类事件**: 军事、政治、人事、外交、经济、文化等
- **9种关系**: 血缘、政治、军事、个人、地理、时间、势力、文献、游戏
- **时间系统**: 公元纪年、年号纪年、干支纪年转换
- **空间系统**: 州郡县行政区划、地理特征、战略要地

## 技术栈
- **后端**: Python, FastAPI, SQLite/PostgreSQL
- **前端**: React, TypeScript, D3.js
- **NLP**: spaCy, transformers, LLM
- **知识图谱**: Neo4j, NetworkX
- **可视化**: ECharts, D3.js

## 开发路线
### Phase 1: 基础设施 (当前)
- [x] 实体类型规范
- [x] 事件类型规范
- [ ] 项目目录结构
- [ ] 数据处理管线

### Phase 2: 数据提取
- [ ] 历史文献文本处理
- [ ] 实体自动提取
- [ ] 事件自动提取
- [ ] 关系构建

### Phase 3: 游戏整合
- [ ] 三国杀卡牌数据整合
- [ ] 技能与历史关联
- [ ] 游戏机制映射

### Phase 4: 应用开发
- [ ] 知识图谱可视化
- [ ] 查询接口开发
- [ ] 策略游戏开发

### Phase 5: 方法论沉淀
- [ ] 技能文档编写
- [ ] 流程标准化
- [ ] 质量控制体系

## 贡献指南
1. 遵循既定的实体和事件类型规范
2. 数据需标注来源(历史/文学/游戏)
3. 提交前需通过数据验证测试
4. 文档需包含使用示例

## 许可证
MIT License

## 联系方式
项目地址: https://github.com/yourusername/sanguo-kb

## 致谢
本项目参考了shiji-kb(史记知识库)的方法论，感谢原作者西瓜(鲍捷)的开源贡献。
