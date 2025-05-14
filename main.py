#!/usr/bin/env python3
"""
Rust Overload - A post-apocalyptic workshop simulator with MFU algorithm
Main entry point for the game
"""

import pygame
import asyncio
import sys
from src.core.game import Game

# Variable global para el juego
game = None

async def main():
    """Main function to initialize and run the game"""
    global game
    
    # Initialize pygame
    pygame.init()
    
    # Initialize mixer if available
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Warning: Audio device not available. Running without sound.")
    
    # Create game
    game = Game()
    
    # Main game loop for WebAssembly compatibility
    while game.running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == game.aging_event:
                game.apply_aging()
            else:
                game.scene_manager.handle_event(event)
        
        # Update active scene
        game.scene_manager.update()
        
        # Update celebration animation if active
        if game.celebrating:
            current_time = pygame.time.get_ticks()
            if current_time - game.celebration_timer > game.celebration_interval:
                game.celebration_frame = (game.celebration_frame % 5) + 1
                game.celebration_timer = current_time
                
                # End celebration after cycling through all frames
                if game.celebration_frame == 1:
                    game.celebrating = False
        
        # Draw active scene
        game.screen.fill((0, 0, 0))
        game.scene_manager.draw(game.screen)
        pygame.display.flip()
        
        # Maintain frame rate
        game.clock.tick(game.config.FPS)
        
        # Yield control to browser
        await asyncio.sleep(0)
    
    # Clean up
    pygame.quit()
    return 0

# Punto de entrada para pygbag
if __name__ == "__main__":
    asyncio.run(main())