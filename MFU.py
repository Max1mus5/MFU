import pygame
import sys
import random

pygame.init()

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MFU - Zelda Style")

# Fuente y colores
FONT = pygame.font.SysFont("PixelOperator", 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (30, 180, 60)

# Ruta de las imágenes
IMAGENES = {
    "Espada": "C:/Users/thepu/Desktop/Python/espada.png",
    "Escudo": "C:/Users/thepu/Desktop/Python/escudo.png",
    "Bomba": "C:/Users/thepu/Desktop/Python/bomba.png",
    "Arco": "C:/Users/thepu/Desktop/Python/arco.png",
    "Poción": "C:/Users/thepu/Desktop/Python/pocion.png"
}

# Redimensionar las imágenes a un tamaño adecuado
TAMANO_IMAGEN = (40, 40)  # Tamaño que le daremos a las imágenes

# Función para cargar las imágenes
def cargar_imagenes():
    cargadas = {}
    for item, path in IMAGENES.items():
        try:
            print(f"Cargando imagen: {path}")  # Depuración
            img = pygame.image.load(path)
            print(f"Tamaño original de {item}: {img.get_size()}")  # Verifica el tamaño original
            img = pygame.transform.scale(img, TAMANO_IMAGEN)
            print(f"Tamaño redimensionado de {item}: {img.get_size()}")  # Verifica el tamaño después de redimensionar
            cargadas[item] = img
            print(f"Imagen cargada: {item}")  # Depuración
        except pygame.error as e:
            print(f"Error al cargar la imagen {path}: {e}")
    return cargadas

# Cargar imágenes
IMAGENES_CARGADAS = cargar_imagenes()

# Clase de Inventario MFU
class InventarioMFU:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.inventario = {}

    def usar(self, item, jugador_pos):
        if item == "Espada":
            print(f"Usando {item}. ¡Atacando a los enemigos!")
            return "espada"
        elif item == "Bomba":
            print(f"Usando {item}. ¡Explosión!")
            return "bomba"
        elif item == "Arco":
            print(f"Usando {item}. ¡Disparando una flecha!")
            return "arco"
        elif item == "Escudo":
            print(f"Usando {item}. ¡Defendiéndose de un ataque!")
            return "escudo"
        elif item == "Poción":
            print(f"Usando {item}. ¡Curando al personaje!")
            return "pocion"
        else:
            return None

    def recoger(self, item):
        if item in self.inventario:
            print(f"{item} ya está en inventario.")
            return
        if len(self.inventario) >= self.capacidad:
            mfu = max(self.inventario, key=self.inventario.get)
            print(f"Inventario lleno. Eliminando '{mfu}' (MFU).")
            del self.inventario[mfu]
        self.inventario[item] = 0
        print(f"Recogiste {item}.")

# Dibuja el inventario en pantalla
def dibujar_inventario(inv):
    pygame.draw.rect(SCREEN, GRAY, (10, HEIGHT - 100, WIDTH - 20, 90))  # Área del inventario
    SCREEN.blit(FONT.render("Inventario MFU:", True, BLACK), (20, HEIGHT - 90))
    
    # Dibujar cada ítem
    for i, (item, usos) in enumerate(inv.inventario.items()):
        x = 40 + i * 150  # Posición horizontal
        y = HEIGHT - 60   # Posición vertical
        pygame.draw.rect(SCREEN, GRAY, (x, y, 120, 50), border_radius=10)  # Fondo del ítem
        
        # Asegúrate de que la imagen se dibuje correctamente
        if item in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS[item], (x + 5, y + 5))  # Dibujar la imagen
        else:
            print(f"Error: {item} no encontrado en IMAGENES_CARGADAS.")

# Dibuja el mundo y los ítems
# Dibuja el mundo y los ítems
def dibujar_mundo(jugador_pos, accion_actual):
    SCREEN.fill(GREEN)
    pygame.draw.circle(SCREEN, (255, 220, 100), jugador_pos, 20)  # Héroe
    
    if accion_actual == "espada":
        if "Espada" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Espada"], (jugador_pos[0] + 30, jugador_pos[1] - 20))
    elif accion_actual == "bomba":
        if "Bomba" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Bomba"], (jugador_pos[0] + 40, jugador_pos[1] - 10))
    elif accion_actual == "arco":
        if "Arco" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Arco"], (jugador_pos[0] + 30, jugador_pos[1] - 20))
    elif accion_actual == "escudo":
        if "Escudo" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Escudo"], (jugador_pos[0] - 40, jugador_pos[1] - 20))
    elif accion_actual == "pocion":
        if "Poción" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Poción"], (jugador_pos[0] - 40, jugador_pos[1] - 20))
    
    texto = FONT.render("Muévete con flechas o WASD | 1-5 para recoger | Click para usar", True, WHITE)
    SCREEN.blit(texto, (20, 20))


# Loop principal
def main():
    clock = pygame.time.Clock()
    inventario = InventarioMFU(3)
    jugador_x, jugador_y = WIDTH // 2, HEIGHT // 2
    velocidad = 5
    accion_actual = None

    while True:
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            jugador_x -= velocidad
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            jugador_x += velocidad
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            jugador_y -= velocidad
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            jugador_y += velocidad

        jugador_x = max(20, min(WIDTH - 20, jugador_x))
        jugador_y = max(20, min(HEIGHT - 120, jugador_y))  # Deja espacio para inventario

        dibujar_mundo((jugador_x, jugador_y), accion_actual)
        dibujar_inventario(inventario)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    index = event.key - pygame.K_1
                    ITEMS = ["Espada", "Escudo", "Bomba", "Arco", "Poción"]
                    inventario.recoger(ITEMS[index])
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, item in enumerate(inventario.inventario):
                    x = 40 + i * 150
                    y = HEIGHT - 60
                    if x <= mx <= x + 120 and y <= my <= y + 50:
                        accion_actual = inventario.usar(item, (jugador_x, jugador_y))

if __name__ == "__main__":
    main()
