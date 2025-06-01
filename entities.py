"""
Entidades del juego: Nave, Enemigos, Jefe Final
"""
import pygame
import math
import random
from config import *


class JefeFinal:
    """Clase para el jefe final del juego"""

    def __init__(self, nivel, boss_img, boss_bullet_frames, boss_missile_frames, boss_homing_bullet_img):
        # Posición inicial
        self.x = ANCHO // 2 - 75
        self.y = -150
        self.img = boss_img
        self.ancho = 150
        self.alto = 150

        # === FÓRMULA DE VIDA ESCALABLE POR NIVEL (BALANCEADA) ===
        # Vida base más conservadora que escala gradualmente
        vida_base = VIDAS_JEFE_BASE  # 300 desde config.py

        # Calcular qué jefe es este basado en el nivel
        numero_jefe = ((nivel - NIVEL_APARICION_JEFE) // 3) + 1

        # Fórmula más balanceada: vida_base + (numero_jefe * 50) + (nivel * 10)
        # Esto hace que cada jefe sea más difícil pero no imposible
        vida_escalada = vida_base + (numero_jefe * 50) + ((nivel - NIVEL_APARICION_JEFE) * 10)

        # Asegurar un mínimo y máximo razonable
        self.vidas_max = max(vida_escalada, vida_base)
        self.vidas_max = min(self.vidas_max, vida_base * 3)  # Máximo 3x la vida base
        self.vidas_actual = self.vidas_max

        # Guardar información del nivel para referencia
        self.nivel = nivel
        self.numero_jefe = numero_jefe

        print(f"Jefe #{numero_jefe} creado - Nivel: {nivel}")
        print(f"Vida del jefe: {self.vidas_actual}/{self.vidas_max}")
        print(f"Fórmula aplicada: {vida_base} + ({numero_jefe} * 150) + ({nivel} * 50) = {self.vidas_max}")

        # Estados del jefe
        self.fase_entrada = True
        self.activo = False
        self.derrotado = False

        # Sistema de fases basado en porcentaje de vida
        self.fase_actual = 1
        self.fases_totales = 3
        self.ultimo_cambio_fase = pygame.time.get_ticks()

        # Movimiento
        self.x_centro = ANCHO // 2 - self.ancho // 2
        self.tiempo_inicio = pygame.time.get_ticks()

        # Timers para ataques (escalados por nivel)
        self.ultimo_disparo_normal = 0
        self.ultimo_lanzamiento_misil = 0
        self.ultimo_disparo_perseguidor = 0
        self.ultima_invocacion = 0

        # Recursos gráficos
        self.bullet_frames = boss_bullet_frames
        self.missile_frames = boss_missile_frames
        self.homing_bullet_img = boss_homing_bullet_img

        # Listas de proyectiles
        self.balas_normales = []
        self.misiles = []
        self.balas_perseguidoras = []
        self.enemigos_invocados = []

        # === ESCALADO DE DIFICULTAD POR NIVEL ===
        # Los jefes de niveles más altos son más agresivos
        self.multiplicador_agresividad = 1.0 + (numero_jefe * 0.2)  # +20% por cada jefe
        self.velocidad_proyectiles = VELOCIDAD_BALA_JEFE * (1.0 + numero_jefe * 0.1)  # +10% velocidad por jefe

        print(f"Multiplicador de agresividad: {self.multiplicador_agresividad:.1f}x")
        print(f"Velocidad de proyectiles: {self.velocidad_proyectiles:.1f}")

    def actualizar(self, tiempo_actual, nave_x, nave_y):
        """Actualiza la lógica del jefe"""
        if self.derrotado:
            return

        # Fase de entrada
        if self.fase_entrada:
            self.y += VELOCIDAD_INICIAL_JEFE
            if self.y >= ALTURA_PARADA_JEFE:
                self.fase_entrada = False
                self.activo = True
                print(f"Jefe #{self.numero_jefe} ha entrado en posición de combate")

        # Movimiento oscilante cuando está activo
        elif self.activo:
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
            self.x = self.x_centro + math.sin(
                tiempo_transcurrido * FRECUENCIA_OSCILACION_JEFE_X) * AMPLITUD_OSCILACION_JEFE_X

            # Actualizar fase según porcentaje de vida
            porcentaje_vida = (self.vidas_actual / self.vidas_max) * 100

            if porcentaje_vida <= 33 and self.fase_actual < 3:
                self.fase_actual = 3
                self.ultimo_cambio_fase = tiempo_actual
                print(f"¡Jefe #{self.numero_jefe} entra en fase 3! ¡Modo frenético!")
            elif porcentaje_vida <= 66 and self.fase_actual < 2:
                self.fase_actual = 2
                self.ultimo_cambio_fase = tiempo_actual
                print(f"¡Jefe #{self.numero_jefe} entra en fase 2! ¡Aumenta la agresividad!")

            # Ejecutar patrones de ataque
            self._ejecutar_ataques(tiempo_actual, nave_x, nave_y)

        # Actualizar proyectiles
        self._actualizar_proyectiles(tiempo_actual, nave_x, nave_y)

    def _ejecutar_ataques(self, tiempo_actual, nave_x, nave_y):
        """Ejecuta los diferentes patrones de ataque del jefe"""
        # Modificar tiempos según la fase actual Y el nivel del jefe
        multiplicador_tiempo = 1.0 / self.multiplicador_agresividad  # Más agresivo = menos tiempo entre ataques

        if self.fase_actual == 2:
            multiplicador_tiempo *= 0.8
        elif self.fase_actual == 3:
            multiplicador_tiempo *= 0.6

        # Ataque 1: Disparos normales (más balas en jefes de nivel alto)
        tiempo_disparo_ajustado = TIEMPO_DISPARO_JEFE_NORMAL * multiplicador_tiempo
        if tiempo_actual - self.ultimo_disparo_normal > tiempo_disparo_ajustado:
            balas_base = 5
            if self.fase_actual == 1:
                num_balas = balas_base + self.numero_jefe  # Más balas por jefe
            elif self.fase_actual == 2:
                num_balas = balas_base + 2 + self.numero_jefe
            else:
                num_balas = balas_base + 4 + self.numero_jefe

            self._disparo_normal(num_balas)
            self.ultimo_disparo_normal = tiempo_actual

        # Ataque 2: Lanzamiento de misiles (más misiles en jefes de nivel alto)
        tiempo_misil_ajustado = TIEMPO_LANZAMIENTO_MISIL_JEFE * multiplicador_tiempo
        if tiempo_actual - self.ultimo_lanzamiento_misil > tiempo_misil_ajustado:
            num_misiles = self.fase_actual + (self.numero_jefe // 2)  # Más misiles por jefe
            for i in range(num_misiles):
                self._lanzar_misil(nave_x, nave_y)
            self.ultimo_lanzamiento_misil = tiempo_actual

        # Ataque 3: Bala perseguidora (solo en fases 2 y 3, más en jefes altos)
        if self.fase_actual >= 2:
            tiempo_perseguidor_ajustado = TIEMPO_DISPARO_BALA_PERSEGUIDORA_JEFE * multiplicador_tiempo
            if tiempo_actual - self.ultimo_disparo_perseguidor > tiempo_perseguidor_ajustado:
                if self.fase_actual == 2:
                    num_balas = 1 + (self.numero_jefe // 3)
                else:
                    num_balas = 2 + (self.numero_jefe // 2)

                for _ in range(num_balas):
                    self._disparar_bala_perseguidora(nave_x, nave_y)
                self.ultimo_disparo_perseguidor = tiempo_actual

        # Ataque 4: Invocar enemigos (solo en fase 3, más enemigos en jefes altos)
        if self.fase_actual == 3:
            tiempo_invocacion_ajustado = TIEMPO_INVOCACION_JEFE * multiplicador_tiempo
            if tiempo_actual - self.ultima_invocacion > tiempo_invocacion_ajustado:
                self._invocar_enemigos()
                self.ultima_invocacion = tiempo_actual

    def _disparo_normal(self, num_balas=5):
        """Disparo normal del jefe - patrón en abanico"""
        centro_x = self.x + self.ancho // 2
        centro_y = self.y + self.alto

        # Calcular ángulos para distribuir las balas uniformemente
        angulo_total = 60 + (self.numero_jefe * 10)  # Ángulo más amplio para jefes de nivel alto
        angulos = []

        if num_balas > 1:
            paso = angulo_total / (num_balas - 1)
            for i in range(num_balas):
                angulos.append(-angulo_total / 2 + i * paso)
        else:
            angulos = [0]

        # Crear las balas con los ángulos calculados
        for angulo in angulos:
            rad = math.radians(angulo)
            vel_x = math.sin(rad) * self.velocidad_proyectiles
            vel_y = math.cos(rad) * self.velocidad_proyectiles

            bala = {
                "x": centro_x,
                "y": centro_y,
                "vel_x": vel_x,
                "vel_y": vel_y,
                "frame_actual": 0,
                "ultimo_frame": pygame.time.get_ticks(),
                "daño": DAÑO_BALA_JEFE + (self.numero_jefe // 2)  # Más daño en jefes altos
            }
            self.balas_normales.append(bala)

        print(f"Jefe #{self.numero_jefe} disparó {len(angulos)} balas normales en fase {self.fase_actual}")

    def _lanzar_misil(self, nave_x, nave_y):
        """Lanza un misil hacia la posición de la nave"""
        centro_x = self.x + self.ancho // 2
        centro_y = self.y + self.alto

        # Calcular dirección hacia la nave
        dx = nave_x - centro_x
        dy = nave_y - centro_y
        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia > 0:
            velocidad_misil = VELOCIDAD_MISIL_JEFE * (1.0 + self.numero_jefe * 0.1)  # Más rápido en jefes altos
            vel_x = (dx / distancia) * velocidad_misil
            vel_y = (dy / distancia) * velocidad_misil

            misil = {
                "x": centro_x,
                "y": centro_y,
                "vel_x": vel_x,
                "vel_y": vel_y,
                "frame_actual": 0,
                "ultimo_frame": pygame.time.get_ticks(),
                "daño": DAÑO_MISIL_JEFE + self.numero_jefe  # Más daño en jefes altos
            }
            self.misiles.append(misil)

    def _disparar_bala_perseguidora(self, nave_x, nave_y):
        """Dispara una bala que persigue a la nave"""
        centro_x = self.x + self.ancho // 2
        centro_y = self.y + self.alto

        velocidad_perseguidor = VELOCIDAD_BALA_PERSEGUIDORA * (1.0 + self.numero_jefe * 0.15)
        bala = {
            "x": centro_x,
            "y": centro_y,
            "vel_x": 0,
            "vel_y": velocidad_perseguidor,
            "daño": DAÑO_BALA_PERSEGUIDORA + (self.numero_jefe // 2)
        }
        self.balas_perseguidoras.append(bala)

    def _invocar_enemigos(self):
        """Invoca enemigos adicionales"""
        max_enemigos = ENEMIGOS_POR_OLEADA_JEFE_INVOCADOS + self.numero_jefe  # Más enemigos en jefes altos
        if len(self.enemigos_invocados) < max_enemigos:
            enemigos_a_crear = max_enemigos - len(self.enemigos_invocados)
            for i in range(enemigos_a_crear):
                enemigo = {
                    "x": random.randint(50, ANCHO - 100),
                    "y": random.randint(-100, -50),
                    "vel_y": 2 + (self.numero_jefe * 0.5),  # Más rápidos en jefes altos
                    "tipo": "invocado",
                    "vida": 1
                }
                self.enemigos_invocados.append(enemigo)
            print(f"Jefe #{self.numero_jefe} invocó {enemigos_a_crear} enemigos")

    def _actualizar_proyectiles(self, tiempo_actual, nave_x, nave_y):
        """Actualiza todos los proyectiles del jefe"""
        # Actualizar balas normales
        for bala in self.balas_normales[:]:
            bala["x"] += bala["vel_x"]
            bala["y"] += bala["vel_y"]

            # Animar frame si hay múltiples frames
            if len(self.bullet_frames) > 1 and tiempo_actual - bala["ultimo_frame"] > 100:
                bala["frame_actual"] = (bala["frame_actual"] + 1) % len(self.bullet_frames)
                bala["ultimo_frame"] = tiempo_actual

            # Eliminar si sale de pantalla
            if (bala["x"] < -50 or bala["x"] > ANCHO + 50 or
                    bala["y"] < -50 or bala["y"] > ALTO + 50):
                self.balas_normales.remove(bala)

        # Actualizar misiles
        for misil in self.misiles[:]:
            misil["x"] += misil["vel_x"]
            misil["y"] += misil["vel_y"]

            # Animar frame
            if len(self.missile_frames) > 1 and tiempo_actual - misil["ultimo_frame"] > 50:
                misil["frame_actual"] = (misil["frame_actual"] + 1) % len(self.missile_frames)
                misil["ultimo_frame"] = tiempo_actual

            # Eliminar si sale de pantalla
            if (misil["x"] < -50 or misil["x"] > ANCHO + 50 or
                    misil["y"] < -50 or misil["y"] > ALTO + 50):
                self.misiles.remove(misil)

        # Actualizar balas perseguidoras
        for bala in self.balas_perseguidoras[:]:
            # Calcular dirección hacia la nave
            dx = nave_x - bala["x"]
            dy = nave_y - bala["y"]
            distancia = math.sqrt(dx * dx + dy * dy)

            if distancia > 0:
                # Ajustar velocidad gradualmente hacia la nave
                velocidad_objetivo = VELOCIDAD_BALA_PERSEGUIDORA * (1.0 + self.numero_jefe * 0.15)
                target_vel_x = (dx / distancia) * velocidad_objetivo
                target_vel_y = (dy / distancia) * velocidad_objetivo

                giro_ajustado = GIRO_BALA_PERSEGUIDORA * (1.0 + self.numero_jefe * 0.1)  # Más ágil en jefes altos
                bala["vel_x"] += (target_vel_x - bala["vel_x"]) * giro_ajustado
                bala["vel_y"] += (target_vel_y - bala["vel_y"]) * giro_ajustado

            bala["x"] += bala["vel_x"]
            bala["y"] += bala["vel_y"]

            # Eliminar si sale de pantalla
            if (bala["x"] < -50 or bala["x"] > ANCHO + 50 or
                    bala["y"] < -50 or bala["y"] > ALTO + 50):
                self.balas_perseguidoras.remove(bala)

        # Actualizar enemigos invocados
        for enemigo in self.enemigos_invocados[:]:
            enemigo["y"] += enemigo["vel_y"]

            # Eliminar si sale de pantalla
            if enemigo["y"] > ALTO + 50:
                self.enemigos_invocados.remove(enemigo)

    def recibir_daño(self, cantidad):
        """El jefe recibe daño"""
        if self.derrotado:
            return False

        # Sistema de resistencia más suave: solo reduce ligeramente el daño
        resistencia_base = 2  # Resistencia base más baja
        resistencia_adicional = max(0, (self.numero_jefe - 1) // 3)  # +1 resistencia cada 3 jefes
        resistencia_total = resistencia_base + resistencia_adicional

        # Reducir el daño recibido de forma más suave
        daño_reducido = max(3, cantidad // resistencia_total)  # Mínimo 3 de daño siempre
        self.vidas_actual -= daño_reducido

        print(f"Jefe #{self.numero_jefe} recibió {daño_reducido} de daño (resistencia: {resistencia_total}x)")
        print(f"Vida restante: {self.vidas_actual}/{self.vidas_max} ({self.obtener_porcentaje_vida():.1f}%)")

        if self.vidas_actual <= 0:
            self.derrotado = True
            print(f"¡Jefe #{self.numero_jefe} derrotado!")
            return True
        return False

    def obtener_rect(self):
        """Retorna el rectángulo de colisión del jefe"""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def obtener_porcentaje_vida(self):
        """Retorna el porcentaje de vida del jefe (0-100)"""
        return (self.vidas_actual / self.vidas_max) * 100

    def obtener_puntos_por_derrota(self):
        """Retorna los puntos que otorga derrotar a este jefe"""
        puntos_base = 500
        bonus_nivel = self.numero_jefe * 250  # +250 puntos por cada jefe
        bonus_dificultad = self.nivel * 50  # +50 puntos por nivel
        return puntos_base + bonus_nivel + bonus_dificultad


def generar_enemigos_sin_superposicion(cantidad, enemigos_actuales, velocidad_enemigo):
    """Genera enemigos sin superposición"""
    nuevos = []
    intentos_maximos = cantidad * 10
    intentos = 0

    tipos_enemigos_disponibles = ["normal", "mosca", "bc", "bichorojo", "bichoverde"]

    while len(nuevos) < cantidad and intentos < intentos_maximos:
        tipo_elegido = random.choice(tipos_enemigos_disponibles)

        # Determinar tamaño según tipo
        enemigo_ancho = 48
        enemigo_alto = 48

        x = random.randint(0, ANCHO - enemigo_ancho)
        y = random.randint(-ALTO, -enemigo_alto)

        muy_cerca = False
        for e in enemigos_actuales + nuevos:
            # Inflar los rectángulos para dar un poco de margen
            rect_nuevo = pygame.Rect(x, y, enemigo_ancho, enemigo_alto).inflate(20, 20)
            rect_existente = pygame.Rect(e["x"], e["y"], 48, 48).inflate(20, 20)

            if rect_nuevo.colliderect(rect_existente):
                muy_cerca = True
                break

        if not muy_cerca:
            velocidad_y_final = velocidad_enemigo
            if tipo_elegido == "mosca":
                velocidad_y_final = velocidad_enemigo * 2.0

            enemigo_data = {
                "x": x,
                "y": y,
                "velocidad_y": velocidad_y_final,
                "fase": random.uniform(0, 2 * math.pi),
                "tipo": tipo_elegido
            }

            # Inicializa propiedades de animación si es un enemigo animado
            if tipo_elegido in ["mosca", "bc", "bichorojo", "bichoverde"]:
                enemigo_data["frame_actual"] = 0
                enemigo_data["ultimo_update_animacion"] = pygame.time.get_ticks()

            if tipo_elegido == "bc":
                enemigo_data["puede_disparar"] = True
                enemigo_data["ultimo_disparo"] = pygame.time.get_ticks()

            nuevos.append(enemigo_data)
        intentos += 1

    return nuevos
