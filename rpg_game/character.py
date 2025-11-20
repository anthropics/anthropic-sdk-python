"""Character system for the RPG game."""
from typing import Optional, List
import random


class Character:
    """Base class for all characters in the game."""

    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int, level: int = 1):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.is_alive = True

    def take_damage(self, damage: int) -> int:
        """Take damage and return actual damage taken."""
        # Defense reduces damage
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage

        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

        return actual_damage

    def heal(self, amount: int) -> int:
        """Heal the character and return actual healing done."""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def attack_target(self, target: 'Character') -> int:
        """Attack a target and return damage dealt."""
        # Random damage between 80% and 120% of attack
        base_damage = self.attack
        damage_variance = random.uniform(0.8, 1.2)
        damage = int(base_damage * damage_variance)

        return target.take_damage(damage)

    def __str__(self) -> str:
        return f"{self.name} (Lvl {self.level}) - HP: {self.hp}/{self.max_hp}"


class Player(Character):
    """Player character with additional features."""

    def __init__(self, name: str, character_class: str):
        self.character_class = character_class
        self.exp = 0
        self.exp_to_next_level = 100
        self.gold = 50
        self.inventory: List['Item'] = []

        # Set initial stats based on class
        if character_class == "Warrior":
            super().__init__(name, hp=120, max_hp=120, attack=15, defense=8, level=1)
        elif character_class == "Mage":
            super().__init__(name, hp=80, max_hp=80, attack=20, defense=3, level=1)
        elif character_class == "Rogue":
            super().__init__(name, hp=100, max_hp=100, attack=17, defense=5, level=1)
        else:
            super().__init__(name, hp=100, max_hp=100, attack=15, defense=5, level=1)

    def gain_exp(self, amount: int) -> bool:
        """Gain experience and return True if leveled up."""
        self.exp += amount

        if self.exp >= self.exp_to_next_level:
            self.level_up()
            return True

        return False

    def level_up(self):
        """Level up the character."""
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)

        # Increase stats based on class
        if self.character_class == "Warrior":
            self.max_hp += 20
            self.attack += 3
            self.defense += 2
        elif self.character_class == "Mage":
            self.max_hp += 10
            self.attack += 5
            self.defense += 1
        elif self.character_class == "Rogue":
            self.max_hp += 15
            self.attack += 4
            self.defense += 1

        # Fully heal on level up
        self.hp = self.max_hp

    def add_item(self, item: 'Item'):
        """Add an item to inventory."""
        self.inventory.append(item)

    def use_item(self, item_index: int) -> Optional[str]:
        """Use an item from inventory."""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            result = item.use(self)
            self.inventory.pop(item_index)
            return result
        return None

    def get_stats(self) -> str:
        """Get formatted stats."""
        return f"""
╔══════════════════════════════════╗
║ {self.name} - Level {self.level} {self.character_class}
╠══════════════════════════════════╣
║ HP: {self.hp}/{self.max_hp}
║ Attack: {self.attack}
║ Defense: {self.defense}
║ EXP: {self.exp}/{self.exp_to_next_level}
║ Gold: {self.gold}
╚══════════════════════════════════╝
"""


class Enemy(Character):
    """Enemy character."""

    def __init__(self, name: str, hp: int, attack: int, defense: int, level: int, exp_reward: int, gold_reward: int):
        super().__init__(name, hp, hp, attack, defense, level)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward


# Pre-defined enemy types
ENEMY_TYPES = {
    "Goblin": lambda level: Enemy(
        "Goblin",
        hp=30 + (level * 10),
        attack=8 + (level * 2),
        defense=2 + level,
        level=level,
        exp_reward=20 + (level * 10),
        gold_reward=10 + (level * 5)
    ),
    "Orc": lambda level: Enemy(
        "Orc",
        hp=50 + (level * 15),
        attack=12 + (level * 3),
        defense=5 + (level * 2),
        level=level,
        exp_reward=35 + (level * 15),
        gold_reward=20 + (level * 10)
    ),
    "Skeleton": lambda level: Enemy(
        "Skeleton",
        hp=40 + (level * 12),
        attack=10 + (level * 2),
        defense=3 + level,
        level=level,
        exp_reward=25 + (level * 12),
        gold_reward=15 + (level * 7)
    ),
    "Dragon": lambda level: Enemy(
        "Dragon",
        hp=150 + (level * 30),
        attack=25 + (level * 5),
        defense=15 + (level * 3),
        level=level,
        exp_reward=100 + (level * 50),
        gold_reward=100 + (level * 50)
    ),
    "Dark Knight": lambda level: Enemy(
        "Dark Knight",
        hp=100 + (level * 20),
        attack=20 + (level * 4),
        defense=10 + (level * 2),
        level=level,
        exp_reward=70 + (level * 30),
        gold_reward=50 + (level * 25)
    ),
}


def create_enemy(enemy_type: str, level: int) -> Enemy:
    """Create an enemy of the specified type and level."""
    if enemy_type in ENEMY_TYPES:
        return ENEMY_TYPES[enemy_type](level)
    else:
        return ENEMY_TYPES["Goblin"](level)
