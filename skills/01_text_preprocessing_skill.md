# Skill 1: Text Preprocessing for Three Kingdoms Sources

## Overview
This skill covers the preprocessing of historical and literary sources for the Three Kingdoms knowledge base, including text cleaning, segmentation, and normalization.

## Input
- Raw text files from various sources:
  - Historical: 《三国志》, 《后汉书》, 《资治通鉴》
  - Literary: 《三国演义》, 《三国志平话》
  - Game: 三国杀 card descriptions and abilities

## Output
- Cleaned and segmented text ready for entity and event extraction
- Structured metadata (source, chapter, time period)
- Standardized text format

## Processing Steps

### 1. Text Cleaning
- Remove extra whitespace and formatting artifacts
- Normalize punctuation (，。！？；)
- Remove non-Chinese characters (except necessary symbols)
- Handle traditional/simplified character conversion if needed

### 2. Source Segmentation
- **Historical texts**: Segment by book (魏书/蜀书/吴书) and biographies
- **Literary texts**: Segment by chapters (三国演义 120回)
- **Game texts**: Segment by card type and character

### 3. Metadata Extraction
- Extract chapter numbers and titles
- Identify time periods and era names
- Tag source types (historical/literary/game)
- Record original text positions

### 4. Text Normalization
- Standardize character names (aliases → primary names)
- Normalize location names (ancient → modern mapping)
- Convert time references (era names → AD years)
- Standardize official titles

## Quality Control

### Consistency Rules
- Same entity across sources must use consistent naming
- Time references must be convertible to AD years
- Location names must include ancient-modern mapping

### Validation Criteria
- All text segments must have source metadata
- Chapter segmentation must be complete
- No text loss during cleaning
- Punctuation normalization > 95%

### Common Errors
- **Over-cleaning**: Removing meaningful characters
- **Segmentation errors**: Breaking mid-sentence
- **Metadata loss**: Missing source information
- **Encoding issues**: Character corruption

## Tools and Scripts
- `text_preprocessor.py`: Main preprocessing script
- Character encoding: UTF-8
- Regular expressions for pattern matching

## Output Format
```json
{
  "content": "cleaned text segment",
  "source": "sanguozhi/sanguoyanyi/sanguosha",
  "chapter": "chapter identifier",
  "segment_id": "unique segment identifier",
  "metadata": {
    "era": "era name",
    "time_period": "AD range",
    "type": "historical/literary/game"
  }
}
```

## Next Steps
After preprocessing, text segments are ready for:
- Skill 2: Entity Extraction
- Skill 3: Event Extraction
- Skill 4: Relationship Extraction

## Notes
- Historical sources have higher priority than literary sources
- Game data should be tagged separately for balance considerations
- Preserve original text positions for citation tracking
