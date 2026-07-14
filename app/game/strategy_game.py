#!/usr/bin/env python3
"""
Three Kingdoms Strategy Game
A turn-based strategy game based on the knowledge graph
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class Faction(Enum):
    WEI = "魏"
    SHU = "蜀"
    WU = "吴"
    QUN = "群"


class ActionType(Enum):
    MILITARY = "military"
    DIPLOMATIC = "diplomatic"
    ECONOMIC = "economic"
    POLITICAL = "political"


@dataclass
class Character:
    """Game character based on knowledge graph data"""
    name: str
    faction: Faction
    strength: int
    intelligence: int
    political: int
    health: int = 100
    loyalty: int = 100
    abilities: List[str] = field(default_factory=list)
    
    def calculate_power(self) -> int:
        """Calculate overall power"""
        return (self.strength * 0.4 + self.intelligence * 0.3 + 
                self.political * 0.3) * (self.health / 100)


@dataclass
class Location:
    """Game location based on knowledge graph data"""
    name: str
    strategic_value: int
    owner: Optional[Faction] = None
    garrison: int = 0
    resources: Dict[str, int] = field(default_factory=dict)


@dataclass
class GameState:
    """Main game state"""
    turn: int = 1
    year: int = 184
    current_faction: Faction = Faction.SHU
    characters: Dict[str, Character] = field(default_factory=dict)
    locations: Dict[str, Location] = field(default_factory=dict)
    faction_resources: Dict[Faction, Dict[str, int]] = field(default_factory=dict)
    event_log: List[str] = field(default_factory=list)


class ThreeKingdomsStrategyGame:
    """Main game engine"""
    
    def __init__(self):
        self.state = GameState()
        self.initialize_game()
    
    def initialize_game(self):
        """Initialize game with historical data"""
        # Initialize characters from knowledge graph
        self.initialize_characters()
        
        # Initialize locations from knowledge graph
        self.initialize_locations()
        
        # Initialize faction resources
        self.initialize_resources()
        
        # Log start event
        self.log_event("游戏开始 - 黄巾起义时期")
    
    def initialize_characters(self):
        """Initialize characters with historical data"""
        character_data = [
            {"name": "刘备", "faction": Faction.SHU, "strength": 6, "intelligence": 8, "political": 9, "abilities": ["仁德", "激将"]},
            {"name": "曹操", "faction": Faction.WEI, "strength": 7, "intelligence": 9, "political": 10, "abilities": ["奸雄", "护驾"]},
            {"name": "孙权", "faction": Faction.WU, "strength": 6, "intelligence": 8, "political": 9, "abilities": ["制衡", "救援"]},
            {"name": "诸葛亮", "faction": Faction.SHU, "strength": 2, "intelligence": 10, "political": 9, "abilities": ["观星", "空城"]},
            {"name": "关羽", "faction": Faction.SHU, "strength": 10, "intelligence": 6, "political": 5, "abilities": ["武圣", "义绝"]},
            {"name": "周瑜", "faction": Faction.WU, "strength": 8, "intelligence": 9, "political": 7, "abilities": ["火攻", "反间"]},
            {"name": "司马懿", "faction": Faction.WEI, "strength": 6, "intelligence": 10, "political": 9, "abilities": ["隐忍", "狼顾"]},
            {"name": "吕布", "faction": Faction.QUN, "strength": 10, "intelligence": 3, "political": 2, "abilities": ["无双"]},
        ]
        
        for data in character_data:
            self.state.characters[data["name"]] = Character(
                name=data["name"],
                faction=data["faction"],
                strength=data["strength"],
                intelligence=data["intelligence"],
                political=data["political"],
                abilities=data["abilities"]
            )
    
    def initialize_locations(self):
        """Initialize strategic locations"""
        location_data = [
            {"name": "洛阳", "strategic_value": 10, "owner": Faction.WEI},
            {"name": "成都", "strategic_value": 8, "owner": Faction.SHU},
            {"name": "建业", "strategic_value": 8, "owner": Faction.WU},
            {"name": "荆州", "strategic_value": 9, "owner": None},
            {"name": "赤壁", "strategic_value": 7, "owner": None},
            {"name": "官渡", "strategic_value": 6, "owner": None},
        ]
        
        for data in location_data:
            self.state.locations[data["name"]] = Location(
                name=data["name"],
                strategic_value=data["strategic_value"],
                owner=data["owner"],
                resources={"gold": random.randint(1000, 5000), "food": random.randint(1000, 5000)}
            )
    
    def initialize_resources(self):
        """Initialize faction resources"""
        for faction in Faction:
            self.state.faction_resources[faction] = {
                "gold": 10000,
                "food": 10000,
                "population": 100000
            }
    
    def log_event(self, event: str):
        """Log game events"""
        self.state.event_log.append(f"Turn {self.state.turn}, Year {self.state.year}: {event}")
        print(f"[EVENT] {event}")
    
    def process_turn(self):
        """Process a single game turn"""
        current_faction = self.state.current_faction
        
        # AI decision making for non-player factions
        if current_faction != Faction.SHU:  # Assuming player controls Shu
            self.ai_faction_turn(current_faction)
        else:
            self.player_turn()
        
        # Advance turn
        self.advance_turn()
    
    def player_turn(self):
        """Process player turn"""
        print(f"\n=== Turn {self.state.turn} - Your Turn ({self.state.current_faction.value}) ===")
        print(f"Year: {self.state.year}")
        print(f"Resources: Gold={self.state.faction_resources[Faction.SHU]['gold']}, "
              f"Food={self.state.faction_resources[Faction.SHU]['food']}")
        
        # Display available actions
        self.display_available_actions()
        
        # Get player input (simplified for demo)
        action = input("Choose action (military/diplomatic/economic/political): ").lower()
        
        if action == "military":
            self.execute_military_action(Faction.SHU)
        elif action == "diplomatic":
            self.execute_diplomatic_action(Faction.SHU)
        elif action == "economic":
            self.execute_economic_action(Faction.SHU)
        elif action == "political":
            self.execute_political_action(Faction.SHU)
        else:
            print("Invalid action")
    
    def ai_faction_turn(self, faction: Faction):
        """Process AI faction turn"""
        print(f"\n=== Turn {self.state.turn} - {faction.value} AI Turn ===")
        
        # Simple AI logic
        action_choice = random.choice(["military", "diplomatic", "economic"])
        
        if action_choice == "military":
            self.execute_military_action(faction)
        elif action_choice == "diplomatic":
            self.execute_diplomatic_action(faction)
        else:
            self.execute_economic_action(faction)
    
    def execute_military_action(self, faction: Faction):
        """Execute military action"""
        print(f"{faction.value} executes military action")
        
        # Get faction characters
        faction_characters = [c for c in self.state.characters.values() if c.faction == faction]
        
        if not faction_characters:
            print("No available characters for military action")
            return
        
        # Select best military character
        best_character = max(faction_characters, key=lambda c: c.strength)
        
        # Select target location
        available_locations = [loc for loc in self.state.locations.values() 
                              if loc.owner != faction]
        
        if available_locations:
            target = random.choice(available_locations)
            success_chance = best_character.strength / 10.0
            
            if random.random() < success_chance:
                target.owner = faction
                target.garrison = random.randint(100, 500)
                self.log_event(f"{faction.value} {best_character.name} conquered {target.name}")
                self.state.faction_resources[faction]["gold"] += target.resources["gold"]
            else:
                self.log_event(f"{faction.value} {best_character.name} failed to conquer {target.name}")
    
    def execute_diplomatic_action(self, faction: Faction):
        """Execute diplomatic action"""
        print(f"{faction.value} executes diplomatic action")
        
        # Simple alliance logic
        other_factions = [f for f in Faction if f != faction]
        target_faction = random.choice(other_factions)
        
        # Check if alliance already exists (simplified)
        alliance_chance = 0.3
        
        if random.random() < alliance_chance:
            self.log_event(f"{faction.value} formed alliance with {target_faction.value}")
        else:
            self.log_event(f"{faction.value} diplomatic overture to {target_faction.value} failed")
    
    def execute_economic_action(self, faction: Faction):
        """Execute economic action"""
        print(f"{faction.value} executes economic action")
        
        # Resource generation
        gold_gain = random.randint(500, 1500)
        food_gain = random.randint(500, 1500)
        
        self.state.faction_resources[faction]["gold"] += gold_gain
        self.state.faction_resources[faction]["food"] += food_gain
        
        self.log_event(f"{faction.value} gained {gold_gain} gold and {food_gain} food")
    
    def execute_political_action(self, faction: Faction):
        """Execute political action"""
        print(f"{faction.value} executes political action")
        
        # Character recruitment or loyalty boost
        faction_characters = [c for c in self.state.characters.values() if c.faction == faction]
        
        if faction_characters:
            character = random.choice(faction_characters)
            character.loyalty = min(100, character.loyalty + 10)
            self.log_event(f"{faction.value} boosted {character.name}'s loyalty to {character.loyalty}")
    
    def display_available_actions(self):
        """Display available actions to player"""
        print("\nAvailable Actions:")
        print("1. Military - Attack or defend locations")
        print("2. Diplomatic - Form alliances or negotiate")
        print("3. Economic - Develop economy and gather resources")
        print("4. Political - Manage internal affairs and characters")
    
    def advance_turn(self):
        """Advance to next turn"""
        # Cycle through factions
        factions = list(Faction)
        current_index = factions.index(self.state.current_faction)
        self.state.current_faction = factions[(current_index + 1) % len(factions)]
        
        # Advance year every 4 turns (one full cycle)
        if self.state.current_faction == Faction.SHU:
            self.state.turn += 1
            if self.state.turn % 4 == 0:
                self.state.year += 1
        
        # Check win conditions
        self.check_win_conditions()
    
    def check_win_conditions(self):
        """Check if any faction has won"""
        faction_control = {}
        
        for location in self.state.locations.values():
            if location.owner:
                faction_control[location.owner] = faction_control.get(location.owner, 0) + 1
        
        # Check if any faction controls majority of locations
        total_locations = len(self.state.locations)
        for faction, count in faction_control.items():
            if count >= total_locations * 0.6:
                self.log_event(f"{faction.value} has achieved dominance! Victory!")
                return True
        
        # Check if year exceeds end date
        if self.state.year >= 280:
            self.log_event("Game ended - reached year 280")
            return True
        
        return False
    
    def display_game_state(self):
        """Display current game state"""
        print("\n=== Game State ===")
        print(f"Turn: {self.state.turn}")
        print(f"Year: {self.state.year}")
        print(f"Current Faction: {self.state.current_faction.value}")
        
        print("\n--- Faction Resources ---")
        for faction, resources in self.state.faction_resources.items():
            print(f"{faction.value}: Gold={resources['gold']}, Food={resources['food']}")
        
        print("\n--- Location Control ---")
        for location in self.state.locations.values():
            owner = location.owner.value if location.owner else "Neutral"
            print(f"{location.name}: {owner} (Value: {location.strategic_value})")
        
        print("\n--- Character Status ---")
        for character in self.state.characters.values():
            print(f"{character.name} ({character.faction.value}): "
                  f"STR={character.strength}, INT={character.intelligence}, "
                  f"POL={character.political}, HP={character.health}")
    
    def run_game(self, max_turns: int = 100):
        """Run the main game loop"""
        print("=== Three Kingdoms Strategy Game ===")
        print("Based on historical knowledge graph data")
        print("=====================================\n")
        
        while self.state.turn <= max_turns:
            self.display_game_state()
            
            # Check win conditions before processing turn
            if self.check_win_conditions():
                break
            
            # Process turn
            self.process_turn()
            
            # Small delay for readability
            input("\nPress Enter to continue...")
        
        print("\n=== Game Over ===")
        print("Final Game State:")
        self.display_game_state()


def main():
    """Main game execution"""
    game = ThreeKingdomsStrategyGame()
    game.run_game(max_turns=50)


if __name__ == "__main__":
    main()
