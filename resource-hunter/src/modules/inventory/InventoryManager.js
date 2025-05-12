/**
 * Gestor de inventario que implementa el algoritmo MFU (Most Frequently Used)
 * Cuando el inventario está lleno y se intenta añadir un nuevo ítem,
 * se elimina el ítem que ha sido usado con mayor frecuencia.
 */
export class InventoryManager {
    /**
     * Constructor del gestor de inventario
     * @param {number} capacity - Capacidad máxima del inventario
     */
    constructor(capacity) {
        this.capacity = capacity;
        this.items = [];
        this.events = {
            onItemAdded: [],
            onItemRemoved: [],
            onItemUsed: []
        };
    }

    /**
     * Añade un ítem al inventario
     * Si el inventario está lleno, aplica el algoritmo MFU
     * @param {Object} item - Ítem a añadir
     * @returns {boolean} - True si se añadió correctamente
     */
    addItem(item) {
        // Verificar si el ítem ya existe
        const existingIndex = this.items.findIndex(i => i.id === item.id);
        if (existingIndex !== -1) {
            console.log(`El ítem ${item.name} ya está en el inventario.`);
            return false;
        }

        // Verificar si hay espacio
        if (this.items.length >= this.capacity) {
            // Aplicar algoritmo MFU: eliminar el ítem más usado
            this.removeMFU();
        }

        // Añadir el nuevo ítem
        this.items.push({
            ...item,
            uses: 0 // Inicializar contador de usos
        });

        // Disparar evento
        this._triggerEvent('onItemAdded', item);
        
        console.log(`Ítem añadido: ${item.name}`);
        return true;
    }

    /**
     * Elimina el ítem más frecuentemente usado (MFU)
     * @returns {Object|null} - El ítem eliminado o null si no hay ítems
     */
    removeMFU() {
        if (this.items.length === 0) return null;

        // Encontrar el ítem con mayor número de usos
        let maxUsesIndex = 0;
        for (let i = 1; i < this.items.length; i++) {
            if (this.items[i].uses > this.items[maxUsesIndex].uses) {
                maxUsesIndex = i;
            }
        }

        // Eliminar el ítem MFU
        const removedItem = this.items.splice(maxUsesIndex, 1)[0];
        
        // Disparar evento
        this._triggerEvent('onItemRemoved', removedItem);
        
        console.log(`Ítem MFU eliminado: ${removedItem.name} (${removedItem.uses} usos)`);
        return removedItem;
    }

    /**
     * Usa un ítem, incrementando su contador de usos
     * @param {string} itemId - ID del ítem a usar
     * @returns {boolean} - True si se usó correctamente
     */
    useItem(itemId) {
        const index = this.items.findIndex(item => item.id === itemId);
        if (index === -1) return false;

        // Incrementar contador de usos
        this.items[index].uses++;
        
        // Disparar evento
        this._triggerEvent('onItemUsed', this.items[index]);
        
        console.log(`Ítem usado: ${this.items[index].name} (${this.items[index].uses} usos)`);
        return true;
    }

    /**
     * Obtiene todos los ítems del inventario
     * @returns {Array} - Array de ítems
     */
    getItems() {
        return [...this.items];
    }

    /**
     * Obtiene un ítem por su ID
     * @param {string} itemId - ID del ítem
     * @returns {Object|undefined} - El ítem o undefined si no existe
     */
    getItem(itemId) {
        return this.items.find(item => item.id === itemId);
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