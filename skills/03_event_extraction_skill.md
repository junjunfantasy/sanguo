# Skill 3: Event Extraction for Three Kingdoms Knowledge Base

## Overview
This skill covers the extraction of historical and literary events from Three Kingdoms texts, including battles, political changes, diplomatic activities, and cultural developments.

## Input
- Preprocessed text segments from Skill 1
- Extracted entities from Skill 2
- Event type specifications (12 categories)
- Temporal and spatial reference systems

## Output
- Structured event records with temporal and spatial data
- Event participants and outcomes
- Event chains and causal relationships
- Source citations and confidence scores

## Event Categories

### 1. Military Events
- **战役**: Large-scale battles with strategic importance
- **战斗**: Smaller military engagements
- **围城**: Siege operations
- **水战**: Naval battles
- **伏击**: Ambush operations

### 2. Political Events
- **政变**: Political coups and power shifts
- **禅让**: Abdication and succession
- **册封**: Official appointments and titles
- **废立**: Deposition and installation of rulers
- **朝议**: Court discussions and decisions

### 3. Personnel Events
- **任命**: Official appointments
- **免职**: Removal from office
- **投奔**: Defections and allegiance changes
- **叛变**: Betrayals and rebellions
- **被俘**: Captures and surrenders
- **死亡**: Deaths of important figures

### 4. Diplomatic Events
- **结盟**: Formation of alliances
- **毁盟**: Breaking of alliances
- **联姻**: Marriage alliances
- **质子**: Exchange of hostages
- **使节**: Diplomatic missions

### 5. Economic Events
- **屯田**: Military agricultural colonies
- **赋税**: Taxation policies
- **贸易**: Commercial activities
- **饥荒**: Famines and food shortages
- **迁民**: Population migrations

### 6. Cultural Events
- **著述**: Literary and scholarly works
- **教育**: Educational activities
- **艺术**: Artistic achievements
- **科技**: Technological inventions
- **宗教**: Religious activities

## Extraction Methods

### 1. Temporal Pattern Matching
- Era name patterns (建安, 黄初, 章武, etc.)
- AD year patterns (184年, 208年, etc.)
- Seasonal markers (春, 夏, 秋, 冬)
- Relative time expressions (其后, 明年, etc.)

### 2. Spatial Pattern Matching
- Location names (洛阳, 长安, 荆州, etc.)
- Directional markers (东, 西, 南, 北)
- Distance expressions (百里, 千里)
- Terrain descriptions (山, 水, 平原)

### 3. Action Pattern Matching
- Military actions (攻, 战, 伐, 征)
- Political actions (立, 废, 禅, 让)
- Personnel actions (拜, 免, 迁, 征)
- Diplomatic actions (盟, 聘, 质, 婚)

### 4. Contextual Analysis
- Participant identification
- Outcome extraction
- Causal relationship detection
- Strategic impact assessment

## Temporal Processing

### Era Name Conversion
- **建安** (196-220): Eastern Han, warlord era
- **黄初** (220-226): Cao Wei, Cao Pi
- **章武** (221-223): Shu Han, Liu Bei
- **建兴** (223-237): Shu Han, Liu Shan
- **嘉禾** (232-238): Eastern Wu, Sun Quan

### Date Standardization
- Convert era names to AD years
- Handle lunar calendar references
- Estimate uncertain dates
- Create date ranges for extended events

### Temporal Relationships
- **Sequential**: Event A before Event B
- **Contemporary**: Events happening simultaneously
- **Causal**: Event A causes Event B
- **Extended**: Events spanning multiple years

## Spatial Processing

### Location Identification
- Ancient place names
- Modern geographical equivalents
- Administrative divisions (州, 郡, 县)
- Strategic features (关隘, 山川, 水系)

### Geographic Relationships
- **Containment**: City within province
- **Adjacency**: Bordering regions
- **Distance**: Travel time and里程
- **Strategic value**: Military importance

### Spatial Validation
- Cross-reference with historical maps
- Verify geographical feasibility
- Check anachronisms
- Validate travel times

## Event Attribute Extraction

### Core Attributes
- **Name**: Event designation
- **Type**: Category classification
- **Date**: Temporal information
- **Location**: Spatial information
- **Participants**: Key figures and factions

### Extended Attributes
- **Causes**: Antecedent events or conditions
- **Process**: Event progression and stages
- **Outcome**: Results and consequences
- **Impact**: Historical significance

### Source Attributes
- **Historical sources**: Primary historical records
- **Literary sources**: Novel and dramatic versions
- **Game references**: Card game integration
- **Academic research**: Modern scholarship

## Quality Control

### Validation Criteria
- Events must have temporal references
- Locations must be geographically valid
- Participants must be historical figures
- Outcomes must be logically consistent

### Confidence Scoring
- **High (0.9+)**: Multiple source confirmation
- **Medium (0.7-0.9)**: Single reliable source
- **Low (0.5-0.7)**: Inferred from context
- **Reject (<0.5)**: Contradictory or unreliable

### Common Errors
- **Temporal confusion**: Wrong era conversion
- **Geographic errors**: Impossible locations
- **Participant errors**: Anachronistic figures
- **Causal errors**: False causality

## Event Relationship Extraction

### Cross-Chapter References
- **共人**: Same participants across different texts
- **共地**: Same location across different events
- **同期**: Contemporary events
- **因果**: Causal relationships

### Event Chains
- **Time chains**: Chronological sequences
- **Causal chains**: Cause-effect sequences
- **Character chains**: Events involving same figures
- **Geographic chains**: Events in same regions

## Output Format
```json
{
  "event_id": "unique identifier",
  "event_type": "military/political/diplomatic/etc",
  "name": "event name",
  "date": "era year",
  "date_ad": "AD year",
  "location": "location name",
  "participants": ["participant1", "participant2"],
  "description": "detailed description",
  "outcome": "event result",
  "source": "text source",
  "confidence": 0.9,
  "metadata": {
    "causes": ["cause_event_ids"],
    "effects": ["effect_event_ids"],
    "related_events": ["related_event_ids"],
    "historical_significance": "high/medium/low"
  }
}
```

## Tools and Scripts
- `event_extractor.py`: Main extraction script
- Temporal conversion libraries
- Geographic databases
- Historical event timelines

## Integration Points
- Uses entities from Skill 2
- Links to Skill 4 (relationship extraction)
- Supports chronology building
- Feeds into game scenario design

## Next Steps
After event extraction:
- Build chronological timelines
- Extract event relationships
- Validate against historical records
- Create event chains and narratives

## Notes
- Military events have highest historical priority
- Literary events should be clearly marked
- Game scenarios can be derived from historical events
- Maintain source provenance for historical accuracy
