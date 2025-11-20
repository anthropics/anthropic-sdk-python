"""Game world and locations for the RPG game."""
import random
from typing import Optional, Dict, List
from character import Player, create_enemy
from items import SHOP_ITEMS


class Location:
    """Represents a location in the game world."""

    def __init__(self, name: str, description: str, enemies: List[str], min_level: int = 1):
        self.name = name
        self.description = description
        self.enemies = enemies
        self.min_level = min_level

    def get_random_enemy(self, player_level: int):
        """Get a random enemy appropriate for this location."""
        enemy_type = random.choice(self.enemies)
        # Enemy level is based on player level
        enemy_level = max(self.min_level, player_level + random.randint(-1, 1))
        return create_enemy(enemy_type, enemy_level)


class Shop:
    """Item shop where players can buy items."""

    def __init__(self, name: str = "Wandering Merchant"):
        self.name = name

    def show_items(self):
        """Display available items."""
        print(f"\n{'='*50}")
        print(f"🏪 Welcome to {self.name}'s Shop!")
        print(f"{'='*50}")
        print("\nAvailable Items:")

        for i, (item_name, item_class) in enumerate(SHOP_ITEMS.items(), 1):
            item_instance = item_class()
            print(f"{i}. {item_instance}")

    def buy_item(self, player: Player, item_number: int) -> bool:
        """Buy an item if player has enough gold."""
        items_list = list(SHOP_ITEMS.items())

        if 1 <= item_number <= len(items_list):
            item_name, item_class = items_list[item_number - 1]
            item_instance = item_class()

            if player.gold >= item_instance.value:
                player.gold -= item_instance.value
                player.add_item(item_instance)
                print(f"\n✅ Purchased {item_instance.name} for {item_instance.value} gold!")
                return True
            else:
                print(f"\n❌ Not enough gold! You need {item_instance.value} gold but only have {player.gold}.")
                return False
        else:
            print("\n❌ Invalid item number!")
            return False


# Define game locations
LOCATIONS = {
    "village": Location(
        "Peaceful Village",
        "A quiet village where your journey begins. The fields nearby sometimes have weak monsters.",
        ["Goblin"],
        min_level=1
    ),
    "forest": Location(
        "Dark Forest",
        "A dense forest filled with dangerous creatures. Strange noises echo through the trees.",
        ["Goblin", "Skeleton"],
        min_level=2
    ),
    "mountains": Location(
        "Misty Mountains",
        "Treacherous peaks shrouded in mist. Only the brave dare venture here.",
        ["Orc", "Skeleton", "Dark Knight"],
        min_level=4
    ),
    "ruins": Location(
        "Ancient Ruins",
        "Crumbling structures from a forgotten civilization. Dark magic permeates the air.",
        ["Skeleton", "Dark Knight"],
        min_level=5
    ),
    "castle": Location(
        "Shadow Castle",
        "The dark lord's fortress. This is where the final battle awaits.",
        ["Dark Knight", "Dragon"],
        min_level=7
    ),
}


class GameWorld:
    """Manages the game world state and progression."""

    def __init__(self):
        self.current_location = "village"
        self.locations_unlocked = {"village"}
        self.story_progress = 0
        self.shop = Shop()

    def get_current_location(self) -> Location:
        """Get the current location object."""
        return LOCATIONS[self.current_location]

    def unlock_location(self, location_name: str):
        """Unlock a new location."""
        if location_name in LOCATIONS:
            self.locations_unlocked.add(location_name)

    def travel(self, location_name: str) -> bool:
        """Travel to a new location if it's unlocked."""
        if location_name in self.locations_unlocked:
            self.current_location = location_name
            return True
        return False

    def show_available_locations(self):
        """Display all unlocked locations."""
        print("\n🗺️  Available Locations:")
        for i, loc_name in enumerate(sorted(self.locations_unlocked), 1):
            loc = LOCATIONS[loc_name]
            current = " (Current)" if loc_name == self.current_location else ""
            print(f"{i}. {loc.name}{current}")
            print(f"   {loc.description}")

    def progress_story(self, player: Player):
        """Progress the story based on player level."""
        if self.story_progress == 0 and player.level >= 2:
            self.story_progress = 1
            self.unlock_location("forest")
            print("\n📜 Story Update:")
            print("The village elder approaches you...")
            print("'You've grown stronger, brave warrior! The Dark Forest has been")
            print(" plagued by monsters. Perhaps you can help?'")
            print("\n🗺️  New location unlocked: Dark Forest")

        elif self.story_progress == 1 and player.level >= 4:
            self.story_progress = 2
            self.unlock_location("mountains")
            print("\n📜 Story Update:")
            print("A mysterious traveler shares a tale...")
            print("'Beyond the forest lie the Misty Mountains. Orcs and dark knights")
            print(" have been spotted there. Are you brave enough to investigate?'")
            print("\n🗺️  New location unlocked: Misty Mountains")

        elif self.story_progress == 2 and player.level >= 6:
            self.story_progress = 3
            self.unlock_location("ruins")
            print("\n📜 Story Update:")
            print("An old wizard warns you...")
            print("'The Ancient Ruins hold dark secrets. Many have entered, few have")
            print(" returned. But we need someone to discover what evil lurks there.'")
            print("\n🗺️  New location unlocked: Ancient Ruins")

        elif self.story_progress == 3 and player.level >= 8:
            self.story_progress = 4
            self.unlock_location("castle")
            print("\n📜 Story Update:")
            print("The kingdom's messenger finds you...")
            print("'Hero! The Shadow Castle has been spotted in the distance. The Dark")
            print(" Lord must be stopped before it's too late! This is your final test!'")
            print("\n🗺️  New location unlocked: Shadow Castle")

    def rest(self, player: Player):
        """Rest at an inn to restore HP."""
        rest_cost = 20
        if player.gold >= rest_cost:
            player.gold -= rest_cost
            player.hp = player.max_hp
            print(f"\n🏨 You rest at the inn for {rest_cost} gold.")
            print("💤 You feel refreshed! HP fully restored!")
        else:
            print(f"\n❌ Not enough gold! Resting costs {rest_cost} gold.")
