"""
Lógica principal del juego
"""
import pygame
import math
import random
import json
import os
import sys
from config import *
from resources import resource_manager
from entities import JefeFinal, generar_enemigos_sin_superposicion

# Variables globales
VENTANA = None


def cargar_high_score():
    """Carga el high score desde archivo JSON"""
    try:
        if os.path.exists("high_score.json"):
            with open("high_score.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error cargando high score: {e}")
    return 0


def guardar_high_score(score):
    """Guarda el high score en archivo JSON"""
    try:
        with open("high_score.json", "w") as f:
            json.dump({"high_score": score}, f)
        print(f"High score guardado: {score}")
    except IOError as e:
        print(f"Error guardando high score: {e}")


def jugar(modo_juego):
    """Función principal del juego"""
    print("DEBUG: Iniciando función jugar().")
    global puntaje
    puntaje = 0
    high_score = cargar_high_score()

    # Variables de estado del juego
    nave_x = ANCHO // 2 - resource_manager.imagenes['nave'].get_width() // 2
    nave_y = ALTO - 100
    velocidad = VELOCIDAD_NAVE
    vidas = 3
    nivel = 1
    enemigos = []
    lasers = []
    powerups = []
    explosiones = []
    balas_enemigas = []

    # Variables del jefe
    jefe_activo = False
    jefe = None
    enemigos_por_oleada = 5
    enemigos_base_velocidad_actual = VELOCIDAD_ENEMIGO_BASE
    enemigos_maximos_en_pantalla = 10

    print(f"DEBUG_INICIO_JUGAR: Puntuacion: {puntaje}, High Score: {high_score}")
    print(f"DEBUG: Iniciando juego en modo: {modo_juego}")

    # Detener la música del menú si estaba sonando
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    # Cargar y reproducir la música del juego
    try:
        pygame.mixer.music.load("assets/TRACKS/megatracks/spaceship.wav")
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música del juego")

    ejecutando = True
    fondo_y = 0
    clock = pygame.time.Clock()

    # Inicialización de la decoración
    NUM_OBJETOS_DECORACION = 5
    objetos_decoracion = []
    if resource_manager.imagenes['decoracion']:
        for _ in range(NUM_OBJETOS_DECORACION):
            img_elegida = random.choice(resource_manager.imagenes['decoracion'])
            x = random.randint(0, ANCHO - img_elegida.get_width())
            y = random.randint(-ALTO, ALTO)
            velocidad_obj = random.uniform(0.2, 0.3)
            objetos_decoracion.append({
                "imagen": img_elegida,
                "x": x,
                "y": y,
                "velocidad": velocidad_obj
            })

    # Variables de tiempo para power-ups y efectos
    ultimo_tiempo_powerup = pygame.time.get_ticks()
    escudo_activo = False
    tiempo_escudo = 0
    tiempo_velocidad = 0

    # Variables específicas del modo
    if modo_juego == "historia":
        nuevos = generar_enemigos_sin_superposicion(enemigos_por_oleada, [], enemigos_base_velocidad_actual)
        enemigos.extend(nuevos)
        print(f"DEBUG: Primera oleada generada. Total enemigos: {len(enemigos)}.")
    elif modo_juego == "supervivencia":
        print(f"DEBUG: Modo supervivencia iniciado. Máx enemigos: {enemigos_maximos_en_pantalla}")

    # === VARIABLES PARA EL SISTEMA DE PAUSA ===
    juego_pausado = False
    boton_pausa_rect = None

    # Crear botón de pausa
    if 'retry_button' in resource_manager.imagenes:
        # Cambiar el tamaño del botón aquí (ancho, alto)
        tamaño_boton = (40, 40)  # Puedes cambiar estos valores
        boton_pausa_img = pygame.transform.scale(resource_manager.imagenes['retry_button'], tamaño_boton)
        boton_pausa_rect = boton_pausa_img.get_rect(topright=(ANCHO - 20, 80))

    # Bucle principal del juego
    while ejecutando:
        clock.tick(60)
        tiempo_actual = pygame.time.get_ticks()

        # === EVENTOS ===
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Pausar/reanudar con ESC
                    juego_pausado = not juego_pausado
                    if juego_pausado:
                        print("Juego pausado")
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                    else:
                        print("Juego reanudado")
                        pygame.mixer.music.unpause()

                elif evento.key == pygame.K_SPACE and not juego_pausado:
                    lasers.append({
                        "x": nave_x + resource_manager.imagenes['nave'].get_width() // 2 - resource_manager.imagenes[
                            'laser'].get_width() // 2,
                        "y": nave_y
                    })
                    resource_manager.reproducir_sonido('laser')

            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en el botón de pausa
                if boton_pausa_rect and boton_pausa_rect.collidepoint(evento.pos):
                    juego_pausado = not juego_pausado
                    if juego_pausado:
                        print("Juego pausado (botón)")
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                    else:
                        print("Juego reanudado (botón)")
                        pygame.mixer.music.unpause()

        # Si el juego está pausado, mostrar pantalla de pausa y saltar el resto del bucle
        if juego_pausado:
            # Dibujar pantalla de pausa
            mostrar_pantalla_pausa()
            continue

        # === MOVIMIENTO DE LA NAVE ===
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_x > 0:
            nave_x -= velocidad
        if teclas[pygame.K_RIGHT] and nave_x < ANCHO - resource_manager.imagenes['nave'].get_width():
            nave_x += velocidad
        if teclas[pygame.K_UP] and nave_y > 0:
            nave_y -= velocidad
        if teclas[pygame.K_DOWN] and nave_y < ALTO - resource_manager.imagenes['nave'].get_height():
            nave_y += velocidad

        # === MOVIMIENTO DE LÁSERES ===
        for laser in lasers[:]:
            laser["y"] -= VELOCIDAD_LASER
            if laser["y"] < 0:
                lasers.remove(laser)

        # === LÓGICA DE GENERACIÓN DE ENEMIGOS ===
        if modo_juego == "historia":
            if len(enemigos) == 0 and not jefe_activo:
                nivel += 1

                if nivel >= NIVEL_APARICION_JEFE and (nivel - NIVEL_APARICION_JEFE) % 3 == 0:
                    jefe = JefeFinal(
                        nivel,
                        resource_manager.imagenes['jefe'],
                        resource_manager.frames['boss_bullet'],
                        resource_manager.frames['boss_missile'],
                        resource_manager.imagenes['boss_homing_bullet']
                    )
                    jefe_activo = True
                    print(f"¡JEFE APARECE EN EL NIVEL {nivel}!")
                else:
                    enemigos_por_oleada += 1
                    enemigos_base_velocidad_actual += 0.2
                    nuevos = generar_enemigos_sin_superposicion(enemigos_por_oleada, [], enemigos_base_velocidad_actual)
                    enemigos.extend(nuevos)
                    print(f"DEBUG: Nivel {nivel}. Enemigos generados: {len(nuevos)}")

        elif modo_juego == "supervivencia":
            if len(enemigos) < enemigos_maximos_en_pantalla:
                velocidad_actual_enemigo = VELOCIDAD_ENEMIGO_BASE + (puntaje // 100) * 0.1
                cantidad_a_generar = random.randint(1, 3) if puntaje < 500 else random.randint(2, 4)
                nuevos = generar_enemigos_sin_superposicion(cantidad_a_generar, enemigos, velocidad_actual_enemigo)
                enemigos.extend(nuevos)

        # === ACTUALIZACIÓN DEL JEFE ===
        if jefe_activo and jefe and not jefe.derrotado:
            jefe.actualizar(tiempo_actual, nave_x, nave_y)
        elif jefe_activo and jefe and jefe.derrotado:
            jefe_activo = False
            jefe = None
            puntaje += 500
            print("DEBUG: Jefe derrotado. Continuando al siguiente nivel.")

        # === DIBUJO DEL FONDO ===
        fondo_y += VELOCIDAD_FONDO
        if fondo_y >= ALTO:
            fondo_y = 0
        VENTANA.blit(resource_manager.imagenes['fondo'], (0, fondo_y))
        VENTANA.blit(resource_manager.imagenes['fondo'], (0, fondo_y - ALTO))

        # === DIBUJO DE DECORACIÓN ===
        for obj in objetos_decoracion:
            obj["y"] += obj["velocidad"] + VELOCIDAD_FONDO * 0.2
            VENTANA.blit(obj["imagen"], (obj["x"], obj["y"]))

            if obj["y"] > ALTO:
                obj["y"] = random.randint(-obj["imagen"].get_height() * 2, -obj["imagen"].get_height())
                obj["x"] = random.randint(0, ANCHO - obj["imagen"].get_width())
                obj["imagen"] = random.choice(resource_manager.imagenes['decoracion'])
                obj["velocidad"] = random.uniform(0.1, 0.5)

        # === DIBUJO DE ENEMIGOS ===
        for enemigo in enemigos:
            # Calcular desplazamiento oscilante
            oscilacion_x = 70 * math.sin((pygame.time.get_ticks() + enemigo["fase"] * 100) / 400)
            current_oscilacion_y = 5 * math.sin((pygame.time.get_ticks() + enemigo["fase"] * 50) / 100)

            if enemigo["tipo"] == "mosca":
                current_oscilacion_y = 0.5 * math.sin((pygame.time.get_ticks() + enemigo["fase"] * 50) / 100)

            x_dibujado = enemigo["x"] + oscilacion_x
            y_dibujado = enemigo["y"] + current_oscilacion_y

            if enemigo["tipo"] == "mosca":
                # Animación de la mosca
                if tiempo_actual - enemigo["ultimo_update_animacion"] > 70:
                    enemigo["frame_actual"] = (enemigo["frame_actual"] + 1) % len(resource_manager.frames['mosca'])
                    enemigo["ultimo_update_animacion"] = tiempo_actual
                VENTANA.blit(resource_manager.frames['mosca'][enemigo["frame_actual"]], (x_dibujado, y_dibujado))
            elif enemigo["tipo"] == "bc":
                # Animación del bc
                if tiempo_actual - enemigo["ultimo_update_animacion"] > 100:
                    enemigo["frame_actual"] = (enemigo["frame_actual"] + 1) % len(resource_manager.frames['bc'])
                    enemigo["ultimo_update_animacion"] = tiempo_actual
                VENTANA.blit(resource_manager.frames['bc'][enemigo["frame_actual"]], (x_dibujado, y_dibujado))
            elif enemigo["tipo"] == "bichorojo":
                # Animación del bichorojo
                if tiempo_actual - enemigo["ultimo_update_animacion"] > 120:
                    enemigo["frame_actual"] = (enemigo["frame_actual"] + 1) % len(resource_manager.frames['bichorojo'])
                    enemigo["ultimo_update_animacion"] = tiempo_actual
                VENTANA.blit(resource_manager.frames['bichorojo'][enemigo["frame_actual"]], (x_dibujado, y_dibujado))
            elif enemigo["tipo"] == "bichoverde":
                # Animación del bichoverde
                if tiempo_actual - enemigo["ultimo_update_animacion"] > 90:
                    enemigo["frame_actual"] = (enemigo["frame_actual"] + 1) % len(resource_manager.frames['bichoverde'])
                    enemigo["ultimo_update_animacion"] = tiempo_actual
                VENTANA.blit(resource_manager.frames['bichoverde'][enemigo["frame_actual"]], (x_dibujado, y_dibujado))
            else:  # Enemigo normal
                VENTANA.blit(resource_manager.imagenes['enemigo'], (x_dibujado, y_dibujado))

        # === DIBUJO DEL JEFE ===
        if jefe_activo and jefe and not jefe.derrotado:
            # Dibujar el jefe
            VENTANA.blit(jefe.img, (jefe.x, jefe.y))

            # Barra de vida del jefe
            barra_ancho = 300
            barra_alto = 20
            barra_x = (ANCHO - barra_ancho) // 2
            barra_y = 30

            # Fondo de la barra (rojo oscuro)
            pygame.draw.rect(VENTANA, (100, 0, 0), (barra_x, barra_y, barra_ancho, barra_alto))

            # Vida actual (rojo brillante)
            vida_ancho = int((jefe.vidas_actual / jefe.vidas_max) * barra_ancho)
            pygame.draw.rect(VENTANA, (255, 0, 0), (barra_x, barra_y, vida_ancho, barra_alto))

            # Borde blanco
            pygame.draw.rect(VENTANA, (255, 255, 255), (barra_x, barra_y, barra_ancho, barra_alto), 2)

            # Texto "JEFE"
            texto_jefe = resource_manager.fuentes['juego'].render("JEFE", True, (255, 255, 255))
            VENTANA.blit(texto_jefe, (barra_x, barra_y - 25))

        # === DIBUJO DE PROYECTILES DEL JEFE ===
        if jefe_activo and jefe:
            # Dibujar balas normales
            for bala in jefe.balas_normales:
                frame_idx = min(bala["frame_actual"], len(jefe.bullet_frames) - 1)
                VENTANA.blit(resource_manager.frames['boss_bullet'][frame_idx], (bala["x"], bala["y"]))

            # Dibujar misiles
            for misil in jefe.misiles:
                frame_idx = min(misil["frame_actual"], len(jefe.missile_frames) - 1)
                VENTANA.blit(resource_manager.frames['boss_missile'][frame_idx], (misil["x"], misil["y"]))

            # Dibujar balas perseguidoras
            for bala in jefe.balas_perseguidoras:
                VENTANA.blit(resource_manager.imagenes['boss_homing_bullet'], (bala["x"], bala["y"]))

            # Dibujar enemigos invocados por el jefe
            for enemigo in jefe.enemigos_invocados:
                VENTANA.blit(resource_manager.imagenes['enemigo'], (enemigo["x"], enemigo["y"]))

        # === DIBUJO DE LA NAVE ===
        VENTANA.blit(resource_manager.imagenes['nave'], (nave_x, nave_y))

        # === DIBUJO DE LÁSERES ===
        for laser in lasers:
            VENTANA.blit(resource_manager.imagenes['laser'], (laser["x"], laser["y"]))

        # === COLISIONES LÁSER-ENEMIGO ===
        for laser in lasers[:]:
            laser_rect = pygame.Rect(laser["x"], laser["y"], resource_manager.imagenes['laser'].get_width(),
                                     resource_manager.imagenes['laser'].get_height())
            for enemigo in enemigos[:]:
                # Determinar la imagen correcta según el tipo de enemigo
                enemigo_actual_img = resource_manager.imagenes['enemigo']
                if enemigo["tipo"] == "mosca":
                    enemigo_actual_img = resource_manager.frames['mosca'][enemigo["frame_actual"]]
                elif enemigo["tipo"] == "bc":
                    enemigo_actual_img = resource_manager.frames['bc'][enemigo["frame_actual"]]
                elif enemigo["tipo"] == "bichorojo":
                    enemigo_actual_img = resource_manager.frames['bichorojo'][enemigo["frame_actual"]]
                elif enemigo["tipo"] == "bichoverde":
                    enemigo_actual_img = resource_manager.frames['bichoverde'][enemigo["frame_actual"]]

                # Calcular posición con oscilación
                oscilacion_x = 70 * math.sin((pygame.time.get_ticks() + enemigo["fase"] * 100) / 400)
                current_oscilacion_y = 5 * math.sin((pygame.time.get_ticks() + enemigo["fase"] * 50) / 100)
                if enemigo["tipo"] == "mosca":
                    current_oscilacion_y = 0.5 * math.sin((pygame.time.get_ticks() + enemigo["fase"] * 50) / 100)

                x_dibujado = enemigo["x"] + oscilacion_x
                y_dibujado = enemigo["y"] + current_oscilacion_y

                enemigo_rect = pygame.Rect(x_dibujado, y_dibujado, enemigo_actual_img.get_width(),
                                           enemigo_actual_img.get_height())

                if laser_rect.colliderect(enemigo_rect):
                    explosiones.append({
                        "x": enemigo["x"],
                        "y": enemigo["y"],
                        "frame": 0,
                        "ultimo_update": pygame.time.get_ticks()
                    })
                    resource_manager.reproducir_sonido('explosion')

                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                    if laser in lasers:
                        lasers.remove(laser)
                    puntaje += 10
                    break

        # === COLISIONES LÁSER-JEFE ===
        if jefe_activo and jefe and not jefe.derrotado:
            jefe_rect = jefe.obtener_rect()
            for laser in lasers[:]:
                laser_rect = pygame.Rect(laser["x"], laser["y"], resource_manager.imagenes['laser'].get_width(),
                                         resource_manager.imagenes['laser'].get_height())
                if laser_rect.colliderect(jefe_rect):
                    # El jefe recibe daño
                    if jefe.recibir_daño(10):
                        explosiones.append({
                            "x": jefe.x + jefe.ancho // 2,
                            "y": jefe.y + jefe.alto // 2,
                            "frame": 0,
                            "ultimo_update": pygame.time.get_ticks()
                        })
                        resource_manager.reproducir_sonido('explosion')

                        # Mostrar pantalla de victoria
                        from ui import mostrar_pantalla_victoria
                        decision = mostrar_pantalla_victoria(puntaje, nivel)
                        if decision == "continuar":
                            # Continuar jugando al siguiente nivel
                            jefe_activo = False
                            jefe = None
                            puntaje += 1000
                            nivel += 1
                            enemigos_por_oleada += 2
                            enemigos_base_velocidad_actual += 0.3
                            nuevos = generar_enemigos_sin_superposicion(enemigos_por_oleada, [],
                                                                        enemigos_base_velocidad_actual)
                            enemigos.extend(nuevos)
                            print(f"DEBUG: Continuando al nivel {nivel} después de derrotar al jefe.")
                        elif decision == "menu":
                            # Volver al menú principal
                            ejecutando = False
                            if puntaje > high_score:
                                high_score = puntaje
                                guardar_high_score(high_score)
                            from ui import main_menu
                            main_menu()
                            return

                    if laser in lasers:
                        lasers.remove(laser)
                    puntaje += 5
                    break

        # === MOVIMIENTO Y COLISIÓN DE ENEMIGOS CON EL JUGADOR ===
        for enemigo in enemigos[:]:
            enemigo["y"] += enemigo["velocidad_y"]

            if enemigo["y"] > ALTO:
                if modo_juego == "supervivencia":
                    vidas -= 1
                    resource_manager.reproducir_sonido('vida_perdida')
                if enemigo in enemigos:
                    enemigos.remove(enemigo)
                continue

            nave_rect = pygame.Rect(nave_x, nave_y, resource_manager.imagenes['nave'].get_width(),
                                    resource_manager.imagenes['nave'].get_height())
            enemigo_rect = pygame.Rect(enemigo["x"], enemigo["y"], 48, 48)

            if nave_rect.colliderect(enemigo_rect):
                if escudo_activo:
                    print("DEBUG: Colisión nave-enemigo bloqueada por escudo. Escudo desactivado.")
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                    escudo_activo = False
                else:
                    VENTANA.fill((255, 255, 255))
                    pygame.display.update()
                    pygame.time.delay(80)
                    resource_manager.reproducir_sonido('vida_perdida')
                    vidas -= 1
                    print(f"DEBUG: Colisión nave-enemigo. Vidas restantes: {vidas}.")
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                break

        # === LÓGICA DE DISPARO DE ENEMIGOS ===
        for enemigo in enemigos:
            if enemigo["y"] > 0 and enemigo["y"] < ALTO and \
                    enemigo.get("puede_disparar", False) and \
                    (tiempo_actual - enemigo.get("ultimo_disparo", 0)) > TIEMPO_DISPARO_ENEMIGO:

                if enemigo["tipo"] == "bc":
                    enemigo_ancho = resource_manager.frames['bc'][0].get_width()
                    enemigo_alto = resource_manager.frames['bc'][0].get_height()

                    puntos_disparo = [
                        (enemigo["x"] + resource_manager.imagenes['laser_enemigo'].get_width() / 2,
                         enemigo["y"] + resource_manager.imagenes['laser_enemigo'].get_height() / 2),
                        (enemigo["x"] + enemigo_ancho - resource_manager.imagenes['laser_enemigo'].get_width() * 1.5,
                         enemigo["y"] + resource_manager.imagenes['laser_enemigo'].get_height() / 2),
                        (enemigo["x"] + resource_manager.imagenes['laser_enemigo'].get_width() / 2,
                         enemigo["y"] + enemigo_alto - resource_manager.imagenes['laser_enemigo'].get_height() * 1.5),
                        (enemigo["x"] + enemigo_ancho - resource_manager.imagenes['laser_enemigo'].get_width() * 1.5,
                         enemigo["y"] + enemigo_alto - resource_manager.imagenes['laser_enemigo'].get_height() * 1.5)
                    ]

                    velocidades_diagonales = [
                        {"vx": -VELOCIDAD_LASER_ENEMIGO * 0.5, "vy": VELOCIDAD_LASER_ENEMIGO},
                        {"vx": VELOCIDAD_LASER_ENEMIGO * 0.5, "vy": VELOCIDAD_LASER_ENEMIGO},
                        {"vx": -VELOCIDAD_LASER_ENEMIGO * 0.2, "vy": VELOCIDAD_LASER_ENEMIGO * 0.8},
                        {"vx": VELOCIDAD_LASER_ENEMIGO * 0.2, "vy": VELOCIDAD_LASER_ENEMIGO * 0.8}
                    ]

                    for i in range(len(puntos_disparo)):
                        bala_x, bala_y = puntos_disparo[i]
                        velocidad_dict = velocidades_diagonales[i]

                        balas_enemigas.append({
                            "x": bala_x,
                            "y": bala_y,
                            "vx": velocidad_dict["vx"],
                            "vy": velocidad_dict["vy"]
                        })

                    enemigo["ultimo_disparo"] = tiempo_actual

        # === ACTUALIZAR BALAS ENEMIGAS ===
        for i in range(len(balas_enemigas) - 1, -1, -1):
            bala = balas_enemigas[i]

            bala["x"] += bala["vx"]
            bala["y"] += bala["vy"]

            VENTANA.blit(resource_manager.imagenes['laser_enemigo'], (bala["x"], bala["y"]))

            nave_rect = pygame.Rect(nave_x, nave_y, resource_manager.imagenes['nave'].get_width(),
                                    resource_manager.imagenes['nave'].get_height())
            bala_rect = pygame.Rect(bala["x"], bala["y"], resource_manager.imagenes['laser_enemigo'].get_width(),
                                    resource_manager.imagenes['laser_enemigo'].get_height())

            if nave_rect.colliderect(bala_rect):
                if escudo_activo:
                    print("DEBUG: Colisión bala enemiga bloqueada por escudo. Escudo desactivado.")
                    escudo_activo = False
                else:
                    VENTANA.fill((255, 255, 255))
                    pygame.display.update()
                    pygame.time.delay(80)
                    resource_manager.reproducir_sonido('vida_perdida')
                    vidas -= 1
                    print(f"DEBUG: Colisión bala enemiga con nave. Vidas restantes: {vidas}.")

                balas_enemigas.pop(i)
                continue

            if (bala["y"] > ALTO or bala["y"] < -resource_manager.imagenes['laser_enemigo'].get_height() or
                    bala["x"] < -resource_manager.imagenes['laser_enemigo'].get_width() or bala["x"] > ANCHO):
                balas_enemigas.pop(i)

        # === COLISIONES PROYECTILES DEL JEFE CON LA NAVE ===
        if jefe_activo and jefe:
            nave_rect = pygame.Rect(nave_x, nave_y, resource_manager.imagenes['nave'].get_width(),
                                    resource_manager.imagenes['nave'].get_height())

            for bala in jefe.balas_normales[:]:
                bala_rect = pygame.Rect(bala["x"], bala["y"], 30, 30)
                if nave_rect.colliderect(bala_rect):
                    if escudo_activo:
                        escudo_activo = False
                    else:
                        VENTANA.fill((255, 255, 255))
                        pygame.display.update()
                        pygame.time.delay(80)
                        resource_manager.reproducir_sonido('vida_perdida')
                        vidas -= bala["daño"]
                    jefe.balas_normales.remove(bala)

            for misil in jefe.misiles[:]:
                misil_rect = pygame.Rect(misil["x"], misil["y"], 50, 50)
                if nave_rect.colliderect(misil_rect):
                    if escudo_activo:
                        escudo_activo = False
                    else:
                        VENTANA.fill((255, 255, 255))
                        pygame.display.update()
                        pygame.time.delay(80)
                        resource_manager.reproducir_sonido('vida_perdida')
                        vidas -= misil["daño"]
                    jefe.misiles.remove(misil)

            for bala in jefe.balas_perseguidoras[:]:
                bala_rect = pygame.Rect(bala["x"], bala["y"], 15, 15)
                if nave_rect.colliderect(bala_rect):
                    if escudo_activo:
                        escudo_activo = False
                    else:
                        VENTANA.fill((255, 255, 255))
                        pygame.display.update()
                        pygame.time.delay(80)
                        resource_manager.reproducir_sonido('vida_perdida')
                        vidas -= bala["daño"]
                    jefe.balas_perseguidoras.remove(bala)

        # === GESTIÓN DE POWER-UPS ===
        if tiempo_actual - ultimo_tiempo_powerup > TIEMPO_ENTRE_POWERUPS:
            tipo = random.choice(list(resource_manager.imagenes['powerups'].keys()))
            powerup_width = resource_manager.imagenes['powerups'][tipo].get_width()
            x = random.randint(0, ANCHO - powerup_width)
            y = random.randint(100, ALTO // 2)
            powerups.append({"tipo": tipo, "x": x, "y": y, "tiempo_creacion": tiempo_actual})
            ultimo_tiempo_powerup = tiempo_actual

        for p in powerups[:]:
            p["y"] += VELOCIDAD_POWERUP

            if p["y"] > ALTO:
                powerups.remove(p)
                continue

            VENTANA.blit(resource_manager.imagenes['powerups'][p["tipo"]], (p["x"], p["y"]))
            powerup_rect = pygame.Rect(p["x"], p["y"], resource_manager.imagenes['powerups'][p["tipo"]].get_width(),
                                       resource_manager.imagenes['powerups'][p["tipo"]].get_height())

            nave_rect = pygame.Rect(nave_x, nave_y, resource_manager.imagenes['nave'].get_width(),
                                    resource_manager.imagenes['nave'].get_height())
            if nave_rect.colliderect(powerup_rect):
                resource_manager.reproducir_sonido('powerup_recogido')

                if p["tipo"] == "vida":
                    vidas += 1
                elif p["tipo"] == "velocidad":
                    velocidad = VELOCIDAD_NAVE + 4
                    tiempo_velocidad = pygame.time.get_ticks()
                elif p["tipo"] == "escudo":
                    escudo_activo = True
                    tiempo_escudo = pygame.time.get_ticks()
                elif p["tipo"] == "mas_dano":
                    enemigos.clear()
                    explosiones.clear()
                    puntaje += 50

                powerups.remove(p)

            elif tiempo_actual - p["tiempo_creacion"] > DURACION_POWERUP_EN_PANTALLA:
                powerups.remove(p)

        # === GESTIÓN DE EFECTOS DE POWER-UPS ===
        if velocidad != VELOCIDAD_NAVE and pygame.time.get_ticks() - tiempo_velocidad > DURACION_POWERUP_VELOCIDAD:
            velocidad = VELOCIDAD_NAVE

        if escudo_activo:
            escudo_x = nave_x - (resource_manager.imagenes['escudo'].get_width() - resource_manager.imagenes[
                'nave'].get_width()) // 2
            escudo_y = nave_y - (resource_manager.imagenes['escudo'].get_height() - resource_manager.imagenes[
                'nave'].get_height()) // 2
            VENTANA.blit(resource_manager.imagenes['escudo'], (escudo_x, escudo_y))

            if pygame.time.get_ticks() - tiempo_escudo > DURACION_POWERUP_ESCUDO:
                escudo_activo = False

        # === GESTIÓN DE EXPLOSIONES ===
        for e in explosiones[:]:
            frame = resource_manager.frames['explosion'][e["frame"]]

            x = e["x"] + 48 // 2 - frame.get_width() // 2
            y = e["y"] + 48 // 2 - frame.get_height() // 2
            VENTANA.blit(frame, (x, y))

            if pygame.time.get_ticks() - e["ultimo_update"] > 50:
                e["frame"] += 1
                e["ultimo_update"] = pygame.time.get_ticks()
            if e["frame"] >= len(resource_manager.frames['explosion']):
                explosiones.remove(e)

        # === MOSTRAR UI ===
        texto_puntaje = resource_manager.fuentes['juego'].render(f"Puntaje: {puntaje}", True, BLANCO)
        VENTANA.blit(texto_puntaje, (10, 10))

        VENTANA.blit(resource_manager.imagenes['vida_icono'], (10, 45))
        texto_vidas = resource_manager.fuentes['juego'].render(f"x {vidas}", True, BLANCO)
        VENTANA.blit(texto_vidas, (50, 45))

        if modo_juego == "historia":
            texto_nivel = resource_manager.fuentes['juego'].render(f"Nivel: {nivel}", True, BLANCO)
            VENTANA.blit(texto_nivel, (ANCHO - texto_nivel.get_width() - 10, 10))
        else:
            texto_modo = resource_manager.fuentes['juego'].render("Modo: Supervivencia", True, BLANCO)
            VENTANA.blit(texto_modo, (ANCHO - texto_modo.get_width() - 10, 10))

        # === DIBUJAR BOTÓN DE PAUSA ===
        if boton_pausa_rect:
            VENTANA.blit(boton_pausa_img, boton_pausa_rect)

            # Dibujar texto "PAUSA" debajo del botón
            texto_pausa = resource_manager.fuentes['record_num'].render("PAUSA", True, BLANCO)
            texto_pausa_rect = texto_pausa.get_rect(
                midtop=(boton_pausa_rect.centerx, boton_pausa_rect.bottom + 5)
            )
            VENTANA.blit(texto_pausa, texto_pausa_rect)

        pygame.display.update()

        # === VERIFICAR GAME OVER ===
        if vidas <= 0:
            print(f"DEBUG_FIN_JUGAR: GAME OVER. Puntuacion final: {puntaje}")
            pygame.mixer.music.stop()

            if puntaje > high_score:
                high_score = puntaje
                guardar_high_score(high_score)

            from ui import game_lose_screen
            game_lose_screen(puntaje)
            ejecutando = False
            return


def mostrar_pantalla_pausa():
    """Muestra la pantalla de pausa"""
    # Crear una superficie semitransparente para oscurecer el juego
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Negro semitransparente
    VENTANA.blit(overlay, (0, 0))



    # Instrucciones
    instrucciones = [
        "Presiona ESC para continuar",
        "Controles:",
        "Flechas - Mover nave",
        "Espacio - Disparar"
    ]

    y_offset = ALTO // 2
    for instruccion in instrucciones:
        texto = resource_manager.fuentes['record_num'].render(instruccion, True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO // 2, y_offset))
        VENTANA.blit(texto, texto_rect)
        y_offset += 40

    pygame.display.update()
