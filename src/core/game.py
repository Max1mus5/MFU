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
        
        # Audio state
        self.audio_enabled = True
        
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
        
        # Load background image
        self.asset_loader.load_image("background", f"{self.config.ASSETS_DIR}/images/backGround.png", (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        
        # Load game over and victory images
        self.asset_loader.load_image("gameover", f"{self.config.ASSETS_DIR}/images/gameover.png", (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.asset_loader.load_image("gamewin", f"{self.config.ASSETS_DIR}/images/gamewin.png", (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        
        # Load sounds
        self.asset_loader.load_sound("point", f"{self.config.ASSETS_DIR}/audio/point.mp3")
        self.asset_loader.load_sound("obtain_element_1", f"{self.config.ASSETS_DIR}/audio/obtener_elemento.mp3")
        self.asset_loader.load_sound("obtain_element_2", f"{self.config.ASSETS_DIR}/audio/obtener_elemento_2.mp3")
        self.asset_loader.load_sound("lose_point", f"{self.config.ASSETS_DIR}/audio/lose_point.mp3")
        
        # Load background music
        self.asset_loader.load_sound("workshop_music", f"{self.config.ASSETS_DIR}/audio/reparar.mp3")
        self.asset_loader.load_sound("collection_music", f"{self.config.ASSETS_DIR}/audio/recolectar.mp3")
        
        # Music state
        self.current_music = None
        self.music_volume = 0.0
        self.target_volume = 0.7  # Maximum target volume
        self.volume_step = 0.01   # Gradual volume increment
        
    # El método run se ha eliminado ya que ahora el bucle principal está en main.py
    # La lógica de actualización de la celebración se maneja directamente en main.py
    
    def apply_aging(self):
        """Apply aging to all resources and weapons"""
        print("Applying aging to resources and weapons...")
        
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
                        print(f"Weapon destroyed! Health reduced to {self.health}")
                        # Play lose point sound
                        self.play_lose_point_sound()
        
        print("Aging process completed")
    
    def check_game_over(self):
        """Check if game is over (player health <= 0)"""
        if self.health <= 0:
            self.game_over("¡Has muerto por exposición tóxica!")
        
    def check_win_condition(self):
        """Check if player has won (repaired enough weapons)"""
        # If WEAPONS_TO_WIN is 0, we're in infinite mode
        if self.config.WEAPONS_TO_WIN > 0 and self.weapons_repaired >= self.config.WEAPONS_TO_WIN:
            self.game_over("¡Has equipado exitosamente a tu facción! ¡Victoria!")
    
    def play_lose_point_sound(self):
        """Play sound when a life is lost"""
        if not self.audio_enabled:
            return
            
        sound = self.asset_loader.get_sound("lose_point")
        if sound:
            sound.play()
            print("Playing lose point sound")
            
    def play_background_music(self, scene_name):
        """Play background music for the current scene with gradual volume increase"""
        if not self.audio_enabled:
            print(f"Audio disabled, not playing music for {scene_name}")
            return
            
        # Determine which music to play based on the scene
        music_name = None
        if scene_name == "workshop":
            music_name = "workshop_music"
        elif scene_name == "collection":
            music_name = "collection_music"
        
        # If no valid scene or already playing the correct music, do nothing
        if not music_name:
            print(f"No music defined for scene: {scene_name}")
            return
        elif self.current_music and self.current_music == music_name:
            print(f"Already playing {music_name}, no change needed")
            return
            
        print(f"Changing music to {music_name} for scene {scene_name}")
        
        # Stop any currently playing music
        pygame.mixer.stop()
        
        # Get the new music and start playing it
        music = self.asset_loader.get_sound(music_name)
        if music:
            # Set initial volume to 0
            music.set_volume(0)
            # Play on loop (-1 means infinite loop)
            music.play(loops=-1)
            # Store current music and reset volume
            self.current_music = music_name
            self.music_volume = 0.0
            print(f"Started playing {music_name} with initial volume 0.0")
        else:
            print(f"Failed to load music: {music_name}")
            
    def update_music_volume(self, dt):
        """Gradually increase music volume"""
        if not self.audio_enabled or not self.current_music:
            return
            
        # Increase volume gradually
        if self.music_volume < self.target_volume:
            # Increase by 0.001 per millisecond, up to target volume
            old_volume = self.music_volume
            self.music_volume = min(self.music_volume + 0.0001 * dt, self.target_volume)
            music = self.asset_loader.get_sound(self.current_music)
            if music:
                music.set_volume(self.music_volume)
                # Only print when volume changes significantly to avoid console spam
                if int(old_volume * 100) != int(self.music_volume * 100) and int(self.music_volume * 100) % 10 == 0:
                    print(f"Music volume updated to {self.music_volume:.2f}")
                
    def play_point_sound(self):
        """Play sound when player gains points"""
        if self.audio_enabled:
            sound = self.asset_loader.get_sound("point")
            if sound:
                sound.play()
                print("Playing point sound")
                
    def play_obtain_element_sound(self):
        """Play a random sound when player obtains an element"""
        if self.audio_enabled:
            # Randomly choose between the two sounds
            import random
            sound_name = random.choice(["obtain_element_1", "obtain_element_2"])
            sound = self.asset_loader.get_sound(sound_name)
            if sound:
                sound.play()
                print(f"Playing obtain element sound: {sound_name}")
                
    def start_celebration(self):
        """Start the character celebration animation and play sound"""
        self.celebrating = True
        self.celebration_frame = 1
        self.celebration_timer = pygame.time.get_ticks()
        print("Starting celebration animation")
        
        # Play point sound
        self.play_point_sound()
    
    def game_over(self, message):
        """Handle game over state"""
        print(f"Game over: {message}")
        print(f"Final score: {self.score}, Weapons repaired: {self.weapons_repaired}")
        
        # Determine which image to use based on the message
        if "Victoria" in message:
            # Victory condition
            background_image = self.asset_loader.get_image("gamewin")
            print("Showing victory screen")
        else:
            # Game over condition
            background_image = self.asset_loader.get_image("gameover")
            print("Showing game over screen")
        
        # Display the background image
        if background_image:
            self.screen.blit(background_image, (0, 0))
        else:
            # Fallback to black background if image not found
            self.screen.fill((0, 0, 0))
            print("Warning: Game over background image not found, using black background")
        
        # Create font for score display
        font_medium = pygame.font.Font(None, 36)
        
        # Score in bottom right corner with white text
        score_text = font_medium.render(f"Puntuación: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.bottomright = (self.config.SCREEN_WIDTH - 20, self.config.SCREEN_HEIGHT - 20)
        self.screen.blit(score_text, score_rect)
        
        # Weapons repaired (slightly above score)
        weapons_text = font_medium.render(f"Armas Reparadas: {self.weapons_repaired}", True, (255, 255, 255))
        weapons_rect = weapons_text.get_rect()
        weapons_rect.bottomright = (self.config.SCREEN_WIDTH - 20, score_rect.top - 10)
        self.screen.blit(weapons_text, weapons_rect)
        
        # Exit instructions at the bottom
        exit_text = font_medium.render("Presiona ESC para salir", True, (255, 255, 255))
        exit_rect = exit_text.get_rect()
        exit_rect.midbottom = (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 20)
        self.screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        
        print("Waiting for ESC key to exit...")
        
        # Wait for ESC key to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event received")
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("ESC key pressed, exiting game")
                        waiting = False
            
            self.clock.tick(30)
        
        self.running = False
        print("Game terminated")