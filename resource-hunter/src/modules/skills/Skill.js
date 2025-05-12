/**
 * Clase que representa una habilidad en el juego
 */
export class Skill {
    /**
     * Constructor de la habilidad
     * @param {Object} config - Configuración de la habilidad
     * @param {string} config.id - Identificador único de la habilidad
     * @param {string} config.name - Nombre de la habilidad
     * @param {string} config.description - Descripción de la habilidad
     * @param {number} config.frame - Frame del spritesheet para esta habilidad
     * @param {number} config.cooldown - Tiempo de enfriamiento en ms
     * @param {number} config.energyCost - Coste de energía
     * @param {Function} config.effect - Función que se ejecuta al usar la habilidad
     */
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.description = config.description || '';
        this.frame = config.frame || 0;
        this.cooldown = config.cooldown || 1000;
        this.energyCost = config.energyCost || 10;
        this.effect = config.effect || (() => {});
        
        // Propiedades internas
        this.uses = 0;
        this.mastery = 0;
        this.lastUsed = 0;
    }

    /**
     * Verifica si la habilidad está en enfriamiento
     * @param {number} currentTime - Tiempo actual en ms
     * @returns {boolean} - True si está en enfriamiento
     */
    isOnCooldown(currentTime) {
        return (currentTime - this.lastUsed) < this.cooldown;
    }

    /**
     * Calcula el tiempo restante de enfriamiento
     * @param {number} currentTime - Tiempo actual en ms
     * @returns {number} - Tiempo restante en ms
     */
    getRemainingCooldown(currentTime) {
        if (!this.isOnCooldown(currentTime)) return 0;
        return this.cooldown - (currentTime - this.lastUsed);
    }

    /**
     * Calcula el nivel de maestría como porcentaje
     * @returns {number} - Porcentaje de maestría (0-100)
     */
    getMasteryPercentage() {
        return this.mastery;
    }

    /**
     * Calcula la efectividad actual de la habilidad
     * @returns {number} - Efectividad (0-100)
     */
    getEffectiveness() {
        // Fórmula: Maestría - (Usos / 10)
        const baseEffectiveness = this.mastery;
        const mfuPenalty = Math.min(50, this.uses / 2);
        
        return Math.max(10, baseEffectiveness - mfuPenalty);
    }

    /**
     * Obtiene una descripción detallada de la habilidad
     * @returns {string} - Descripción detallada
     */
    getDetailedDescription() {
        return `${this.description}\n\nMaestría: ${this.mastery}%\nUsos: ${this.uses}\nEfectividad: ${this.getEffectiveness().toFixed(1)}%\nEnfriamiento: ${this.cooldown/1000}s\nCoste de energía: ${this.energyCost}`;
    }
}