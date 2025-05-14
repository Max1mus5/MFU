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

# Estado de la pantalla de inicio
waiting_for_start = True
audio_initialized = False

async def show_start_screen(screen, clock, config):
    """Muestra la pantalla de inicio y espera a que el usuario presione espacio"""
    global waiting_for_start, audio_initialized
    
    # Crear fuente para el texto
    try:
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
    except:
        font_large = pygame.font.SysFont("Arial", 64)
        font_medium = pygame.font.SysFont("Arial", 36)
        font_small = pygame.font.SysFont("Arial", 24)
    
    # Textos
    title_text = font_large.render("SOBRECARGA DE ÓXIDO", True, (245, 166, 35))
    subtitle_text = font_medium.render("Un simulador post-apocalíptico", True, (200, 200, 200))
    start_text = font_medium.render("Presiona ESPACIO para comenzar", True, (255, 255, 255))
    
    # Posiciones
    title_pos = ((config.SCREEN_WIDTH - title_text.get_width()) // 2, config.SCREEN_HEIGHT // 3)
    subtitle_pos = ((config.SCREEN_WIDTH - subtitle_text.get_width()) // 2, title_pos[1] + 80)
    start_pos = ((config.SCREEN_WIDTH - start_text.get_width()) // 2, config.SCREEN_HEIGHT * 2 // 3)
    audio_pos = ((config.SCREEN_WIDTH - audio_text.get_width()) // 2, start_pos[1] + 50)
    
    # Efecto de parpadeo para el texto de inicio
    blink_timer = 0
    show_start_text = True
    
    while waiting_for_start:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Inicializar audio cuando el usuario interactúa
                    if not audio_initialized:
                        try:
                            pygame.mixer.init()
                            # Reproducir un sonido silencioso para activar el audio
                            silent_sound = pygame.mixer.Sound(bytes(bytearray([0] * 44)))
                            silent_sound.play()
                            audio_initialized = True
                        except Exception as e:
                            print(f"Error initializing audio: {e}")
                    
                    waiting_for_start = False
                    return True
        
        # Actualizar parpadeo
        blink_timer += clock.get_time()
        if blink_timer >= 500:  # Cambiar cada 500ms
            blink_timer = 0
            show_start_text = not show_start_text
        
        # Dibujar fondo
        screen.fill((40, 40, 40))
        
        # Dibujar textos
        screen.blit(title_text, title_pos)
        screen.blit(subtitle_text, subtitle_pos)
        
        if show_start_text:
            screen.blit(start_text, start_pos)
        
        screen.blit(audio_text, audio_pos)
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Mantener tasa de frames
        clock.tick(60)
        
        # Ceder control al navegador
        await asyncio.sleep(0)
    
    return True

async def main():
    """Main function to initialize and run the game"""
    global game, waiting_for_start, audio_initialized
    
    # Initialize pygame
    pygame.init()
    
    # Crear reloj para controlar FPS
    clock = pygame.time.Clock()
    
    # Cargar configuración básica para la pantalla de inicio
    from src.core.config import Config
    config = Config()
    
    # Crear pantalla
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Sobrecarga de Óxido")
    
    # Mostrar pantalla de inicio y esperar a que el usuario presione espacio
    if not await show_start_screen(screen, clock, config):
        return 0
    
    # Inicializar audio si no se ha hecho ya
    if not audio_initialized:
        try:
            pygame.mixer.init()
            audio_initialized = True
        except pygame.error:
            print("Warning: Audio device not available. Running without sound.")
    
    # Create game
    game = Game()
    
    # Asegurarse de que el audio esté habilitado en el juego
    game.audio_enabled = audio_initialized
    
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