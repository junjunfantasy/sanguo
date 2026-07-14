# Skill 5: Temporal Normalization for Three Kingdoms Knowledge Base

## Overview
This skill covers the conversion and normalization of temporal references in Three Kingdoms texts, including era names, lunar calendar dates, and relative time expressions to standard AD years.

## Input
- Preprocessed text segments with temporal references
- Era name patterns and conversion tables
- Historical calendar systems
- Relative time expressions

## Output
- Standardized AD year dates
- Era name to AD year mappings
- Temporal relationship data
- Date confidence scores

## Time Systems in Three Kingdoms Period

### 1. Era Name System (年号纪年)
- **Eastern Han**: 建宁, 熹平, 光和, 中平, 初平, 兴平, 建安
- **Cao Wei**: 黄初, 黄太, 青龙, 景初, 正始, 嘉平
- **Shu Han**: 章武, 建兴, 延熙, 景耀, 炎兴
- **Eastern Wu**: 黄武, 黄龙, 嘉禾, 赤乌, 太元, 神凤

### 2. Lunar Calendar System (农历)
- 12 lunar months per year
- Intercalary months (闰月) for calendar adjustment
- 24 solar terms (节气) for agricultural timing
- Sexagenary cycle (干支纪年) for year identification

### 3. AD Year System (公元纪年)
- Standard international calendar
- Used for modern historical analysis
- Reference point for all temporal calculations
- Range: 184 AD (Yellow Turban) to 280 AD (Fall of Wu)

## Conversion Tables

### Major Era Conversions
| Era Name | Period | AD Range | Ruler |
|----------|--------|----------|-------|
| 建安 | 196-220 | 196-220 | Eastern Han/Emperor Xian |
| 黄初 | 220-226 | 220-226 | Cao Pi (Wei) |
| 章武 | 221-223 | 221-223 | Liu Bei (Shu) |
| 建兴 | 223-237 | 223-237 | Liu Shan (Shu) |
| 黄武 | 222-229 | 222-229 | Sun Quan (Wu) |
| 嘉禾 | 232-238 | 232-238 | Sun Quan (Wu) |

### Key Event Dates
| Event | Era Date | AD Year |
|-------|----------|---------|
| Yellow Turban Rebellion | 中平元年 | 184 |
| Dong Zhuo's Rise | 初平元年 | 190 |
| Battle of Guandu | 建安五年 | 200 |
| Battle of Red Cliffs | 建安十三年 | 208 |
| Cao Pi's Usurpation | 黄初元年 | 220 |
| Liu Bei's Death | 章武三年 | 223 |
| Zhuge Liang's Death | 建兴十二年 | 234 |
| Fall of Shu | 炎兴元年 | 263 |
| Fall of Wu | 太康元年 | 280 |

## Extraction Patterns

### Era Name Patterns
- Complete: `建安十三年` (13th year of Jian'an)
- Incomplete: `建安中` (middle of Jian'an period)
- Abbreviated: `十三年` (13th year, context-dependent)

### Seasonal Patterns
- `春` (Spring): 1st-3rd lunar months
- `夏` (Summer): 4th-6th lunar months
- `秋` (Autumn): 7th-9th lunar months
- `冬` (Winter): 10th-12th lunar months

### Relative Time Patterns
- `明年` (Next year): Current year + 1
- `后年` (Year after next): Current year + 2
- `当年` (Same year): Current year
- `是年` (This year): Current year

### Age-Based Patterns
- `时年X` (Age X): Birth year calculation
- `年X` (Age X): Alternative age expression
- `少时` (Young age): Childhood/adolescence

## Conversion Algorithm

### 1. Era Name to AD Year
```python
def convert_era_to_ad(era_name, year_number):
    base_year = ERA_BASE_YEARS[era_name]
    return base_year + year_number - 1
```

### 2. Lunar to Solar Approximation
- Lunar months generally 1-2 months behind solar
- Use seasonal markers for rough solar conversion
- Document uncertainty in date precision

### 3. Relative Time Resolution
- Chain relative time references to absolute dates
- Use context to resolve ambiguous references
- Track temporal context through documents

### 4. Age-Based Date Calculation
- Extract birth year from death year and age
- Cross-reference with multiple sources
- Handle different age calculation methods

## Quality Control

### Validation Rules
- Era names must match historical records
- AD years must be within 184-280 range
- Relative dates must resolve to absolute dates
- Age calculations must be chronologically possible

### Precision Levels
- **Exact**: Day and month specified
- **Year**: Only year specified
- **Approximate**: "Early/Middle/Late" period
- **Estimated**: Inferred from context

### Confidence Scoring
- **High (0.9+)**: Direct era name with year number
- **Medium (0.7-0.9)**: Seasonal or relative reference
- **Low (0.5-0.7)**: Approximate period reference
- **Reject (<0.5)**: Contradictory or impossible dates

### Common Errors
- **Era confusion**: Wrong era base year
- **Calculation errors**: Off-by-one errors in year counting
- **Anachronisms**: Dates before entity existed
- **Context errors**: Wrong temporal context

## Temporal Relationships

### Sequential Relationships
- **Before**: Event A precedes Event B
- **After**: Event A follows Event B
- **Contemporary**: Events occur in same time period

### Duration Relationships
- **Instantaneous**: Single moment events
- **Short-term**: Days to weeks
- **Medium-term**: Months to years
- **Long-term**: Decades

### Causal Relationships
- **Immediate cause**: Direct causal link
- **Contributing cause**: Partial causal influence
- **Background condition**: Enabling circumstances

## Output Format
```json
{
  "temporal_id": "unique identifier",
  "original_text": "建安十三年冬",
  "era_name": "建安",
  "era_year": 13,
  "ad_year": 208,
  "season": "winter",
  "precision": "season",
  "confidence": 0.9,
  "metadata": {
    "conversion_method": "era_table",
    "context": "Battle of Red Cliffs",
    "source": "sanguozhi"
  }
}
```

## Tools and Scripts
- Era name conversion tables
- Lunar-solar calendar conversion algorithms
- Relative time resolution functions
- Temporal relationship extractors

## Integration Points
- Uses preprocessed text from Skill 1
- Supports event dating in Skill 3
- Enables temporal relationship extraction
- Facilitates chronology building

## Next Steps
After temporal normalization:
- Build chronological timelines
- Extract temporal relationships
- Create time-based visualizations
- Enable temporal queries

## Notes
- Historical accuracy takes priority over precision
- Document all assumptions and approximations
- Maintain source provenance for temporal data
- Cross-reference with multiple historical sources
