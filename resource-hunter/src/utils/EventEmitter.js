/**
 * Sistema simple de eventos para comunicación entre módulos
 */
export class EventEmitter {
    constructor() {
        this.events = {};
    }

    /**
     * Registra un listener para un evento
     * @param {string} event - Nombre del evento
     * @param {Function} callback - Función a ejecutar
     * @returns {Function} - Función para eliminar el listener
     */
    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        
        this.events[event].push(callback);
        
        // Devolver función para eliminar el listener
        return () => {
            this.off(event, callback);
        };
    }

    /**
     * Registra un listener que se ejecuta una sola vez
     * @param {string} event - Nombre del evento
     * @param {Function} callback - Función a ejecutar
     */
    once(event, callback) {
        const onceCallback = (...args) => {
            this.off(event, onceCallback);
            callback.apply(this, args);
        };
        
        return this.on(event, onceCallback);
    }

    /**
     * Elimina un listener
     * @param {string} event - Nombre del evento
     * @param {Function} callback - Función a eliminar
     */
    off(event, callback) {
        if (!this.events[event]) return;
        
        this.events[event] = this.events[event].filter(cb => cb !== callback);
        
        // Limpiar array si está vacío
        if (this.events[event].length === 0) {
            delete this.events[event];
        }
    }

    /**
     * Emite un evento
     * @param {string} event - Nombre del evento
     * @param {...any} args - Argumentos a pasar a los callbacks
     */
    emit(event, ...args) {
        if (!this.events[event]) return;
        
        this.events[event].forEach(callback => {
            callback.apply(this, args);
        });
    }

    /**
     * Elimina todos los listeners
     * @param {string} [event] - Nombre del evento (opcional)
     */
    removeAllListeners(event) {
        if (event) {
            delete this.events[event];
        } else {
            this.events = {};
        }
    }
}