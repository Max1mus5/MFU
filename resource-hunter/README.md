# Resource Hunter: Tactical Survival

Un juego de supervivencia táctica que implementa el algoritmo MFU (Most Frequently Used) como elemento central de gameplay.

## Concepto

En Resource Hunter, el jugador debe gestionar recursos limitados en un entorno hostil. El algoritmo MFU no es solo una implementación técnica, sino un elemento narrativo y estratégico:

- **Inventario con desgaste**: Los objetos más usados se desgastan y eventualmente se rompen.
- **Memoria de habilidades**: Las habilidades más utilizadas se vuelven automáticas pero menos efectivas.
- **Recursos con ciclo de vida**: Los recursos más utilizados se agotan más rápido.
- **Enemigos adaptativos**: Desarrollan resistencias contra tus ataques más frecuentes.

## Tecnologías

- JavaScript (ES6+)
- Phaser 3
- Webpack
- Jest (pruebas)

## Estructura del Proyecto

```
resource-hunter/
├─ public/                  # HTML y assets estáticos
├─ src/
│  ├─ main.js               # Punto de entrada
│  ├─ game/                 # Core del motor de juego
│  ├─ modules/              # Lógica modular del juego
│  │  ├─ inventory/         # Módulo MFU de inventario
│  │  ├─ skills/            # Módulo de habilidades y MFU mental
│  │  ├─ resources/         # Módulo de gestión de recursos con desgaste
│  │  └─ enemies/           # IA adaptativa y resistencias
│  ├─ ui/                   # Componentes UI
│  ├─ assets/               # Sprites, audio, configuración
│  └─ utils/                # Helpers genéricos
└─ tests/                   # Pruebas unitarias
```

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/resource-hunter.git

# Instalar dependencias
cd resource-hunter
npm install

# Iniciar servidor de desarrollo
npm start
```

## Algoritmo MFU

El algoritmo MFU (Most Frequently Used) es el núcleo del juego:

1. **Inventario**: Cuando está lleno y recoges un nuevo ítem, se elimina el ítem más usado.
2. **Habilidades**: Al aprender una nueva habilidad con memoria llena, se olvida la más usada.
3. **Recursos**: Los más utilizados se agotan más rápido, obligando a rotar su uso.
4. **Enemigos**: Adaptan sus defensas contra tus ataques más frecuentes.

Este diseño crea una tensión estratégica constante: usar demasiado algo significa arriesgarse a perderlo o a que se vuelva menos efectivo.

## Desarrollo

```bash
# Ejecutar pruebas
npm test

# Construir para producción
npm run build

# Linting
npm run lint

# Formatear código
npm run format
```

## Licencia

ISC