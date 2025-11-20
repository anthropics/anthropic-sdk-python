"""Combat system for the RPG game."""
import random
from typing import Optional, Tuple
from character import Player, Enemy
from items import Potion


def display_combat_status(player: Player, enemy: Enemy):
    """Display the current combat status."""
    print("\n" + "="*50)
    print(f"🗡️  {player.name} (Lvl {player.level})")
    print(f"   HP: {'█' * int(player.hp / player.max_hp * 20)}{'░' * (20 - int(player.hp / player.max_hp * 20))} {player.hp}/{player.max_hp}")
    print()
    print(f"👹 {enemy.name} (Lvl {enemy.level})")
    print(f"   HP: {'█' * int(enemy.hp / enemy.max_hp * 20)}{'░' * (20 - int(enemy.hp / enemy.max_hp * 20))} {enemy.hp}/{enemy.max_hp}")
    print("="*50)


def combat(player: Player, enemy: Enemy) -> bool:
    """
    Run a combat encounter.
    Returns True if player wins, False if player loses.
    """
    print(f"\n⚔️  A wild {enemy.name} (Level {enemy.level}) appears!\n")

    while player.is_alive and enemy.is_alive:
        display_combat_status(player, enemy)

        print("\nWhat will you do?")
        print("1. Attack")
        print("2. Use Item")
        print("3. Run Away")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            # Player attacks
            damage = player.attack_target(enemy)
            print(f"\n💥 You attack {enemy.name} for {damage} damage!")

            if not enemy.is_alive:
                print(f"\n🎉 Victory! You defeated the {enemy.name}!")
                print(f"📈 Gained {enemy.exp_reward} EXP and {enemy.gold_reward} Gold!")

                player.gold += enemy.gold_reward
                leveled_up = player.gain_exp(enemy.exp_reward)

                if leveled_up:
                    print(f"\n⭐ LEVEL UP! You are now level {player.level}!")
                    print(f"   HP: {player.max_hp} | ATK: {player.attack} | DEF: {player.defense}")

                # Random item drop
                if random.random() < 0.3:  # 30% chance
                    dropped_item = Potion()
                    player.add_item(dropped_item)
                    print(f"💊 The {enemy.name} dropped a {dropped_item.name}!")

                return True

            # Enemy attacks
            enemy_damage = enemy.attack_target(player)
            print(f"👹 {enemy.name} attacks you for {enemy_damage} damage!")

            if not player.is_alive:
                print("\n💀 You have been defeated...")
                return False

        elif choice == "2":
            # Use item
            if not player.inventory:
                print("\n❌ You have no items!")
                continue

            print("\nInventory:")
            for i, item in enumerate(player.inventory):
                print(f"{i + 1}. {item.name}")
            print(f"{len(player.inventory) + 1}. Cancel")

            item_choice = input("\nSelect an item: ").strip()

            if item_choice.isdigit():
                item_index = int(item_choice) - 1

                if item_index == len(player.inventory):
                    continue

                if 0 <= item_index < len(player.inventory):
                    result = player.use_item(item_index)
                    if result:
                        print(f"\n{result}")

                        # Enemy still gets to attack
                        enemy_damage = enemy.attack_target(player)
                        print(f"👹 {enemy.name} attacks you for {enemy_damage} damage!")

                        if not player.is_alive:
                            print("\n💀 You have been defeated...")
                            return False
                else:
                    print("\n❌ Invalid item selection!")
            else:
                print("\n❌ Invalid input!")

        elif choice == "3":
            # Run away
            run_chance = random.random()
            if run_chance < 0.5:  # 50% chance to escape
                print("\n🏃 You successfully ran away!")
                return True
            else:
                print("\n❌ You couldn't escape!")
                # Enemy gets a free attack
                enemy_damage = enemy.attack_target(player)
                print(f"👹 {enemy.name} attacks you for {enemy_damage} damage!")

                if not player.is_alive:
                    print("\n💀 You have been defeated...")
                    return False

        else:
            print("\n❌ Invalid choice!")

    return player.is_alive


def boss_fight(player: Player, boss: Enemy) -> bool:
    """
    Special boss fight with more dramatic presentation.
    Returns True if player wins, False if player loses.
    """
    print("\n" + "="*50)
    print("⚡" * 25)
    print(f"    🐉 BOSS BATTLE: {boss.name} 🐉")
    print("⚡" * 25)
    print("="*50)

    return combat(player, boss)
