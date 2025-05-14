#!/usr/bin/env python3
"""
Rust Overload - A post-apocalyptic workshop simulator with MFU algorithm
Main entry point for the game
"""

import pygame
import sys
from src.core.game import Game

def main():
    """Main function to initialize and run the game"""
    # Initialize pygame
    pygame.init()
    
    # Initialize mixer if available
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Warning: Audio device not available. Running without sound.")
    
    # Create and run game
    game = Game()
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()