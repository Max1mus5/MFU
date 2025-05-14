# Sobrecarga de Óxido

Un simulador de taller post-apocalíptico que implementa el algoritmo de Más Frecuentemente Usado (MFU) para la gestión de recursos.

## Concepto del Juego

En el año 2147, después de un colapso ambiental, la humanidad sobrevive en ciudades subterráneas. Juegas como Jax, un ingeniero que mantiene armas para la defensa contra bandidos y mutantes. Tu taller tiene espacio de inventario limitado, y debes recolectar recursos en misiones rápidas.

El desafío principal: Los materiales se oxidan si no se usan con frecuencia (¡el aire está lleno de ácido!). Para evitar desperdiciar espacio, debes descartar estratégicamente los recursos más frecuentemente utilizados que se han degradado.

## Mecánicas del Juego

### Recursos y Contadores de Uso
- **Tipos de Recursos**:
  - 🟫 Tuerca Oxidada (básico, usado en cualquier arma)
  - 🔵 Circuito Frágil (para armas eléctricas)
  - 🔋 Celda de Energía (para láseres)
  - 💀 Núcleo Radioactivo (para armas pesadas)

- **MFU con Envejecimiento**:
  - Cada recurso tiene un contador de 8 bits (0-255) que aumenta cuando se usa
  - Cada 15 segundos, los contadores se dividen por 2 (simulando oxidación)
  - Cuando el inventario está lleno, el recurso con el contador más alto es reemplazado

### Flujo de Juego
1. **Fase de Recolección**: Viaja a zonas de riesgo para recolectar recursos
2. **Fase de Reparación**: Elige armas dañadas para reparar usando combinaciones específicas de recursos
3. **Fase de Reemplazo**: Cuando el inventario está lleno, el algoritmo MFU elimina automáticamente el recurso más usado

## Estructura del Proyecto

```
MFU/
├── assets/
│   ├── audio/       # Efectos de sonido y música del juego
│   └── images/      # Sprites y elementos de la interfaz de usuario
├── src/
│   ├── core/        # Sistemas principales del juego
│   │   ├── config.py            # Configuraciones y constantes del juego
│   │   ├── game.py              # Controlador principal del juego
│   │   ├── mfu_algorithm.py     # Algoritmo de reemplazo MFU
│   │   ├── resource_manager.py  # Gestión de inventario y recursos
│   │   └── scene_manager.py     # Sistema de gestión de escenas
│   ├── entities/    # Entidades del juego
│   │   ├── resource.py          # Entidad de recurso
│   │   └── weapon.py            # Entidad de arma
│   ├── scenes/      # Escenas del juego
│   │   ├── base_scene.py        # Clase base abstracta para escenas
│   │   ├── collection_scene.py  # Gameplay de recolección de recursos
│   │   └── workshop_scene.py    # Gameplay de reparación en el taller
│   ├── ui/          # Componentes de interfaz de usuario
│   │   ├── inventory_panel.py   # Visualización del inventario
│   │   ├── repair_panel.py      # Interfaz de reparación de armas
│   │   └── status_panel.py      # Estado del juego y navegación
│   └── utils/       # Funciones de utilidad
│       └── asset_loader.py      # Utilidades para cargar recursos
└── main.py          # Punto de entrada del juego
```

## Descripción de Módulos

### Módulos Principales (Core)

- **config.py**: Contiene configuraciones del juego, constantes y valores de configuración
  - Aquí se definen los tipos de armas, recursos, y sus características
  - Contiene constantes como PLAYER_MAX_HEALTH, AGING_INTERVAL, WEAPONS_TO_WIN
  - Define rutas a archivos de recursos (imágenes, sonidos)

- **game.py**: Controlador principal que gestiona el bucle del juego y las escenas
  - Maneja la lógica de celebración cuando se ganan puntos
  - Contiene métodos para reproducir sonidos (play_point_sound, play_obtain_element_sound, play_lose_point_sound)
  - Implementa la lógica de pérdida de vida y condiciones de fin de juego

- **mfu_algorithm.py**: Implementa el algoritmo de reemplazo Más Frecuentemente Usado
  - Gestiona los contadores de uso de recursos
  - Implementa la lógica de envejecimiento (oxidación) de recursos

- **resource_manager.py**: Gestiona el inventario del jugador y la recolección de recursos
  - Controla el límite de inventario y la lógica de reemplazo
  - Maneja la adición y eliminación de recursos

- **scene_manager.py**: Maneja diferentes escenas del juego y transiciones entre ellas
  - Controla el cambio entre escenas de taller y recolección

### Módulos de Entidades

- **resource.py**: Define la clase Resource para elementos coleccionables
  - Implementa propiedades como tipo, contador de uso y estado

- **weapon.py**: Define la clase Weapon para armas reparables
  - Contiene la lógica de reparación y requisitos de recursos
  - Implementa estados de armas (dañada, reparada, destruida)
  - Gestiona el envejecimiento de armas y su destrucción

### Módulos de Escenas

- **base_scene.py**: Clase base abstracta para todas las escenas del juego
  - Define la interfaz común para todas las escenas

- **collection_scene.py**: Escena para recolectar recursos en el páramo
  - Implementa la generación aleatoria de recursos
  - Maneja la colisión con recursos y la lógica de daño
  - Reproduce sonidos al obtener elementos

- **workshop_scene.py**: Escena principal de juego en el taller para reparar armas
  - Gestiona la selección y reparación de armas
  - Inicia la animación de celebración cuando se repara un arma
  - Muestra la animación de celebración del personaje

### Módulos de Interfaz de Usuario

- **inventory_panel.py**: Componente UI para mostrar e interactuar con el inventario
  - Visualiza los recursos disponibles y sus contadores

- **repair_panel.py**: Componente UI para la interfaz de reparación de armas
  - Muestra las armas disponibles y su estado

- **status_panel.py**: Componente UI para el estado del juego y botones de navegación
  - Muestra salud, puntuación y otros indicadores

### Módulos de Utilidad

- **asset_loader.py**: Utilidad para cargar y gestionar recursos del juego (imágenes, sonidos, fuentes)
  - Proporciona métodos para acceder a recursos cargados

## Objetivos del Juego

- **Condición de Victoria**: Reparar 10 armas para equipar a tu facción y resistir un ataque final de mutantes
- **Condición de Derrota**: 
  - Salud agotada (por reemplazos de recursos tóxicos)
  - No reparar suficientes armas antes del límite de tiempo

## Elementos Estratégicos

- No sobreutilizar un solo tipo de recurso (contador alto = candidato para eliminación)
- Equilibrar el envejecimiento usando recursos antes de que se oxiden demasiado
- Priorizar estratégicamente recursos raros como núcleos radioactivos

## Características Especiales

- **Animación de Celebración**: Cuando se repara un arma o se ganan puntos, el personaje realiza una animación de celebración
- **Efectos de Sonido**:
  - Sonido de punto cuando se ganan puntos (assets/audio/point.mp3)
  - Sonidos aleatorios al obtener elementos (assets/audio/obtener_elemento.mp3 o assets/audio/obtener_elemento_2.mp3)
  - Sonido cuando se pierde una vida (assets/audio/lose_point.mp3)

## Configuraciones y Ajustes

- **Configuración de Dificultad**: En config.py puedes ajustar:
  - PLAYER_MAX_HEALTH: Salud máxima del jugador
  - AGING_INTERVAL: Frecuencia de oxidación (en milisegundos)
  - WEAPONS_TO_WIN: Número de armas necesarias para ganar
  - INVENTORY_SIZE: Tamaño máximo del inventario

- **Configuración de Armas**: En config.py se definen los tipos de armas:
  - Pistola Oxidada: Arma básica
  - Escopeta de Chatarra: Arma de medio alcance
  - Rifle Improvisado: Arma de largo alcance
  - Cortador Láser: Arma avanzada
  - Cañón de Plasma: Arma pesada

## Instalación y Ejecución

1. Asegúrate de tener Python 3.6+ y Pygame instalados
2. Clona este repositorio
3. Ejecuta `python main.py` para iniciar el juego

## Controles

- **Escena de Taller**:
  - Ratón: Seleccionar recursos y armas, hacer clic en el botón de reparación
  - Tecla C: Cambiar a la escena de recolección

- **Escena de Recolección**:
  - Flechas Izquierda/Derecha: Mover al jugador
  - Tecla W: Cambiar a la escena de taller