import Phaser from 'phaser';

export class BootScene extends Phaser.Scene {
    constructor() {
        super('BootScene');
    }

    preload() {
        // Cargar assets mínimos necesarios para la pantalla de carga
        this.load.image('loading-background', 'assets/ui/loading-background.png');
        this.load.image('loading-bar', 'assets/ui/loading-bar.png');
    }

    create() {
        // Configuraciones iniciales
        this.scale.pageAlignHorizontally = true;
        this.scale.pageAlignVertically = true;
        
        // Pasar a la escena de precarga
        this.scene.start('PreloadScene');
    }
}