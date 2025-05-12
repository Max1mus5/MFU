/**
 * Gestor de recursos que implementa un ciclo de vida basado en el uso
 * Los recursos más utilizados se agotan más rápido (concepto MFU)
 */
export class ResourceManager {
    constructor() {
        this.resources = {};
        this.events = {
            onResourceAdded: [],
            onResourceDepleted: [],
            onResourceUsed: []
        };
    }

    /**
     * Añade un recurso al gestor
     * @param {string} id - Identificador único del recurso
     * @param {Object} resource - Datos del recurso
     * @returns {boolean} - True si se añadió correctamente
     */
    addResource(id, resource) {
        if (this.resources[id]) {
            console.log(`El recurso ${id} ya existe. Incrementando cantidad.`);
            this.resources[id].quantity += resource.quantity || 1;
            return true;
        }

        this.resources[id] = {
            ...resource,
            uses: 0,
            depletion: 0 // Porcentaje de agotamiento (0-100)
        };

        // Disparar evento
        this._triggerEvent('onResourceAdded', { id, resource: this.resources[id] });
        
        console.log(`Recurso añadido: ${id} (${this.resources[id].quantity})`);
        return true;
    }

    /**
     * Usa un recurso, incrementando su contador de usos y agotamiento
     * @param {string} id - ID del recurso
     * @param {number} amount - Cantidad a usar
     * @returns {boolean} - True si se usó correctamente
     */
    useResource(id, amount = 1) {
        if (!this.resources[id] || this.resources[id].quantity < amount) {
            console.log(`No hay suficiente ${id} disponible.`);
            return false;
        }

        // Incrementar contador de usos
        this.resources[id].uses += amount;
        
        // Reducir cantidad
        this.resources[id].quantity -= amount;
        
        // Calcular agotamiento basado en usos (concepto MFU)
        // Cuanto más se usa un recurso, más rápido se agota
        this.resources[id].depletion = Math.min(100, (this.resources[id].uses / 10) * 100);
        
        // Verificar si se ha agotado completamente
        if (this.resources[id].quantity <= 0) {
            const depleted = this.resources[id];
            delete this.resources[id];
            
            // Disparar evento
            this._triggerEvent('onResourceDepleted', { id, resource: depleted });
            
            console.log(`Recurso agotado: ${id}`);
        } else {
            // Disparar evento
            this._triggerEvent('onResourceUsed', { 
                id, 
                resource: this.resources[id],
                amount
            });
            
            console.log(`Recurso usado: ${id} (${amount}). Quedan: ${this.resources[id].quantity}`);
        }
        
        return true;
    }

    /**
     * Obtiene un recurso por su ID
     * @param {string} id - ID del recurso
     * @returns {Object|undefined} - El recurso o undefined si no existe
     */
    getResource(id) {
        return this.resources[id];
    }

    /**
     * Obtiene todos los recursos
     * @returns {Object} - Objeto con todos los recursos
     */
    getAllResources() {
        return { ...this.resources };
    }

    /**
     * Calcula la eficiencia de un recurso basada en su agotamiento
     * @param {string} id - ID del recurso
     * @returns {number} - Eficiencia (0-1)
     */
    getResourceEfficiency(id) {
        if (!this.resources[id]) return 0;
        
        // La eficiencia disminuye con el agotamiento
        return 1 - (this.resources[id].depletion / 100);
    }

    /**
     * Regenera parcialmente un recurso
     * @param {string} id - ID del recurso
     * @param {number} amount - Cantidad a regenerar
     */
    regenerateResource(id, amount) {
        if (!this.resources[id]) return;
        
        this.resources[id].quantity += amount;
        
        // Reducir agotamiento
        this.resources[id].depletion = Math.max(0, this.resources[id].depletion - 10);
        
        console.log(`Recurso regenerado: ${id} (+${amount}). Total: ${this.resources[id].quantity}`);
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