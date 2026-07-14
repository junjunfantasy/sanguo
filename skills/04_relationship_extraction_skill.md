# Skill 4: Relationship Extraction for Three Kingdoms Knowledge Base

## Overview
This skill covers the extraction of relationships between entities in the Three Kingdoms knowledge base, including personal, political, military, and geographical relationships.

## Input
- Extracted entities from Skill 2
- Extracted events from Skill 3
- Relationship type specifications (9 categories)
- Historical relationship records

## Output
- Structured relationship records
- Relationship networks and graphs
- Relationship strength indicators
- Temporal relationship dynamics

## Relationship Categories

### 1. Blood Relationships (血缘关系)
- **父子**: Father-son relationships
- **母子**: Mother-son relationships
- **夫妻**: Husband-wife relationships
- **兄弟**: Brother relationships
- **姐妹**: Sister relationships
- **祖孙**: Grandparent-grandchild relationships
- **叔侄**: Uncle-nephew relationships
- **姻亲**: Marriage-based relationships

### 2. Political Relationships (政治关系)
- **君臣**: Ruler-subject relationships
- **同僚**: Colleague relationships
- **上下级**: Hierarchical relationships
- **政敌**: Political enemies
- **盟友**: Political allies

### 3. Military Relationships (军事关系)
- **统帅-部将**: Commander-subordinate relationships
- **同袍**: Comrade-in-arms relationships
- **敌对**: Military enemies
- **投降**: Surrender relationships
- **救援**: Rescue/support relationships

### 4. Personal Relationships (个人关系)
- **朋友**: Friendship relationships
- **师徒**: Teacher-student relationships
- **恩人**: Beneficiary relationships
- **仇敌**: Personal enemies
- **知己**: Close confidants

### 5. Geographical Relationships (地理关系)
- **隶属**: Administrative hierarchy
- **相邻**: Geographic adjacency
- **包含**: Spatial containment
- **距离**: Geographic distance
- **交通**: Transportation routes

### 6. Temporal Relationships (时间关系)
- **先后**: Chronological sequence
- **同期**: Contemporary existence
- **重叠**: Time period overlap
- **因果**: Causal relationships

### 7. Faction Relationships (势力关系)
- **从属**: Subordination relationships
- **联盟**: Alliance relationships
- **敌对**: Factional enmity
- **臣服**: Vassal relationships
- **竞争**: Competitive relationships

### 8. Literature Relationships (文献关系)
- **记载**: Documentation relationships
- **引用**: Citation relationships
- **补充**: Supplementary information
- **矛盾**: Contradictory accounts
- **评价**: Evaluative relationships

### 9. Game Relationships (游戏关系)
- **技能关联**: Skill-based relationships
- **卡牌配合**: Card synergy relationships
- **阵营归属**: Faction assignments
- **平衡关系**: Game balance considerations

## Extraction Methods

### 1. Direct Text Extraction
- Kinship terms (父, 母, 子, 女, 兄, 姐)
- Political terms (君, 臣, 主, 公)
- Military terms (将, 卒, 部, 军)
- Personal terms (友, 师, 徒, 恩)

### 2. Event-Based Inference
- Co-participation in events
- Command structures in battles
- Political alliances and conflicts
- Marriage alliances

### 3. Temporal Analysis
- Relationship duration
- Relationship changes over time
- End of relationships (death, betrayal)
- Relationship evolution

### 4. Cross-Reference Validation
- Multiple source confirmation
- Historical record verification
- Literary vs historical comparison
- Game mechanics alignment

## Relationship Attributes

### Core Attributes
- **Type**: Relationship category
- **Source**: First entity
- **Target**: Second entity
- **Nature**: Relationship quality (positive/negative/neutral)

### Temporal Attributes
- **Start date**: When relationship began
- **End date**: When relationship ended
- **Duration**: Length of relationship
- **Changes**: Evolution over time

### Strength Attributes
- **Intensity**: Relationship strength (1-10)
- **Frequency**: Interaction frequency
- **Impact**: Historical significance
- **Stability**: Relationship consistency

### Source Attributes
- **Historical basis**: Primary sources
- **Literary enhancement**: Novel additions
- **Game interpretation**: Game mechanics
- **Academic analysis**: Modern scholarship

## Relationship Dynamics

### Positive Relationships
- **Loyalty**: 君臣忠诚, 师徒情深
- **Friendship**: 桃园结义, 知己之情
- **Alliance**: 政治联盟, 军事合作
- **Family**: 血缘亲情, 婚姻联盟

### Negative Relationships
- **Enmity**: 政治敌对, 军事对抗
- **Betrayal**: 叛变投敌, 背信弃义
- **Competition**: 权力争夺, 利益冲突
- **Revenge**: 杀父之仇, 夺妻之恨

### Complex Relationships
- **Shifting alliances**: Political realignment
- **Love-hate dynamics**: Complex personal relationships
- **Utilitarian partnerships**: Strategic cooperation
- **Reluctant service**: Forced allegiance

## Quality Control

### Validation Rules
- Relationships must have source citations
- Temporal attributes must be consistent
- Geographic relationships must be spatially valid
- Family relationships must respect chronology

### Confidence Scoring
- **High (0.9+)**: Explicit historical records
- **Medium (0.7-0.9)**: Strong contextual evidence
- **Low (0.5-0.7)**: Inferred from events
- **Reject (<0.5)**: Speculative or contradictory

### Common Errors
- **Anachronisms**: Relationships before entities existed
- **Geographic impossibility**: Relationships across impossible distances
- **Conflicting sources**: Contradictory relationship records
- **Over-extraction**: False positive relationships

## Relationship Networks

### Network Types
- **Character networks**: Personal relationship graphs
- **Faction networks**: Political alliance structures
- **Geographic networks**: Spatial relationship maps
- **Event networks**: Causal relationship chains

### Network Metrics
- **Centrality**: Importance of entities
- **Betweenness**: Bridge relationships
- **Clustering**: Relationship groups
- **Density**: Network connectivity

### Visualization
- **Node-link diagrams**: Standard network visualization
- **Matrix views**: Relationship matrices
- **Temporal views**: Relationship evolution over time
- **Geographic views**: Spatial relationship mapping

## Output Format
```json
{
  "relationship_id": "unique identifier",
  "relationship_type": "blood/political/military/etc",
  "source_entity": "entity_id_1",
  "target_entity": "entity_id_2",
  "nature": "positive/negative/neutral",
  "start_date": "start date",
  "end_date": "end date",
  "strength": 8,
  "metadata": {
    "historical_basis": "primary source",
    "literary_references": [],
    "game_mechanics": "",
    "temporal_changes": [],
    "confidence": 0.9
  }
}
```

## Tools and Scripts
- Relationship extraction algorithms
- Network analysis libraries (NetworkX)
- Temporal relationship tracking
- Geographic relationship validation

## Integration Points
- Uses entities from Skill 2
- Uses events from Skill 3
- Supports knowledge graph construction
- Enables network analysis and visualization

## Next Steps
After relationship extraction:
- Build relationship networks
- Analyze network metrics
- Visualize relationship structures
- Enable relationship-based queries

## Notes
- Historical relationships take priority over literary interpretations
- Game relationships should be tagged separately
- Maintain temporal accuracy for relationship dynamics
- Document source conflicts and resolutions
