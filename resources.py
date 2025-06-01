"""
Manejo de recursos del juego (imágenes, sonidos, fuentes)
"""
import pygame
import sys
from config import ANCHO, ALTO


class ResourceManager:
    """Clase para manejar todos los recursos del juego"""

    def __init__(self):
        self.imagenes = {}
        self.sonidos = {}
        self.fuentes = {}
        self.frames = {}

    def cargar_todos_los_recursos(self):
        """Carga todos los recursos del juego"""
        try:
            self._cargar_imagenes_basicas()
            self._cargar_imagenes_menu()
            self._cargar_imagenes_game_over()
            self._cargar_frames_animados()
            self._cargar_sonidos()
            self._cargar_fuentes()
            self._cargar_decoracion()
            self._cargar_powerups()
            print("Todos los recursos cargados correctamente")
            return True
        except Exception as e:
            print(f"Error cargando recursos: {e}")
            return False

    def _cargar_imagenes_basicas(self):
        """Carga imágenes básicas del juego"""
        # Nave
        self.imagenes['nave'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/Shooter/images/1B.png").convert_alpha(),
            (48, 48)
        )

        # Láser
        self.imagenes['laser'] = pygame.image.load(
            "assets/PNG/Shooter/images/PlayProjectile.png"
        ).convert_alpha()

        self.imagenes['laser_enemigo'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/Lasers/laserRed02.png").convert_alpha(),
            (6, 16)
        )

        # Enemigo básico
        self.imagenes['enemigo'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/Enemies/enemyBlack1.png").convert_alpha(),
            (48, 48)
        )

        # Fondo
        self.imagenes['fondo'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/Main_Menu/BG.png").convert(),
            (ANCHO, ALTO)
        )

        # UI
        self.imagenes['vida_icono'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/UI/playerLife2_red.png").convert_alpha(),
            (32, 32)
        )

        # Escudo
        self.imagenes['escudo'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/Effects/shield2.png").convert_alpha(),
            (68, 68)
        )

        # Jefe
        self.imagenes['jefe'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/Shooter/images/9.png").convert_alpha(),
            (150, 150)
        )

        self.imagenes['boss_homing_bullet'] = pygame.image.load(
            "assets/PNG/Shooter/images/EnemyProjectile1.png"
        ).convert_alpha()

    def _cargar_imagenes_menu(self):
        """Carga imágenes del menú"""
        self.imagenes['background'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/Main_Menu/BG.png").convert(),
            (ANCHO, ALTO)
        )

        self.imagenes['header'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/Main_Menu/Header.png").convert_alpha(),
            (int(ANCHO * 0.8), int(ALTO * 0.2))
        )

        self.imagenes['start_button'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/Main_Menu/Start_BTN.png").convert_alpha(),
            (200, 75)
        )

        self.imagenes['exit_button'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/Main_Menu/Exit_BTN.png").convert_alpha(),
            (200, 75)
        )

    def _cargar_imagenes_game_over(self):
        """Carga imágenes específicas de Game Over"""
        # Ventana principal de Game Over
        self.imagenes['game_over_window'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/You_Win/Window.png").convert_alpha(),
            (int(ANCHO * 0.55), int(ALTO * 0.6))
        )

        # Botones de Game Over
        self.imagenes['retry_button'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/You_Win/Play_BTN.png").convert_alpha(),
            (150, 60)
        )

        self.imagenes['menu_button'] = pygame.transform.scale(
            pygame.image.load("assets/PNG/c2/PNG/You_Win/Close_BTN.png").convert_alpha(),
            (150, 60)
        )

        # Elementos de la interfaz de Game Over
        try:
            self.imagenes['record_title'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/You_Win/Record.png").convert_alpha(),
                (int(self.imagenes['game_over_window'].get_width() * 0.4),
                 int(self.imagenes['game_over_window'].get_height() * 0.08))
            )
        except:
            print("No se pudo cargar Record.png, se usará texto")
            self.imagenes['record_title'] = None

        try:
            self.imagenes['table'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/You_Win/Table.png").convert_alpha(),
                (int(self.imagenes['game_over_window'].get_width() * 0.45),
                 int(self.imagenes['game_over_window'].get_height() * 0.12))
            )
        except:
            print("No se pudo cargar Table.png, se usará rectángulo")
            self.imagenes['table'] = None

        try:
            table_width = self.imagenes['table'].get_width() if self.imagenes['table'] else 200
            table_height = self.imagenes['table'].get_height() if self.imagenes['table'] else 40
            self.imagenes['score_label'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/You_Win/Score.png").convert_alpha(),
                (int(table_width * 0.7), int(table_height * 0.7))
            )
        except:
            print("No se pudo cargar Score.png, se usará texto")
            self.imagenes['score_label'] = None

    def _cargar_frames_animados(self):
        """Carga frames para animaciones"""
        # Enemigo BC
        self.frames['bc'] = []
        try:
            for i in range(1, 4):
                frame = pygame.transform.scale(
                    pygame.image.load(f"assets/PNG/bien diseñado/bc{i}.png").convert_alpha(),
                    (48, 48)
                )
                self.frames['bc'].append(frame)
        except:
            print("Error cargando frames BC, usando imagen por defecto")
            self.frames['bc'] = [self.imagenes['enemigo']]

        # Enemigo bicho rojo
        self.frames['bichorojo'] = []
        try:
            for i in range(1, 4):
                frame = pygame.transform.scale(
                    pygame.image.load(f"assets/PNG/bien diseñado/bichorojo{i}.png").convert_alpha(),
                    (48, 48)
                )
                self.frames['bichorojo'].append(frame)
        except:
            print("Error cargando frames bichorojo, usando imagen por defecto")
            self.frames['bichorojo'] = [self.imagenes['enemigo']]

        # Enemigo bicho verde
        self.frames['bichoverde'] = []
        try:
            for i in range(1, 4):
                frame = pygame.transform.scale(
                    pygame.image.load(f"assets/PNG/bien diseñado/bichoverde{i}.png").convert_alpha(),
                    (48, 48)
                )
                self.frames['bichoverde'].append(frame)
        except:
            print("Error cargando frames bichoverde, usando imagen por defecto")
            self.frames['bichoverde'] = [self.imagenes['enemigo']]

        # Mosca
        self.frames['mosca'] = []
        try:
            mosca_sheet = pygame.image.load("assets/PNG/bien diseñado/enemigo_mosca.png").convert_alpha()
            frame_ancho = mosca_sheet.get_width() // 8
            frame_alto = mosca_sheet.get_height()

            for i in range(8):
                frame = mosca_sheet.subsurface(pygame.Rect(i * frame_ancho, 0, frame_ancho, frame_alto))
                frame = pygame.transform.scale(frame, (48, 48))
                self.frames['mosca'].append(frame)
        except:
            print("Error cargando frames mosca, usando imagen por defecto")
            self.frames['mosca'] = [self.imagenes['enemigo']]

        # Explosiones
        try:
            self.frames['explosion'] = self._cortar_sprite_sheet(
                "assets/PNG/conjunto-efecto-explosion-estilo-comic-dibujos-animados.png",
                3, 3, 666, 609
            )
        except:
            print("Error cargando explosiones, creando frames por defecto")
            # Crear frames de explosión simples
            self.frames['explosion'] = []
            for i in range(9):
                frame = pygame.Surface((96, 96), pygame.SRCALPHA)
                color_intensity = 255 - (i * 25)
                pygame.draw.circle(frame, (color_intensity, color_intensity // 2, 0), (48, 48), 48 - i * 5)
                self.frames['explosion'].append(frame)

        # Proyectiles del jefe
        try:
            self.frames['boss_bullet'] = [
                pygame.transform.scale(
                    pygame.image.load("assets/PNG/Shooter/images/EnemyProjectile2.png").convert_alpha(),
                    (30, 30)
                )
            ]
        except:
            print("Error cargando bala del jefe, creando por defecto")
            frame = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(frame, (255, 0, 0), (15, 15), 15)
            self.frames['boss_bullet'] = [frame]

        # Misiles del jefe
        self.frames['boss_missile'] = []
        try:
            for i in range(19):
                frame = pygame.transform.scale(
                    pygame.image.load(f"assets/PNG/c1/PNG/Sprites/bomba/Bomb{i}.png").convert_alpha(),
                    (50, 50)
                )
                self.frames['boss_missile'].append(frame)
        except:
            print("Error cargando misiles del jefe, creando por defecto")
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(frame, (0, 0, 255), (25, 25), 25)
            self.frames['boss_missile'] = [frame]

    def _cargar_sonidos(self):
        """Carga todos los sonidos"""
        pygame.mixer.init()

        try:
            self.sonidos['laser'] = pygame.mixer.Sound("assets/Bonus/sfx_laser1.ogg")
        except:
            print("Error cargando sonido laser")
            self.sonidos['laser'] = None

        try:
            self.sonidos['vida_perdida'] = pygame.mixer.Sound("assets/Bonus/sfx_twoTone.ogg")
        except:
            print("Error cargando sonido vida perdida")
            self.sonidos['vida_perdida'] = None

        try:
            self.sonidos['explosion'] = pygame.mixer.Sound(
                "assets/TRACKS/megatracks/506825__mrthenoronha__explosion-2-8-bit.wav"
            )
        except:
            print("Error cargando sonido explosión")
            self.sonidos['explosion'] = None

        try:
            self.sonidos['powerup_recogido'] = pygame.mixer.Sound("assets/Bonus/sfx_twoTone.ogg")
        except:
            print("Error cargando sonido powerup")
            self.sonidos['powerup_recogido'] = None

        # Power-ups específicos
        try:
            self.sonidos['powerup_vida'] = pygame.mixer.Sound("assets/Bonus/Audio/forceField_000.ogg")
            self.sonidos['powerup_velocidad'] = pygame.mixer.Sound("assets/Bonus/Audio/forceField_002.ogg")
            self.sonidos['powerup_escudo'] = pygame.mixer.Sound("assets/Bonus/sfx_shieldUp.ogg")
            self.sonidos['powerup_mas_dano'] = pygame.mixer.Sound("assets/Bonus/Audio/laserRetro_001.ogg")
        except:
            print("Error cargando algunos sonidos de powerup")

    def _cargar_fuentes(self):
        """Carga las fuentes del juego"""
        try:
            self.fuentes['menu'] = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 80)
            self.fuentes['juego'] = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 40)
            self.fuentes['record_num'] = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 22)
            self.fuentes['actual_score_num'] = pygame.font.Font("assets/Bonus/kenvector_future.ttf", 22)
        except:
            print("Error cargando fuentes personalizadas, usando fuentes del sistema")
            # Fallback a fuentes del sistema
            self.fuentes['menu'] = pygame.font.Font(None, 80)
            self.fuentes['juego'] = pygame.font.Font(None, 40)
            self.fuentes['record_num'] = pygame.font.Font(None, 22)
            self.fuentes['actual_score_num'] = pygame.font.Font(None, 22)

    def _cargar_decoracion(self):
        """Carga objetos de decoración"""
        self.imagenes['decoracion'] = []

        # Intentar cargar meteoritos
        try:
            base_path = "assets/PNG/c1/PNG/Meteors/Meteor_"
            for i in range(1, 11):
                file_name = f"{i:02d}.png"
                full_path = f"{base_path}{file_name}"
                img = pygame.transform.scale(
                    pygame.image.load(full_path).convert_alpha(),
                    (70, 70)
                )
                self.imagenes['decoracion'].append(img)
        except:
            print("Error cargando meteoritos, creando decoración por defecto")
            # Crear decoración simple si no se pueden cargar los meteoritos
            for i in range(5):
                img = pygame.Surface((70, 70), pygame.SRCALPHA)
                color = (100 + i * 30, 100 + i * 20, 100 + i * 10)
                pygame.draw.circle(img, color, (35, 35), 35)
                self.imagenes['decoracion'].append(img)

    def _cargar_powerups(self):
        """Carga imágenes de power-ups"""
        self.imagenes['powerups'] = {}

        try:
            self.imagenes['powerups']['vida'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/Ship_Parts/HP_Icon.png").convert_alpha(),
                (32, 32)
            )
        except:
            # Crear power-up de vida por defecto
            img = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(img, (255, 0, 0), (16, 16), 16)
            pygame.draw.circle(img, (255, 255, 255), (16, 16), 12)
            self.imagenes['powerups']['vida'] = img

        try:
            self.imagenes['powerups']['velocidad'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/Ship_Parts/Speed_Icon.png").convert_alpha(),
                (32, 32)
            )
        except:
            # Crear power-up de velocidad por defecto
            img = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(img, (0, 255, 0), (16, 16), 16)
            pygame.draw.circle(img, (255, 255, 255), (16, 16), 12)
            self.imagenes['powerups']['velocidad'] = img

        try:
            self.imagenes['powerups']['escudo'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/Ship_Parts/Armor_Icon.png").convert_alpha(),
                (32, 32)
            )
        except:
            # Crear power-up de escudo por defecto
            img = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(img, (0, 0, 255), (16, 16), 16)
            pygame.draw.circle(img, (255, 255, 255), (16, 16), 12)
            self.imagenes['powerups']['escudo'] = img

        try:
            self.imagenes['powerups']['mas_dano'] = pygame.transform.scale(
                pygame.image.load("assets/PNG/c2/PNG/Ship_Parts/Damage_Icon.png").convert_alpha(),
                (32, 32)
            )
        except:
            # Crear power-up de más daño por defecto
            img = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(img, (255, 255, 0), (16, 16), 16)
            pygame.draw.circle(img, (255, 255, 255), (16, 16), 12)
            self.imagenes['powerups']['mas_dano'] = img

    def _cortar_sprite_sheet(self, sheet_path, num_columnas, num_filas, frame_ancho, frame_alto):
        """Corta un sprite sheet en frames individuales"""
        sheet = pygame.image.load(sheet_path).convert_alpha()
        frames = []
        for fila in range(num_filas):
            for col in range(num_columnas):
                x = col * frame_ancho
                y = fila * frame_alto
                frame = sheet.subsurface(pygame.Rect(x, y, frame_ancho, frame_alto))
                frame = pygame.transform.scale(frame, (96, 96))
                frames.append(frame)
        return frames

    def reproducir_sonido(self, nombre_sonido):
        """Reproduce un sonido de forma segura"""
        if nombre_sonido in self.sonidos and self.sonidos[nombre_sonido]:
            try:
                self.sonidos[nombre_sonido].play()
            except:
                print(f"Error reproduciendo sonido: {nombre_sonido}")


# Instancia global del gestor de recursos
resource_manager = ResourceManager()
