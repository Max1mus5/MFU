"""
Workshop Scene module - Main gameplay scene in the workshop
"""

import pygame
from src.scenes.base_scene import Scene
from src.entities.weapon import Weapon
from src.ui.inventory_panel import InventoryPanel
from src.ui.repair_panel import RepairPanel
from src.ui.status_panel import StatusPanel

class WorkshopScene(Scene):
    """Workshop scene where player repairs weapons"""
    
    def __init__(self, game):
        """Initialize the workshop scene"""
        super().__init__(game)
        self.config = game.config
        
        # Create UI panels
        self.inventory_panel = InventoryPanel(
            game,
            pygame.Rect(50, 100, 300, 500),
            self.config
        )
        
        self.repair_panel = RepairPanel(
            pygame.Rect(400, 100, 350, 500),
            self.config
        )
        
        self.status_panel = StatusPanel(
            game,
            pygame.Rect(50, 50, 700, 40),
            self.config
        )
        
        # Available weapons to repair
        self.available_weapons = [
            Weapon("pistol", self.config),
            Weapon("shotgun", self.config),
            Weapon("rifle", self.config)
        ]
        
        # Currently selected weapon
        self.selected_weapon = None
    
    def on_enter(self):
        """Called when scene becomes active"""
        # Load any necessary resources
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle inventory clicks
            self.inventory_panel.handle_click(event.pos)
            
            # Handle repair panel clicks
            weapon_clicked = self.repair_panel.handle_click(event.pos)
            if weapon_clicked is not None:
                self.selected_weapon = weapon_clicked
            
            # Handle repair button click
            if self.repair_panel.repair_button_rect.collidepoint(event.pos):
                self.try_repair_weapon()
            
            # Handle collection button click
            if self.status_panel.collection_button_rect.collidepoint(event.pos):
                self.game.scene_manager.set_active_scene("collection")
        
        # Handle keyboard shortcuts
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                # Shortcut to collection scene
                self.game.scene_manager.set_active_scene("collection")
    
    def update(self):
        """Update scene logic"""
        # Update UI panels
        self.inventory_panel.update()
        self.repair_panel.update(self.available_weapons, self.selected_weapon, self.game)
        self.status_panel.update()
        
        # Check game over conditions
        self.game.check_game_over()
        self.game.check_win_condition()
    
    def draw(self, surface):
        """Draw scene elements"""
        # Draw background
        self.draw_background(surface)
        
        # Draw UI panels
        self.inventory_panel.draw(surface)
        self.repair_panel.draw(surface)
        self.status_panel.draw(surface)
    
    def draw_background(self, surface):
        """Draw the workshop background"""
        # Draw workshop elements (shelves, workbench, etc.)
        pygame.draw.rect(surface, (60, 50, 40), pygame.Rect(30, 80, 740, 540))
        pygame.draw.rect(surface, (70, 60, 50), pygame.Rect(400, 100, 350, 500))
        
        # Draw character on the right side of the workshop
        character_image = self.game.asset_loader.get_image("character")
        if character_image:
            surface.blit(character_image, (780, 300))
    
    def try_repair_weapon(self):
        """Attempt to repair the selected weapon"""
        if self.selected_weapon and not self.selected_weapon.repaired:
            if self.selected_weapon.repair(self.game.resource_manager):
                # Weapon repaired successfully
                self.game.weapons_repaired += 1
                self.game.score += self.selected_weapon.points
                
                # Replace with a new weapon of random type
                weapon_types = list(self.config.WEAPONS.keys())
                import random
                new_type = random.choice(weapon_types)
                
                # Find and replace the repaired weapon
                for i, weapon in enumerate(self.available_weapons):
                    if weapon == self.selected_weapon:
                        self.available_weapons[i] = Weapon(new_type, self.config)
                        break
                
                # Deselect the weapon
                self.selected_weapon = None