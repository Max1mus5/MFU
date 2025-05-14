"""
Status Panel module - UI component for game status
"""

import pygame

class StatusPanel:
    """UI panel for displaying game status and navigation buttons"""
    
    def __init__(self, game, rect, config):
        """
        Initialize the status panel
        
        Args:
            game (Game): Reference to the main game object
            rect (pygame.Rect): Rectangle defining panel position and size
            config (Config): Game configuration
        """
        self.game = game
        self.rect = rect
        self.config = config
        
        # Navigation buttons
        button_width = 120
        button_height = 30
        
        self.workshop_button_rect = pygame.Rect(
            self.rect.x + self.rect.width - 260,
            self.rect.y + 5,
            button_width,
            button_height
        )
        
        self.collection_button_rect = pygame.Rect(
            self.rect.x + self.rect.width - 130,
            self.rect.y + 5,
            button_width,
            button_height
        )
        
        # Aging timer display
        self.timer_rect = pygame.Rect(
            self.rect.x + 300,
            self.rect.y + 5,
            100,
            button_height
        )
    
    def update(self):
        """Update status panel"""
        pass
    
    def draw(self, surface):
        """
        Draw the status panel
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw panel background
        pygame.draw.rect(surface, (40, 35, 30), self.rect)
        pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, self.rect, 2)
        
        # Draw health
        health_text = self.config.FONT_SMALL.render(f"Health: ", True, self.config.TEXT_COLOR)
        surface.blit(health_text, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw health hearts
        for i in range(self.config.PLAYER_MAX_HEALTH):
            color = (200, 50, 50) if i < self.game.health else (100, 30, 30)
            pygame.draw.circle(surface, color, (self.rect.x + 80 + i * 20, self.rect.y + 20), 8)
        
        # Draw score
        score_text = self.config.FONT_SMALL.render(f"Score: {self.game.score}", True, self.config.TEXT_COLOR)
        surface.blit(score_text, (self.rect.x + 180, self.rect.y + 10))
        
        # Draw aging timer
        # Calculate time until next aging
        next_aging = (self.config.AGING_INTERVAL - pygame.time.get_ticks() % self.config.AGING_INTERVAL) // 1000
        
        # Draw clock icon if available
        clock_icon = self.game.asset_loader.get_image("clock_icon")
        if clock_icon:
            surface.blit(clock_icon, (self.rect.x + 300, self.rect.y + 10))
            timer_text = self.config.FONT_SMALL.render(f"{next_aging}s", True, self.config.TEXT_COLOR)
            surface.blit(timer_text, (self.rect.x + 325, self.rect.y + 10))
        else:
            timer_text = self.config.FONT_SMALL.render(f"Aging: {next_aging}s", True, self.config.TEXT_COLOR)
            surface.blit(timer_text, (self.rect.x + 300, self.rect.y + 10))
        
        # Draw navigation buttons
        pygame.draw.rect(surface, (60, 55, 50), self.workshop_button_rect)
        pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, self.workshop_button_rect, 2)
        workshop_text = self.config.FONT_SMALL.render("Workshop", True, self.config.TEXT_COLOR)
        workshop_text_rect = workshop_text.get_rect(center=self.workshop_button_rect.center)
        surface.blit(workshop_text, workshop_text_rect)
        
        pygame.draw.rect(surface, (60, 55, 50), self.collection_button_rect)
        pygame.draw.rect(surface, self.config.UI_BORDER_COLOR, self.collection_button_rect, 2)
        collection_text = self.config.FONT_SMALL.render("Collection", True, self.config.TEXT_COLOR)
        collection_text_rect = collection_text.get_rect(center=self.collection_button_rect.center)
        surface.blit(collection_text, collection_text_rect)