# Rust Overload

A post-apocalyptic workshop simulator game implementing the Most Frequently Used (MFU) algorithm for resource management.

## Game Concept

In the year 2147, after an environmental collapse, humanity survives in underground cities. You play as Jax, an engineer maintaining weapons for defense against bandits and mutants. Your workshop has limited inventory space, and you must collect resources in quick missions.

The key challenge: Materials oxidize if not used frequently (the air is full of acid!). To avoid wasting space, you must strategically discard the most frequently used resources that have degraded.

## Game Mechanics

### Resources and Usage Counters
- **Resource Types**:
  - 🟫 Rusty Nuts (basic, used in any weapon)
  - 🔵 Fragile Circuits (for electric weapons)
  - 🔋 Energy Cells (for lasers)
  - 💀 Radioactive Cores (for heavy weapons)

- **MFU with Aging**:
  - Each resource has an 8-bit counter (0-255) that increases when used
  - Every 15 seconds, counters are divided by 2 (simulating oxidation)
  - When inventory is full, the resource with the highest counter is replaced

### Gameplay Flow
1. **Collection Phase**: Travel to risk zones to collect resources
2. **Repair Phase**: Choose damaged weapons to repair using specific resource combinations
3. **Replacement Phase**: When inventory is full, MFU algorithm automatically removes the most used resource

## Project Structure

```
MFU/
├── assets/
│   ├── audio/       # Game sound effects and music
│   └── images/      # Game sprites and UI elements
├── src/
│   ├── core/        # Core game systems
│   │   ├── config.py            # Game settings and constants
│   │   ├── game.py              # Main game controller
│   │   ├── mfu_algorithm.py     # MFU replacement algorithm
│   │   ├── resource_manager.py  # Inventory and resource management
│   │   └── scene_manager.py     # Scene management system
│   ├── entities/    # Game entities
│   │   ├── resource.py          # Resource entity
│   │   └── weapon.py            # Weapon entity
│   ├── scenes/      # Game scenes
│   │   ├── base_scene.py        # Abstract base scene class
│   │   ├── collection_scene.py  # Resource collection gameplay
│   │   └── workshop_scene.py    # Workshop repair gameplay
│   ├── ui/          # User interface components
│   │   ├── inventory_panel.py   # Inventory display
│   │   ├── repair_panel.py      # Weapon repair interface
│   │   └── status_panel.py      # Game status and navigation
│   └── utils/       # Utility functions
│       └── asset_loader.py      # Asset loading utilities
└── main.py          # Game entry point
```

## Module Descriptions

### Core Modules

- **config.py**: Contains game settings, constants, and configuration values
- **game.py**: Main game controller that manages the game loop and scenes
- **mfu_algorithm.py**: Implements the Most Frequently Used replacement algorithm
- **resource_manager.py**: Manages the player's inventory and resource collection
- **scene_manager.py**: Handles different game scenes and transitions between them

### Entity Modules

- **resource.py**: Defines the Resource class for collectible items
- **weapon.py**: Defines the Weapon class for repairable weapons

### Scene Modules

- **base_scene.py**: Abstract base class for all game scenes
- **collection_scene.py**: Scene for collecting resources in the wasteland
- **workshop_scene.py**: Main gameplay scene in the workshop for repairing weapons

### UI Modules

- **inventory_panel.py**: UI component for displaying and interacting with inventory
- **repair_panel.py**: UI component for weapon repair interface
- **status_panel.py**: UI component for game status and navigation buttons

### Utility Modules

- **asset_loader.py**: Utility for loading and managing game assets (images, sounds, fonts)

## Game Objectives

- **Win Condition**: Repair 10 weapons to equip your faction and resist a final mutant attack
- **Lose Condition**: 
  - Health depleted (from toxic resource replacements)
  - Failure to repair enough weapons before the time limit

## Strategic Elements

- Don't overuse a single resource type (high counter = candidate for removal)
- Balance aging by using resources before they oxidize too much
- Prioritize rare resources like radioactive cores strategically

## Installation and Running

1. Ensure you have Python 3.6+ and Pygame installed
2. Clone this repository
3. Run `python main.py` to start the game

## Controls

- **Workshop Scene**:
  - Mouse: Select resources and weapons, click repair button
  - C key: Switch to collection scene

- **Collection Scene**:
  - Left/Right arrows: Move player
  - W key: Switch to workshop scene