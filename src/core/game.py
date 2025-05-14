"""
Game module - Main game controller
"""

import pygame
import sys
from src.core.config import Config
from src.core.resource_manager import ResourceManager
from src.core.scene_manager import SceneManager
from src.core.mfu_algorithm import MFUAlgorithm
from src.scenes.workshop_scene import WorkshopScene
from src.scenes.collection_scene import CollectionScene
from src.utils.asset_loader import AssetLoader

class Game:
    """Main game class that manages the game loop and scenes"""
    
    def __init__(self):
        """Initialize the game"""
        self.config = Config()
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Rust Overload")
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        
        # Initialize asset loader
        self.asset_loader = AssetLoader()
        self.load_assets()
        
        # Initialize resource manager
        self.resource_manager = ResourceManager()
        
        # Initialize MFU algorithm
        self.mfu_algorithm = MFUAlgorithm()
        
        # Initialize scene manager and scenes
        self.scene_manager = SceneManager()
        self.scene_manager.add_scene("workshop", WorkshopScene(self))
        self.scene_manager.add_scene("collection", CollectionScene(self))
        self.scene_manager.set_active_scene("workshop")
        
        # Set up aging timer (15 seconds)
        self.aging_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.aging_event, self.config.AGING_INTERVAL)
        
        # Game state
        self.running = True
        self.score = 0
        self.health = self.config.PLAYER_MAX_HEALTH
        self.weapons_repaired = 0
    
    def load_assets(self):
        """Load all game assets"""
        # Load character image
        self.asset_loader.load_image("character", self.config.CHARACTER_IMAGE, (80, 120))
        
        # Load resource images
        for resource_type, path in self.config.RESOURCE_IMAGES.items():
            self.asset_loader.load_image(f"resource_{resource_type}", path, (40, 40))
        
        # Load weapon images
        for weapon_type, path in self.config.WEAPON_IMAGES.items():
            self.asset_loader.load_image(f"weapon_{weapon_type}", path, (80, 60))
        
        # Load UI images
        self.asset_loader.load_image("clock_icon", self.config.CLOCK_ICON, (20, 20))
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == self.aging_event:
                    self.apply_aging()
                else:
                    self.scene_manager.handle_event(event)
            
            # Update
            self.scene_manager.update()
            
            # Draw
            self.screen.fill(self.config.BACKGROUND_COLOR)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.config.FPS)
    
    def apply_aging(self):
        """Apply aging to all resources (divide counters by 2)"""
        self.resource_manager.apply_aging()
    
    def check_game_over(self):
        """Check if game is over (player health <= 0)"""
        if self.health <= 0:
            self.game_over("You died from toxic exposure!")
        
    def check_win_condition(self):
        """Check if player has won (repaired enough weapons)"""
        if self.weapons_repaired >= self.config.WEAPONS_TO_WIN:
            self.game_over("You've successfully equipped your faction! Victory!")
    
    def game_over(self, message):
        """Handle game over state"""
        print(message)  # Replace with proper game over screen
        self.running = False