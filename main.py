#!/usr/bin/env python3
"""
Rust Overload - A post-apocalyptic workshop simulator with MFU algorithm
Main entry point for the game
"""

import pygame, asyncio
import sys
from src.core.game import Game

async def main():
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
    await asyncio.sleep(0)  # Yield control to the event loop

asyncio.run(main())