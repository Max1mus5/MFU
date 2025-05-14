"""
Configuration module - Game settings and constants
"""

import pygame

class Config:
    """Configuration class for game settings"""
    
    def __init__(self):
        # Display settings
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # Colors
        self.BACKGROUND_COLOR = (40, 35, 30)  # Dark brown
        self.TEXT_COLOR = (220, 220, 220)  # Light gray
        self.COUNTER_LOW_COLOR = (50, 200, 50)  # Green
        self.COUNTER_HIGH_COLOR = (200, 50, 50)  # Red
        self.UI_BORDER_COLOR = (100, 90, 80)  # Medium brown
        
        # Game mechanics
        self.INVENTORY_SIZE = 6  # Number of inventory slots
        self.AGING_INTERVAL = 15000  # Milliseconds (15 seconds)
        self.COUNTER_INCREMENT = 8  # How much counter increases when used
        self.COUNTER_MAX = 255  # Maximum counter value (8-bit)
        self.TOXIC_THRESHOLD = 64  # Counter value above which removal is toxic
        
        # Player settings
        self.PLAYER_MAX_HEALTH = 5
        self.WEAPONS_TO_WIN = 10
        
        # Resource types
        self.RESOURCE_TYPES = {
            "nut": {"name": "Rusty Nut", "rarity": 1, "color": (139, 69, 19)},
            "circuit": {"name": "Fragile Circuit", "rarity": 2, "color": (30, 144, 255)},
            "cell": {"name": "Energy Cell", "rarity": 3, "color": (50, 205, 50)},
            "core": {"name": "Radioactive Core", "rarity": 4, "color": (148, 0, 211)}
        }
        
        # Weapon types and requirements
        self.WEAPONS = {
            "pistol": {
                "name": "Rusty Pistol",
                "requirements": {"nut": 2, "circuit": 1},
                "points": 1
            },
            "shotgun": {
                "name": "Scrap Shotgun",
                "requirements": {"nut": 3, "circuit": 2},
                "points": 2
            },
            "rifle": {
                "name": "Makeshift Rifle",
                "requirements": {"nut": 2, "circuit": 2, "cell": 1},
                "points": 3
            },
            "laser": {
                "name": "Laser Cutter",
                "requirements": {"circuit": 3, "cell": 2},
                "points": 4
            },
            "cannon": {
                "name": "Plasma Cannon",
                "requirements": {"nut": 2, "circuit": 2, "cell": 1, "core": 1},
                "points": 5
            }
        }
        
        # Fonts
        pygame.font.init()
        self.FONT_SMALL = pygame.font.Font(None, 24)
        self.FONT_MEDIUM = pygame.font.Font(None, 32)
        self.FONT_LARGE = pygame.font.Font(None, 48)