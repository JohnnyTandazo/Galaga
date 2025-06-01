"""
Archivo principal del juego Galaga Style
"""
import pygame
import sys
from config import ANCHO, ALTO
from resources import resource_manager
from ui import main_menu


def inicializar_pygame():
    """Inicializa pygame y crea la ventana principal"""
    pygame.init()

    # Crear ventana
    global VENTANA
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Galaga Style - Argely")

    print("Pygame inicializado correctamente")


def main():
    """Función principal del programa"""
    try:
        # Inicializar pygame
        inicializar_pygame()

        # Cargar recursos
        if not resource_manager.cargar_todos_los_recursos():
            print("Error: No se pudieron cargar los recursos del juego")
            return

        # Hacer la ventana accesible globalmente
        import config
        config.VENTANA = VENTANA

        import ui
        ui.VENTANA = VENTANA

        import game_logic
        game_logic.VENTANA = VENTANA

        # Iniciar el menú principal
        main_menu()

    except Exception as e:
        print(f"Error crítico en el juego: {e}")
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    main()