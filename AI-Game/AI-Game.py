import random as r
import time as t
from typing import List, Dict, Optional 
from dataclasses import dataclass
from enum import Enum as e
import os as o
p=print
B='\033[94m'
G='\033[92m'
Y='\033[93m'
R='\033[91m'
E='\033[0m'
def clear_screen():
    o.system('class' if o.name=='int' else 'clear')
def dramatic_print(text:str, delay:float=0.03):
    for char in text:
        p(char, end='', flush=True)
        t.sleep(delay)
    p()  
class CharacterClass(e):
    WARRIOR="Warrior"
    MAGE="Mage"
    ROGUE="Rogue"
    PALADIN="Paladin"
class ItemType(e):
    WEAPON="weapon"
    POTION="potion"
    SCROLL="scroll"
@dataclass
class A:
    name:str
    description:str
    damage_multiplier:float
    cooldown:int
    current_cooldown:int=0
@dataclass
class S:
    strength:int
    agility:int
    magic:int
    health:int
    max_health:int
    mana:int=100
    max_mana:int=100
    critical_chance:float=0.1
@dataclass
class Item:
    name:str
    item_type:ItemType
    description:str
    power:int
    uses:Optional[int]=None
    special_effect:Optional[str]=None
@dataclass
class Enemy:
    name:str
    health:int
    max_health:int
    damage:int
    description:str
    special_A:Optional[str]=None
    special_ability_chance:float=0.2
    loot:List[Item]=None
    def __pot_init__(self):
        if self.loot is None:
            self.loot=[]
class Player:
    def __init__(self, name:str, character_class:CharacterClass):
        self.name=name
        self.character_class=character_class
        self.inventory:List[Item]=[]
        self.stats=self._initialize_stats()
        self.story_choices:Dict[str, str]={}
        self.abilities=self._initialize_abilities()
        self.level=1
        self.experience=0
        self.gold=50
    def _initialize_stats(self) -> S:
        base_health=100
        if self.character_class==CharacterClass.WARRIOR:
            return S(strength=8, agility=5, magic=2, health=base_health + 30, max_health=base_health + 30)
        elif self.character_class==CharacterClass.MAGE:
            return S(strength=3, agility=4, magic=8, health=base_health, max_health=base_health, mana=150, max_mana=150)
        elif self.character_class==CharacterClass.PALADIN:
            return S(strength=7, agility=3, magic=5, health=base_health + 40, max_health=base_health + 40)
        else:
            return S(strength=5, agility=8, magic=2, health=base_health + 10, max_health=base_health + 10, critical_chance=0.2)
    def _initialize_abilities(self) -> List[A]:
        abilities=[]
        if self.character_class==CharacterClass.WARRIOR:
            abilities=[
                A("Whirlwind", "Spin attack hitting all enemies", 1.5, 3),
                A("Battle Cry", "Boot damage for next attack", 2.0, 4)
            ]
        elif self.character_class==CharacterClass.MAGE:
            abilities=[
                A("Fireball", "Powerful fire magic", 2.0, 2),
                A("Ice Storm", "Freezing area attack", 1.8, 3)
            ]
        elif self.character_class==CharacterClass.ROGUE:
            abilities=[
                A("Backstab", "Critical strike from shadows", 2.5, 3),
                A("Smoke Bomb", "Escape from battle", 0, 5)
            ]
        elif self.character_class==CharacterClass.PALADIN:
            abilities=[
                A("Holy Strike", "Divine damage + healing", 1.7, 3),
                A("Divine Shield", "Temporary invulnerability", 0, 6)
            ]
        return abilities
    def add_item(self, item:Item) -> bool:
        if len(self.inventory) < 10:
            self.inventory.append(item)
            return True
        return False
    def show_inventory(self):
        if not self.inventory:
            p(f"{Y}Your inventory is empty.{E}")
            return
        p(f"\n{B}=== Inventory ==={E}")
        for i, item in e(self.inventory, 1):
            p(f"{i}. {item.name} - {item.description}")
            if item.uses is not None:
                p(f"   Uses remaining:{item.uses}")
    def use_item(self, item_index:int) -> bool:
        if item_index < 0 or item_index >= len(self.inventory):
            return False
        item=self.inventory[item_index]
        if item.item_type==ItemType.POTION:
            self.stats.health=min(self.stats.health + item.power, self.stats.max_health)
            p(f"{G}You recover {item.power} health!{E}")
            if item.uses is not None:
                item.uses -= 1
                if item.uses <= 0:
                    self.inventory.pop(item_index)
            else:
                self.inventory.pop(item_index)
            return True
        elif item.item_type==ItemType.SCROLL:
            p(f"{Y}You use {item.name}!{E}")
            if item.special_effect:
                p(f"Effect:{item.special_effect}")
            self.inventory.pop(item_index)
            return True
        return False
    def gain_experience(self, amount:int):
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()
    def level_up(self):
        self.level += 1
        self.experience=0
        self.stats.max_health += 20
        self.stats.health=self.stats.max_health
        dramatic_print(f"\n{Y}*** LEVEL UP! ***{E}")
        dramatic_print(f"You are now level {self.level}!")
        self._improve_stats()
    def i_(self):
        if self.character_class==CharacterClass.WARRIOR:
            self.stats.strength += 3
        elif self.character_class==CharacterClass.MAGE:
            self.stats.magic += 3
            self.stats.max_mana += 20
        elif self.character_class==CharacterClass.ROGUE:
            self.stats.agility += 3
            self.stats.critical_chance += 0.05
    def show_status(self):
        p(f"\n{B}=== {self.name} the {self.character_class.value} ===")
        p(f"Level:{self.level} | XP:{self.experience}/100")
        p(f"Health:{self.stats.health}/{self.stats.max_health}")
        p(f"Mana:{self.stats.mana}/{self.stats.max_mana}")
        p(f"Gold:{self.gold}{E}")
    def gain_experience(self, amount:int):
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()
    def level_up(self):
        self.level += 1
        self.experience=0
        self.stats.max_health += 20
        self.stats.health=self.stats.max_health
        dramatic_print(f"\n{Y}*** LEVEL UP! ***{E}")
        dramatic_print(f"You are now level {self.level}!")
        self._improve_stats()
    def _improve_stats(self):
        if self.character_class==CharacterClass.WARRIOR:
            self.stats.strength += 3
        elif self.character_class==CharacterClass.MAGE:
            self.stats.magic += 3
            self.stats.max_mana += 20
        elif self.character_class==CharacterClass.ROGUE:
            self.stats.agility += 3
            self.stats.critical_chance += 0.05
    def show_status(self):
        p(f"\n{B}=== {self.name} the {self.character_class.value} ===")
        p(f"Level:{self.level} | XP:{self.experience}/100")
        p(f"Health:{self.stats.health}/{self.stats.max_health}")
        p(f"Mana:{self.stats.mana}/{self.stats.max_mana}")
        p(f"Gold:{self.gold}{E}")
class Game:
    def __init__(self):
        self.player:Optional[Player]=None
        self.current_location="start"
        self.game_state="running"
        self.current_quest=None
    def initialize_game(self):
        clear_screen()
        dramatic_print(f"{Y}Welcome to the Epic Quest of Destiny!{E}")
        t.sleep(1)
        name=input(f"\n{G}Enter your character's name:{E}")
        p(f"\n{B}Chooe your class:{E}")
        for char_class in CharacterClass:
            p(f"- {char_class.value}")
            if char_class==CharacterClass.WARRIOR:
                p("  Master of weapons and combat")
            elif char_class==CharacterClass.MAGE:
                p("  Wielder of powerful magic")
            elif char_class==CharacterClass.ROGUE:
                p("  Expert in stealth and critical strikes")
            elif char_class==CharacterClass.PALADIN:
                p("  Holy warrior with healing powers")
            p()
        while True:
            class_choice=input(f"{G}Enter your choice:{E}").upper()
            try:
                character_class=CharacterClass[class_choice]
                break
            except KeyError:
                p(f"{R}Invalid class choice. Please try again.{E}")
        self.player=Player(name, character_class)
        self._give_starting_items()
    def _give_starting_items(self):
        starting_items={
            CharacterClass.WARRIOR:[
                Item("Steel Greatsword", ItemType.WEAPON, "A mighty two-handed sword", 8),
                Item("Chain Mail", ItemType.ARTIFACT, "Standard protective armor", 5)
            ],
            CharacterClass.MAGE:[
                Item("Enchanted Staff", ItemType.WEAPON, "A staff crackling with energy", 6),
                Item("Mana Crystal", ItemType.ARTIFACT, "Restores mana over t", 5)
            ],
            CharacterClass.ROGUE:[
                Item("Shadow Daggers", ItemType.WEAPON, "Twin daggers for swift strikes", 7),
                Item("Smoke Bombs", ItemType.ARTIFACT, "Provides quick escape", 5, uses=3)
            ],
            CharacterClass.PALADIN:[
                Item("Holy Mace", ItemType.WEAPON, "A mace blessed with divine power", 7),
                Item("Holy Symbol", ItemType.ARTIFACT, "Enhances healing abilities", 5)
            ]
        }
        for item in starting_items[self.player.character_class]:
            self.player.add_item(item)
        self.player.add_item(Item("Health Potion", ItemType.POTION, "Restores 30 HP", 30, 2))
    def handle_combat(self, enemy:Enemy) -> bool:
        dramatic_print(f"\n{R}A {enemy.name} appears! {enemy.description}{E}")
        t.sleep(1)
        while enemy.health > 0 and self.player.stats.health > 0:
            clear_screen()
            self.player.show_status()
            p(f"\n{R}Enemy:{enemy.name}")
            p(f"Health:{enemy.health}/{enemy.max_health}{E}")
            p("\nActions:")
            p("1. Attack")
            p("2. Defend")
            p("3. Use Item")
            p("4. Use Ability")
            action=input(f"\n{G}Chooe your action (1-4):{E}")
            if action=="1":
                damage=self._calculate_damage()
                if r.r() < self.player.stats.critical_chance:
                    damage *= 2
                    dramatic_print(f"{Y}CRITICAL HIT!{E}")
                enemy.health -= damage
                dramatic_print(f"You deal {G}{damage}{E} damage!")
            elif action=="2":
                dramatic_print(f"{B}You take a defensive stance!{E}")
                damage_Ruction=0.5
            elif action=="3":
                self.player.show_inventory()
                try:
                    item_choice=int(input(f"{G}Chooe item number (0 to cancel):{E}")) - 1
                    if item_choice >= -1:
                        self.player.use_item(item_choice)
                except ValueError:
                    p(f"{R}Invalid input!{E}")
                    continue
            elif action=="4":
                if not self.player.abilities:
                    dramatic_print(f"{R}No abilities available!{E}")
                    continue
                p("\nAbilities:")
                for i, ability in e(self.player.abilities, 1):
                    if ability.current_cooldown==0:
                        p(f"{i}. {ability.name} - {ability.description}")
                    else:
                        p(f"{i}. {ability.name} - Cooldown:{ability.current_cooldown} turns")
                try:
                    ability_choice=int(input(f"{G}Chooe ability (0 to cancel):{E}")) - 1
                    if 0 <= ability_choice < len(self.player.abilities):
                        ability=self.player.abilities[ability_choice]
                        if ability.current_cooldown==0:
                            damage=self._calculate_damage() * ability.damage_multiplier
                            enemy.health -= damage
                            ability.current_cooldown=ability.cooldown
                            dramatic_print(f"\n{Y}You use {ability.name}!")
                            dramatic_print(f"It deals {G}{damage}{E} damage!")
                        else:
                            p(f"{R}That ability is on cooldown!{E}")
                except ValueError:
                    p(f"{R}Invalid input!{E}")
                    continue
            else:
                p(f"{R}Invalid action!{E}")
                continue
            for ability in self.player.abilities:
                if ability.current_cooldown > 0:
                    ability.current_cooldown -= 1
            if enemy.health > 0:
                if r.r() < enemy.special_ability_chance and enemy.special_ability:
                    damage=enemy.damage * 1.5
                    dramatic_print(f"\n{R}{enemy.name} uses {enemy.special_ability}!{E}")
                else:
                    damage=max(0, enemy.damage - r.randint(0, 2))
                if action=="2":
                    damage=int(damage * 0.5)
                self.player.stats.health -= damage
                dramatic_print(f"{enemy.name} attacks you for {R}{damage}{E} damage!")
            t.sleep(1)
        if enemy.health <= 0:
            dramatic_print(f"\n{G}Victory! You've defeated the {enemy.name}!{E}")
            self._handle_victory_rewards(enemy)
            return True
        return False
    def _handle_victory_rewards(self, enemy:Enemy):
        exp_gain=r.randint(20, 40)
        gold_gain=r.randint(10, 30)
        self.player.gain_experience(exp_gain)
        self.player.gold += gold_gain
        dramatic_print(f"\n{Y}You gained:")
        dramatic_print(f"+ {exp_gain} experience")
        dramatic_print(f"+ {gold_gain} gold{E}")
        if enemy.loot:
            item=r.choice(enemy.loot)
            if self.player.add_item(item):
                dramatic_print(f"\n{G}You found:{item.name}!{E}")
    def _calculate_damage(self) -> int:
        base_damage=5
        if self.player.character_class==CharacterClass.WARRIOR:
            base_damage += self.player.stats.strength * 1.5
        elif self.player.character_class==CharacterClass.MAGE:
            base_damage += self.player.stats.magic * 1.5
        elif self.player.character_class==CharacterClass.PALADIN:
            base_damage += (self.player.stats.strength + self.player.stats.magic) * 0.8
        else:
            base_damage += self.player.stats.agility * 1.3
        return int(base_damage + r.randint(-2, 4))
    def _calculate_damage(self) -> int:
        base_damage=5
        if self.player.character_class==CharacterClass.WARRIOR:
            base_damage += self.player.stats.strength * 1.5
        elif self.player.character_class==CharacterClass.MAGE:
            base_damage += self.player.stats.magic * 1.5
        elif self.player.character_class==CharacterClass.PALADIN:
            base_damage += (self.player.stats.strength + self.player.stats.magic) * 0.8
        else:
            base_damage += self.player.stats.agility * 1.3
        return int(base_damage + r.randint(-2, 4))
    def run(self):
        self.initialize_game()
        self._show_intro_cutscene()
        while self.game_state=="running":
            if self.current_location=="start":
                self._handle_start()
            elif self.current_location=="forest":
                self._handle_forest()
            elif self.current_location=="castle":
                self._handle_castle()
            elif self.current_location=="catacombs":
                self._handle_catacombs()
            elif self.current_location=="dragon_lair":
                self._handle_dragon_lair()
            elif self.current_location=="end":
                self._handle_ending()
                break
            if self.player.stats.health <= 0:
                self._handle_game_over()
                break
    def _show_intro_cutscene(self):
        clear_screen()
        dramatic_print(f"\n{Y}The Kingdom of Aldermere lies in shadow...{E}", 0.05)
        t.sleep(1)
        dramatic_print(f"{R}The ancient Dragon Emperor has awakened after centuries of slumber,{E}", 0.05)
        t.sleep(1)
        dramatic_print(f"{B}and only a brave hero can restore peace to the realm.{E}", 0.05)
        t.sleep(1)
        input(f"\n{G}Press Enter to begin your journey...{E}")
    def _handle_start(self):
        clear_screen()
        dramatic_print(f"\n{Y}You stand at the crosroads of destiny.{E}")
        dramatic_print("The town crier has announced three urgent quests:")
        p(f"\n{B}1. The Haunted Forest{E}")
        p("   Reports of dark creatures terrorizing travelers.")
        p("   Reward:Enchanted weapon + 100 gold")
        p(f"\n{B}2. The Enchanted Castle{E}")
        p("   Strange lights and mysterious disappearances.")
        p("   Reward:Magical artifact + 150 gold")
        p(f"\n{B}3. The Ancient Catacombs{E}")
        p("   Undead rising from forgotten tombs.")
        p("   Reward:Legendary armor + 200 gold")
        while True:
            choice=input(f"\n{G}Which quest will you undertake? (1-3):{E}")
            if choice in ['1', '2', '3']:
                self.player.story_choices["first_quest"]=choice
                if choice=='1':
                    self.current_location="forest"
                elif choice=='2':
                    self.current_location="castle"
                else:
                    self.current_location="catacombs"
                break
            p(f"{R}Invalid choice. Try again.{E}")
    def _handle_forest(self):
        clear_screen()
        dramatic_print(f"\n{G}You enter the Haunted Forest...{E}")
        t.sleep(1)
        dramatic_print("The trees seem to whisper ancient secrets...")
        encounters=[
            Enemy("Shadow Wolf", 40, 40, 8, 
                "A ghotly wolf with glowing R eyes",
                "Shadow Bite",
                loot=[Item("Shadow Fang", ItemType.ARTIFACT, "A fang that gleams with dark energy", 10)]),
            Enemy("Corrupted Treant", 60, 60, 6,
                "An ancient tree posessed by dark magic",
                "Root Crush",
                loot=[Item("Heartwood Core", ItemType.ARTIFACT, "The magical core of a treant", 15)]),
            Enemy("Forest Witch", 45, 45, 10,
                "A mysterious witch wielding nature magic",
                "Nature's Wrath",
                loot=[Item("Witch's Staff", ItemType.WEAPON, "A staff infused with forest magic", 12)])
        ]
        for encounter in r.sample(encounters, 2):
            if not self.handle_combat(encounter):
                return
            if r.r() < 0.3:
                dramatic_print(f"\n{B}You discover a healing spring!{E}")
                heal_amount=30
                self.player.stats.health=min(self.player.stats.health + heal_amount, self.player.stats.max_health)
                dramatic_print(f"You recover {heal_amount} health!")
                t.sleep(1)
        dramatic_print(f"\n{Y}You come acros a mysterious shrine...{E}")
        p("\n1. Make an offering (Loe 20 gold for a blessing)")
        p("2. Continue on your path")
        p("3. Search for hidden treasures (Might be risky)")
        choice=input(f"\n{G}What do you do? (1-3):{E}")
        if choice=="1" and self.player.gold >= 20:
            self.player.gold -= 20
            blessing=r.choice([
                ("strength", 2),
                ("agility", 2),
                ("magic", 2),
                ("max_health", 20)
            ])
            setattr(self.player.stats, blessing[0], 
                    getattr(self.player.stats, blessing[0]) + blessing[1])
            dramatic_print(f"\n{Y}The shrine grants you increased {blessing[0]}!{E}")
        elif choice=="3":
            if r.r() < 0.6:
                treasure=r.choice([
                    Item("Ancient Scroll", ItemType.SCROLL, "A scroll of forgotten magic", 15),
                    Item("Forest Gem", ItemType.ARTIFACT, "A precious magical gem", 20)
                ])
                self.player.add_item(treasure)
                dramatic_print(f"\n{G}You found a {treasure.name}!{E}")
            else:
                damage=r.randint(10, 20)
                self.player.stats.health -= damage
                dramatic_print(f"\n{R}A trap! You take {damage} damage!{E}")
        dramatic_print(f"\n{B}The forest path leads you to the Enchanted Castle...{E}")
        self.current_location="castle"
    def _handle_castle(self):
        clear_screen()
        dramatic_print(f"\n{B}You arrive at the Enchanted Castle...{E}")
        dramatic_print("The ancient stones pulse with magical energy.")
        areas=["Great Hall", "Wizard's Tower", "Dungeon"]
        current_area=r.choice(areas)
        
        dramatic_print(f"\nYou enter the {current_area}...")
        
        if current_area=="Great Hall":
            enemy=Enemy("Phantom Knight", 55, 55, 12,
                        "A spectral warrior in ancient armor",
                        "Ghotly Strike",
                        loot=[Item("Spectral Blade", ItemType.WEAPON, "A sword that phases through armor", 15)])
        elif current_area=="Wizard's Tower":
            enemy=Enemy("Arcane Construct", 50, 50, 14,
                        "A magical automaton gone rogue",
                        "Energy Blast",
                        loot=[Item("Mage's Orb", ItemType.ARTIFACT, "An orb crackling with magic", 15)])
        else:
            enemy=Enemy("Prison Wraith", 45, 45, 16,
                        "A vengeful spirit of a forgotten prisoner",
                        "Soul Drain",
                        loot=[Item("Spirit Chain", ItemType.ARTIFACT, "Binds magical energy", 15)])
        if not self.handle_combat(enemy):
            return
        dramatic_print(f"\n{Y}You discover a mysterious room...{E}")
        p("\n1. Enter the room")
        p("2. Continue exploring")
        if input(f"\n{G}What do you do? (1-2):{E}")=="1":
            if r.r() < 0.7:
                treasure=r.choice([
                    Item("Royal Crown", ItemType.ARTIFACT, "A crown of the ancient kings", 20),
                    Item("Enchanted Armor", ItemType.ARTIFACT, "Magical protective armor", 25),
                    Item("Spell Tome", ItemType.SCROLL, "Contains powerful magic", 20)
                ])
                self.player.add_item(treasure)
                dramatic_print(f"\n{G}You found {treasure.name}!{E}")
            else:
                damage=r.randint(15, 25)
                self.player.stats.health -= damage
                dramatic_print(f"\n{R}A magical trap explodes! You take {damage} damage!{E}")
        dramatic_print(f"\n{Y}You hear a mighty roar from above...{E}")
        self.current_location="dragon_lair"
    def _handle_dragon_lair(self):
        clear_screen()
        dramatic_print(f"\n{R}You enter the Dragon Emperor's lair...{E}")
        dramatic_print("Ancient treasures glitter in the massive chamber.")
        p("\nThe Dragon Emperor regards you with ancient wisdom...")
        p("\n1. Attempt to negotiate peace")
        p("2. Challenge to honorable combat")
        p("3. Try to trick the dragon")
        choice=input(f"\n{G}How do you approach? (1-3):{E}")
        self.player.story_choices["dragon_approach"]=choice
        if choice=="1":
            if self.player.character_class in [CharacterClass.MAGE, CharacterClass.PALADIN]:
                dramatic_print(f"\n{G}The Dragon Emperor senses your wisdom...{E}")
                self._handle_peaceful_resolution()
                return
        dragon=Enemy("Dragon Emperor", 100, 100, 20,
                      "The ancient ruler of these lands",
                      "Dragon's Breath",
                      special_ability_chance=0.3,
                      loot=[Item("Dragon Crown", ItemType.ARTIFACT, "The crown of dragon kings", 30)])
        if self.handle_combat(dragon):
            dramatic_print(f"\n{Y}The Dragon Emperor falls...{E}")
            self._handle_victory_ending()
        else:
            self._handle_game_over()
    def _handle_peaceful_resolution(self):
        dramatic_print(f"\n{Y}Through wisdom and diplomacy, you forge a peace treaty with the Dragon Emperor.{E}")
        dramatic_print("The ancient dragon shares its wisdom and power with you.")
        self.player.add_item(Item("Dragon's Blessing", ItemType.ARTIFACT, "A mark of dragon friendship", 25))
        self.current_location="end"
        self.player.story_choices["ending"]="peace"
    def _handle_victory_ending(self):
        self.current_location="end"
        self.player.story_choices["ending"]="victory"
    def _handle_game_over(self):
        clear_screen()
        dramatic_print(f"\n{R}GAME OVER{E}")
        dramatic_print("Your journey has come to an end...")
        dramatic_print(f"\nFinal Level:{self.player.level}")
        dramatic_print(f"Gold Collected:{self.player.gold}")
        input("\nPress Enter to exit...")
    def _handle_ending(self):
        clear_screen()
        if self.player.story_choices.get("ending")=="peace":
            dramatic_print(f"\n{Y}=== The Diplomat's Victory ==={E}")
            dramatic_print("You have brought peace to the realm through wisdom and understanding.")
            dramatic_print("The Dragon Emperor becomes a powerful ally, ushering in a new golden age.")
        else:
            dramatic_print(f"\n{Y}=== The Hero's Victory ==={E}")
            dramatic_print("Through courage and strength, you have defeated the Dragon Emperor.")
            dramatic_print("The realm is saved, and your name will be remembeR in legend.")
        p(f"\n{G}Final Statistics:{E}")
        p(f"Level Reached:{self.player.level}")
        p(f"Gold Collected:{self.player.gold}")
        p(f"Items Collected:{len(self.player.inventory)}")
        achievements=[]
        if self.player.level >= 5:
            achievements.append("Seasoned Adventurer")
        if self.player.gold >= 200:
            achievements.append("Master of Coin")
        if len(self.player.inventory) >= 8:
            achievements.append("Master Collector")
        if achievements:
            p(f"\n{Y}Achievements Unlocked:{E}")
            for achievement in achievements:
                p(f"- {achievement}")
        input(f"\n{G}Press Enter to end your journey...{E}")
if __name__=="__main__":
    try:
        game=Game()
        game.run()
    except KeyboardInterrupt:
        p(f"\n{Y}Game saved. Thanks for playing!{E}")
    except Exception as e:
        p(f"\n{R}An error occurR:{e}{E}")