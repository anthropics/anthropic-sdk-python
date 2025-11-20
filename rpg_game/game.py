#!/usr/bin/env python3
"""
Epic RPG Adventure Game
A text-based RPG with combat, exploration, and character progression.
"""
import sys
from character import Player, create_enemy
from combat import combat, boss_fight
from world import GameWorld, LOCATIONS
from items import Potion


def print_banner():
    """Display the game banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ⚔️  EPIC RPG ADVENTURE  ⚔️                                 ║
║                                                              ║
║        A Text-Based Role Playing Game                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def create_character() -> Player:
    """Character creation process."""
    print("\n🌟 Welcome, brave adventurer!")
    print("\nWhat is your name?")
    name = input("Name: ").strip()

    if not name:
        name = "Hero"

    print(f"\nGreetings, {name}! Choose your class:")
    print("\n1. ⚔️  Warrior - High HP and Defense, balanced attack")
    print("   Starting Stats: HP 120, ATK 15, DEF 8")
    print("\n2. 🔮 Mage - Powerful magic attacks, low defense")
    print("   Starting Stats: HP 80, ATK 20, DEF 3")
    print("\n3. 🗡️  Rogue - High damage, moderate defense")
    print("   Starting Stats: HP 100, ATK 17, DEF 5")

    while True:
        choice = input("\nChoose your class (1-3): ").strip()

        if choice == "1":
            player = Player(name, "Warrior")
            break
        elif choice == "2":
            player = Player(name, "Mage")
            break
        elif choice == "3":
            player = Player(name, "Rogue")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

    print(f"\n✨ {player.name} the {player.character_class} has been created!")
    print(player.get_stats())

    return player


def show_main_menu():
    """Display the main game menu."""
    print("\n" + "="*50)
    print("What would you like to do?")
    print("="*50)
    print("1. 🗡️  Explore and Fight")
    print("2. 🗺️  Travel to Different Location")
    print("3. 🏪 Visit Shop")
    print("4. 🎒 Check Inventory")
    print("5. 📊 View Stats")
    print("6. 🏨 Rest at Inn (Restore HP)")
    print("7. 💾 Save & Quit")
    print("="*50)


def explore(player: Player, world: GameWorld) -> bool:
    """
    Explore and encounter enemies.
    Returns False if player dies, True otherwise.
    """
    current_loc = world.get_current_location()

    print(f"\n🌍 You explore the {current_loc.name}...")
    print(f"   {current_loc.description}")

    # Check for boss fight at castle
    if world.current_location == "castle" and player.level >= 8:
        print("\n⚠️  You sense an overwhelming dark presence...")
        boss = create_enemy("Dragon", player.level + 2)
        result = boss_fight(player, boss)

        if result and player.is_alive:
            print("\n" + "="*50)
            print("🎊" * 25)
            print("\n   🏆 CONGRATULATIONS! 🏆")
            print("\n   You have defeated the Dark Lord!")
            print("   Peace is restored to the kingdom!")
            print("\n   Thanks for playing!")
            print("\n🎊" * 25)
            print("="*50)
            sys.exit(0)

        return player.is_alive

    # Normal encounter
    enemy = current_loc.get_random_enemy(player.level)
    result = combat(player, enemy)

    if result and player.is_alive:
        # Check for story progression
        world.progress_story(player)

    return player.is_alive


def travel(player: Player, world: GameWorld):
    """Travel to a different location."""
    world.show_available_locations()

    print(f"\n{len(world.locations_unlocked) + 1}. Cancel")

    choice = input("\nWhere would you like to go? ").strip()

    if choice.isdigit():
        choice_num = int(choice)
        locations_list = sorted(world.locations_unlocked)

        if choice_num == len(locations_list) + 1:
            return

        if 1 <= choice_num <= len(locations_list):
            new_location = locations_list[choice_num - 1]

            if new_location != world.current_location:
                world.travel(new_location)
                loc = LOCATIONS[new_location]
                print(f"\n🚶 You travel to {loc.name}.")
                print(f"   {loc.description}")
            else:
                print("\n❌ You're already here!")
        else:
            print("\n❌ Invalid choice!")
    else:
        print("\n❌ Invalid input!")


def visit_shop(player: Player, world: GameWorld):
    """Visit the item shop."""
    while True:
        world.shop.show_items()
        print(f"\n💰 Your gold: {player.gold}")
        print(f"\n{len(list(SHOP_ITEMS.keys())) + 1}. Leave Shop")

        choice = input("\nWhat would you like to buy? ").strip()

        if choice.isdigit():
            choice_num = int(choice)

            if choice_num == len(SHOP_ITEMS) + 1:
                print("\n👋 Come back soon!")
                break

            world.shop.buy_item(player, choice_num)
        else:
            print("\n❌ Invalid input!")


def check_inventory(player: Player):
    """Check player inventory."""
    print("\n🎒 Inventory:")

    if not player.inventory:
        print("   (Empty)")
        return

    for i, item in enumerate(player.inventory, 1):
        print(f"{i}. {item.name} - {item.description}")

    print(f"\n{len(player.inventory) + 1}. Back")

    choice = input("\nUse an item? ").strip()

    if choice.isdigit():
        choice_num = int(choice)

        if choice_num == len(player.inventory) + 1:
            return

        if 1 <= choice_num <= len(player.inventory):
            result = player.use_item(choice_num - 1)
            if result:
                print(f"\n{result}")
        else:
            print("\n❌ Invalid choice!")
    else:
        print("\n❌ Invalid input!")


def main():
    """Main game loop."""
    print_banner()

    # Character creation
    player = create_character()

    # Initialize game world
    world = GameWorld()

    # Give starting potion
    player.add_item(Potion())

    print("\n📜 Your adventure begins in the Peaceful Village...")
    print("Dark forces threaten the kingdom. Only you can save it!")

    # Main game loop
    while player.is_alive:
        show_main_menu()

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            # Explore and fight
            if not explore(player, world):
                print("\n💀 GAME OVER 💀")
                print(f"You reached level {player.level}.")
                print("Thanks for playing!")
                break

        elif choice == "2":
            # Travel
            travel(player, world)

        elif choice == "3":
            # Visit shop
            visit_shop(player, world)

        elif choice == "4":
            # Check inventory
            check_inventory(player)

        elif choice == "5":
            # View stats
            print(player.get_stats())

        elif choice == "6":
            # Rest
            world.rest(player)

        elif choice == "7":
            # Quit
            print("\n💾 Progress saved! (Not really, this is a demo)")
            print("Thanks for playing!")
            break

        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
        sys.exit(0)
