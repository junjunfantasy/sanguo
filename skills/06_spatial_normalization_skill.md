# Skill 6: Spatial Normalization for Three Kingdoms Knowledge Base

## Overview
This skill covers the normalization and mapping of geographical references in Three Kingdoms texts, including ancient place names, administrative divisions, and modern geographical equivalents.

## Input
- Preprocessed text segments with geographical references
- Historical place name dictionaries
- Administrative division records
- Modern geographical databases

## Output
- Standardized location entities
- Ancient-to-modern place name mappings
- Administrative hierarchy data
- Geographic coordinates and relationships

## Geographic Systems in Three Kingdoms Period

### 1. Administrative Divisions
- **州**: Highest level (13 major provinces)
  - 豫州, 兖州, 徐州, 青州, 凉州, 并州, 冀州
  - 幽州, 扬州, 荆州, 益州, 交州, 雍州
- **郡国**: Second level (commanderies and kingdoms)
- **县**: Basic administrative unit

### 2. Strategic Geographic Features
- **关隘**: Mountain passes and strategic points
  - 函谷关, 潼关, 武关, 散关
  - 剑阁, 阳平关, 潼关
- **水系**: Rivers and lakes
  - 长江, 黄河, 淮水, 汉水
  - 洞庭湖, 鄱阳湖
- **山脉**: Mountain ranges
  - 秦岭, 巴山, 岷山, 太行山

### 3. Major Cities and Capitals
- **洛阳**: Eastern Han capital
- **长安**: Former Han capital, strategic importance
- **许都**: Cao Cao's capital
- **成都**: Shu Han capital
- **建业**: Eastern Wu capital
- **邺城**: Cao Wei base

## Place Name Categories

### 1. Administrative Centers
- **Capitals**: Political centers of major factions
- **Commandery seats**: Regional administrative centers
- **County seats**: Local administrative centers

### 2. Military Locations
- **Battlefields**: Major battle sites
- **Fortresses**: Defensive structures
- **Garrisons**: Military bases
- **Strategic points**: Passes, crossings, bridges

### 3. Economic Centers
- **Commercial cities**: Trade centers
- **Agricultural regions**: Farming areas
- **Resource locations**: Mines, forests, fisheries

### 4. Cultural/Religious Sites
- **Temples**: Religious structures
- **Academies**: Educational institutions
- **Tombs**: Burial sites

## Ancient-Modern Mapping

### Major City Mappings
| Ancient Name | Modern Name | Province | Coordinates |
|--------------|-------------|----------|-------------|
| 洛阳 | Luoyang | Henan | 34.62°N, 112.45°E |
| 长安 | Xi'an | Shaanxi | 34.34°N, 108.93°E |
| 许今 | Xuchang | Henan | 34.04°N, 113.85°E |
| 成都 | Chengdu | Sichuan | 30.67°N, 104.06°E |
| 建业 | Nanjing | Jiangsu | 32.06°N, 118.78°E |
| 荆州 | Jingzhou | Hubei | 30.33°N, 112.19°E |

### Strategic Location Mappings
| Ancient Name | Modern Name | Strategic Importance |
|--------------|-------------|---------------------|
| 赤壁 | Chibi | Hubei, Yangtze River |
| 官渡 | Guandu | Henan, Yellow River |
| 夷陵 | Yiling | Hubei, Yangtze Gorges |
| 五丈原 | Wuzhangyuan | Shaanxi, Wei River |
| 街亭 | Jieting | Gansu, strategic pass |

## Extraction Patterns

### Place Name Patterns
- **Complete names**: 荆州, 洛阳, 赤壁
- **Directional modifiers**: 东吴, 西蜀, 北魏
- **Compound names**: 江东, 关中, 河北地区
- **Fortress names**: 虎牢关, 阳平关

### Geographic Relationship Patterns
- **Administrative**: 荆州刺史, 洛阳太守
- **Directional**: 江东六郡, 关中平原
- **Distance**: 百里, 千里, 五里
- **Terrain**: 山川, 河流, 平原

### Movement Patterns
- **Direction**: 东进, 南下, 西征
- **Crossing**: 渡江, 越关, 过河
- **Route**: 经, 过, 至, 达

## Normalization Algorithm

### 1. Place Name Standardization
```python
def normalize_place_name(ancient_name):
    # Check direct mapping
    if ancient_name in ANCIENT_MODERN_MAP:
        return ANCIENT_MODERN_MAP[ancient_name]
    
    # Check partial matches
    for ancient, modern in ANCIENT_MODERN_MAP.items():
        if ancient_name in ancient or ancient in ancient_name:
            return modern
    
    # Return original if no match found
    return ancient_name
```

### 2. Administrative Hierarchy Resolution
- Determine administrative level (州/郡/县)
- Identify parent administrative units
- Establish hierarchical relationships

### 3. Geographic Coordinate Assignment
- Use historical maps for approximate locations
- Cross-reference with modern geographic databases
- Document coordinate uncertainty

### 4. Strategic Value Assessment
- Military importance
- Economic value
- Political significance
- Transportation utility

## Quality Control

### Validation Rules
- Ancient names must have historical documentation
- Modern mappings must be geographically plausible
- Administrative hierarchies must be historically accurate
- Strategic assessments must be contextually appropriate

### Precision Levels
- **Exact**: Precise modern location identified
- **Approximate**: General region identified
- **Historical**: Location no longer exists
- **Disputed**: Location historically contested

### Confidence Scoring
- **High (0.9+)**: Well-documented major cities
- **Medium (0.7-0.9)**: Known historical locations
- **Low (0.5-0.7)**: Minor or uncertain locations
- **Reject (<0.5)**: Unidentified or impossible locations

### Common Errors
- **Anachronistic names**: Using modern names for ancient locations
- **Geographic impossibility**: Locations in wrong regions
- **Administrative errors**: Wrong hierarchy levels
- **Confusion with similar names**: Different places with similar names

## Geographic Relationships

### Spatial Relationships
- **Containment**: Location within administrative unit
- **Adjacency**: Bordering locations
- **Distance**: Travel time and里程
- **Route**: Transportation corridors

### Strategic Relationships
- **Control**: Political/military control
- **Influence**: Sphere of influence
- **Access**: Strategic access points
- **Defense**: Defensive relationships

## Output Format
```json
{
  "location_id": "unique identifier",
  "ancient_name": "洛阳",
  "modern_name": "Luoyang",
  "administrative_level": "capital",
  "parent_admin": "Henan Province",
  "coordinates": {
    "latitude": 34.62,
    "longitude": 112.45,
    "precision": "city_center"
  },
  "strategic_value": {
    "military": "high",
    "political": "high",
    "economic": "medium"
  },
  "metadata": {
    "historical_period": "Eastern Han",
    "modern_province": "Henan",
    "confidence": 0.95
  }
}
```

## Tools and Scripts
- Ancient-modern place name dictionaries
- Geographic coordinate databases
- Administrative hierarchy records
- Historical map references

## Integration Points
- Uses preprocessed text from Skill 1
- Supports entity extraction in Skill 2
- Enables event geolocation in Skill 3
- Facilitates spatial relationship extraction

## Next Steps
After spatial normalization:
- Build geographic databases
- Create spatial relationship networks
- Enable geographic visualizations
- Support location-based queries

## Notes
- Historical accuracy takes priority over precise coordinates
- Document uncertainty in location identifications
- Maintain source provenance for geographic data
- Cross-reference with multiple historical sources
