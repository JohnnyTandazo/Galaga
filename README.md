#DESARROLLADO POR:

TANDAZO ROJAS JOHNNY 

PRADO ALCIVAR STEVEEN

# 🚀  Juego de Naves Espaciales

Un juego de naves espaciales inspirado en el clásico Galaga, desarrollado en Python con Pygame. Incluye múltiples tipos de enemigos, jefes finales, power-ups, efectos visuales y un sistema de puntuación.

## 📋 Características

### 🎮 Modos de Juego
- **Modo Historia**: Progresa a través de niveles con dificultad creciente


### 👾 Enemigos Variados
- **Enemigos básicos**: Movimiento simple hacia abajo
- **Moscas**: Enemigos rápidos con animación fluida
- **BC (Battle Cruiser)**: Enemigos que disparan proyectiles diagonales
- **Bichos Rojos**: Enemigos con animación y resistencia media
- **Bichos Verdes**: Enemigos ágiles con patrones de movimiento únicos

### 🏆 Jefes Finales
- Aparecen cada 3 niveles a partir del nivel 10
- **Sistema de fases**: Los jefes cambian su comportamiento según su vida restante
- **Múltiples ataques**: Disparos normales, misiles dirigidos, balas perseguidoras
- **Invocación de enemigos**: Los jefes pueden invocar refuerzos
- **Escalado de dificultad**: Cada jefe es más poderoso que el anterior

### 💎 Power-ups
- **Vida Extra**: Aumenta las vidas del jugador
- **Velocidad**: Incrementa temporalmente la velocidad de movimiento
- **Escudo**: Protección temporal contra un impacto
- **Más Daño**: Elimina todos los enemigos en pantalla

### 🎵 Audio y Efectos
- Música de fondo para menús y gameplay
- Efectos de sonido para disparos, explosiones y power-ups
- Sistema de pausa con control de audio

### 🎨 Gráficos y Animaciones
- Sprites animados para enemigos y efectos
- Explosiones con múltiples frames
- Fondo en movimiento con objetos decorativos
- Interfaz de usuario completa con iconos

## 🕹️ Controles

### Durante el Juego
- **Flechas direccionales**: Mover la nave
- **Espacio**: Disparar
- **ESC**: Pausar/Reanudar el juego
- **Botón de Pausa**: Click en el botón superior derecho

### En los Menús
- **Click del mouse**: Navegar por las opciones
- **ESC**: Volver al menú anterior (en algunas pantallas)

## 📁 Estructura del Proyecto

\`\`\`
galaga_mejorado/
├── main.py              # Archivo principal de ejecución
├── config.py            # Configuración y constantes del juego
├── resources.py         # Gestión de recursos (imágenes, sonidos, fuentes)
├── entities.py          # Clases de entidades (Jefe Final, generación de enemigos)
├── game_logic.py        # Lógica principal del juego
├── ui.py               # Interfaz de usuario y menús
├── README.md           # Este archivo
└── assets/             # Carpeta con todos los recursos
    ├── PNG/            # Imágenes del juego
    ├── TRACKS/         # Música de fondo
    └── Bonus/          # Sonidos y fuentes
\`\`\`

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.7 o superior
- Pygame

### Instalación
1. Clona o descarga el proyecto
2. Instala Pygame:
   \`\`\`bash
   pip install pygame
   \`\`\`
3. Asegúrate de que la carpeta `assets` esté en el directorio del juego
4. Ejecuta el juego:
   \`\`\`bash
   python main.py
   \`\`\`

## 🎯 Sistema de Puntuación

- **Enemigo básico**: 10 puntos
- **Enemigos especiales**: 10 puntos
- **Impacto al jefe**: 5 puntos
- **Derrotar al jefe**: 500-1000+ puntos (según el nivel)
- **Power-up de Más Daño**: 50 puntos adicionales

## 🏅 Sistema de Niveles

### Modo Historia
- **Nivel 1-3**: Enemigos básicos con dificultad creciente
- **Nivel 4, 7, 10...**: Aparición de jefes finales
- **Escalado**: Cada nivel aumenta la velocidad y cantidad de enemigos


## 🔧 Configuración

El archivo `config.py` contiene todas las constantes del juego que puedes modificar:

- **Dimensiones de pantalla**: `ANCHO`, `ALTO`
- **Velocidades**: Nave, enemigos, proyectiles
- **Tiempos**: Aparición de power-ups, duración de efectos
- **Dificultad**: Vida de jefes, daño de proyectiles

## 🎨 Personalización

### Agregar Nuevos Enemigos
1. Añade las imágenes en la carpeta `assets/PNG/`
2. Modifica `resources.py` para cargar las nuevas imágenes
3. Actualiza `entities.py` para incluir el nuevo tipo en la generación

### Modificar Jefes
- Ajusta las constantes en `config.py` para cambiar la dificultad
- Modifica `entities.py` para cambiar patrones de ataque
- Cambia las imágenes en `assets/PNG/Shooter/`

### Nuevos Power-ups
1. Añade la imagen del power-up en `assets/PNG/c2/PNG/Ship_Parts/`
2. Actualiza `resources.py` para cargar la imagen
3. Implementa la lógica en `game_logic.py`

## 🐛 Solución de Problemas

### El juego no inicia
- Verifica que Pygame esté instalado: `pip install pygame`
- Asegúrate de que la carpeta `assets` esté presente
- Comprueba que tienes Python 3.7 o superior

### No hay sonido
- Verifica que los archivos de audio estén en `assets/TRACKS/` y `assets/Bonus/`
- Algunos sistemas pueden requerir codecs adicionales para ciertos formatos

### Rendimiento lento
- Reduce el número de objetos decorativos en `config.py`
- Ajusta la resolución de pantalla si es necesario

## 📝 Notas de Desarrollo

### Arquitectura Modular
El juego está diseñado con una arquitectura modular que separa:
- **Lógica de juego** (`game_logic.py`)
- **Gestión de recursos** (`resources.py`)
- **Entidades del juego** (`entities.py`)
- **Interfaz de usuario** (`ui.py`)
- **Configuración** (`config.py`)

### Sistema de Estados
- El juego maneja diferentes estados (menú, jugando, pausado, game over)
- Cada estado tiene su propia lógica de eventos y renderizado

### Gestión de Memoria
- Los recursos se cargan una vez al inicio
- Las listas de entidades se limpian automáticamente
- Sistema de fallback para recursos faltantes

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Reportar bugs
- Sugerir nuevas características
- Mejorar el código existente
- Añadir nuevos recursos gráficos o de audio

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🎮 ¡Disfruta el Juego!

¡Esperamos que disfrutes jugando Galaga Mejorado! Si tienes alguna pregunta o sugerencia, no dudes en contactarnos.

---
*Desarrollado con ❤️ usando Python y Pygame*
