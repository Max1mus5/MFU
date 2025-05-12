import Phaser from 'phaser';

export class MainScene extends Phaser.Scene {
    constructor() {
        super('MainScene');
    }

    init() {
        // Inicializar variables
        this.player = null;
        this.cursors = null;
        this.inventoryUI = null;
        this.skillsUI = null;
    }

    create() {
        // Crear el mundo
        this.createWorld();
        
        // Crear el jugador
        this.createPlayer();
        
        // Configurar la cámara
        this.cameras.main.setBounds(0, 0, 1600, 1200);
        this.cameras.main.startFollow(this.player, true, 0.08, 0.08);
        
        // Configurar controles
        this.cursors = this.input.keyboard.createCursorKeys();
        
        // Inicializar sistemas
        this.initSystems();
        
        // Crear UI
        this.createUI();
        
        // Iniciar música de fondo
        this.sound.play('background-music', { loop: true, volume: 0.5 });
    }

    createWorld() {
        // Crear un mapa simple para pruebas
        this.add.grid(0, 0, 1600, 1200, 32, 32, 0x000000, 0, 0x333333, 0.2)
            .setOrigin(0, 0);
    }

    createPlayer() {
        // Crear sprite del jugador
        this.player = this.physics.add.sprite(400, 300, 'player');
        this.player.setCollideWorldBounds(true);
        this.player.play('player-idle');
    }

    initSystems() {
        // Importar e inicializar los sistemas necesarios
        const { InventoryManager } = require('../../modules/inventory/InventoryManager');
        const { SkillManager } = require('../../modules/skills/SkillManager');
        const { ResourceManager } = require('../../modules/resources/ResourceManager');
        const { EnemyManager } = require('../../modules/enemies/EnemyManager');
        
        // Inicializar sistemas
        this.inventoryManager = new InventoryManager(3); // Capacidad 3
        this.skillManager = new SkillManager(4); // Capacidad 4
        this.resourceManager = new ResourceManager();
        this.enemyManager = new EnemyManager(this);
        
        // Crear algunos ítems de prueba
        this.createTestItems();
    }

    createTestItems() {
        // Crear ítems de prueba en el mundo
        const items = [
            { id: 'sword', name: 'Espada', x: 200, y: 200, frame: 0 },
            { id: 'shield', name: 'Escudo', x: 300, y: 250, frame: 1 },
            { id: 'potion', name: 'Poción', x: 400, y: 350, frame: 2 },
            { id: 'bow', name: 'Arco', x: 500, y: 400, frame: 3 },
            { id: 'axe', name: 'Hacha', x: 600, y: 300, frame: 4 }
        ];
        
        this.itemSprites = [];
        
        items.forEach(item => {
            const sprite = this.physics.add.sprite(item.x, item.y, 'items', item.frame);
            sprite.itemData = item;
            this.itemSprites.push(sprite);
            
            // Colisión con el jugador para recoger
            this.physics.add.overlap(this.player, sprite, this.collectItem, null, this);
        });
    }

    collectItem(player, itemSprite) {
        const item = itemSprite.itemData;
        
        // Intentar añadir al inventario
        const added = this.inventoryManager.addItem({
            id: item.id,
            name: item.name,
            frame: item.frame,
            uses: 0
        });
        
        if (added) {
            // Reproducir sonido y eliminar sprite
            this.sound.play('item-pickup');
            itemSprite.destroy();
            
            // Eliminar de la lista de sprites
            const index = this.itemSprites.indexOf(itemSprite);
            if (index > -1) {
                this.itemSprites.splice(index, 1);
            }
            
            // Actualizar UI
            this.updateInventoryUI();
        }
    }

    createUI() {
        // Crear UI de inventario
        this.inventoryUI = this.add.container(10, this.cameras.main.height - 100);
        this.inventoryUI.setScrollFactor(0); // Fijar a la cámara
        
        // Crear UI de habilidades
        this.skillsUI = this.add.container(10, this.cameras.main.height - 170);
        this.skillsUI.setScrollFactor(0); // Fijar a la cámara
        
        // Inicializar UI
        this.updateInventoryUI();
        this.updateSkillsUI();
    }

    updateInventoryUI() {
        // Limpiar UI existente
        this.inventoryUI.removeAll(true);
        
        // Título
        const title = this.add.text(0, 0, 'Inventario (MFU)', { 
            font: '16px Arial', 
            fill: '#ffffff' 
        });
        this.inventoryUI.add(title);
        
        // Mostrar slots de inventario
        const items = this.inventoryManager.getItems();
        items.forEach((item, index) => {
            // Crear slot
            const slotX = index * 110;
            const slot = this.add.image(slotX + 50, 40, 'inventory-slot');
            
            // Crear icono de ítem
            const icon = this.add.sprite(slotX + 50, 40, 'items', item.frame);
            
            // Mostrar contador de usos
            const usesText = this.add.text(slotX + 50, 60, `Usos: ${item.uses}`, { 
                font: '12px Arial', 
                fill: '#ffffff',
                align: 'center'
            }).setOrigin(0.5);
            
            // Añadir a la UI
            this.inventoryUI.add([slot, icon, usesText]);
            
            // Hacer interactivo
            icon.setInteractive();
            icon.on('pointerdown', () => {
                this.useItem(item.id);
            });
        });
    }

    updateSkillsUI() {
        // Implementación similar a updateInventoryUI para habilidades
        this.skillsUI.removeAll(true);
        
        const title = this.add.text(0, 0, 'Habilidades (MFU)', { 
            font: '16px Arial', 
            fill: '#ffffff' 
        });
        this.skillsUI.add(title);
        
        // Aquí iría el código para mostrar las habilidades
    }

    useItem(itemId) {
        const used = this.inventoryManager.useItem(itemId);
        if (used) {
            // Reproducir sonido
            this.sound.play('item-use');
            
            // Actualizar UI
            this.updateInventoryUI();
            
            // Mostrar efecto visual
            this.showItemUseEffect(itemId);
        }
    }

    showItemUseEffect(itemId) {
        // Efectos visuales según el ítem usado
        // Implementación básica para demostración
        const effectSprite = this.add.sprite(this.player.x, this.player.y, 'items');
        
        switch (itemId) {
            case 'sword':
                effectSprite.setFrame(0);
                effectSprite.setScale(2);
                break;
            case 'shield':
                effectSprite.setFrame(1);
                effectSprite.setScale(2);
                break;
            // Otros casos...
        }
        
        // Animación simple
        this.tweens.add({
            targets: effectSprite,
            alpha: 0,
            scale: 3,
            duration: 500,
            onComplete: () => {
                effectSprite.destroy();
            }
        });
    }

    update() {
        // Movimiento del jugador
        if (this.cursors.left.isDown) {
            this.player.setVelocityX(-160);
            this.player.flipX = true;
            this.player.play('player-walk', true);
        } else if (this.cursors.right.isDown) {
            this.player.setVelocityX(160);
            this.player.flipX = false;
            this.player.play('player-walk', true);
        } else {
            this.player.setVelocityX(0);
        }

        if (this.cursors.up.isDown) {
            this.player.setVelocityY(-160);
            this.player.play('player-walk', true);
        } else if (this.cursors.down.isDown) {
            this.player.setVelocityY(160);
            this.player.play('player-walk', true);
        } else {
            this.player.setVelocityY(0);
        }
        
        // Si no hay movimiento, reproducir animación idle
        if (this.player.body.velocity.x === 0 && this.player.body.velocity.y === 0) {
            this.player.play('player-idle', true);
        }
    }
}