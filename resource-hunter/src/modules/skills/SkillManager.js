/**
 * Gestor de habilidades que implementa el algoritmo MFU (Most Frequently Used)
 * Cuando la memoria de habilidades está llena y se intenta aprender una nueva,
 * se olvida la habilidad que ha sido usada con mayor frecuencia.
 */
export class SkillManager {
    /**
     * Constructor del gestor de habilidades
     * @param {number} capacity - Capacidad máxima de la memoria de habilidades
     */
    constructor(capacity) {
        this.capacity = capacity;
        this.skills = [];
        this.events = {
            onSkillLearned: [],
            onSkillForgotten: [],
            onSkillUsed: []
        };
    }

    /**
     * Aprende una nueva habilidad
     * Si la memoria está llena, aplica el algoritmo MFU
     * @param {Object} skill - Habilidad a aprender
     * @returns {boolean} - True si se aprendió correctamente
     */
    learnSkill(skill) {
        // Verificar si la habilidad ya existe
        const existingIndex = this.skills.findIndex(s => s.id === skill.id);
        if (existingIndex !== -1) {
            console.log(`La habilidad ${skill.name} ya está aprendida.`);
            return false;
        }

        // Verificar si hay espacio en la memoria
        if (this.skills.length >= this.capacity) {
            // Aplicar algoritmo MFU: olvidar la habilidad más usada
            this.forgetMFU();
        }

        // Añadir la nueva habilidad
        this.skills.push({
            ...skill,
            uses: 0, // Inicializar contador de usos
            mastery: 0 // Nivel de maestría (0-100)
        });

        // Disparar evento
        this._triggerEvent('onSkillLearned', skill);
        
        console.log(`Habilidad aprendida: ${skill.name}`);
        return true;
    }

    /**
     * Olvida la habilidad más frecuentemente usada (MFU)
     * @returns {Object|null} - La habilidad olvidada o null si no hay habilidades
     */
    forgetMFU() {
        if (this.skills.length === 0) return null;

        // Encontrar la habilidad con mayor número de usos
        let maxUsesIndex = 0;
        for (let i = 1; i < this.skills.length; i++) {
            if (this.skills[i].uses > this.skills[maxUsesIndex].uses) {
                maxUsesIndex = i;
            }
        }

        // Olvidar la habilidad MFU
        const forgottenSkill = this.skills.splice(maxUsesIndex, 1)[0];
        
        // Disparar evento
        this._triggerEvent('onSkillForgotten', forgottenSkill);
        
        console.log(`Habilidad MFU olvidada: ${forgottenSkill.name} (${forgottenSkill.uses} usos)`);
        return forgottenSkill;
    }

    /**
     * Usa una habilidad, incrementando su contador de usos y maestría
     * @param {string} skillId - ID de la habilidad a usar
     * @param {Object} context - Contexto en el que se usa la habilidad
     * @returns {boolean} - True si se usó correctamente
     */
    useSkill(skillId, context) {
        const index = this.skills.findIndex(skill => skill.id === skillId);
        if (index === -1) return false;

        // Incrementar contador de usos
        this.skills[index].uses++;
        
        // Incrementar maestría (hasta un máximo de 100)
        this.skills[index].mastery = Math.min(100, this.skills[index].mastery + 2);
        
        // Calcular efectividad basada en la maestría y el algoritmo MFU
        // Cuanto más se usa, menos efectiva se vuelve (representando el desgaste mental)
        const effectiveness = this.calculateEffectiveness(this.skills[index]);
        
        // Ejecutar efecto de la habilidad con la efectividad calculada
        if (this.skills[index].effect) {
            this.skills[index].effect(context, effectiveness);
        }
        
        // Disparar evento
        this._triggerEvent('onSkillUsed', {
            skill: this.skills[index],
            effectiveness
        });
        
        console.log(`Habilidad usada: ${this.skills[index].name} (${this.skills[index].uses} usos, ${effectiveness.toFixed(2)}% efectividad)`);
        return true;
    }

    /**
     * Calcula la efectividad de una habilidad basada en su maestría y uso
     * @param {Object} skill - Habilidad
     * @returns {number} - Efectividad (0-100)
     * @private
     */
    calculateEffectiveness(skill) {
        // Fórmula: Maestría - (Usos / 10)
        // Esto hace que las habilidades más usadas sean menos efectivas
        const baseEffectiveness = skill.mastery;
        const mfuPenalty = Math.min(50, skill.uses / 2); // Máximo 50% de penalización
        
        return Math.max(10, baseEffectiveness - mfuPenalty);
    }

    /**
     * Obtiene todas las habilidades aprendidas
     * @returns {Array} - Array de habilidades
     */
    getSkills() {
        return [...this.skills];
    }

    /**
     * Obtiene una habilidad por su ID
     * @param {string} skillId - ID de la habilidad
     * @returns {Object|undefined} - La habilidad o undefined si no existe
     */
    getSkill(skillId) {
        return this.skills.find(skill => skill.id === skillId);
    }

    /**
     * Registra un callback para un evento
     * @param {string} eventName - Nombre del evento
     * @param {Function} callback - Función a ejecutar
     */
    on(eventName, callback) {
        if (this.events[eventName]) {
            this.events[eventName].push(callback);
        }
    }

    /**
     * Dispara un evento
     * @param {string} eventName - Nombre del evento
     * @param {*} data - Datos a pasar al callback
     * @private
     */
    _triggerEvent(eventName, data) {
        if (this.events[eventName]) {
            this.events[eventName].forEach(callback => callback(data));
        }
    }
}