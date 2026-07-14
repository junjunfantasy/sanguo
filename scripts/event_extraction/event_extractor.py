#!/usr/bin/env python3
"""
Three Kingdoms Event Extractor
Extracts events from processed text segments using NLP and rule-based methods
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class EventType(Enum):
    """Event types for Three Kingdoms knowledge base"""
    MILITARY = "military"
    POLITICAL = "political"
    PERSONNEL = "personnel"
    DIPLOMATIC = "diplomatic"
    ECONOMIC = "economic"
    CULTURAL = "cultural"
    NATURAL_DISASTER = "natural_disaster"
    SOCIAL = "social"
    ENGINEERING = "engineering"
    RELIGIOUS = "religious"
    LEGAL = "legal"
    INTELLIGENCE = "intelligence"


@dataclass
class Event:
    """Represents an extracted event"""
    event_id: str
    event_type: EventType
    name: str
    date: str
    date_ad: str
    location: str
    participants: List[str]
    description: str
    outcome: str
    source: str
    confidence: float
    metadata: Dict


class ThreeKingdomsEventExtractor:
    """Event extractor for Three Kingdoms texts"""
    
    def __init__(self, knowledge_base_path: Path):
        self.kb_path = knowledge_base_path
        self.event_patterns = self._load_event_patterns()
        self.extracted_events: Dict[str, Event] = {}
        
    def _load_event_patterns(self) -> Dict[EventType, List[Dict]]:
        """Load event patterns and rules"""
        return {
            EventType.MILITARY: [
                {"pattern": r'(.*?战)', "type": "battle"},
                {"pattern": r'(.*?攻.*?)(?:不克|克之|破之)', "type": "siege"},
                {"pattern": r'(.*?伏.*?)(?:大败|大胜)', "type": "ambush"},
                {"pattern": r'(火攻)(.*?)(?:大胜|大败)', "type": "fire_attack"},
            ],
            EventType.POLITICAL: [
                {"pattern": r'(.*?篡位)', "type": "usurpation"},
                {"pattern": r'(.*?禅让)', "type": "abdication"},
                {"pattern": r'(.*?自立)(?:为|称)(?:帝|王|公)', "type": "self_declaration"},
                {"pattern": r'(杀|害)(.*?)(?:及|并)', "type": "political_killing"},
            ],
            EventType.PERSONNEL: [
                {"pattern": r'(.*?)(?:投|降|奔)(.*?)(?:军|部)', "type": "defection"},
                {"pattern": r'(.*?)(?:拜|封|任命)(.*?)(?:为|作|任)(.*?)(?:将军|太守|刺史)', "type": "appointment"},
                {"pattern": r'(.*?)(?:被|遭)(?:擒|捕|获)', "type": "capture"},
                {"pattern": r'(.*?)(?:卒|死|被害|被杀)', "type": "death"},
            ],
            EventType.DIPLOMATIC: [
                {"pattern": r'(.*?)(?:结盟|联盟)(.*?)(?:共|合)(?:抗|讨)(.*?)', "type": "alliance"},
                {"pattern": r'(.*?)(?:遣|派)(.*?)(?:为|作)(?:使|使者)(?:于|往)(.*?)', "type": "diplomatic_mission"},
                {"pattern": r'(.*?)(?:嫁|娶)(.*?)(?:为|作)(?:妻|夫人)', "type": "marriage_alliance"},
            ],
            EventType.ECONOMIC: [
                {"pattern": r'(.*?屯田)(.*?)(?:于|在)(.*?)', "type": "farming_colony"},
                {"pattern": r'(.*?)(?:兴修|修筑)(.*?)(?:水利|堤坝|运河)', "type": "infrastructure"},
                {"pattern": r'(.*?)(?:大|饥)(?:旱|水|疫|蝗)', "type": "disaster_response"},
            ],
            EventType.CULTURAL: [
                {"pattern": r'(.*?)(?:著|撰|写)(.*?)(?:书|文|诗|赋)', "type": "literary_work"},
                {"pattern": r'(.*?)(?:创|造)(.*?)(?:器|械|物)', "type": "invention"},
            ],
            EventType.NATURAL_DISASTER: [
                {"pattern": r'(.*?)(?:大水|洪水|水灾)', "type": "flood"},
                {"pattern": r'(.*?)(?:大旱|旱灾|干旱)', "type": "drought"},
                {"pattern": r'(.*?)(?:大疫|瘟疫|疫病)', "type": "epidemic"},
                {"pattern": r'(.*?)(?:地震|地动)', "type": "earthquake"},
            ],
            EventType.SOCIAL: [
                {"pattern": r'(黄巾)(?:起义|作乱|反)', "type": "rebellion"},
                {"pattern": r'(.*?)(?:民变|暴动|起义)', "type": "uprising"},
            ],
            EventType.ENGINEERING: [
                {"pattern": r'(筑|建)(.*?)(?:城|台|宫|殿)', "type": "construction"},
                {"pattern": r'(修|筑)(.*?)(?:墙|垣|壁垒)', "type": "fortification"},
            ],
        }
    
    def extract_events_from_text(self, text: str, source: str, chapter: str) -> List[Event]:
        """Extract events from a text segment"""
        events = []
        
        for event_type, patterns in self.event_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                matches = re.finditer(pattern, text)
                
                for match in matches:
                    event = self._create_event(
                        match, event_type, source, chapter, pattern_info
                    )
                    events.append(event)
        
        return events
    
    def _create_event(self, match: re.Match, event_type: EventType, 
                      source: str, chapter: str, pattern_info: Dict) -> Event:
        """Create an event from extraction"""
        # Generate event ID
        event_id = f"{event_type.value}_{source}_{chapter}_{match.start()}"
        
        # Extract event name from match
        event_name = match.group(0)
        
        # Extract date from context
        date, date_ad = self._extract_date(match.string, match.start())
        
        # Extract location from context
        location = self._extract_location(match.string, match.start())
        
        # Extract participants
        participants = self._extract_participants(match.string, match.start())
        
        # Extract description
        description = self._extract_description(match.string, match.start(), match.end())
        
        # Extract outcome
        outcome = self._extract_outcome(match.string, match.end())
        
        return Event(
            event_id=event_id,
            event_type=event_type,
            name=event_name,
            date=date,
            date_ad=date_ad,
            location=location,
            participants=participants,
            description=description,
            outcome=outcome,
            source=source,
            confidence=0.8,
            metadata={
                "chapter": chapter,
                "pattern_type": pattern_info["type"],
                "text_position": match.start()
            }
        )
    
    def _extract_date(self, text: str, position: int) -> Tuple[str, str]:
        """Extract date from text context"""
        # Look for era names (建安, 黄初, etc.)
        era_pattern = r'([建安黄初章武建兴嘉禾太和][0-9]+年)'
        era_match = re.search(era_pattern, text[max(0, position-50):position+50])
        
        if era_match:
            era_date = era_match.group(1)
            ad_date = self._convert_era_to_ad(era_date)
            return era_date, ad_date
        
        # Look for AD years
        ad_pattern = r'([0-9]{3})年'
        ad_match = re.search(ad_pattern, text[max(0, position-50):position+50])
        
        if ad_match:
            ad_date = ad_match.group(1)
            return ad_date, ad_date
        
        return "unknown", "unknown"
    
    def _convert_era_to_ad(self, era_date: str) -> str:
        """Convert era name to AD year"""
        era_conversions = {
            "建安": 196,  # 建安元年 = 196 AD
            "黄初": 220,  # 黄初元年 = 220 AD
            "章武": 221,  # 章武元年 = 221 AD
            "建兴": 223,  # 建兴元年 = 223 AD
            "嘉禾": 232,  # 嘉禾元年 = 232 AD
            "太和": 227,  # 太和元年 = 227 AD
        }
        
        for era, base_year in era_conversions.items():
            if era in era_date:
                year_match = re.search(r'([0-9]+)年', era_date)
                if year_match:
                    year_num = int(year_match.group(1))
                    return str(base_year + year_num - 1)
        
        return "unknown"
    
    def _extract_location(self, text: str, position: int) -> str:
        """Extract location from text context"""
        # Look for location indicators (于, 在, 至)
        location_pattern = r'(?:于|在|至)([一-龥]{2,4})(?:战|攻|军|屯)'
        location_match = re.search(location_pattern, text[position:position+30])
        
        if location_match:
            return location_match.group(1)
        
        # Look for major locations
        major_locations = ["洛阳", "长安", "许都", "成都", "建业", "荆州", "赤壁", "官渡"]
        for location in major_locations:
            if location in text[position-20:position+20]:
                return location
        
        return "unknown"
    
    def _extract_participants(self, text: str, position: int) -> List[str]:
        """Extract participants from text context"""
        participants = []
        
        # Look for character names near the event
        context = text[max(0, position-100):position+100]
        
        # Major characters to look for
        major_characters = [
            "刘备", "曹操", "孙权", "诸葛亮", "关羽", "张飞", "赵云", "马超", "黄忠",
            "周瑜", "鲁肃", "吕蒙", "陆逊", "孙策", "孙坚",
            "司马懿", "荀彧", "郭嘉", "程昱", "贾诩"
        ]
        
        for character in major_characters:
            if character in context:
                participants.append(character)
        
        return participants
    
    def _extract_description(self, text: str, start: int, end: int) -> str:
        """Extract event description"""
        # Get a broader context around the event
        context_start = max(0, start - 30)
        context_end = min(len(text), end + 50)
        return text[context_start:context_end].strip()
    
    def _extract_outcome(self, text: str, position: int) -> str:
        """Extract event outcome"""
        # Look for outcome indicators
        outcome_pattern = r'(?:大胜|大败|克之|破之|不克|退走|投降|被擒)'
        outcome_match = re.search(outcome_pattern, text[position:position+30])
        
        if outcome_match:
            return outcome_match.group(0)
        
        return "unknown"
    
    def merge_events(self, events: List[Event]) -> Dict[str, Event]:
        """Merge duplicate or related events"""
        event_dict = {}
        
        for event in events:
            key = (event.event_type, event.name, event.location)
            if key in event_dict:
                # Merge with existing event
                existing = event_dict[key]
                if event.confidence > existing.confidence:
                    event_dict[key] = event
                # Merge participants
                for participant in event.participants:
                    if participant not in existing.participants:
                        existing.participants.append(participant)
            else:
                event_dict[key] = event
        
        return event_dict
    
    def extract_event_relations(self, events: Dict[str, Event]) -> List[Dict]:
        """Extract relationships between events"""
        relations = []
        
        events_list = list(events.values())
        
        for i, event1 in enumerate(events_list):
            for event2 in events_list[i+1:]:
                # Check for temporal relationships
                if self._is_temporal_related(event1, event2):
                    relations.append({
                        "type": "temporal",
                        "source": event1.event_id,
                        "target": event2.event_id,
                        "relation": self._get_temporal_relation(event1, event2)
                    })
                
                # Check for causal relationships
                if self._is_causal_related(event1, event2):
                    relations.append({
                        "type": "causal",
                        "source": event1.event_id,
                        "target": event2.event_id,
                        "relation": "causes"
                    })
                
                # Check for spatial relationships
                if self._is_spatial_related(event1, event2):
                    relations.append({
                        "type": "spatial",
                        "source": event1.event_id,
                        "target": event2.event_id,
                        "relation": "same_location"
                    })
        
        return relations
    
    def _is_temporal_related(self, event1: Event, event2: Event) -> bool:
        """Check if events are temporally related"""
        if event1.date_ad == "unknown" or event2.date_ad == "unknown":
            return False
        return abs(int(event1.date_ad) - int(event2.date_ad)) <= 5
    
    def _get_temporal_relation(self, event1: Event, event2: Event) -> str:
        """Get temporal relation type"""
        if event1.date_ad == "unknown" or event2.date_ad == "unknown":
            return "unknown"
        if int(event1.date_ad) < int(event2.date_ad):
            return "before"
        elif int(event1.date_ad) > int(event2.date_ad):
            return "after"
        else:
            return "contemporary"
    
    def _is_causal_related(self, event1: Event, event2: Event) -> bool:
        """Check if events are causally related."""
        # Simple heuristic: if events involve same participants and are close in time
        if not set(event1.participants) & set(event2.participants):
            return False
        if self._is_temporal_related(event1, event2):
            return True
        return False
    
    def _is_spatial_related(self, event1: Event, event2: Event) -> bool:
        """Check if events are spatially related"""
        return event1.location == event2.location and event1.location != "unknown"
    
    def save_events(self, events: Dict[str, Event], output_path: Path):
        """Save extracted events to JSON"""
        output_data = []
        for event in events.values():
            event_dict = asdict(event)
            event_dict["event_type"] = event.event_type.value
            output_data.append(event_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    def save_event_relations(self, relations: List[Dict], output_path: Path):
        """Save event relations to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(relations, f, ensure_ascii=False, indent=2)
    
    def load_processed_segments(self, segments_path: Path) -> List[Dict]:
        """Load processed text segments"""
        with open(segments_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def main():
    """Main execution function"""
    kb_path = Path("/Users/macbook/AI/sanguo/kg")
    segments_path = kb_path / "processed_segments.json"
    
    extractor = ThreeKingdomsEventExtractor(kb_path)
    
    # Load processed segments
    segments = extractor.load_processed_segments(segments_path)
    
    # Extract events from all segments
    all_events = []
    for segment in segments:
        text = segment["content"]
        source = segment["source"]
        chapter = segment["chapter"]
        events = extractor.extract_events_from_text(text, source, chapter)
        all_events.extend(events)
    
    # Merge duplicate events
    merged_events = extractor.merge_events(all_events)
    
    # Extract event relations
    event_relations = extractor.extract_event_relations(merged_events)
    
    # Save events
    events_output = kb_path / "events" / "extracted_events.json"
    extractor.save_events(merged_events, events_output)
    
    # Save event relations
    relations_output = kb_path / "relations" / "event_relations.json"
    extractor.save_event_relations(event_relations, relations_output)
    
    print(f"Extracted {len(merged_events)} unique events")
    print(f"Extracted {len(event_relations)} event relations")
    print(f"Events saved to {events_output}")
    print(f"Relations saved to {relations_output}")


if __name__ == "__main__":
    main()
