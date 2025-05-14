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
        pygame.display.set_caption("Sobrecarga de Óxido")
        
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
        
        # Celebration animation state
        self.celebrating = False
        self.celebration_frame = 1
        self.celebration_timer = 0
        self.celebration_interval = 200  # milliseconds between frames
    
    def load_assets(self):
        """Load all game assets"""
        # Load character image
        self.asset_loader.load_image("character", self.config.CHARACTER_IMAGE, (80, 120))
        
        # Load celebration images
        for i in range(1, 6):
            self.asset_loader.load_image(f"celebration_{i}", 
                                        f"{self.config.IMAGES_DIR}/Character/celebracion_{i}.png", 
                                        (80, 120))
        
        # Load resource images
        for resource_type, path in self.config.RESOURCE_IMAGES.items():
            self.asset_loader.load_image(f"resource_{resource_type}", path, (40, 40))
        
        # Load weapon images for all states
        for state, weapons in self.config.WEAPON_IMAGES.items():
            for weapon_type, path in weapons.items():
                self.asset_loader.load_image(f"weapon_{weapon_type}_{state}", path, (80, 60))
        
        # Load UI images
        self.asset_loader.load_image("clock_icon", self.config.CLOCK_ICON, (20, 20))
        
        # Load sounds
        self.asset_loader.load_sound("point", f"{self.config.ASSETS_DIR}/audio/point.mp3")
        self.asset_loader.load_sound("obtain_element_1", f"{self.config.ASSETS_DIR}/audio/obtener_elemento.mp3")
        self.asset_loader.load_sound("obtain_element_2", f"{self.config.ASSETS_DIR}/audio/obtener_elemento_2.mp3")
        self.asset_loader.load_sound("lose_point", f"{self.config.ASSETS_DIR}/audio/lose_point.mp3")
        
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
            
            # Update celebration animation if active
            if self.celebrating:
                self.celebration_timer += self.clock.get_time()
                if self.celebration_timer >= self.celebration_interval:
                    self.celebration_frame += 1
                    self.celebration_timer = 0
                    
                    # End celebration after showing all frames
                    if self.celebration_frame > 5:
                        self.celebrating = False
                        self.celebration_frame = 1
            
            # Draw
            self.screen.fill(self.config.BACKGROUND_COLOR)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.config.FPS)
    
    def apply_aging(self):
        """Apply aging to all resources and weapons"""
        # Apply aging to resources
        self.resource_manager.apply_aging()
        
        # Apply aging to weapons in workshop scene
        workshop_scene = self.scene_manager.scenes.get("workshop")
        if workshop_scene:
            # Track if any weapon was destroyed this round
            weapon_destroyed_this_round = False
            
            for weapon in workshop_scene.available_weapons:
                # Update weapon state and check if it was destroyed
                if weapon.update_state(self.config.AGING_INTERVAL):
                    if not weapon_destroyed_this_round:
                        # Only lose health once per round for destroyed weapons
                        self.health -= 1
                        weapon_destroyed_this_round = True
                        # Play lose point sound
                        self.play_lose_point_sound()
    
    def check_game_over(self):
        """Check if game is over (player health <= 0)"""
        if self.health <= 0:
            self.game_over("¡Has muerto por exposición tóxica!")
        
    def check_win_condition(self):
        """Check if player has won (repaired enough weapons)"""
        # If WEAPONS_TO_WIN is 0, we're in infinite mode
        if self.config.WEAPONS_TO_WIN > 0 and self.weapons_repaired >= self.config.WEAPONS_TO_WIN:
            self.game_over("¡Has equipado exitosamente a tu facción! ¡Victoria!")
    
    def start_celebration(self):
        """Start the celebration animation and play sound when points are gained"""
        self.celebrating = True
        self.celebration_frame = 1
        self.celebration_timer = 0
        
        # Play the point sound
        point_sound = self.asset_loader.get_sound("point")
        if point_sound:
            point_sound.play()
    
    def play_obtain_element_sound(self):
        """Play a random sound when an element is obtained"""
        import random
        sound_name = random.choice(["obtain_element_1", "obtain_element_2"])
        sound = self.asset_loader.get_sound(sound_name)
        if sound:
            sound.play()
    
    def play_lose_point_sound(self):
        """Play sound when a life is lost"""
        sound = self.asset_loader.get_sound("lose_point")
        if sound:
            sound.play()
    
    def game_over(self, message):
        """Handle game over state"""
        # Create game over screen
        self.screen.fill((0, 0, 0))
        
        # Draw game over message
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        
        # Game over title
        title_text = font_large.render("FIN DEL JUEGO", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        # Result message
        message_text = font_medium.render(message, True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 280))
        self.screen.blit(message_text, message_rect)
        
        # Score
        score_text = font_medium.render(f"Puntuación Final: {self.score}", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 340))
        self.screen.blit(score_text, score_rect)
        
        # Weapons repaired
        weapons_text = font_medium.render(f"Armas Reparadas: {self.weapons_repaired}", True, (200, 200, 200))
        weapons_rect = weapons_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 380))
        self.screen.blit(weapons_text, weapons_rect)
        
        # Exit instructions
        exit_text = font_medium.render("Presiona ESC para salir", True, (150, 150, 150))
        exit_rect = exit_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 450))
        self.screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        
        # Wait for ESC key to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
            
            self.clock.tick(30)
        
        self.running = False