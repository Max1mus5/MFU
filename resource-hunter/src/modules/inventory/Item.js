/**
 * Clase que representa un ítem en el juego
 */
export class Item {
    /**
     * Constructor del ítem
     * @param {Object} config - Configuración del ítem
     * @param {string} config.id - Identificador único del ítem
     * @param {string} config.name - Nombre del ítem
     * @param {string} config.description - Descripción del ítem
     * @param {number} config.frame - Frame del spritesheet para este ítem
     * @param {number} config.durability - Durabilidad máxima del ítem (opcional)
     * @param {Function} config.useEffect - Función que se ejecuta al usar el ítem (opcional)
     */
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.description = config.description || '';
        this.frame = config.frame || 0;
        this.uses = 0;
        this.durability = config.durability || Infinity;
        this.useEffect = config.useEffect || (() => {});
    }

    /**
     * Usa el ítem, incrementando su contador de usos
     * @param {Object} context - Contexto en el que se usa el ítem (ej: escena, jugador)
     * @returns {boolean} - True si se usó correctamente, false si está roto
     */
    use(context) {
        // Verificar si el ítem está roto
        if (this.durability !== Infinity && this.uses >= this.durability) {
            console.log(`${this.name} está roto y no puede usarse.`);
            return false;
        }

        // Incrementar contador de usos
        this.uses++;
        
        // Ejecutar efecto
        this.useEffect(context);
        
        console.log(`Usando ${this.name} (${this.uses}/${this.durability} usos)`);
        return true;
    }

    /**
     * Calcula el porcentaje de desgaste del ítem
     * @returns {number} - Porcentaje de desgaste (0-100)
     */
    getWearPercentage() {
        if (this.durability === Infinity) return 0;
        return Math.min(100, (this.uses / this.durability) * 100);
    }

    /**
     * Verifica si el ítem está roto
     * @returns {boolean} - True si está roto
     */
    isBroken() {
        return this.durability !== Infinity && this.uses >= this.durability;
    }

    /**
     * Repara el ítem, reduciendo su contador de usos
     * @param {number} amount - Cantidad de usos a reparar
     */
    repair(amount) {
        this.uses = Math.max(0, this.uses - amount);
        console.log(`${this.name} reparado. Usos restantes: ${this.durability - this.uses}`);
    }
}