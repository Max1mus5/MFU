import Phaser from 'phaser';

export class PreloadScene extends Phaser.Scene {
    constructor() {
        super('PreloadScene');
    }

    preload() {
        // Crear barra de carga
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(width / 2 - 160, height / 2 - 25, 320, 50);
        
        const loadingText = this.make.text({
            x: width / 2,
            y: height / 2 - 50,
            text: 'Cargando...',
            style: {
                font: '20px monospace',
                fill: '#ffffff'
            }
        });
        loadingText.setOrigin(0.5, 0.5);
        
        const percentText = this.make.text({
            x: width / 2,
            y: height / 2,
            text: '0%',
            style: {
                font: '18px monospace',
                fill: '#ffffff'
            }
        });
        percentText.setOrigin(0.5, 0.5);
        
        // Eventos de carga
        this.load.on('progress', (value) => {
            percentText.setText(parseInt(value * 100) + '%');
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(width / 2 - 150, height / 2 - 15, 300 * value, 30);
        });
        
        this.load.on('complete', () => {
            progressBar.destroy();
            progressBox.destroy();
            loadingText.destroy();
            percentText.destroy();
        });
        
        // Cargar todos los assets del juego
        this.loadAssets();
    }

    loadAssets() {
        // Sprites del jugador
        this.load.spritesheet('player', 'assets/characters/player.png', { 
            frameWidth: 32, 
            frameHeight: 32 
        });
        
        // Sprites de ítems
        this.load.spritesheet('items', 'assets/items/items.png', { 
            frameWidth: 32, 
            frameHeight: 32 
        });
        
        // Sprites de enemigos
        this.load.spritesheet('enemies', 'assets/characters/enemies.png', { 
            frameWidth: 32, 
            frameHeight: 32 
        });
        
        // Tiles del mapa
        this.load.image('tiles', 'assets/tiles/tileset.png');
        
        // UI
        this.load.image('inventory-slot', 'assets/ui/inventory-slot.png');
        this.load.image('skill-slot', 'assets/ui/skill-slot.png');
        this.load.image('health-bar', 'assets/ui/health-bar.png');
        this.load.image('energy-bar', 'assets/ui/energy-bar.png');
        
        // Audio
        this.load.audio('background-music', 'assets/audio/background.mp3');
        this.load.audio('item-pickup', 'assets/audio/item-pickup.wav');
        this.load.audio('item-use', 'assets/audio/item-use.wav');
    }

    create() {
        // Crear animaciones
        this.createAnimations();
        
        // Pasar a la escena principal
        this.scene.start('MainScene');
    }

    createAnimations() {
        // Animaciones del jugador
        this.anims.create({
            key: 'player-idle',
            frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
            frameRate: 8,
            repeat: -1
        });
        
        this.anims.create({
            key: 'player-walk',
            frames: this.anims.generateFrameNumbers('player', { start: 4, end: 7 }),
            frameRate: 12,
            repeat: -1
        });
    }
}