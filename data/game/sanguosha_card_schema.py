#!/usr/bin/env python3
"""
Three Kingdoms Kill (三国杀) Card Data Schema
Defines the data structure for integrating card game mechanics with historical data
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum


class CardType(Enum):
    """Card types in Three Kingdoms Kill"""
    BASIC = "basic"           # 基本牌
    TRICK = "trick"           # 锦囊牌
    EQUIPMENT = "equipment"   # 装备牌
    CHARACTER = "character"  # 武将牌


class CardSubType(Enum):
    """Card subtypes"""
    # Basic cards
    STRIKE = "strike"        # 杀
    DODGE = "dodge"          # 闪
    PEACH = "peach"          # 桃
    
    # Trick cards
    DISMANTLEMENT = "dismantlement"      # 过河拆桥
    STEALING = "stealing"                # 顺手牵羊
    BARBARIAN_INVASION = "barbarian_invasion"  # 南蛮入侵
    RAINING_ARROWS = "raining_arrows"    # 万箭齐发
    SOMA = "soma"                        # 无中生有
    ARCHERY_ATTACK = "archery_attack"    # 借刀杀人
    DUEL = "duel"                        # 决斗
    EXTINGUISH = "extinguish"            # 乐不思蜀
    LIGHTNING = "lightning"              # 闪电
    
    # Equipment cards
    WEAPON = "weapon"                    # 武器
    ARMOR = "armor"                      # 防具
    HORSE = "horse"                      # 坐骑
    DEFENSIVE_HORSE = "defensive_horse" # 防御马
    OFFENSIVE_HORSE = "offensive_horse" # 进攻马


class Faction(Enum):
    """Character factions in the game"""
    WEI = "wei"              # 魏
    SHU = "shu"              # 蜀
    WU = "wu"                # 吴
    QUN = "qun"              # 群


@dataclass
class Card:
    """Base card class"""
    card_id: str
    name: str
    card_type: CardType
    sub_type: CardSubType
    description: str
    effect: str
    historical_source: Optional[str] = None
    game_version: str = "standard"
    rarity: str = "common"
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CharacterCard(Card):
    """Character card with abilities and stats"""
    faction: Faction
    health: int
    abilities: List[str]
    skills: List[Dict]
    strength: int = 0      # 武力
    intelligence: int = 0  # 智力
    political: int = 0     # 政治
    historical_figure: Optional[str] = None  # Linked historical entity
    design_notes: str = ""


@dataclass
class EquipmentCard(Card):
    """Equipment card with stats"""
    attack_range: int = 1
    defense_bonus: int = 0
    special_effect: str = ""
    historical_weapon: Optional[str] = None  # Linked historical weapon


@dataclass
class Skill:
    """Character skill definition"""
    skill_id: str
    name: str
    type: str  # passive, active, triggered
    description: str
    condition: str
    effect: str
    historical_basis: Optional[str] = None
    game_mechanic: str = ""


class SanguoshaDataSchema:
    """Schema for Three Kingdoms Kill data integration"""
    
    @staticmethod
    def create_character_card(
        name: str,
        faction: Faction,
        health: int,
        abilities: List[str],
        skills: List[Dict],
        historical_figure: str = None
    ) -> CharacterCard:
        """Create a character card"""
        return CharacterCard(
            card_id=f"character_{name}",
            name=name,
            card_type=CardType.CHARACTER,
            sub_type=None,
            description=f"{faction.value.upper()} faction character",
            effect="Character abilities and skills",
            historical_source=historical_figure,
            faction=faction,
            health=health,
            abilities=abilities,
            skills=skills,
            historical_figure=historical_figure
        )
    
    @staticmethod
    def create_basic_card(
        name: str,
        sub_type: CardSubType,
        description: str,
        effect: str
    ) -> Card:
        """Create a basic card"""
        return Card(
            card_id=f"basic_{name}",
            name=name,
            card_type=CardType.BASIC,
            sub_type=sub_type,
            description=description,
            effect=effect
        )
    
    @staticmethod
    def create_trick_card(
        name: str,
        sub_type: CardSubType,
        description: str,
        effect: str,
        historical_source: str = None
    ) -> Card:
        """Create a trick card"""
        return Card(
            card_id=f"trick_{name}",
            name=name,
            card_type=CardType.TRICK,
            sub_type=sub_type,
            description=description,
            effect=effect,
            historical_source=historical_source
        )
    
    @staticmethod
    def create_equipment_card(
        name: str,
        sub_type: CardSubType,
        description: str,
        effect: str,
        attack_range: int = 1,
        defense_bonus: int = 0,
        historical_weapon: str = None
    ) -> EquipmentCard:
        """Create an equipment card"""
        return EquipmentCard(
            card_id=f"equipment_{name}",
            name=name,
            card_type=CardType.EQUIPMENT,
            sub_type=sub_type,
            description=description,
            effect=effect,
            attack_range=attack_range,
            defense_bonus=defense_bonus,
            historical_weapon=historical_weapon
        )
    
    @staticmethod
    def link_historical_entity(card: Card, entity_id: str, entity_data: Dict) -> Card:
        """Link a card to a historical entity"""
        card.metadata["historical_entity_id"] = entity_id
        card.metadata["historical_entity_data"] = entity_data
        return card


# Sample character cards based on historical figures
SAMPLE_CHARACTERS = [
    {
        "name": "刘备",
        "faction": Faction.SHU,
        "health": 4,
        "abilities": ["仁德", "激将"],
        "skills": [
            {
                "name": "仁德",
                "type": "active",
                "description": "可以将手牌赠予其他角色",
                "condition": "出牌阶段",
                "effect": "回复1点体力或摸2张牌"
            }
        ],
        "historical_figure": "刘备",
        "strength": 6,
        "intelligence": 8,
        "political": 9
    },
    {
        "name": "曹操",
        "faction": Faction.WEI,
        "health": 4,
        "abilities": ["奸雄", "护驾"],
        "skills": [
            {
                "name": "奸雄",
                "type": "triggered",
                "description": "受到伤害后可以获得造成伤害的牌",
                "condition": "受到伤害后",
                "effect": "获得伤害来源使用的牌"
            }
        ],
        "historical_figure": "曹操",
        "strength": 7,
        "intelligence": 9,
        "political": 10
    },
    {
        "name": "孙权",
        "faction": Faction.WU,
        "health": 4,
        "abilities": ["制衡", "救援"],
        "skills": [
            {
                "name": "制衡",
                "type": "active",
                "description": "可以弃置任意张牌，然后摸等量的牌",
                "condition": "出牌阶段",
                "effect": "弃置X张牌，摸X张牌"
            }
        ],
        "historical_figure": "孙权",
        "strength": 6,
        "intelligence": 8,
        "political": 9
    },
    {
        "name": "诸葛亮",
        "faction": Faction.SHU,
        "health": 3,
        "abilities": ["观星", "空城"],
        "skills": [
            {
                "name": "观星",
                "type": "active",
                "description": "可以查看牌堆顶的牌并调整顺序",
                "condition": "回合开始阶段",
                "effect": "查看牌堆顶5张牌并重新排列"
            },
            {
                "name": "空城",
                "type": "passive",
                "description": "手牌为0时不能成为杀的目标",
                "condition": "手牌为0",
                "effect": "免疫杀"
            }
        ],
        "historical_figure": "诸葛亮",
        "strength": 2,
        "intelligence": 10,
        "political": 9
    },
    {
        "name": "关羽",
        "faction": Faction.SHU,
        "health": 4,
        "abilities": ["武圣", "义绝"],
        "skills": [
            {
                "name": "武圣",
                "type": "active",
                "description": "可以将红色牌当作杀使用",
                "condition": "出牌阶段",
                "effect": "红色牌视为杀"
            }
        ],
        "historical_figure": "关羽",
        "strength": 10,
        "intelligence": 6,
        "political": 5
    },
    {
        "name": "吕布",
        "faction": Faction.QUN,
        "health": 5,
        "abilities": ["无双"],
        "skills": [
            {
                "name": "无双",
                "type": "passive",
                "description": "使用杀时需要两张闪才能抵消",
                "condition": "使用杀",
                "effect": "目标需要使用两张闪"
            }
        ],
        "historical_figure": "吕布",
        "strength": 10,
        "intelligence": 3,
        "political": 2
    }
]

# Sample equipment cards
SAMPLE_EQUIPMENT = [
    {
        "name": "青龙偃月刀",
        "sub_type": CardSubType.WEAPON,
        "description": "关羽的标志性武器",
        "effect": "使用杀被闪避后可以再使用一张杀",
        "attack_range": 3,
        "historical_weapon": "青龙偃月刀"
    },
    {
        "name": "丈八蛇矛",
        "sub_type": CardSubType.WEAPON,
        "description": "张飞的标志性武器",
        "effect": "可以将两张手牌当作杀使用",
        "attack_range": 3,
        "historical_weapon": "丈八蛇矛"
    },
    {
        "name": "八卦阵",
        "sub_type": CardSubType.ARMOR,
        "description": "诸葛亮发明的防御阵法",
        "effect": "可以判定是否闪避杀",
        "defense_bonus": 1
    },
    {
        "name": "赤兔马",
        "sub_type": CardSubType.OFFENSIVE_HORSE,
        "description": "吕布/关羽的坐骑",
        "effect": "攻击距离+1",
        "attack_range": 1,
        "historical_weapon": "赤兔马"
    }
]

# Sample trick cards with historical references
SAMPLE_TRICKS = [
    {
        "name": "无中生有",
        "sub_type": CardSubType.SOMA,
        "description": "凭空创造",
        "effect": "摸2张牌",
        "historical_source": "诸葛亮空城计"
    },
    {
        "name": "借刀杀人",
        "sub_type": CardSubType.ARCHERY_ATTACK,
        "description": "借用他人之力",
        "effect": "指定一名角色对另一名角色使用杀",
        "historical_source": "周瑜借刀杀曹操"
    },
    {
        "name": "苦肉计",
        "sub_type": CardSubType.DUEL,
        "description": "自残以取信",
        "effect": "失去1点体力，摸2张牌",
        "historical_source": "黄盖苦肉计"
    }
]


def main():
    """Generate sample card data"""
    schema = SanguoshaDataSchema()
    
    # Create character cards
    character_cards = []
    for char_data in SAMPLE_CHARACTERS:
        card = schema.create_character_card(
            name=char_data["name"],
            faction=char_data["faction"],
            health=char_data["health"],
            abilities=char_data["abilities"],
            skills=char_data["skills"],
            historical_figure=char_data["historical_figure"]
        )
        card.strength = char_data["strength"]
        card.intelligence = char_data["intelligence"]
        card.political = char_data["political"]
        character_cards.append(card)
    
    # Create equipment cards
    equipment_cards = []
    for equip_data in SAMPLE_EQUIPMENT:
        card = schema.create_equipment_card(
            name=equip_data["name"],
            sub_type=equip_data["sub_type"],
            description=equip_data["description"],
            effect=equip_data["effect"],
            attack_range=equip_data.get("attack_range", 1),
            defense_bonus=equip_data.get("defense_bonus", 0),
            historical_weapon=equip_data.get("historical_weapon")
        )
        equipment_cards.append(card)
    
    # Create trick cards
    trick_cards = []
    for trick_data in SAMPLE_TRICKS:
        card = schema.create_trick_card(
            name=trick_data["name"],
            sub_type=trick_data["sub_type"],
            description=trick_data["description"],
            effect=trick_data["effect"],
            historical_source=trick_data.get("historical_source")
        )
        trick_cards.append(card)
    
    print(f"Generated {len(character_cards)} character cards")
    print(f"Generated {len(equipment_cards)} equipment cards")
    print(f"Generated {len(trick_cards)} trick cards")
    
    return {
        "characters": [asdict(card) for card in character_cards],
        "equipment": [asdict(card) for card in equipment_cards],
        "tricks": [asdict(card) for card in trick_cards]
    }


if __name__ == "__main__":
    card_data = main()
    import json
    print(json.dumps(card_data, ensure_ascii=False, indent=2))
