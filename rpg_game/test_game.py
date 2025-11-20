#!/usr/bin/env python3
"""Quick test to verify game components work correctly."""

from character import Player, create_enemy
from items import Potion, MegaPotion, AttackBoost
from world import GameWorld, LOCATIONS
from combat import display_combat_status


def test_character_creation():
    """Test character creation."""
    print("Testing character creation...")
    player = Player("TestHero", "Warrior")
    assert player.name == "TestHero"
    assert player.character_class == "Warrior"
    assert player.hp == 120
    assert player.is_alive
    print("✓ Character creation works!")


def test_items():
    """Test item system."""
    print("\nTesting item system...")
    player = Player("TestHero", "Warrior")
    player.hp = 50  # Damage the player

    potion = Potion()
    player.add_item(potion)
    assert len(player.inventory) == 1

    result = player.use_item(0)
    assert player.hp == 100  # Should heal 50 HP
    assert len(player.inventory) == 0
    print("✓ Item system works!")


def test_combat_setup():
    """Test combat setup."""
    print("\nTesting combat setup...")
    player = Player("TestHero", "Mage")
    enemy = create_enemy("Goblin", 1)

    assert enemy.name == "Goblin"
    assert enemy.level == 1
    assert enemy.is_alive
    print("✓ Combat setup works!")


def test_leveling():
    """Test leveling system."""
    print("\nTesting leveling system...")
    player = Player("TestHero", "Rogue")
    initial_level = player.level

    player.gain_exp(100)
    assert player.level == initial_level + 1
    print("✓ Leveling system works!")


def test_world():
    """Test world system."""
    print("\nTesting world system...")
    world = GameWorld()

    assert world.current_location == "village"
    assert "village" in world.locations_unlocked

    current_loc = world.get_current_location()
    assert current_loc.name == "Peaceful Village"
    print("✓ World system works!")


def test_stat_boosts():
    """Test permanent stat boost items."""
    print("\nTesting stat boost items...")
    player = Player("TestHero", "Warrior")
    initial_attack = player.attack

    boost = AttackBoost()
    player.add_item(boost)
    player.use_item(0)

    assert player.attack == initial_attack + 5
    print("✓ Stat boost items work!")


if __name__ == "__main__":
    print("="*50)
    print("Running RPG Game Tests")
    print("="*50)

    try:
        test_character_creation()
        test_items()
        test_combat_setup()
        test_leveling()
        test_world()
        test_stat_boosts()

        print("\n" + "="*50)
        print("✅ All tests passed!")
        print("="*50)
        print("\nThe game is ready to play!")
        print("Run: python game.py")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
