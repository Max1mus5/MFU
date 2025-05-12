import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene';
import { PreloadScene } from './scenes/PreloadScene';
import { MainScene } from './scenes/MainScene';

export class Game {
    constructor() {
        // Configuración del juego
        const config = {
            type: Phaser.AUTO,
            parent: 'game-container',
            width: 1280,
            height: 720,
            pixelArt: true,
            physics: {
                default: 'arcade',
                arcade: {
                    gravity: { y: 0 },
                    debug: false
                }
            },
            scene: [BootScene, PreloadScene, MainScene]
        };

        // Crear la instancia del juego
        this.game = new Phaser.Game(config);
    }
}