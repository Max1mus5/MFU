"""
Inventory Panel module - UI component for displaying inventory
"""

import pygame

class InventoryPanel:
    """UI panel for displaying and interacting with inventory"""
    
    def __init__(self, game, rect, config):
        """
        Initialize the inventory panel
        
        Args:
            game (Game): Reference to the main game object
            rect (pygame.Rect): Rectangle defining panel position and size
            config (Config): Game configuration
        """
        self.game = game
        self.resource_manager = game.resource_manager
        self.rect = rect
        self.config = config
        
        # Calculate slot positions
        self.slots = []
        slot_width = 80
        slot_height = 80
        slots_per_row = 2
        
        for i in range(self.config.INVENTORY_SIZE):
            row = i // slots_per_row
            col = i % slots_per_row
            
            x = self.rect.x + 20 + col * (slot_width + 10)
            y = self.rect.y + 60 + row * (slot_height + 30)
            
            self.slots.append(pygame.Rect(x, y, slot_width, slot_height))
    
    def update(self):
        """Update inventory panel"""
        pass
    
    def draw(self, surface):
        """
        Draw the inventory panel
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw panel background
        pygame.draw.rect(surface, (50, 45, 40), self.rect)
        pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, self.rect, 2)
        
        # Draw title
        font = self.config.FONT_MEDIUM
        title = font.render("INVENTARIO", True, self.config.TEXT_COLOR)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw inventory slots
        for i, slot_rect in enumerate(self.slots):
            # Draw slot background
            pygame.draw.rect(surface, (30, 25, 20), slot_rect)
            pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, slot_rect, 2)
            
            # Draw resource if slot is filled
            if i < len(self.resource_manager.inventory):
                resource = self.resource_manager.inventory[i]
                
                # Get resource color
                color = self.config.RESOURCE_TYPES[resource.type]["color"]
                
                # Draw resource icon
                resource_image = self.game.asset_loader.get_image(f"resource_{resource.type}")
                if resource_image:
                    # Center the image in the slot
                    image_x = slot_rect.x + (slot_rect.width - resource_image.get_width()) // 2
                    image_y = slot_rect.y + 10
                    surface.blit(resource_image, (image_x, image_y))
                else:
                    # Fallback to colored rectangle if image not available
                    pygame.draw.rect(surface, color, pygame.Rect(
                        slot_rect.x + 10,
                        slot_rect.y + 10,
                        slot_rect.width - 20,
                        slot_rect.height - 30
                    ))
                
                # Draw resource name
                name = self.config.RESOURCE_TYPES[resource.type]["name"]
                name_text = self.config.FONT_SMALL.render(name, True, self.config.TEXT_COLOR)
                surface.blit(name_text, (slot_rect.x + 5, slot_rect.y + slot_rect.height - 20))
                
                # Draw counter bar
                counter_width = int((slot_rect.width - 20) * (resource.counter / 255))
                
                # Calculate color based on counter value (green to red)
                if resource.counter < resource.TOXIC_THRESHOLD:
                    bar_color = self.config.COUNTER_LOW_COLOR
                else:
                    bar_color = self.config.COUNTER_HIGH_COLOR
                
                pygame.draw.rect(surface, bar_color, pygame.Rect(
                    slot_rect.x + 10,
                    slot_rect.y + slot_rect.height - 5,
                    counter_width,
                    3
                ))
    
    def handle_click(self, pos):
        """
        Handle mouse click on inventory
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            bool: Whether a slot was clicked
        """
        for i, slot_rect in enumerate(self.slots):
            if slot_rect.collidepoint(pos):
                # Slot was clicked
                if i < len(self.resource_manager.inventory):
                    # Resource exists in this slot
                    resource = self.resource_manager.inventory[i]
                    # Could implement selection or other interaction here
                return True
        
        return False