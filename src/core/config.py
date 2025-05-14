"""
Configuration module - Game settings and constants
"""

import pygame
import os

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
        
        # Asset paths
        self.ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        self.IMAGES_DIR = os.path.join(self.ASSETS_DIR, "images")
        
        # Character image
        self.CHARACTER_IMAGE = os.path.join(self.IMAGES_DIR, "main_character.png")
        
        # Resource images
        self.RESOURCE_IMAGES = {
            "nut": os.path.join(self.IMAGES_DIR, "elementos", "tuerca.png"),
            "circuit": os.path.join(self.IMAGES_DIR, "elementos", "circuito.png"),
            "cell": os.path.join(self.IMAGES_DIR, "elementos", "energia.png"),
            "core": os.path.join(self.IMAGES_DIR, "elementos", "element_radioactivo.png")
        }
        
        # Weapon images by state
        self.WEAPON_IMAGES = {
            "normal": {
                "pistol": os.path.join(self.IMAGES_DIR, "armas", "arma_pistola.png"),
                "shotgun": os.path.join(self.IMAGES_DIR, "armas", "arma_escopeta.png"),
                "rifle": os.path.join(self.IMAGES_DIR, "armas", "arma_rifle.png"),
                "laser": os.path.join(self.IMAGES_DIR, "armas", "arma_laser.png"),
                "cannon": os.path.join(self.IMAGES_DIR, "armas", "arma_cañon.png")
            },
            "oxidized": {
                "pistol": os.path.join(self.IMAGES_DIR, "armas_oxidadas", "arma_pistola.png"),
                "shotgun": os.path.join(self.IMAGES_DIR, "armas_oxidadas", "arma_escopeta.png"),
                "rifle": os.path.join(self.IMAGES_DIR, "armas_oxidadas", "arma_rifle.png"),
                "laser": os.path.join(self.IMAGES_DIR, "armas_oxidadas", "arma_laser.png"),
                "cannon": os.path.join(self.IMAGES_DIR, "armas_oxidadas", "arma_cañon.png")
            },
            "destroyed": {
                "pistol": os.path.join(self.IMAGES_DIR, "armas_destruidas", "arma_pistola.png"),
                "shotgun": os.path.join(self.IMAGES_DIR, "armas_destruidas", "arma_escopeta.png"),
                "rifle": os.path.join(self.IMAGES_DIR, "armas_destruidas", "arma_rifle.png"),
                "laser": os.path.join(self.IMAGES_DIR, "armas_destruidas", "arma_laser.png"),
                "cannon": os.path.join(self.IMAGES_DIR, "armas_destruidas", "arma_cañon.png")
            }
        }
        
        # UI images
        self.CLOCK_ICON = os.path.join(self.IMAGES_DIR, "reloj_icon.png")
        
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