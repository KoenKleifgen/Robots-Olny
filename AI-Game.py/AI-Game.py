import random
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import json
from enum import Enum
import os

# ANSI color codes for text coloring
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def dramatic_print(text: str, delay: float = 0.03):
    """Print text dramatically with a slight delay between characters"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

class CharacterClass(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    PALADIN = "Paladin"  # New class!

class ItemType(Enum):
    WEAPON = "weapon"
    POTION = "potion"
    ARTIFACT = "artifact"
    SCROLL = "scroll"  # New item type!

@dataclass
class Ability:
    name: str
    description: str
    damage_multiplier: float
    cooldown: int
    current_cooldown: int = 0

@dataclass
class Stats:
    strength: int
    agility: int
    magic: int
    health: int
    max_health: int
    mana: int = 100
    max_mana: int = 100
    critical_chance: float = 0.1

@dataclass
class Item:
    name: str
    item_type: ItemType
    description: str
    power: int
    uses: Optional[int] = None
    special_effect: Optional[str] = None

@dataclass
class Enemy:
    name: str
    health: int
    max_health: int
    damage: int
    description: str
    special_ability: Optional[str] = None
    special_ability_chance: float = 0.2
    loot: List[Item] = None

    def __post_init__(self):
        if self.loot is None:
            self.loot = []

class Player:
    def __init__(self, name: str, character_class: CharacterClass):
        self.name = name
        self.character_class = character_class
        self.inventory: List[Item] = []
        self.stats = self._initialize_stats()
        self.story_choices: Dict[str, str] = {}
        self.abilities = self._initialize_abilities()
        self.level = 1
        self.experience = 0
        self.gold = 50
        
    def _initialize_stats(self) -> Stats:
        base_health = 100
        if self.character_class == CharacterClass.WARRIOR:
            return Stats(strength=8, agility=5, magic=2, health=base_health + 30, max_health=base_health + 30)
        elif self.character_class == CharacterClass.MAGE:
            return Stats(strength=3, agility=4, magic=8, health=base_health, max_health=base_health, mana=150, max_mana=150)
        elif self.character_class == CharacterClass.PALADIN:
            return Stats(strength=7, agility=3, magic=5, health=base_health + 40, max_health=base_health + 40)
        else:  # Rogue
            return Stats(strength=5, agility=8, magic=2, health=base_health + 10, max_health=base_health + 10, critical_chance=0.2)

    def _initialize_abilities(self) -> List[Ability]:
        abilities = []
        if self.character_class == CharacterClass.WARRIOR:
            abilities = [
                Ability("Whirlwind", "Spin attack hitting all enemies", 1.5, 3),
                Ability("Battle Cry", "Boost damage for next attack", 2.0, 4)
            ]
        elif self.character_class == CharacterClass.MAGE:
            abilities = [
                Ability("Fireball", "Powerful fire magic", 2.0, 2),
                Ability("Ice Storm", "Freezing area attack", 1.8, 3)
            ]
        elif self.character_class == CharacterClass.ROGUE:
            abilities = [
                Ability("Backstab", "Critical strike from shadows", 2.5, 3),
                Ability("Smoke Bomb", "Escape from battle", 0, 5)
            ]
        elif self.character_class == CharacterClass.PALADIN:
            abilities = [
                Ability("Holy Strike", "Divine damage + healing", 1.7, 3),
                Ability("Divine Shield", "Temporary invulnerability", 0, 6)
            ]
        return abilities
    
    def add_item(self, item: Item) -> bool:
     
        if len(self.inventory) < 10:  # Assuming max inventory size of 10
            self.inventory.append(item)
            return True
        return False

    # Add the missing show_inventory method
    def show_inventory(self):
        """Display the player's inventory"""
        if not self.inventory:
            print(f"{Colors.YELLOW}Your inventory is empty.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BLUE}=== Inventory ==={Colors.ENDC}")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name} - {item.description}")
            if item.uses is not None:
                print(f"   Uses remaining: {item.uses}")

    # Add the missing use_item method
    def use_item(self, item_index: int) -> bool:
        """
        Use an item from the inventory.
        Returns True if the item was successfully used.
        """
        if item_index < 0 or item_index >= len(self.inventory):
            return False
            
        item = self.inventory[item_index]
        
        if item.item_type == ItemType.POTION:
            self.stats.health = min(self.stats.health + item.power, self.stats.max_health)
            print(f"{Colors.GREEN}You recover {item.power} health!{Colors.ENDC}")
            
            if item.uses is not None:
                item.uses -= 1
                if item.uses <= 0:
                    self.inventory.pop(item_index)
            else:
                self.inventory.pop(item_index)
            return True
            
        elif item.item_type == ItemType.SCROLL:
            # Implement scroll effects here
            print(f"{Colors.YELLOW}You use {item.name}!{Colors.ENDC}")
            if item.special_effect:
                print(f"Effect: {item.special_effect}")
            
            self.inventory.pop(item_index)
            return True
            
        return False

    def gain_experience(self, amount: int):
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.stats.max_health += 20
        self.stats.health = self.stats.max_health
        dramatic_print(f"\n{Colors.YELLOW}*** LEVEL UP! ***{Colors.ENDC}")
        dramatic_print(f"You are now level {self.level}!")
        self._improve_stats()

    def _improve_stats(self):
        if self.character_class == CharacterClass.WARRIOR:
            self.stats.strength += 3
        elif self.character_class == CharacterClass.MAGE:
            self.stats.magic += 3
            self.stats.max_mana += 20
        elif self.character_class == CharacterClass.ROGUE:
            self.stats.agility += 3
            self.stats.critical_chance += 0.05

    def show_status(self):
        print(f"\n{Colors.BLUE}=== {self.name} the {self.character_class.value} ===")
        print(f"Level: {self.level} | XP: {self.experience}/100")
        print(f"Health: {self.stats.health}/{self.stats.max_health}")
        print(f"Mana: {self.stats.mana}/{self.stats.max_mana}")
        print(f"Gold: {self.gold}{Colors.ENDC}")

    def gain_experience(self, amount: int):
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.stats.max_health += 20
        self.stats.health = self.stats.max_health
        dramatic_print(f"\n{Colors.YELLOW}*** LEVEL UP! ***{Colors.ENDC}")
        dramatic_print(f"You are now level {self.level}!")
        self._improve_stats()

    def _improve_stats(self):
        if self.character_class == CharacterClass.WARRIOR:
            self.stats.strength += 3
        elif self.character_class == CharacterClass.MAGE:
            self.stats.magic += 3
            self.stats.max_mana += 20
        elif self.character_class == CharacterClass.ROGUE:
            self.stats.agility += 3
            self.stats.critical_chance += 0.05

    def show_status(self):
        print(f"\n{Colors.BLUE}=== {self.name} the {self.character_class.value} ===")
        print(f"Level: {self.level} | XP: {self.experience}/100")
        print(f"Health: {self.stats.health}/{self.stats.max_health}")
        print(f"Mana: {self.stats.mana}/{self.stats.max_mana}")
        print(f"Gold: {self.gold}{Colors.ENDC}")

class Game:
    def __init__(self):
        self.player: Optional[Player] = None
        self.current_location = "start"
        self.game_state = "running"
        self.current_quest = None
        
    def initialize_game(self):
        clear_screen()
        dramatic_print(f"{Colors.YELLOW}Welcome to the Epic Quest of Destiny!{Colors.ENDC}")
        time.sleep(1)
        
        name = input(f"\n{Colors.GREEN}Enter your character's name: {Colors.ENDC}")
        
        print(f"\n{Colors.BLUE}Choose your class:{Colors.ENDC}")
        for char_class in CharacterClass:
            print(f"- {char_class.value}")
            if char_class == CharacterClass.WARRIOR:
                print("  Master of weapons and combat")
            elif char_class == CharacterClass.MAGE:
                print("  Wielder of powerful magic")
            elif char_class == CharacterClass.ROGUE:
                print("  Expert in stealth and critical strikes")
            elif char_class == CharacterClass.PALADIN:
                print("  Holy warrior with healing powers")
            print()
            
        while True:
            class_choice = input(f"{Colors.GREEN}Enter your choice: {Colors.ENDC}").upper()
            try:
                character_class = CharacterClass[class_choice]
                break
            except KeyError:
                print(f"{Colors.RED}Invalid class choice. Please try again.{Colors.ENDC}")
        
        self.player = Player(name, character_class)
        self._give_starting_items()
        
    def _give_starting_items(self):
        starting_items = {
            CharacterClass.WARRIOR: [
                Item("Steel Greatsword", ItemType.WEAPON, "A mighty two-handed sword", 8),
                Item("Chain Mail", ItemType.ARTIFACT, "Standard protective armor", 5)
            ],
            CharacterClass.MAGE: [
                Item("Enchanted Staff", ItemType.WEAPON, "A staff crackling with energy", 6),
                Item("Mana Crystal", ItemType.ARTIFACT, "Restores mana over time", 5)
            ],
            CharacterClass.ROGUE: [
                Item("Shadow Daggers", ItemType.WEAPON, "Twin daggers for swift strikes", 7),
                Item("Smoke Bombs", ItemType.ARTIFACT, "Provides quick escape", 5, uses=3)
            ],
            CharacterClass.PALADIN: [
                Item("Holy Mace", ItemType.WEAPON, "A mace blessed with divine power", 7),
                Item("Holy Symbol", ItemType.ARTIFACT, "Enhances healing abilities", 5)
            ]
        }
        
        for item in starting_items[self.player.character_class]:
            self.player.add_item(item)
        self.player.add_item(Item("Health Potion", ItemType.POTION, "Restores 30 HP", 30, 2))

    def handle_combat(self, enemy: Enemy) -> bool:
        dramatic_print(f"\n{Colors.RED}A {enemy.name} appears! {enemy.description}{Colors.ENDC}")
        time.sleep(1)
        
        while enemy.health > 0 and self.player.stats.health > 0:
            clear_screen()
            self.player.show_status()
            print(f"\n{Colors.RED}Enemy: {enemy.name}")
            print(f"Health: {enemy.health}/{enemy.max_health}{Colors.ENDC}")
            
            print("\nActions:")
            print("1. Attack")
            print("2. Defend")
            print("3. Use Item")
            print("4. Use Ability")
            
            action = input(f"\n{Colors.GREEN}Choose your action (1-4): {Colors.ENDC}")
            
            if action == "1":  # Attack
                damage = self._calculate_damage()
                if random.random() < self.player.stats.critical_chance:
                    damage *= 2
                    dramatic_print(f"{Colors.YELLOW}CRITICAL HIT!{Colors.ENDC}")
                enemy.health -= damage
                dramatic_print(f"You deal {Colors.GREEN}{damage}{Colors.ENDC} damage!")
                
            elif action == "2":  # Defend
                dramatic_print(f"{Colors.BLUE}You take a defensive stance!{Colors.ENDC}")
                damage_reduction = 0.5
                
            elif action == "3":  # Use Item
                self.player.show_inventory()
                try:
                    item_choice = int(input(f"{Colors.GREEN}Choose item number (0 to cancel): {Colors.ENDC}")) - 1
                    if item_choice >= -1:
                        self.player.use_item(item_choice)
                except ValueError:
                    print(f"{Colors.RED}Invalid input!{Colors.ENDC}")
                    continue
                    
            elif action == "4":  # Use Ability
                if not self.player.abilities:
                    dramatic_print(f"{Colors.RED}No abilities available!{Colors.ENDC}")
                    continue
                    
                print("\nAbilities:")
                for i, ability in enumerate(self.player.abilities, 1):
                    if ability.current_cooldown == 0:
                        print(f"{i}. {ability.name} - {ability.description}")
                    else:
                        print(f"{i}. {ability.name} - Cooldown: {ability.current_cooldown} turns")
                
                try:
                    ability_choice = int(input(f"{Colors.GREEN}Choose ability (0 to cancel): {Colors.ENDC}")) - 1
                    if 0 <= ability_choice < len(self.player.abilities):
                        ability = self.player.abilities[ability_choice]
                        if ability.current_cooldown == 0:
                            damage = self._calculate_damage() * ability.damage_multiplier
                            enemy.health -= damage
                            ability.current_cooldown = ability.cooldown
                            dramatic_print(f"\n{Colors.YELLOW}You use {ability.name}!")
                            dramatic_print(f"It deals {Colors.GREEN}{damage}{Colors.ENDC} damage!")
                        else:
                            print(f"{Colors.RED}That ability is on cooldown!{Colors.ENDC}")
                except ValueError:
                    print(f"{Colors.RED}Invalid input!{Colors.ENDC}")
                    continue
            
            else:
                print(f"{Colors.RED}Invalid action!{Colors.ENDC}")
                continue
            
            # Update ability cooldowns
            for ability in self.player.abilities:
                if ability.current_cooldown > 0:
                    ability.current_cooldown -= 1
            
            # Enemy turn
            if enemy.health > 0:
                if random.random() < enemy.special_ability_chance and enemy.special_ability:
                    damage = enemy.damage * 1.5
                    dramatic_print(f"\n{Colors.RED}{enemy.name} uses {enemy.special_ability}!{Colors.ENDC}")
                else:
                    damage = max(0, enemy.damage - random.randint(0, 2))
                    
                if action == "2":  # If player defended
                    damage = int(damage * 0.5)
                self.player.stats.health -= damage
                dramatic_print(f"{enemy.name} attacks you for {Colors.RED}{damage}{Colors.ENDC} damage!")
                
            time.sleep(1)
            
        if enemy.health <= 0:
            dramatic_print(f"\n{Colors.GREEN}Victory! You've defeated the {enemy.name}!{Colors.ENDC}")
            self._handle_victory_rewards(enemy)
            return True
        return False

    def _handle_victory_rewards(self, enemy: Enemy):
        exp_gain = random.randint(20, 40)
        gold_gain = random.randint(10, 30)
        
        self.player.gain_experience(exp_gain)
        self.player.gold += gold_gain
        
        dramatic_print(f"\n{Colors.YELLOW}You gained:")
        dramatic_print(f"+ {exp_gain} experience")
        dramatic_print(f"+ {gold_gain} gold{Colors.ENDC}")
        
        if enemy.loot:
            item = random.choice(enemy.loot)
            if self.player.add_item(item):
                dramatic_print(f"\n{Colors.GREEN}You found: {item.name}!{Colors.ENDC}")

    # [Previous code remains the same until the _calculate_damage method]

    def _calculate_damage(self) -> int:
        base_damage = 5
        if self.player.character_class == CharacterClass.WARRIOR:
            base_damage += self.player.stats.strength * 1.5
        elif self.player.character_class == CharacterClass.MAGE:
            base_damage += self.player.stats.magic * 1.5
        elif self.player.character_class == CharacterClass.PALADIN:
            base_damage += (self.player.stats.strength + self.player.stats.magic) * 0.8
        else:  # Rogue
            base_damage += self.player.stats.agility * 1.3
            
        return int(base_damage + random.randint(-2, 4))

    def _calculate_damage(self) -> int:  # Continuing from previous code
        base_damage = 5
        if self.player.character_class == CharacterClass.WARRIOR:
            base_damage += self.player.stats.strength * 1.5
        elif self.player.character_class == CharacterClass.MAGE:
            base_damage += self.player.stats.magic * 1.5
        elif self.player.character_class == CharacterClass.PALADIN:
            base_damage += (self.player.stats.strength + self.player.stats.magic) * 0.8
        else:  # Rogue
            base_damage += self.player.stats.agility * 1.3
            
        return int(base_damage + random.randint(-2, 4))

    def run(self):
        self.initialize_game()
        self._show_intro_cutscene()
        
        while self.game_state == "running":
            if self.current_location == "start":
                self._handle_start()
            elif self.current_location == "forest":
                self._handle_forest()
            elif self.current_location == "castle":
                self._handle_castle()
            elif self.current_location == "catacombs":
                self._handle_catacombs()
            elif self.current_location == "dragon_lair":
                self._handle_dragon_lair()
            elif self.current_location == "end":
                self._handle_ending()
                break
                
            if self.player.stats.health <= 0:
                self._handle_game_over()
                break

    def _show_intro_cutscene(self):
        clear_screen()
        dramatic_print(f"\n{Colors.YELLOW}The Kingdom of Aldermere lies in shadow...{Colors.ENDC}", 0.05)
        time.sleep(1)
        dramatic_print(f"{Colors.RED}The ancient Dragon Emperor has awakened after centuries of slumber,{Colors.ENDC}", 0.05)
        time.sleep(1)
        dramatic_print(f"{Colors.BLUE}and only a brave hero can restore peace to the realm.{Colors.ENDC}", 0.05)
        time.sleep(1)
        input(f"\n{Colors.GREEN}Press Enter to begin your journey...{Colors.ENDC}")

    def _handle_start(self):
        clear_screen()
        dramatic_print(f"\n{Colors.YELLOW}You stand at the crossroads of destiny.{Colors.ENDC}")
        dramatic_print("The town crier has announced three urgent quests:")
        print(f"\n{Colors.BLUE}1. The Haunted Forest{Colors.ENDC}")
        print("   Reports of dark creatures terrorizing travelers.")
        print("   Reward: Enchanted weapon + 100 gold")
        
        print(f"\n{Colors.BLUE}2. The Enchanted Castle{Colors.ENDC}")
        print("   Strange lights and mysterious disappearances.")
        print("   Reward: Magical artifact + 150 gold")
        
        print(f"\n{Colors.BLUE}3. The Ancient Catacombs{Colors.ENDC}")
        print("   Undead rising from forgotten tombs.")
        print("   Reward: Legendary armor + 200 gold")
        
        while True:
            choice = input(f"\n{Colors.GREEN}Which quest will you undertake? (1-3): {Colors.ENDC}")
            if choice in ['1', '2', '3']:
                self.player.story_choices["first_quest"] = choice
                if choice == '1':
                    self.current_location = "forest"
                elif choice == '2':
                    self.current_location = "castle"
                else:
                    self.current_location = "catacombs"
                break
            print(f"{Colors.RED}Invalid choice. Try again.{Colors.ENDC}")

    def _handle_forest(self):
        clear_screen()
        dramatic_print(f"\n{Colors.GREEN}You enter the Haunted Forest...{Colors.ENDC}")
        time.sleep(1)
        dramatic_print("The trees seem to whisper ancient secrets...")
        
        # Random forest encounters
        encounters = [
            Enemy("Shadow Wolf", 40, 40, 8, 
                "A ghostly wolf with glowing red eyes",
                "Shadow Bite",
                loot=[Item("Shadow Fang", ItemType.ARTIFACT, "A fang that gleams with dark energy", 10)]),
            Enemy("Corrupted Treant", 60, 60, 6,
                "An ancient tree possessed by dark magic",
                "Root Crush",
                loot=[Item("Heartwood Core", ItemType.ARTIFACT, "The magical core of a treant", 15)]),
            Enemy("Forest Witch", 45, 45, 10,
                "A mysterious witch wielding nature magic",
                "Nature's Wrath",
                loot=[Item("Witch's Staff", ItemType.WEAPON, "A staff infused with forest magic", 12)])
        ]
        
        for encounter in random.sample(encounters, 2):
            if not self.handle_combat(encounter):
                return
            
            # Healing spring chance after combat
            if random.random() < 0.3:
                dramatic_print(f"\n{Colors.BLUE}You discover a healing spring!{Colors.ENDC}")
                heal_amount = 30
                self.player.stats.health = min(self.player.stats.health + heal_amount, self.player.stats.max_health)
                dramatic_print(f"You recover {heal_amount} health!")
                time.sleep(1)
        
        # Forest decision point
        dramatic_print(f"\n{Colors.YELLOW}You come across a mysterious shrine...{Colors.ENDC}")
        print("\n1. Make an offering (Lose 20 gold for a blessing)")
        print("2. Continue on your path")
        print("3. Search for hidden treasures (Might be risky)")
        
        choice = input(f"\n{Colors.GREEN}What do you do? (1-3): {Colors.ENDC}")
        if choice == "1" and self.player.gold >= 20:
            self.player.gold -= 20
            blessing = random.choice([
                ("strength", 2),
                ("agility", 2),
                ("magic", 2),
                ("max_health", 20)
            ])
            setattr(self.player.stats, blessing[0], 
                    getattr(self.player.stats, blessing[0]) + blessing[1])
            dramatic_print(f"\n{Colors.YELLOW}The shrine grants you increased {blessing[0]}!{Colors.ENDC}")
        elif choice == "3":
            if random.random() < 0.6:
                treasure = random.choice([
                    Item("Ancient Scroll", ItemType.SCROLL, "A scroll of forgotten magic", 15),
                    Item("Forest Gem", ItemType.ARTIFACT, "A precious magical gem", 20)
                ])
                self.player.add_item(treasure)
                dramatic_print(f"\n{Colors.GREEN}You found a {treasure.name}!{Colors.ENDC}")
            else:
                damage = random.randint(10, 20)
                self.player.stats.health -= damage
                dramatic_print(f"\n{Colors.RED}A trap! You take {damage} damage!{Colors.ENDC}")
        
        dramatic_print(f"\n{Colors.BLUE}The forest path leads you to the Enchanted Castle...{Colors.ENDC}")
        self.current_location = "castle"

    def _handle_castle(self):
        clear_screen()
        dramatic_print(f"\n{Colors.BLUE}You arrive at the Enchanted Castle...{Colors.ENDC}")
        dramatic_print("The ancient stones pulse with magical energy.")
        
        # Castle exploration
        areas = ["Great Hall", "Wizard's Tower", "Dungeon"]
        current_area = random.choice(areas)
        
        dramatic_print(f"\nYou enter the {current_area}...")
        
        if current_area == "Great Hall":
            enemy = Enemy("Phantom Knight", 55, 55, 12,
                        "A spectral warrior in ancient armor",
                        "Ghostly Strike",
                        loot=[Item("Spectral Blade", ItemType.WEAPON, "A sword that phases through armor", 15)])
        elif current_area == "Wizard's Tower":
            enemy = Enemy("Arcane Construct", 50, 50, 14,
                        "A magical automaton gone rogue",
                        "Energy Blast",
                        loot=[Item("Mage's Orb", ItemType.ARTIFACT, "An orb crackling with magic", 15)])
        else:  # Dungeon
            enemy = Enemy("Prison Wraith", 45, 45, 16,
                        "A vengeful spirit of a forgotten prisoner",
                        "Soul Drain",
                        loot=[Item("Spirit Chain", ItemType.ARTIFACT, "Binds magical energy", 15)])
        
        if not self.handle_combat(enemy):
            return
            
        # Special room discovery
        dramatic_print(f"\n{Colors.YELLOW}You discover a mysterious room...{Colors.ENDC}")
        print("\n1. Enter the room")
        print("2. Continue exploring")
        
        if input(f"\n{Colors.GREEN}What do you do? (1-2): {Colors.ENDC}") == "1":
            if random.random() < 0.7:
                treasure = random.choice([
                    Item("Royal Crown", ItemType.ARTIFACT, "A crown of the ancient kings", 20),
                    Item("Enchanted Armor", ItemType.ARTIFACT, "Magical protective armor", 25),
                    Item("Spell Tome", ItemType.SCROLL, "Contains powerful magic", 20)
                ])
                self.player.add_item(treasure)
                dramatic_print(f"\n{Colors.GREEN}You found {treasure.name}!{Colors.ENDC}")
            else:
                damage = random.randint(15, 25)
                self.player.stats.health -= damage
                dramatic_print(f"\n{Colors.RED}A magical trap explodes! You take {damage} damage!{Colors.ENDC}")
        
        dramatic_print(f"\n{Colors.YELLOW}You hear a mighty roar from above...{Colors.ENDC}")
        self.current_location = "dragon_lair"

    def _handle_dragon_lair(self):
        clear_screen()
        dramatic_print(f"\n{Colors.RED}You enter the Dragon Emperor's lair...{Colors.ENDC}")
        dramatic_print("Ancient treasures glitter in the massive chamber.")
        
        print("\nThe Dragon Emperor regards you with ancient wisdom...")
        print("\n1. Attempt to negotiate peace")
        print("2. Challenge to honorable combat")
        print("3. Try to trick the dragon")
        
        choice = input(f"\n{Colors.GREEN}How do you approach? (1-3): {Colors.ENDC}")
        self.player.story_choices["dragon_approach"] = choice
        
        if choice == "1":
            if self.player.character_class in [CharacterClass.MAGE, CharacterClass.PALADIN]:
                dramatic_print(f"\n{Colors.GREEN}The Dragon Emperor senses your wisdom...{Colors.ENDC}")
                self._handle_peaceful_resolution()
                return
                
        # Dragon boss battle
        dragon = Enemy("Dragon Emperor", 100, 100, 20,
                      "The ancient ruler of these lands",
                      "Dragon's Breath",
                      special_ability_chance=0.3,
                      loot=[Item("Dragon Crown", ItemType.ARTIFACT, "The crown of dragon kings", 30)])
        
        if self.handle_combat(dragon):
            dramatic_print(f"\n{Colors.YELLOW}The Dragon Emperor falls...{Colors.ENDC}")
            self._handle_victory_ending()
        else:
            self._handle_game_over()

    def _handle_peaceful_resolution(self):
        dramatic_print(f"\n{Colors.YELLOW}Through wisdom and diplomacy, you forge a peace treaty with the Dragon Emperor.{Colors.ENDC}")
        dramatic_print("The ancient dragon shares its wisdom and power with you.")
        self.player.add_item(Item("Dragon's Blessing", ItemType.ARTIFACT, "A mark of dragon friendship", 25))
        self.current_location = "end"
        self.player.story_choices["ending"] = "peace"

    def _handle_victory_ending(self):
        self.current_location = "end"
        self.player.story_choices["ending"] = "victory"

    def _handle_game_over(self):
        clear_screen()
        dramatic_print(f"\n{Colors.RED}GAME OVER{Colors.ENDC}")
        dramatic_print("Your journey has come to an end...")
        dramatic_print(f"\nFinal Level: {self.player.level}")
        dramatic_print(f"Gold Collected: {self.player.gold}")
        input("\nPress Enter to exit...")

    def _handle_ending(self):
        clear_screen()
        if self.player.story_choices.get("ending") == "peace":
            dramatic_print(f"\n{Colors.YELLOW}=== The Diplomat's Victory ==={Colors.ENDC}")
            dramatic_print("You have brought peace to the realm through wisdom and understanding.")
            dramatic_print("The Dragon Emperor becomes a powerful ally, ushering in a new golden age.")
        else:
            dramatic_print(f"\n{Colors.YELLOW}=== The Hero's Victory ==={Colors.ENDC}")
            dramatic_print("Through courage and strength, you have defeated the Dragon Emperor.")
            dramatic_print("The realm is saved, and your name will be remembered in legend.")
        
        # Display final stats
        print(f"\n{Colors.GREEN}Final Statistics:{Colors.ENDC}")
        print(f"Level Reached: {self.player.level}")
        print(f"Gold Collected: {self.player.gold}")
        print(f"Items Collected: {len(self.player.inventory)}")
        
        # Achievement system
        achievements = []
        if self.player.level >= 5:
            achievements.append("Seasoned Adventurer")
        if self.player.gold >= 200:
            achievements.append("Master of Coin")
        if len(self.player.inventory) >= 8:
            achievements.append("Master Collector")
            
        if achievements:
            print(f"\n{Colors.YELLOW}Achievements Unlocked:{Colors.ENDC}")
            for achievement in achievements:
                print(f"- {achievement}")
        
        input(f"\n{Colors.GREEN}Press Enter to end your journey...{Colors.ENDC}")

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Game saved. Thanks for playing!{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.ENDC}")