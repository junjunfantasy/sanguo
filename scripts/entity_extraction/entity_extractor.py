#!/usr/bin/env python3
"""
Three Kingdoms Entity Extractor
Extracts entities from processed text segments using NLP and rule-based methods
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class EntityType(Enum):
    """Entity types for Three Kingdoms knowledge base"""
    CHARACTER = "character"
    FACTION = "faction"
    LOCATION = "location"
    OFFICE = "office"
    WEAPON = "weapon"
    BATTLE = "battle"
    STRATEGY = "strategy"
    ITEM = "item"
    YEAR_ERA = "year_era"
    ORGANIZATION = "organization"


@dataclass
class Entity:
    """Represents an extracted entity"""
    entity_id: str
    entity_type: EntityType
    name: str
    aliases: List[str]
    attributes: Dict
    source: str
    confidence: float
    metadata: Dict


class ThreeKingdomsEntityExtractor:
    """Entity extractor for Three Kingdoms texts"""
    
    def __init__(self, knowledge_base_path: Path):
        self.kb_path = knowledge_base_path
        self.entity_patterns = self._load_entity_patterns()
        self.extracted_entities: Dict[str, Entity] = {}
        
    def _load_entity_patterns(self) -> Dict[EntityType, List[Dict]]:
        """Load entity patterns and rules"""
        return {
            EntityType.CHARACTER: [
                {"pattern": r'([刘曹孙关张诸葛赵马黄周吕陆])', "type": "surname"},
                {"pattern": r'(刘备|曹操|孙权|诸葛亮|关羽|张飞|赵云|马超|黄忠)', "type": "major_character"},
                {"pattern': r'([一-龥]{2,4})(?:字|表字)([一-龥]{1,2})', "type": "character_with_style_name"},
            ],
            EntityType.LOCATION: [
                {"pattern": r'(洛阳|长安|许都|成都|建业|荆州|益州|扬州)', "type": "major_city"},
                {"pattern": r'(赤壁|官渡|夷陵|五丈原|街亭)', "type": "battlefield"},
                {"pattern": r'(虎牢关|阳平关|剑阁|濡须口)', "type": "strategic_pass"},
            ],
            EntityType.FACTION: [
                {"pattern": r'(蜀汉|曹魏|东吴|蜀|魏|吴)', "type": "major_faction"},
                {"pattern": r'(袁绍|董卓|吕布)(?:军|部|集团)', "type": "warlord_faction"},
            ],
            EntityType.OFFICE: [
                {"pattern": r'(丞相|大将军|太尉|司徒|司空)', "type": "high_official"},
                {"pattern": r'(太守|刺史|牧|督)', "type": "regional_official"},
            ],
            EntityType.WEAPON: [
                {"pattern": r'(青龙偃月刀|方天画戟|丈八蛇矛|倚天剑|青釭剑)', "type": "legendary_weapon"},
            ],
            EntityType.YEAR_ERA: [
                {"pattern": r'(建安|黄初|章武|建兴|嘉禾)(?:元年|二年|三年|四年|五年|[0-9]+年)', "type": "era_name"},
                {"pattern": r'([0-9]{3})年', "type": "ad_year"},
            ],
        }
    
    def extract_entities_from_text(self, text: str, source: str) -> List[Entity]:
        """Extract entities from a text segment"""
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                matches = re.finditer(pattern, text)
                
                for match in matches:
                    entity_name = match.group(1) if match.groups() else match.group(0)
                    entity = self._create_entity(
                        entity_name, entity_type, source, pattern_info
                    )
                    entities.append(entity)
        
        return entities
    
    def _create_entity(self, name: str, entity_type: EntityType, 
                       source: str, pattern_info: Dict) -> Entity:
        """Create an entity from extraction"""
        # Generate entity ID
        entity_id = f"{entity_type.value}_{name}_{source}"
        
        # Extract aliases if present in text
        aliases = self._extract_aliases(name)
        
        # Set confidence based on pattern type
        confidence = 0.9 if pattern_info["type"] == "major_character" else 0.7
        
        return Entity(
            entity_id=entity_id,
            entity_type=entity_type,
            name=name,
            aliases=aliases,
            attributes={},
            source=source,
            confidence=confidence,
            metadata={"extraction_pattern": pattern_info["type"]}
        )
    
    def _extract_aliases(self, name: str) -> List[str]:
        """Extract aliases for an entity"""
        aliases = []
        # Common alias patterns
        if name == "刘备":
            aliases = ["玄德", "刘皇叔"]
        elif name == "曹操":
            aliases = ["孟德", "曹孟德", "曹公"]
        elif name == "孙权":
            aliases = ["仲谋", "孙仲谋", "吴侯"]
        elif name == "诸葛亮":
            aliases = ["孔明", "诸葛孔明", "武侯"]
        elif name == "关羽":
            aliases = ["云长", "关云长", "关公", "武圣"]
        elif name == "张飞":
            aliases = ["翼德", "张翼德"]
        return aliases
    
    def merge_entities(self, entities: List[Entity]) -> Dict[str, Entity]:
        """Merge duplicate entities"""
        entity_dict = {}
        
        for entity in entities:
            key = (entity.entity_type, entity.name)
            if key in entity_dict:
                # Merge with existing entity
                existing = entity_dict[key]
                if entity.confidence > existing.confidence:
                    entity_dict[key] = entity
                # Merge sources
                if source not in existing.metadata.get("sources", []):
                    existing.metadata.setdefault("sources", []).append(entity.source)
            else:
                entity.metadata["sources"] = [entity.source]
                entity_dict[key] = entity
        
        return entity_dict
    
    def extract_attributes(self, entity: Entity, text: str) -> Dict:
        """Extract additional attributes for an entity"""
        attributes = {}
        
        if entity.entity_type == EntityType.CHARACTER:
            attributes = self._extract_character_attributes(entity, text)
        elif entity.entity_type == EntityType.BATTLE:
            attributes = self._extract_battle_attributes(entity, text)
        elif entity.entity_type == EntityType.LOCATION:
            attributes = self._extract_location_attributes(entity, text)
            
        return attributes
    
    def _extract_character_attributes(self, entity: Entity, text: str) -> Dict:
        """Extract character-specific attributes"""
        attributes = {}
        
        # Extract style name (字)
        style_pattern = rf'{entity.name}([，,])?(?:字|表字)([一-龥]+)'
        style_match = re.search(style_pattern, text)
        if style_match:
            attributes["style_name"] = style_match.group(2)
        
        # Extract birth/death info
        birth_pattern = rf'{entity.name}.*?生.*?([0-9]+)'
        birth_match = re.search(birth_pattern, text)
        if birth_match:
            attributes["birth_year"] = birth_match.group(1)
        
        # Extract faction affiliation
        faction_pattern = rf'{entity.name}.*?(蜀|魏|吴|汉)'
        faction_match = re.search(faction_pattern, text)
        if faction_match:
            attributes["faction"] = faction_match.group(1)
        
        return attributes
    
    def _extract_battle_attributes(self, entity: Entity, text: str) -> Dict:
        """Extract battle-specific attributes"""
        attributes = {}
        
        # Extract date
        date_pattern = rf'{entity.name}.*?([建安黄初章武]+[0-9]+年)'
        date_match = re.search(date_pattern, text)
        if date_match:
            attributes["date"] = date_match.group(1)
        
        # Extract location
        location_pattern = rf'{entity.name}.*?(于|在)([一-龥]{2,4})'
        location_match = re.search(location_pattern, text)
        if location_match:
            attributes["location"] = location_match.group(2)
        
        return attributes
    
    def _extract_location_attributes(self, entity: Entity, text: str) -> Dict:
        """Extract location-specific attributes"""
        attributes = {}
        
        # Extract modern location
        modern_pattern = rf'{entity.name}.*?今([一-龥]{2,4})'
        modern_match = re.search(modern_pattern, text)
        if modern_match:
            attributes["modern_name"] = modern_match.group(1)
        
        return attributes
    
    def save_entities(self, entities: Dict[str, Entity], output_path: Path):
        """Save extracted entities to JSON"""
        output_data = []
        for entity in entities.values():
            entity_dict = asdict(entity)
            entity_dict["entity_type"] = entity.entity_type.value
            output_data.append(entity_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    def load_processed_segments(self, segments_path: Path) -> List[Dict]:
        """Load processed text segments"""
        with open(segments_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def main():
    """Main execution function"""
    kb_path = Path("/Users/macbook/AI/sanguo/kg")
    segments_path = kb_path / "processed_segments.json"
    
    extractor = ThreeKingdomsEntityExtractor(kb_path)
    
    # Load processed segments
    segments = extractor.load_processed_segments(segments_path)
    
    # Extract entities from all segments
    all_entities = []
    for segment in segments:
        text = segment["content"]
        source = segment["source"]
        entities = extractor.extract_entities_from_text(text, source)
        all_entities.extend(entities)
    
    # Merge duplicate entities
    merged_entities = extractor.merge_entities(all_entities)
    
    # Extract additional attributes
    for entity in merged_entities.values():
        # Find original text for attribute extraction
        for segment in segments:
            if entity.name in segment["content"]:
                attributes = extractor.extract_attributes(entity, segment["content"])
                entity.attributes.update(attributes)
                break
    
    # Save entities
    output_path = kb_path / "entities" / "extracted_entities.json"
    extractor.save_entities(merged_entities, output_path)
    
    print(f"Extracted {len(merged_entities)} unique entities")
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    main()
