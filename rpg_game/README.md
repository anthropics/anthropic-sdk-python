# Epic RPG Adventure

A text-based role-playing game with character classes, combat, exploration, and story progression!

## Features

### Character Classes
- **Warrior**: High HP and defense, balanced attack
- **Mage**: Powerful magic attacks, low defense
- **Rogue**: High damage, moderate defense

### Game Systems
- **Turn-based combat** with attack and item usage
- **Experience and leveling** system with stat increases
- **Inventory system** with consumable and permanent stat boost items
- **Multiple locations** to explore, unlocked through story progression
- **Item shop** to purchase potions and upgrades
- **Random enemy encounters** that scale with your level
- **Boss battles** for epic confrontations
- **Story progression** that unfolds as you level up

### Locations
1. **Peaceful Village** - Your starting point
2. **Dark Forest** - Face goblins and skeletons
3. **Misty Mountains** - Battle orcs and dark knights
4. **Ancient Ruins** - Explore dangerous ruins
5. **Shadow Castle** - The final showdown with the Dark Lord!

### Items
- **Health Potion** - Restores 50 HP
- **Mega Potion** - Restores 100 HP
- **Elixir** - Fully restores HP
- **Attack Boost** - Permanently increases Attack by 5
- **Defense Boost** - Permanently increases Defense by 3
- **Max HP Boost** - Permanently increases Max HP by 20

### Enemies
- Goblins
- Orcs
- Skeletons
- Dark Knights
- Dragons

## How to Play

### Installation
No installation required! Just Python 3.6+ needed.

### Running the Game
```bash
python game.py
```

Or make it executable:
```bash
chmod +x game.py
./game.py
```

### Gameplay

1. **Create your character** - Choose a name and class
2. **Explore locations** - Fight enemies to gain experience and gold
3. **Level up** - Grow stronger with each level
4. **Buy items** - Visit shops to purchase helpful items
5. **Progress the story** - Unlock new locations as you level up
6. **Defeat the Dark Lord** - Complete your quest!

### Controls
The game uses a menu-driven interface. Simply enter the number of your choice:

- **Explore and Fight** - Battle random enemies in your current location
- **Travel** - Move to different unlocked locations
- **Visit Shop** - Buy items with your gold
- **Check Inventory** - View and use items
- **View Stats** - See your character's current statistics
- **Rest at Inn** - Restore HP for a cost
- **Save & Quit** - Exit the game

### Combat
During combat you can:
- **Attack** - Deal damage to the enemy
- **Use Item** - Consume items from your inventory
- **Run Away** - Attempt to flee (50% success rate)

### Tips
- Rest at the inn when your HP is low (costs 20 gold)
- Buy potions before exploring dangerous areas
- Stat boost items are expensive but permanent
- Enemy drops include free potions (30% chance)
- Level up strategically - each class has different growth rates
- Running away is sometimes the smart choice!

## Game Structure

```
rpg_game/
├── game.py          # Main game loop and menu
├── character.py     # Player and enemy classes
├── combat.py        # Combat system
├── items.py         # Item system
├── world.py         # World locations and shop
└── README.md        # This file
```

## Credits

Created as a demonstration RPG game showcasing:
- Object-oriented Python design
- Turn-based combat mechanics
- Progressive difficulty scaling
- Story-driven gameplay

Enjoy your adventure! 🗡️⚔️🐉
