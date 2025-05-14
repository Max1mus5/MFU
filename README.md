# Rust Overload

A post-apocalyptic workshop simulator that implements the Most Frequently Used (MFU) algorithm for resource management.

## Game Concept

In the year 2147, after an environmental collapse, humanity survives in underground cities. You play as Jax, an engineer who maintains weapons for defense against bandits and mutants. Your workshop has limited inventory space, and you must collect resources in quick missions.

The main challenge: Materials rust if not used frequently (the air is full of acid!). To avoid wasting space, you must strategically discard the most frequently used resources that have degraded.

## Game Mechanics

### Resources and Usage Counters
- **Resource Types**:
  - 🟫 Rusty Nuts (basic, used in any weapon)
  - 🔵 Fragile Circuits (for electrical weapons)
  - 🔋 Energy Cells (for lasers)
  - 💀 Radioactive Cores (for heavy weapons)

- **MFU with Aging**:
  - Each resource has an 8-bit counter (0-255) that increases when used
  - Every 15 seconds, counters are divided by 2 (simulating oxidation)
  - When inventory is full, the resource with the highest counter is replaced

### Game Flow
1. **Collection Phase**: Travel to risk zones to collect resources
2. **Repair Phase**: Choose damaged weapons to repair using specific resource combinations
3. **Replacement Phase**: When inventory is full, the MFU algorithm automatically removes the most used resource

## Project Structure

```
MFU/
├── assets/                # Game assets (images, audio)
│   ├── audio/            # Sound effects and music
│   └── images/           # Game graphics
├── src/                  # Source code
│   ├── core/             # Core game systems
│   │   ├── asset_loader.py       # Asset loading utilities
│   │   ├── config.py             # Game configuration
│   │   ├── game.py               # Main game class
│   │   ├── resource_manager.py   # MFU resource management
│   │   └── scene_manager.py      # Scene management
│   ├── entities/         # Game entities
│   │   ├── resource.py           # Resource class
│   │   └── weapon.py             # Weapon class
│   └── scenes/           # Game scenes
│       ├── collection_scene.py   # Resource collection gameplay
│       └── workshop_scene.py     # Weapon repair gameplay
└── main.py               # Entry point
```

## Code Highlights

### MFU Algorithm Implementation

The MFU algorithm is implemented in the `ResourceManager` class:

- When a resource is used, its usage counter is incremented
- Periodically, all counters are aged (divided by 2)
- When inventory is full, the resource with the highest counter is replaced

### Scene Management

The game uses a scene-based architecture:

- `CollectionScene`: Where the player collects resources
- `WorkshopScene`: Where the player repairs weapons

### Resource Aging

Resources age over time, simulating oxidation in the toxic atmosphere:

- Every 15 seconds, all resource counters are divided by 2
- This creates a dynamic where frequently used resources are prioritized
- Players must strategically manage which resources to keep

## Controls

- **Arrow Keys**: Navigate menus and move in collection scene
- **Space/Enter**: Select options and collect resources
- **Tab**: Switch between workshop and collection scenes
- **ESC**: Exit game

## Installation and Running

1. Ensure Python 3.8+ and Pygame are installed
2. Clone the repository
3. Run `python main.py`

## Future Enhancements

- Additional weapon types with unique repair requirements
- More complex resource collection missions
- Difficulty levels affecting resource oxidation rates
- Upgrades for workshop capacity