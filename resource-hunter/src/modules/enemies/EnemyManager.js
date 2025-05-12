/**
 * Gestor de enemigos que implementa adaptación basada en MFU
 * Los enemigos desarrollan resistencias contra los ataques más frecuentes del jugador
 */
export class EnemyManager {
    /**
     * Constructor del gestor de enemigos
     * @param {Phaser.Scene} scene - Escena del juego
     */
    constructor(scene) {
        this.scene = scene;
        this.enemies = [];
        this.playerAttackStats = {}; // Estadísticas de ataques del jugador
        this.adaptationRate = 0.05; // Tasa de adaptación (0-1)
    }

    /**
     * Crea un nuevo enemigo
     * @param {number} x - Posición X
     * @param {number} y - Posición Y
     * @param {string} type - Tipo de enemigo
     * @returns {Object} - El enemigo creado
     */
    createEnemy(x, y, type) {
        // Configuración base del enemigo
        const enemyConfig = {
            x,
            y,
            type,
            health: 100,
            maxHealth: 100,
            damage: 10,
            speed: 100,
            resistances: {}, // Resistencias a diferentes tipos de ataque
            sprite: null
        };
        
        // Crear sprite
        enemyConfig.sprite = this.scene.physics.add.sprite(x, y, 'enemies', this.getEnemyFrame(type));
        enemyConfig.sprite.setCollideWorldBounds(true);
        
        // Añadir a la lista
        this.enemies.push(enemyConfig);
        
        return enemyConfig;
    }

    /**
     * Obtiene el frame del spritesheet según el tipo de enemigo
     * @param {string} type - Tipo de enemigo
     * @returns {number} - Frame del spritesheet
     * @private
     */
    getEnemyFrame(type) {
        const frames = {
            'slime': 0,
            'skeleton': 1,
            'goblin': 2,
            'orc': 3,
            'demon': 4
        };
        
        return frames[type] || 0;
    }

    /**
     * Actualiza todos los enemigos
     * @param {Object} player - Jugador
     */
    update(player) {
        this.enemies.forEach(enemy => {
            // Movimiento básico hacia el jugador
            this.moveTowardsPlayer(enemy, player);
            
            // Actualizar barra de vida
            this.updateHealthBar(enemy);
        });
    }

    /**
     * Mueve un enemigo hacia el jugador
     * @param {Object} enemy - Enemigo
     * @param {Object} player - Jugador
     * @private
     */
    moveTowardsPlayer(enemy, player) {
        // Calcular dirección hacia el jugador
        const dx = player.x - enemy.sprite.x;
        const dy = player.y - enemy.sprite.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Si está lo suficientemente cerca, moverse hacia el jugador
        if (distance < 300) {
            const speed = enemy.speed;
            const vx = (dx / distance) * speed;
            const vy = (dy / distance) * speed;
            
            enemy.sprite.setVelocity(vx, vy);
            
            // Voltear sprite según dirección
            if (dx < 0) {
                enemy.sprite.flipX = true;
            } else {
                enemy.sprite.flipX = false;
            }
        } else {
            enemy.sprite.setVelocity(0, 0);
        }
    }

    /**
     * Actualiza la barra de vida de un enemigo
     * @param {Object} enemy - Enemigo
     * @private
     */
    updateHealthBar(enemy) {
        // Implementación de la barra de vida
        // (Se implementaría con gráficos de Phaser)
    }

    /**
     * Registra un ataque del jugador
     * @param {string} attackType - Tipo de ataque
     * @param {number} damage - Daño base
     */
    registerPlayerAttack(attackType, damage) {
        // Incrementar contador de uso de este tipo de ataque
        if (!this.playerAttackStats[attackType]) {
            this.playerAttackStats[attackType] = {
                uses: 0,
                totalDamage: 0
            };
        }
        
        this.playerAttackStats[attackType].uses++;
        this.playerAttackStats[attackType].totalDamage += damage;
        
        console.log(`Ataque registrado: ${attackType} (${this.playerAttackStats[attackType].uses} usos)`);
        
        // Adaptar resistencias de los enemigos
        this.adaptEnemyResistances();
    }

    /**
     * Adapta las resistencias de los enemigos según los ataques MFU
     * @private
     */
    adaptEnemyResistances() {
        // Encontrar el ataque más usado (MFU)
        let mfuAttack = null;
        let maxUses = 0;
        
        for (const [attackType, stats] of Object.entries(this.playerAttackStats)) {
            if (stats.uses > maxUses) {
                maxUses = stats.uses;
                mfuAttack = attackType;
            }
        }
        
        if (!mfuAttack) return;
        
        // Aumentar resistencia a ese tipo de ataque en todos los enemigos
        this.enemies.forEach(enemy => {
            if (!enemy.resistances[mfuAttack]) {
                enemy.resistances[mfuAttack] = 0;
            }
            
            // Aumentar resistencia (máximo 80%)
            enemy.resistances[mfuAttack] = Math.min(0.8, enemy.resistances[mfuAttack] + this.adaptationRate);
            
            console.log(`Enemigo ${enemy.type} adaptado: +${(this.adaptationRate * 100).toFixed(1)}% resistencia a ${mfuAttack}`);
        });
    }

    /**
     * Aplica daño a un enemigo, considerando resistencias
     * @param {Object} enemy - Enemigo
     * @param {string} attackType - Tipo de ataque
     * @param {number} baseDamage - Daño base
     * @returns {number} - Daño real aplicado
     */
    damageEnemy(enemy, attackType, baseDamage) {
        // Calcular resistencia
        const resistance = enemy.resistances[attackType] || 0;
        
        // Calcular daño real
        const actualDamage = baseDamage * (1 - resistance);
        
        // Aplicar daño
        enemy.health -= actualDamage;
        
        // Verificar si el enemigo ha muerto
        if (enemy.health <= 0) {
            this.killEnemy(enemy);
        }
        
        console.log(`Daño a ${enemy.type}: ${actualDamage.toFixed(1)} (resistencia: ${(resistance * 100).toFixed(1)}%)`);
        
        return actualDamage;
    }

    /**
     * Elimina un enemigo
     * @param {Object} enemy - Enemigo
     * @private
     */
    killEnemy(enemy) {
        // Eliminar sprite
        enemy.sprite.destroy();
        
        // Eliminar de la lista
        const index = this.enemies.indexOf(enemy);
        if (index !== -1) {
            this.enemies.splice(index, 1);
        }
        
        console.log(`Enemigo ${enemy.type} eliminado`);
        
        // Aquí se podrían generar recompensas, experiencia, etc.
    }

    /**
     * Obtiene las estadísticas de resistencia de un enemigo
     * @param {Object} enemy - Enemigo
     * @returns {Object} - Estadísticas de resistencia
     */
    getEnemyResistanceStats(enemy) {
        const stats = {};
        
        for (const [attackType, resistance] of Object.entries(enemy.resistances)) {
            stats[attackType] = {
                resistance: resistance,
                percentage: (resistance * 100).toFixed(1) + '%'
            };
        }
        
        return stats;
    }

    /**
     * Obtiene las estadísticas de ataques del jugador
     * @returns {Object} - Estadísticas de ataques
     */
    getPlayerAttackStats() {
        const stats = {};
        
        for (const [attackType, data] of Object.entries(this.playerAttackStats)) {
            stats[attackType] = {
                uses: data.uses,
                totalDamage: data.totalDamage,
                averageDamage: data.totalDamage / data.uses
            };
        }
        
        return stats;
    }
}