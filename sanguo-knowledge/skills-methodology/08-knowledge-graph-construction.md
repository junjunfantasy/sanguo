---
type: methodology
title: 知识图谱构建
phase: 8
tags: [知识图谱, 图数据库, Schema设计, Neo4j, 查询优化]
---

# 知识图谱构建

## 概述

知识图谱构建是将前序流程提取的实体、事件、关系数据组织为图结构，存储于图数据库中的最终整合环节。本流程定义图数据库Schema设计、实体-关系模型、存储策略和查询优化方案。目标是构建一个可查询、可推理、可扩展的三国领域知识图谱，支撑历史分析、游戏数据映射、智能问答等上层应用。

## 输入

- 验证通过的实体数据（20类实体，约5000+实体实例）
- 验证通过的事件数据（12类事件，约2000+事件实例）
- 验证通过的关系数据（9类关系，约10000+关系三元组）
- 时间/空间归一化映射结果

## 处理流程

### 1. 图数据模型设计

采用属性图模型（Property Graph Model），节点和关系均可携带属性。

#### 节点标签（Labels）

| 标签 | 实体类型 | 核心属性 | 预期规模 |
|------|---------|---------|---------|
| Person | 人物 | id, name, alias, birthYear, deathYear, styleName, posthumousTitle | ~3000 |
| Location | 地点/城池/关隘 | id, name, ancientName, modernName, lat, lng, level(州/郡/县/关) | ~1500 |
| Faction | 势力 | id, name, founder, capital, startYear, endYear | ~50 |
| Battle | 战役 | id, name, year, location, victor, loser, significance | ~200 |
| Event | 一般事件 | id, type(12类), trigger, time, description | ~2000 |
| Document | 典籍/文章 | id, title, author, year, type(书/表/令/诏) | ~100 |
| Title | 官职/爵位 | id, name, rank, category(中央/地方/军) | ~300 |
| Artifact | 武器/宝物 | id, name, type, owner, description | ~100 |

#### 关系类型（Relationship Types）

| 关系 | 源节点→目标节点 | 属性 |
|------|---------------|------|
| BORN_IN | Person→Location | confidence |
| DIED_IN | Person→Location | confidence |
| SERVED_UNDER | Person→Faction | title, startYear, endYear |
| HELD_TITLE | Person→Title | startYear, endYear |
| PARTICIPATED_IN | Person→Battle | role(commander/soldier/strategist) |
| PART_OF | Location→Location | type(capital_of/belongs_to) |
| ALLIED_WITH | Faction→Faction | startYear, endYear |
| HOSTILE_TO | Faction→Faction | startYear, endYear |
| AUTHORED | Person→Document | year |
| MARRIED_TO | Person→Person | startYear, endYear |
| FATHER_OF | Person→Person | type(biological/adopted) |
| MENTOR_OF | Person→Person | type(teacher/recommender) |
| SUCCEEDED | Person→Person | title, year |
| DEFEATED_BY | Person→Person | battle, year |

### 2. 图数据库选型与存储

- **数据库选型**：Neo4j Community Edition（主选，Cypher查询成熟）+ ArangoDB（备选，支持多模型）
- **索引策略**：
  - Person.name、Location.name、Faction.name建立唯一索引（BTREE）
  - 全文索引：Person.name支持模糊搜索
  - 复合索引：(name, birthYear) 加速按名+时间段筛选
- **数据导入**：使用Neo4j Batch Importer批量导入初始数据
- **增量更新**：通过Cypher CREATE/MERGE语句逐条添加

### 3. 查询优化

- **常见查询模式优化**：
  - "曹操的相关关系"→MATCH (p:Person {name:'曹操'})-[r]-(n) RETURN r,n
  - "赤壁之战的参与者"→MATCH (b:Battle {name:'赤壁之战'})-[r:PARTICIPATED_IN]-(p) RETURN p,r
  - "三国人物世系"→MATCH (p:Person)-[:FATHER_OF*]->(descendant) RETURN descendant
- **Cypher优化技巧**：
  - 使用PROFILE分析查询执行计划
  - 关系查询中指定方向（→而非-）减少扫描范围
  - 使用标签提前过滤（WHERE p:Person AND p.birthYear>150）
- **缓存策略**：热点查询结果（高频人物/战役）使用Redis二级缓存

### 4. 知识推理与补全

- **规则推理**：基于SWRL规则的推理引擎（如"X是Y的父亲，Y是Z的父亲→X是Z的祖父"）
- **推理规则集**：15条确定性推理规则（传递性、对称性、逆关系推断）
- **缺失补全**：基于TransE等知识图谱嵌入模型预测缺失关系

## 输出

- Neo4j数据库dump文件（完整数据快照）
- Schema定义文档（节点标签、关系类型、属性约束）
- 查询模板库（50+个常用Cypher查询模板）
- 数据统计报告（节点数、关系数、各类分布）
- Neo4j Browser可视化配置（样式、颜色定义）

## 常见问题

1. **数据稀疏性**：大量人物只有少数关系→使用默认值填充+置信度标记
2. **关系方向**：FATHER_OF方向从父到子，但查询时需双向→创建索引时同时创建反向关系
3. **版本迭代**：知识库不断扩充→使用Neo4j标签版本标记（v1.0, v2.0）
4. **性能瓶颈**：全图遍历查询（如世系链）时间长→限制深度6层+添加LIMIT

## 参考

- Neo4j官方文档: Graph Data Modeling Guidelines
- Wang et al. "A Survey on Knowledge Graph Construction" (2021)
- 《三国志》世系表整合方案（万斯同《历代史表》）
