"""
Asset Loader module - Utility for loading and managing game assets
"""

import os
import pygame

class AssetLoader:
    """Utility class for loading and managing game assets"""
    
    def __init__(self):
        """Initialize the asset loader"""
        self.images = {}
        self.sounds = {}
        self.fonts = {}
    
    def load_image(self, name, path, scale=None):
        """
        Load an image asset
        
        Args:
            name (str): Reference name for the image
            path (str): File path to the image
            scale (tuple, optional): Width and height to scale the image to
            
        Returns:
            bool: Whether the image was successfully loaded
        """
        try:
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                
                if scale:
                    image = pygame.transform.scale(image, scale)
                
                self.images[name] = image
                return True
            else:
                print(f"Image file not found: {path}")
                return False
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return False
    
    def load_sound(self, name, path):
        """
        Load a sound asset
        
        Args:
            name (str): Reference name for the sound
            path (str): File path to the sound
            
        Returns:
            bool: Whether the sound was successfully loaded
        """
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                self.sounds[name] = sound
                return True
            else:
                print(f"Sound file not found: {path}")
                return False
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return False
    
    def load_font(self, name, path, size):
        """
        Load a font asset
        
        Args:
            name (str): Reference name for the font
            path (str): File path to the font
            size (int): Font size
            
        Returns:
            bool: Whether the font was successfully loaded
        """
        try:
            if os.path.exists(path):
                font = pygame.font.Font(path, size)
                self.fonts[name] = font
                return True
            else:
                # Fall back to system font
                font = pygame.font.SysFont(name, size)
                self.fonts[name] = font
                return True
        except pygame.error as e:
            print(f"Error loading font {path}: {e}")
            return False
    
    def get_image(self, name):
        """
        Get a loaded image by name
        
        Args:
            name (str): Name of the image to get
            
        Returns:
            pygame.Surface: The requested image, or None if not found
        """
        return self.images.get(name)
    
    def get_sound(self, name):
        """
        Get a loaded sound by name
        
        Args:
            name (str): Name of the sound to get
            
        Returns:
            pygame.mixer.Sound: The requested sound, or None if not found
        """
        return self.sounds.get(name)
    
    def get_font(self, name):
        """
        Get a loaded font by name
        
        Args:
            name (str): Name of the font to get
            
        Returns:
            pygame.font.Font: The requested font, or None if not found
        """
        return self.fonts.get(name)