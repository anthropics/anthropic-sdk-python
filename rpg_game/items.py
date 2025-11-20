"""Item system for the RPG game."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Player


class Item:
    """Base class for all items."""

    def __init__(self, name: str, description: str, value: int):
        self.name = name
        self.description = description
        self.value = value

    def use(self, player: 'Player') -> str:
        """Use the item on the player."""
        return f"You can't use {self.name}."

    def __str__(self) -> str:
        return f"{self.name} - {self.description} (Value: {self.value}g)"


class Potion(Item):
    """Health potion that restores HP."""

    def __init__(self, name: str = "Health Potion", heal_amount: int = 50, value: int = 25):
        super().__init__(name, f"Restores {heal_amount} HP", value)
        self.heal_amount = heal_amount

    def use(self, player: 'Player') -> str:
        """Use the potion to heal."""
        if player.hp == player.max_hp:
            return "You are already at full health!"

        healed = player.heal(self.heal_amount)
        return f"You used {self.name} and restored {healed} HP!"


class MegaPotion(Potion):
    """Stronger health potion."""

    def __init__(self):
        super().__init__(name="Mega Potion", heal_amount=100, value=50)


class Elixir(Item):
    """Fully restores HP."""

    def __init__(self):
        super().__init__("Elixir", "Fully restores HP", 100)

    def use(self, player: 'Player') -> str:
        """Use the elixir to fully heal."""
        if player.hp == player.max_hp:
            return "You are already at full health!"

        healed = player.heal(player.max_hp)
        return f"You used Elixir and restored {healed} HP! You're at full health!"


class AttackBoost(Item):
    """Permanently increases attack."""

    def __init__(self):
        super().__init__("Attack Boost", "Permanently increases Attack by 5", 150)

    def use(self, player: 'Player') -> str:
        """Use to increase attack."""
        player.attack += 5
        return "You used Attack Boost! Your Attack increased by 5!"


class DefenseBoost(Item):
    """Permanently increases defense."""

    def __init__(self):
        super().__init__("Defense Boost", "Permanently increases Defense by 3", 150)

    def use(self, player: 'Player') -> str:
        """Use to increase defense."""
        player.defense += 3
        return "You used Defense Boost! Your Defense increased by 3!"


class MaxHPBoost(Item):
    """Permanently increases max HP."""

    def __init__(self):
        super().__init__("Max HP Boost", "Permanently increases Max HP by 20", 200)

    def use(self, player: 'Player') -> str:
        """Use to increase max HP."""
        player.max_hp += 20
        player.hp += 20
        return "You used Max HP Boost! Your Max HP increased by 20!"


# Shop inventory
SHOP_ITEMS = {
    "Health Potion": Potion,
    "Mega Potion": MegaPotion,
    "Elixir": Elixir,
    "Attack Boost": AttackBoost,
    "Defense Boost": DefenseBoost,
    "Max HP Boost": MaxHPBoost,
}
