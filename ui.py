"""
Interfaz de usuario y menús del juego
"""
import pygame
import sys
from config import *
from resources import resource_manager

# Variable global para la ventana
VENTANA = None


def main_menu():
    """Muestra el menú principal del juego"""
    print("DEBUG: Entrando al Main Menu (con imágenes).")
    menu_activo = True
    clock = pygame.time.Clock()

    while menu_activo:
        # Dibujar el fondo
        VENTANA.blit(resource_manager.imagenes['background'], (0, 0))

        # Dibujar el título
        header_rect = resource_manager.imagenes['header'].get_rect(center=(ANCHO // 2, ALTO * 0.2))
        VENTANA.blit(resource_manager.imagenes['header'], header_rect)

        # Dibujar el botón de Inicio
        start_button_rect = resource_manager.imagenes['start_button'].get_rect(center=(ANCHO // 2, ALTO * 0.5))
        VENTANA.blit(resource_manager.imagenes['start_button'], start_button_rect)

        # Dibujar el botón de Salir
        exit_button_rect = resource_manager.imagenes['exit_button'].get_rect(center=(ANCHO // 2, ALTO * 0.7))
        VENTANA.blit(resource_manager.imagenes['exit_button'], exit_button_rect)

        # Actualizar la pantalla
        pygame.display.update()

        # Detectar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos

                if start_button_rect.collidepoint(mouse_pos):
                    print("DEBUG: ¡Click en Iniciar Juego (Modo Historia)!")
                    from game_logic import jugar
                    jugar("historia")
                    menu_activo = False

                elif exit_button_rect.collidepoint(mouse_pos):
                    print("DEBUG: ¡Click en Salir del Juego!")
                    pygame.quit()
                    sys.exit()

        clock.tick(60)


def game_lose_screen(puntuacion_final):
    """Muestra la pantalla de Game Over"""
    print(f"DEBUG: Entrando a la pantalla de Game Over. Puntuación: {puntuacion_final}")
    screen_active = True
    clock = pygame.time.Clock()

    # Cargar high score actual
    from game_logic import cargar_high_score, guardar_high_score
    high_score_actual = cargar_high_score()

    # Actualizar high score si es necesario
    if puntuacion_final > high_score_actual:
        high_score_actual = puntuacion_final
        guardar_high_score(high_score_actual)
        print(f"¡NUEVO RÉCORD! {high_score_actual}")

    # Detener la música del juego si estaba sonando
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    while screen_active:
        VENTANA.blit(resource_manager.imagenes['background'], (0, 0))

        # Dibujar la ventana emergente de Game Over
        window_rect = resource_manager.imagenes['game_over_window'].get_rect(center=(ANCHO // 2, ALTO // 2))
        VENTANA.blit(resource_manager.imagenes['game_over_window'], window_rect)

        # Título "GAME OVER"
        titulo_game_over = resource_manager.fuentes['juego'].render("GAME OVER", True, (255, 0, 0))
        titulo_rect = titulo_game_over.get_rect(
            center=(window_rect.centerx, window_rect.top + window_rect.height * 0.09)
        )
        VENTANA.blit(titulo_game_over, titulo_rect)

        # Título "Record" - usar imagen si está disponible, sino texto
        if resource_manager.imagenes.get('record_title'):
            record_title_rect = resource_manager.imagenes['record_title'].get_rect(
                center=(window_rect.centerx, titulo_rect.bottom + 30)
            )
            VENTANA.blit(resource_manager.imagenes['record_title'], record_title_rect)
        else:
            record_text = resource_manager.fuentes['juego'].render("RECORD", True, BLANCO)
            record_title_rect = record_text.get_rect(
                center=(window_rect.centerx, titulo_rect.bottom + 30)
            )
            VENTANA.blit(record_text, record_title_rect)

        # High Score - usar tabla si está disponible, sino rectángulo simple
        if resource_manager.imagenes.get('table'):
            high_score_table_rect = resource_manager.imagenes['table'].get_rect(
                center=(window_rect.centerx, record_title_rect.bottom + 20)
            )
            VENTANA.blit(resource_manager.imagenes['table'], high_score_table_rect)
        else:
            high_score_table_rect = pygame.Rect(
                window_rect.centerx - 100,
                record_title_rect.bottom + 20,
                200, 40
            )
            pygame.draw.rect(VENTANA, (100, 100, 100), high_score_table_rect)
            pygame.draw.rect(VENTANA, BLANCO, high_score_table_rect, 2)

        # Número del high score
        texto_high_score_num = resource_manager.fuentes['record_num'].render(str(high_score_actual), True, BLANCO)
        texto_high_score_num_rect = texto_high_score_num.get_rect(center=high_score_table_rect.center)
        VENTANA.blit(texto_high_score_num, texto_high_score_num_rect)

        # Label "Score" - usar imagen si está disponible, sino texto
        if resource_manager.imagenes.get('score_label'):
            score_label_rect = resource_manager.imagenes['score_label'].get_rect(
                center=(window_rect.centerx, high_score_table_rect.bottom + 30)
            )
            VENTANA.blit(resource_manager.imagenes['score_label'], score_label_rect)
        else:
            score_text = resource_manager.fuentes['juego'].render("SCORE", True, BLANCO)
            score_label_rect = score_text.get_rect(
                center=(window_rect.centerx, high_score_table_rect.bottom + 30)
            )
            VENTANA.blit(score_text, score_label_rect)

        # Score actual - usar tabla si está disponible, sino rectángulo simple
        if resource_manager.imagenes.get('table'):
            current_score_table_rect = resource_manager.imagenes['table'].get_rect(
                center=(window_rect.centerx, score_label_rect.bottom + 20)
            )
            VENTANA.blit(resource_manager.imagenes['table'], current_score_table_rect)
        else:
            current_score_table_rect = pygame.Rect(
                window_rect.centerx - 100,
                score_label_rect.bottom + 20,
                200, 40
            )
            pygame.draw.rect(VENTANA, (100, 100, 100), current_score_table_rect)
            pygame.draw.rect(VENTANA, BLANCO, current_score_table_rect, 2)

        # Número del score actual
        texto_actual_score_num = resource_manager.fuentes['actual_score_num'].render(str(puntuacion_final), True,
                                                                                     BLANCO)
        texto_actual_score_num_rect = texto_actual_score_num.get_rect(center=current_score_table_rect.center)
        VENTANA.blit(texto_actual_score_num, texto_actual_score_num_rect)

        # Mensaje si es nuevo récord
        if puntuacion_final == high_score_actual and puntuacion_final > 0:
            nuevo_record_text = resource_manager.fuentes['juego'].render("¡NUEVO RÉCORD!", True, (255, 255, 0))
            nuevo_record_rect = nuevo_record_text.get_rect(
                center=(window_rect.centerx, current_score_table_rect.bottom + 20)
            )
            VENTANA.blit(nuevo_record_text, nuevo_record_rect)
            buttons_y_pos = nuevo_record_rect.bottom + 30
        else:
            buttons_y_pos = current_score_table_rect.bottom + 40

        # Botones
        retry_button_rect = resource_manager.imagenes['retry_button'].get_rect(
            center=(window_rect.centerx - 80, buttons_y_pos)
        )
        VENTANA.blit(resource_manager.imagenes['retry_button'], retry_button_rect)

        menu_button_rect = resource_manager.imagenes['menu_button'].get_rect(
            center=(window_rect.centerx + 80, buttons_y_pos)
        )
        VENTANA.blit(resource_manager.imagenes['menu_button'], menu_button_rect)

        # Etiquetas de los botones
        retry_text = resource_manager.fuentes['record_num'].render("REINTENTAR", True, BLANCO)
        retry_text_rect = retry_text.get_rect(center=(retry_button_rect.centerx, retry_button_rect.bottom + 15))
        VENTANA.blit(retry_text, retry_text_rect)

        menu_text = resource_manager.fuentes['record_num'].render("MENÚ", True, BLANCO)
        menu_text_rect = menu_text.get_rect(center=(menu_button_rect.centerx, menu_button_rect.bottom + 15))
        VENTANA.blit(menu_text, menu_text_rect)

        pygame.display.update()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if retry_button_rect.collidepoint(mouse_pos):
                    print("DEBUG: Reintentando juego desde pantalla Game Over.")
                    from game_logic import jugar
                    jugar("historia")
                    screen_active = False
                elif menu_button_rect.collidepoint(mouse_pos):
                    print("DEBUG: Volviendo al menú principal desde pantalla Game Over.")
                    main_menu()
                    screen_active = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    print("DEBUG: Reintentando juego con ESPACIO.")
                    from game_logic import jugar
                    jugar("historia")
                    screen_active = False
                elif evento.key == pygame.K_ESCAPE:
                    print("DEBUG: Volviendo al menú con ESC.")
                    main_menu()
                    screen_active = False


def mostrar_pantalla_victoria(puntuacion, nivel):
    """Muestra una pantalla de victoria después de derrotar al jefe final"""
    print(f"DEBUG: Mostrando pantalla de victoria. Puntuación: {puntuacion}, Nivel: {nivel}")

    pantalla_activa = True
    clock = pygame.time.Clock()

    # Detener la música del juego si estaba sonando
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    # Reproducir sonido de victoria si existe
    resource_manager.reproducir_sonido('powerup_escudo')

    # Fuentes más pequeñas para la pantalla de victoria
    try:
        fuente_titulo_victoria = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 24)
        fuente_texto_victoria = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 18)
        fuente_botones_victoria = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 16)
    except:
        fuente_titulo_victoria = pygame.font.Font(None, 32)
        fuente_texto_victoria = pygame.font.Font(None, 24)
        fuente_botones_victoria = pygame.font.Font(None, 20)

    while pantalla_activa:
        VENTANA.blit(resource_manager.imagenes['background'], (0, 0))

        # Dibujar la ventana emergente de Victoria
        window_rect = resource_manager.imagenes['game_over_window'].get_rect(center=(ANCHO // 2, ALTO // 2))
        VENTANA.blit(resource_manager.imagenes['game_over_window'], window_rect)

        # Título "¡VICTORIA!"
        titulo_victoria = fuente_titulo_victoria.render("¡VICTORIA!", True, (255, 255, 0))
        titulo_rect = titulo_victoria.get_rect(
            center=(window_rect.centerx, window_rect.top + window_rect.height * 0.2)
        )
        VENTANA.blit(titulo_victoria, titulo_rect)

        # Mensaje de felicitación
        mensaje = fuente_texto_victoria.render(f"¡Derrotaste al jefe en nivel {nivel}!", True, BLANCO)
        mensaje_rect = mensaje.get_rect(center=(window_rect.centerx, titulo_rect.bottom + 20))
        VENTANA.blit(mensaje, mensaje_rect)

        # Puntuación
        texto_puntuacion = fuente_texto_victoria.render(f"Puntuación: {puntuacion}", True, BLANCO)
        puntuacion_rect = texto_puntuacion.get_rect(center=(window_rect.centerx, mensaje_rect.bottom + 15))
        VENTANA.blit(texto_puntuacion, puntuacion_rect)

        # Mensaje adicional
        mensaje_extra = fuente_texto_victoria.render("¿Quieres continuar jugando?", True, BLANCO)
        mensaje_extra_rect = mensaje_extra.get_rect(center=(window_rect.centerx, puntuacion_rect.bottom + 15))
        VENTANA.blit(mensaje_extra, mensaje_extra_rect)

        # Instrucciones
        instrucciones1 = fuente_botones_victoria.render("ESPACIO = Continuar", True, (200, 200, 200))
        instrucciones1_rect = instrucciones1.get_rect(center=(window_rect.centerx, mensaje_extra_rect.bottom + 25))
        VENTANA.blit(instrucciones1, instrucciones1_rect)

        instrucciones2 = fuente_botones_victoria.render("ESC = Menú Principal", True, (200, 200, 200))
        instrucciones2_rect = instrucciones2.get_rect(center=(window_rect.centerx, instrucciones1_rect.bottom + 15))
        VENTANA.blit(instrucciones2, instrucciones2_rect)

        # Botones
        buttons_y_pos = instrucciones2_rect.bottom + 20

        continuar_button_rect = resource_manager.imagenes['retry_button'].get_rect(
            center=(window_rect.centerx - 80, buttons_y_pos)
        )
        VENTANA.blit(resource_manager.imagenes['retry_button'], continuar_button_rect)

        texto_continuar = fuente_botones_victoria.render("Continuar", True, BLANCO)
        texto_continuar_rect = texto_continuar.get_rect(
            center=(continuar_button_rect.centerx, continuar_button_rect.bottom + 10)
        )
        VENTANA.blit(texto_continuar, texto_continuar_rect)

        menu_button_rect = resource_manager.imagenes['menu_button'].get_rect(
            center=(window_rect.centerx + 80, buttons_y_pos)
        )
        VENTANA.blit(resource_manager.imagenes['menu_button'], menu_button_rect)

        texto_menu = fuente_botones_victoria.render("Menú", True, BLANCO)
        texto_menu_rect = texto_menu.get_rect(center=(menu_button_rect.centerx, menu_button_rect.bottom + 10))
        VENTANA.blit(texto_menu, texto_menu_rect)

        pygame.display.update()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "continuar"
                elif evento.key == pygame.K_ESCAPE:
                    return "menu"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if continuar_button_rect.collidepoint(mouse_pos):
                    print("DEBUG: Continuando juego después de victoria.")
                    return "continuar"
                elif menu_button_rect.collidepoint(mouse_pos):
                    print("DEBUG: Volviendo al menú principal desde pantalla de victoria.")
                    return "menu"
