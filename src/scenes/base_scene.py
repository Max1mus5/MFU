"""
Base Scene module - Abstract base class for all game scenes
"""

import pygame

class Scene:
    """Abstract base class for all game scenes"""
    
    def __init__(self, game):
        """
        Initialize the scene
        
        Args:
            game (Game): Reference to the main game object
        """
        self.game = game
    
    def on_enter(self):
        """Called when scene becomes active"""
        pass
    
    def on_exit(self):
        """Called when scene is no longer active"""
        pass
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event to handle
        """
        pass
    
    def update(self):
        """Update scene logic"""
        pass
    
    def draw(self, surface):
        """
        Draw scene elements
        
        Args:
            surface: Pygame surface to draw on
        """
        pass