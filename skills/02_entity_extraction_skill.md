# Skill 2: Entity Extraction for Three Kingdoms Knowledge Base

## Overview
This skill covers the extraction of entities from preprocessed Three Kingdoms texts, including characters, locations, factions, weapons, and other domain-specific entities.

## Input
- Preprocessed text segments from Skill 1
- Entity type specifications (20 categories)
- Historical entity dictionaries and gazetteers

## Output
- Structured entity records with attributes
- Entity aliases and mappings
- Source citations for each entity
- Confidence scores for extraction

## Entity Categories

### 1. Core Entities (High Priority)
- **人物**: Names, style names, aliases, titles
- **势力**: Faction names, rulers, time periods
- **地点**: Cities, regions, battlefields, strategic points
- **官职**: Official titles, ranks, responsibilities

### 2. Military Entities
- **兵种**: Unit types, characteristics, famous users
- **武器**: Legendary weapons, owners, descriptions
- **战役**: Battle names, participants, outcomes

### 3. Cultural Entities
- **典故**: Idioms, stories, cultural references
- **文献**: Book titles, authors, periods
- **技能**: Character abilities, historical basis

### 4. Game-Specific Entities
- **卡牌**: Card names, types, effects
- **机制**: Game rules, skill interactions

## Extraction Methods

### 1. Pattern-Based Extraction
- Regular expressions for known entities
- Name pattern matching (surname + given name)
- Title and official position patterns
- Location and place name patterns

### 2. Dictionary-Based Extraction
- Historical character dictionaries
- Geographical gazetteers
- Official title lists
- Weapon and equipment catalogs

### 3. Context-Based Extraction
- Co-occurrence with known entities
- Syntactic role analysis
- Semantic context understanding
- Cross-reference validation

### 4. NLP-Assisted Extraction
- Named entity recognition (NER)
- Part-of-speech tagging
- Dependency parsing
- Coreference resolution

## Attribute Extraction

### Character Attributes
- Basic: Name, style name (字), aliases, birth/death dates
- Political: Faction, official titles, territories
- Military: Commands, battles, achievements
- Personal: Relationships, reputation, historical evaluation
- Game: Stats (武力/智力/政治), skills, card abilities

### Location Attributes
- Names: Ancient name, modern name, aliases
- Geography: Coordinates, terrain type, strategic value
- Political: Administrative level, controlling faction
- Historical: Related events, historical significance

### Event Attributes
- Temporal: Date, era name, AD year, duration
- Spatial: Location, geographical scope
- Participants: Key figures, factions, armies
- Outcome: Results, casualties, political impact

## Quality Control

### Validation Rules
- Historical entities must have source citations
- Character names must include style names when available
- Locations must have ancient-modern mapping
- Time references must be convertible to AD years

### Confidence Scoring
- **High (0.9+)**: Direct matches with historical records
- **Medium (0.7-0.9)**: Pattern matches with context support
- **Low (0.5-0.7)**: Inferred from context, needs verification
- **Reject (<0.5)**: Insufficient evidence

### Common Errors
- **False positives**: Common words mistaken for names
- **Entity merging**: Different entities with same name
- **Attribute errors**: Wrong attributes assigned
- **Source confusion**: Literary vs historical sources mixed

## Disambiguation Strategies

### Name Disambiguation
- Use temporal context (different time periods)
- Use geographical context (different regions)
- Use faction affiliation (different political groups)
- Use relationship networks (family, colleagues)

### Source Disambiguation
- Tag historical vs literary sources
- Note fictional characters from literature
- Mark game-only entities separately
- Cross-reference with historical records

## Output Format
```json
{
  "entity_id": "unique identifier",
  "entity_type": "character/location/faction/etc",
  "name": "primary name",
  "aliases": ["alias1", "alias2"],
  "attributes": {
    "style_name": "字",
    "birth_year": "AD year",
    "faction": "political affiliation"
  },
  "source": "text source",
  "confidence": 0.9,
  "metadata": {
    "extraction_method": "pattern/dictionary/nlp",
    "historical_validated": true,
    "literary_references": []
  }
}
```

## Tools and Scripts
- `entity_extractor.py`: Main extraction script
- Historical dictionaries and gazetteers
- NLP models for Chinese NER
- Pattern libraries for entity matching

## Integration Points
- Links to Skill 1 (text preprocessing)
- Feeds into Skill 3 (event extraction)
- Connects to Skill 4 (relationship extraction)
- Supports game data integration

## Next Steps
After entity extraction:
- Validate entities against historical records
- Merge duplicate entities across sources
- Extract entity relationships
- Link to game card data

## Notes
- Historical accuracy takes priority over literary sources
- Game entities should be tagged for balance considerations
- Maintain source provenance for all entities
- Regular updates as new sources are added
