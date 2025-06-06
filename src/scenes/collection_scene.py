"""
Collection Scene module - Scene for collecting resources
"""

import pygame
import random
from src.scenes.base_scene import Scene
from src.entities.resource import Resource
from src.ui.status_panel import StatusPanel

class CollectionScene(Scene):
    """Scene where player collects resources from the wasteland"""
    
    def __init__(self, game):
        """Initialize the collection scene"""
        super().__init__(game)
        self.config = game.config
        
        # Status panel (shared with workshop scene)
        self.status_panel = StatusPanel(
            game,
            pygame.Rect(50, 50, 700, 40),
            self.config
        )
        
        # Resource spawning
        self.resources = []
        self.spawn_timer = 0
        self.spawn_interval = 1000  # ms
        
        # Player character
        self.player_x = self.config.SCREEN_WIDTH // 2
        self.player_y = self.config.SCREEN_HEIGHT - 100
        self.player_speed = 5
        self.player_rect = pygame.Rect(self.player_x, self.player_y, 40, 60)
        
        # Movement flags
        self.moving_left = False
        self.moving_right = False
        self.facing_left = False  # Track which direction the player is facing
    
    def on_enter(self):
        """Called when scene becomes active"""
        # Reset resources
        self.resources = []
        self.spawn_timer = 0
        
        # Start playing collection background music
        self.game.play_background_music("collection")
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
            elif event.key == pygame.K_w:
                # Shortcut to workshop scene
                self.game.scene_manager.set_active_scene("workshop")
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle workshop button click
            if self.status_panel.workshop_button_rect.collidepoint(event.pos):
                self.game.scene_manager.set_active_scene("workshop")
    
    def update(self):
        """Update scene logic"""
        # Update player movement
        if self.moving_left:
            self.player_x = max(50, self.player_x - self.player_speed)
            self.facing_left = True
        if self.moving_right:
            self.player_x = min(self.config.SCREEN_WIDTH - 90, self.player_x + self.player_speed)
            self.facing_left = False
        
        self.player_rect.x = self.player_x
        
        # Spawn resources
        self.spawn_timer += self.game.clock.get_time()
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_resource()
            self.spawn_timer = 0
        
        # Update resources
        for resource in self.resources[:]:
            resource["y"] += 3  # Fall speed
            
            # Check if player collected the resource
            resource_rect = pygame.Rect(resource["x"], resource["y"], 30, 30)
            if resource_rect.colliderect(self.player_rect):
                # Add to inventory
                success, replaced, damage = self.game.resource_manager.add_resource(resource["type"])
                
                # Play sound when obtaining an element
                self.game.play_obtain_element_sound()
                
                # Apply damage if toxic replacement
                if damage > 0:
                    self.game.health -= damage
                    # Play lose point sound
                    self.game.play_lose_point_sound()
                
                # Apply additional damage if collecting radioactive core
                if resource["type"] == "core":
                    self.game.health -= 1
                    # Play lose point sound
                    self.game.play_lose_point_sound()
                
                # Remove from scene
                self.resources.remove(resource)
            
            # Remove if off-screen
            elif resource["y"] > self.config.SCREEN_HEIGHT:
                self.resources.remove(resource)
        
        # Update status panel
        self.status_panel.update()
        
        # Check game over conditions
        self.game.check_game_over()
    
    def draw(self, surface):
        """Draw scene elements"""
        # Draw wasteland background
        self.draw_background(surface)
        
        # Draw resources
        for resource in self.resources:
            resource_image = self.game.asset_loader.get_image(f"resource_{resource['type']}")
            if resource_image:
                surface.blit(resource_image, (resource["x"], resource["y"]))
            else:
                # Fallback to colored rectangle if image not available
                color = self.config.RESOURCE_TYPES[resource["type"]]["color"]
                pygame.draw.rect(surface, color, pygame.Rect(resource["x"], resource["y"], 30, 30))
        
        # Draw player character
        character_image = self.game.asset_loader.get_image("character")
        if character_image:
            if self.facing_left:
                # Flip the image horizontally when facing left
                flipped_image = pygame.transform.flip(character_image, True, False)
                surface.blit(flipped_image, (self.player_rect.x - 20, self.player_rect.y - 30))
            else:
                surface.blit(character_image, (self.player_rect.x - 20, self.player_rect.y - 30))
        else:
            # Fallback to rectangle if image not available
            pygame.draw.rect(surface, (200, 200, 200), self.player_rect)
        
        # Draw status panel
        self.status_panel.draw(surface)
        
        # Draw instructions
        font = self.config.FONT_SMALL
        text = font.render("Usa las flechas IZQUIERDA/DERECHA para moverte. Recoge los recursos que caen.", True, self.config.TEXT_COLOR)
        surface.blit(text, (50, self.config.SCREEN_HEIGHT - 50))
    
    def draw_background(self, surface):
        """Draw the wasteland background"""
        # Draw background image
        background_image = self.game.asset_loader.get_image("background")
        if background_image:
            surface.blit(background_image, (0, 0))
        else:
            # Fallback to original colored rectangles if image not available
            # Draw sky
            pygame.draw.rect(surface, (80, 60, 80), pygame.Rect(0, 0, self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            
            # Draw ground
            pygame.draw.rect(surface, (100, 80, 60), pygame.Rect(0, self.config.SCREEN_HEIGHT - 50, self.config.SCREEN_WIDTH, 50))
    
    def spawn_resource(self):
        """Spawn a random resource"""
        # Determine resource type based on rarity
        roll = random.random()
        
        if roll < 0.5:  # 50% chance
            resource_type = "nut"
        elif roll < 0.8:  # 30% chance
            resource_type = "circuit"
        elif roll < 0.95:  # 15% chance
            resource_type = "cell"
        else:  # 5% chance
            resource_type = "core"
        
        # Random x position
        x = random.randint(50, self.config.SCREEN_WIDTH - 80)
        
        # Add to resources list
        self.resources.append({
            "type": resource_type,
            "x": x,
            "y": 0
        })