# Sobrecarga de Óxido (Rust Overload)

Un simulador de taller post-apocalíptico que implementa el algoritmo de Más Frecuentemente Usado (MFU) para la gestión de recursos.

## Concepto del Juego

En el año 2147, después de un colapso ambiental, la humanidad sobrevive en ciudades subterráneas. Juegas como Jax, un ingeniero que mantiene armas para la defensa contra bandidos y mutantes. Tu taller tiene espacio de inventario limitado, y debes recolectar recursos en misiones rápidas.

El desafío principal: Los materiales se oxidan si no se usan con frecuencia (¡el aire está lleno de ácido!). Para evitar desperdiciar espacio, debes descartar estratégicamente los recursos más utilizados que se han degradado.

## Mecánicas del Juego

### Recursos y Contadores de Uso
- **Tipos de Recursos**:
  - 🟫 Tuercas Oxidadas (básicas, usadas en cualquier arma)
  - 🔵 Circuitos Frágiles (para armas eléctricas)
  - 🔋 Celdas de Energía (para láseres)
  - 💀 Núcleos Radioactivos (para armas pesadas)

- **MFU con Envejecimiento**:
  - Cada recurso tiene un contador de 8 bits (0-255) que aumenta cuando se usa
  - Cada 15 segundos, los contadores se dividen por 2 (simulando oxidación)
  - Cuando el inventario está lleno, se reemplaza el recurso con el contador más alto

### Flujo de Juego
1. **Fase de Recolección**: Viaja a zonas de riesgo para recolectar recursos
2. **Fase de Reparación**: Elige armas dañadas para reparar usando combinaciones específicas de recursos
3. **Fase de Reemplazo**: Cuando el inventario está lleno, el algoritmo MFU elimina automáticamente el recurso más usado

## Estructura del Proyecto

```
MFU/
├── assets/
│   ├── audio/       # Efectos de sonido y música del juego
│   │   ├── lose_point.mp3         # Sonido al perder vida
│   │   ├── obtener_elemento.mp3   # Sonido al obtener elemento (opción 1)
│   │   ├── obtener_elemento_2.mp3 # Sonido al obtener elemento (opción 2)
│   │   └── point.mp3              # Sonido al ganar puntos
│   └── images/      # Sprites y elementos de UI
│       ├── Character/             # Imágenes de celebración del personaje
│       │   ├── celebracion_1.png  # Frame 1 de celebración
│       │   ├── celebracion_2.png  # Frame 2 de celebración
│       │   ├── celebracion_3.png  # Frame 3 de celebración
│       │   ├── celebracion_4.png  # Frame 4 de celebración
│       │   └── celebracion_5.png  # Frame 5 de celebración
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
│       └── asset_loader.py      # Utilidades para cargar assets
└── main.py          # Punto de entrada del juego
```

## Documentación Detallada del Código

### Configuraciones Generales
- **src/core/config.py**: Contiene todas las configuraciones del juego:
  - Líneas 13-14: Configuración de pantalla (ancho y alto)
  - Línea 15: FPS del juego
  - Líneas 18-22: Colores utilizados en el juego
  - Líneas 25-29: Mecánicas del juego (tamaño de inventario, intervalo de envejecimiento, etc.)
  - Líneas 32-33: Configuración del jugador (salud máxima, armas para ganar)
  - Líneas 36-37: Rutas de assets
  - Líneas 79-84: Definición de tipos de recursos con nombres, rareza y colores
  - Líneas 87-113: Definición de tipos de armas, requisitos y puntos

### Gestión de Recursos y Armas
- **src/entities/resource.py**: Define la clase Resource con:
  - Contador de uso que aumenta cuando se usa un recurso
  - Umbral tóxico que determina cuándo un recurso es peligroso de reemplazar
  
- **src/entities/weapon.py**: Define la clase Weapon con:
  - Estados de arma (normal, oxidada, destruida)
  - Requisitos de recursos para reparación
  - Método de reparación que consume recursos

### Sistema de Daño y Pérdida de Vida
- **src/core/game.py**: 
  - Líneas 125-144: Método `apply_aging()` que maneja el envejecimiento de recursos y armas
  - Líneas 139-144: Cuando un arma se destruye, el jugador pierde 1 punto de salud y se reproduce el sonido de pérdida
  - Líneas 146-149: Método `check_game_over()` que verifica si la salud del jugador llegó a 0
  
- **src/scenes/collection_scene.py**:
  - Líneas 101-111: Daño al jugador cuando recolecta recursos tóxicos o núcleos radioactivos

### Animaciones y Efectos de Sonido
- **src/core/game.py**:
  - Líneas 55-59: Inicialización del estado de celebración
  - Líneas 155-164: Método `start_celebration()` que inicia la animación y reproduce el sonido
  - Líneas 166-172: Método `play_obtain_element_sound()` que reproduce un sonido aleatorio al obtener un elemento
  - Líneas 174-178: Método `play_lose_point_sound()` que reproduce el sonido al perder vida
  - Líneas 105-115: Actualización de la animación de celebración en el bucle principal

- **src/scenes/workshop_scene.py**:
  - Líneas 106-115: Renderizado de la animación de celebración o personaje normal
  - Líneas 118-119: Inicio de la celebración cuando se repara un arma

### Escenas del Juego
- **src/scenes/workshop_scene.py**: Escena principal del taller donde:
  - Se reparan armas usando recursos del inventario
  - Se ganan puntos al reparar armas
  - Se inicia la animación de celebración al reparar un arma

- **src/scenes/collection_scene.py**: Escena de recolección donde:
  - El jugador se mueve para recolectar recursos que caen
  - Se reproducen sonidos al obtener elementos
  - Se puede perder salud al recolectar elementos peligrosos

### Interfaz de Usuario
- **src/ui/status_panel.py**: Panel de estado que muestra:
  - Salud del jugador (líneas 64-71)
  - Puntuación y armas reparadas (líneas 73-88)
  - Temporizador de oxidación (líneas 90-102)
  - Botones de navegación (líneas 104-115)

- **src/ui/repair_panel.py**: Panel de reparación que muestra:
  - Armas disponibles para reparar (líneas 73-113)
  - Botón de reparación (líneas 115-122)

- **src/ui/inventory_panel.py**: Panel de inventario que muestra:
  - Recursos en el inventario (líneas 60-107)
  - Barra de contador para cada recurso (líneas 93-107)

## Objetivos del Juego

- **Condición de Victoria**: Reparar 10 armas para equipar a tu facción y resistir un ataque final de mutantes
- **Condición de Derrota**: 
  - Salud agotada (por reemplazos tóxicos de recursos)
  - No reparar suficientes armas antes del límite de tiempo

## Elementos Estratégicos

- No sobreutilizar un solo tipo de recurso (contador alto = candidato para eliminación)
- Equilibrar el envejecimiento usando recursos antes de que se oxiden demasiado
- Priorizar estratégicamente recursos raros como núcleos radioactivos

## Instalación y Ejecución

1. Asegúrate de tener Python 3.6+ y Pygame instalados
2. Clona este repositorio
3. Ejecuta `python main.py` para iniciar el juego

## Controles

- **Escena del Taller**:
  - Ratón: Seleccionar recursos y armas, hacer clic en el botón de reparación
  - Tecla C: Cambiar a la escena de recolección

- **Escena de Recolección**:
  - Flechas Izquierda/Derecha: Mover al jugador
  - Tecla W: Cambiar a la escena del taller