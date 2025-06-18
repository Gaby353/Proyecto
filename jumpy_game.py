
# ------------------ FUNCIÓN PRINCIPAL ------------------
def iniciar_juego_saltos():
    """
    Función que inicializa y ejecuta el juego de saltos 'Jumpy_Game'.
    """

    # ------------------ IMPORTACIÓN DE MÓDULOS ------------------
    import pygame  # Librería para el desarrollo de videojuegos
    import random  # Para generar valores aleatorios
    import os      # Para comprobar la existencia de archivos
    from pygame import mixer  # Para manejar música y sonidos
    from spritesheet import SpriteSheet  # Clase para manejar hojas de sprites
    from enemy import Enemy  # Clase que define a los enemigos
    

    import sys
    sys.path.append(r"E:/cecy/Proyecto_PEC/VSCode_1/Jumpy_Game")  # Agrega la ruta del proyecto

    # ------------------ INICIALIZACIÓN ------------------
    mixer.init()  # Inicializa el mezclador de audio
    pygame.init()  # Inicializa Pygame

    # Tamaño de la ventana
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Jumpy_Game')  # Título de la ventana
    icon = pygame.image.load('ghost.png')
    pygame.display.set_icon(icon)  # Icono de la ventana

    # Control de FPS (fotogramas por segundo)
    clock = pygame.time.Clock()
    FPS = 60

    # ------------------ SONIDOS ------------------
    pygame.mixer.music.load('Jumpy_Game/assets/fuyu-biyori bgm.mp3')  # Música de fondo
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play(-1, 0.0)  # Se repite infinitamente

    jump_fx = pygame.mixer.Sound('Jumpy_Game/assets/jump.mp3')  # Sonido de salto
    jump_fx.set_volume(1)
    death_fx = pygame.mixer.Sound('Jumpy_Game/assets/death.mp3')  # Sonido de muerte
    death_fx.set_volume(1)

    # ------------------ VARIABLES GLOBALES ------------------
    SCROLL_THRESH = 200  # Umbral de desplazamiento (scroll)
    GRAVITY = 1          # Gravedad que afecta al jugador
    MAX_PLATFORMS = 10   # Número máximo de plataformas
    scroll = 0           # Desplazamiento vertical
    bg_scroll = 0        # Desplazamiento del fondo
    game_over = False    # Estado del juego
    score = 0            # Puntuación
    fade_counter = 0     # Contador para la animación de fade

    # Carga del puntaje más alto desde un archivo
    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as file:
            high_score = int(file.read())
    else: 
        high_score = 0

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Fuentes
    font_small = pygame.font.SysFont('Lucida Sans', 20)
    font_big = pygame.font.SysFont('Lucida Sans', 24)

    # ------------------ IMÁGENES ------------------
    jumpy_image = pygame.image.load('Jumpy_Game/assets/bocchi1.png').convert_alpha()
    bg_image = pygame.image.load('Jumpy_Game/assets/background2.png').convert_alpha()
    platform_image = pygame.image.load('Jumpy_Game/assets/wood.png').convert_alpha()

    # Hoja de sprites para los enemigos (aves)
    bird_sheet_img = pygame.image.load('Jumpy_Game/assets/bird.png').convert_alpha()
    bird_sheet = SpriteSheet(bird_sheet_img)

    # ------------------ FUNCIONES AUXILIARES ------------------
    def draw_text(text, font, text_col, x, y):
        """
        Dibuja un texto en la pantalla.
        """
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_panel():
        """
        Dibuja el panel superior con la puntuación.
        """
        draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)

    def draw_bg(bg_scroll):
        """
        Dibuja el fondo y lo desplaza con el scroll.
        """
        screen.blit(bg_image, (0, 0 + bg_scroll))
        screen.blit(bg_image, (0, -600 + bg_scroll))

    # ------------------ CLASE DEL JUGADOR ------------------
    class Player():
        def __init__(self, x, y):
            """
            Inicializa al jugador.
            """
            self.image = pygame.transform.scale(jumpy_image, (45, 45))  # Escala de la imagen
            self.width = 25
            self.height = 40
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.center = (x, y)  # Posición inicial
            self.vel_y = 0             # Velocidad vertical
            self.flip = False          # Si el sprite está volteado

        def move(self):
            """
            Maneja el movimiento del jugador.
            """
            nonlocal scroll
            scroll = 0
            dx = 0  # Movimiento horizontal
            dy = 0  # Movimiento vertical

            # Controles del teclado
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                dx = -10
                self.flip = False
            if key[pygame.K_d]:
                dx = 10
                self.flip = True

            # Gravedad
            self.vel_y += GRAVITY
            dy += self.vel_y

            # Límite de pantalla
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > SCREEN_WIDTH:
                dx = SCREEN_WIDTH - self.rect.right

            # Colisión con plataformas
            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20  # Salto
                        jump_fx.play()

            # Desplazamiento si sube
            if self.rect.top <= SCROLL_THRESH:
                if self.vel_y < 0:
                    scroll = -dy

            # Actualiza posición
            self.rect.x += dx
            self.rect.y += dy + scroll

            # Crea máscara para colisiones precisas
            self.mask = pygame.mask.from_surface(self.image)

            return scroll

        def draw(self):
            """
            Dibuja al jugador en pantalla.
            """
            screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))

    # ------------------ CLASE DE PLATAFORMAS ------------------
    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, width, moving):
            """
            Inicializa una plataforma.
            """
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(platform_image, (width, 10))
            self.moving = moving
            self.move_counter = random.randint(0, 50)
            self.direction = random.choice([-1, 1])
            self.speed = random.randint(1, 2)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self, scroll):
            """
            Actualiza la posición de la plataforma.
            """
            # Movimiento horizontal si es móvil
            if self.moving:
                self.move_counter += 1
                self.rect.x += self.direction * self.speed

            # Cambia de dirección si llega al límite
            if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.direction *= -1
                self.move_counter = 0

            # Desplazamiento vertical
            self.rect.y += scroll

            # Elimina la plataforma si sale de la pantalla
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

    # ------------------ CREACIÓN DE OBJETOS ------------------
    jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)  # Jugador
    platform_group = pygame.sprite.Group()  # Grupo de plataformas
    enemy_group = pygame.sprite.Group()     # Grupo de enemigos

    # Plataforma inicial
    platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
    platform_group.add(platform)

    # ------------------ BUCLE PRINCIPAL ------------------
    run = True
    while run:
        clock.tick(FPS)  # Controla la velocidad del juego

        if not game_over:
            # Movimiento del jugador
            scroll = jumpy.move()
            bg_scroll += scroll
            if bg_scroll >= 600:
                bg_scroll = 0

            # Dibuja el fondo
            draw_bg(bg_scroll)

            # Genera nuevas plataformas si faltan
            if len(platform_group) < MAX_PLATFORMS:
                p_w = random.randint(40, 60)
                p_x = random.randint(0, SCREEN_WIDTH - p_w)
                p_y = platform.rect.y - random.randint(80, 120)
                p_type = random.randint(1, 2)
                p_moving = True if p_type == 1 and score > 1000 else False
                platform = Platform(p_x, p_y, p_w, p_moving)
                platform_group.add(platform)

            # Actualiza las plataformas
            platform_group.update(scroll)

            # Genera enemigo si la puntuación es alta
            if len(enemy_group) == 0 and score > 2000:
                enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
                enemy_group.add(enemy)

            # Actualiza los enemigos
            enemy_group.update(scroll, SCREEN_WIDTH)

            # Actualiza la puntuación
            if scroll > 0:
                score += scroll

            # Línea para mostrar el récord
            pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
            draw_text('HIGH SCORE', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH)

            # Dibuja los elementos
            platform_group.draw(screen)
            enemy_group.draw(screen)
            jumpy.draw()
            draw_panel()

            # Si el jugador cae de la pantalla
            if jumpy.rect.top > SCREEN_HEIGHT:
                game_over = True
                death_fx.play()

            # Colisión con enemigos
            if pygame.sprite.spritecollide(jumpy, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()
        else:
            # Animación de fade al perder
            if fade_counter < SCREEN_WIDTH:
                fade_counter += 5
                for y in range(0, 6, 2):
                    pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
            else:
                # Muestra pantalla de derrota
                draw_text('PERDISTE!', font_big, WHITE, 130, 200)
                draw_text('PUNTAJE: ' + str(score), font_big, WHITE, 130, 250)
                draw_text('PRESIONA ESPACIO', font_big, WHITE, 40, 300)

                # Guarda nuevo récord si es necesario
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))

                # Reinicia si se presiona espacio
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    game_over = False
                    score = 0
                    scroll = 0
                    fade_counter = 0
                    jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                    enemy_group.empty()
                    platform_group.empty()
                    platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                    platform_group.add(platform)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                run = False

        pygame.display.update()  # Actualiza la pantalla

    pygame.quit()  # Sale de Pygame
