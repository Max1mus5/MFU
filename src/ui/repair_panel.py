"""
Repair Panel module - UI component for weapon repair
"""

import pygame

class RepairPanel:
    """UI panel for displaying and repairing weapons"""
    
    def __init__(self, rect, config):
        """
        Initialize the repair panel
        
        Args:
            rect (pygame.Rect): Rectangle defining panel position and size
            config (Config): Game configuration
        """
        self.rect = rect
        self.config = config
        self.game = None  # Will be set when update is called
        
        # Calculate weapon positions
        self.weapon_rects = []
        weapon_height = 100
        
        for i in range(3):  # Support for 3 weapons
            y = self.rect.y + 60 + i * (weapon_height + 20)
            self.weapon_rects.append(pygame.Rect(
                self.rect.x + 20,
                y,
                self.rect.width - 40,
                weapon_height
            ))
        
        # Repair button
        self.repair_button_rect = pygame.Rect(
            self.rect.x + 50,
            self.rect.y + self.rect.height - 60,
            self.rect.width - 100,
            40
        )
    
    def update(self, weapons, selected_weapon, game=None):
        """
        Update repair panel
        
        Args:
            weapons (list): List of available weapons
            selected_weapon (Weapon): Currently selected weapon
            game (Game, optional): Reference to the main game object
        """
        self.weapons = weapons
        self.selected_weapon = selected_weapon
        if game:
            self.game = game
    
    def draw(self, surface):
        """
        Draw the repair panel
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw panel background
        pygame.draw.rect(surface, (60, 55, 50), self.rect)
        pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, self.rect, 2)
        
        # Draw title
        font = self.config.FONT_MEDIUM
        title = font.render("REPAIR STATION", True, self.config.TEXT_COLOR)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw weapons
        for i, weapon_rect in enumerate(self.weapon_rects):
            if i < len(self.weapons):
                weapon = self.weapons[i]
                
                # Highlight if selected
                if weapon == self.selected_weapon:
                    pygame.draw.rect(surface, (80, 70, 60), weapon_rect)
                else:
                    pygame.draw.rect(surface, (50, 45, 40), weapon_rect)
                
                pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, weapon_rect, 2)
                
                # Draw weapon image if available
                if self.game and self.game.asset_loader:
                    # Get image based on weapon state
                    weapon_image = self.game.asset_loader.get_image(f"weapon_{weapon.type}_{weapon.state}")
                    if weapon_image:
                        image_x = weapon_rect.x + 10
                        image_y = weapon_rect.y + 10
                        surface.blit(weapon_image, (image_x, image_y))
                
                # Draw weapon name
                name_text = self.config.FONT_MEDIUM.render(weapon.name, True, self.config.TEXT_COLOR)
                surface.blit(name_text, (weapon_rect.x + 100, weapon_rect.y + 10))
                
                # Draw requirements
                y_offset = 40
                for resource_type, amount in weapon.requirements.items():
                    req_text = self.config.FONT_SMALL.render(
                        f"{self.config.RESOURCE_TYPES[resource_type]['name']}: {amount}",
                        True,
                        self.config.RESOURCE_TYPES[resource_type]['color']
                    )
                    surface.blit(req_text, (weapon_rect.x + 150, weapon_rect.y + y_offset))
                    y_offset += 20
                
                # Draw repaired status if applicable
                if weapon.repaired:
                    status_text = self.config.FONT_SMALL.render("REPAIRED", True, (0, 200, 0))
                    surface.blit(status_text, (weapon_rect.x + weapon_rect.width - 100, weapon_rect.y + 10))
        
        # Draw repair button
        button_color = (100, 150, 100) if self.selected_weapon and not self.selected_weapon.repaired else (80, 80, 80)
        pygame.draw.rect(surface, button_color, self.repair_button_rect)
        pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, self.repair_button_rect, 2)
        
        button_text = self.config.FONT_MEDIUM.render("REPAIR", True, self.config.TEXT_COLOR)
        text_rect = button_text.get_rect(center=self.repair_button_rect.center)
        surface.blit(button_text, text_rect)
    
    def handle_click(self, pos):
        """
        Handle mouse click on repair panel
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            Weapon or None: The weapon that was clicked, if any
        """
        for i, weapon_rect in enumerate(self.weapon_rects):
            if weapon_rect.collidepoint(pos) and i < len(self.weapons):
                return self.weapons[i]
        
        return None