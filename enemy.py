# ------------------ IMPORTACIÓN DE MÓDULOS ------------------
import pygame  # Librería para desarrollo de videojuegos en Python
import random  # Para elegir aleatoriamente la dirección del enemigo

# ------------------ CLASE ENEMY (ENEMIGO) ------------------
class Enemy(pygame.sprite.Sprite):
    """
    Esta clase representa a un enemigo en el juego.
    Hereda de pygame.sprite.Sprite, lo que facilita su uso con grupos de sprites.
    """
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        """
        Constructor de la clase Enemy.
        Parámetros:
        - SCREEN_WIDTH: ancho de la pantalla (para calcular posiciones y eliminación).
        - y: posición vertical donde aparece el enemigo.
        - sprite_sheet: hoja de sprites que contiene las imágenes de animación.
        - scale: escala para redimensionar las imágenes.
        """
        # Inicializamos la clase base Sprite
        pygame.sprite.Sprite.__init__(self)

        # Lista para almacenar los fotogramas de animación
        self.animation_list = []

        # Índice del fotograma actual
        self.frame_index = 0

        # Marca de tiempo de la última actualización de animación
        self.update_time = pygame.time.get_ticks()

        # Dirección de movimiento (1: derecha, -1: izquierda)
        self.direction = random.choice([-1, 1])  # Se elige aleatoriamente la dirección

        # Si se mueve hacia la derecha, se invierte la imagen horizontalmente
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        # ------------------ CARGA DE IMÁGENES DE ANIMACIÓN ------------------
        animation_steps = 8  # Número de fotogramas de la animación
        for animation in range(animation_steps):
            # Obtiene una imagen del sprite_sheet
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            
            # Invierte la imagen horizontalmente si es necesario
            image = pygame.transform.flip(image, self.flip, False)
            
            # Establece el color negro como transparente
            image.set_colorkey((0, 0, 0))
            
            # Añade la imagen a la lista de animación
            self.animation_list.append(image)
        
        # Selecciona la imagen inicial
        self.image = self.animation_list[self.frame_index]

        # Obtiene el rectángulo que representa al enemigo en pantalla
        self.rect = self.image.get_rect()

        # Establece la posición inicial en el eje x (borde izquierdo o derecho)
        if self.direction == 1:
            self.rect.x = 0  # Aparece en el borde izquierdo
        else:
            self.rect.x = SCREEN_WIDTH  # Aparece en el borde derecho

        # Establece la posición vertical del enemigo
        self.rect.y = y
    
    def update(self, scroll, SCREEN_WIDTH):
        """
        Método para actualizar el estado del enemigo.
        Parámetros:
        - scroll: desplazamiento vertical (útil si el fondo se desplaza).
        - SCREEN_WIDTH: ancho de la pantalla, para saber si el enemigo sale de la pantalla.
        """

        # ------------------ ACTUALIZACIÓN DE ANIMACIÓN ------------------
        ANIMATION_COOLDOWN = 50  # Milisegundos que dura cada fotograma

        # Establece la imagen actual
        self.image = self.animation_list[self.frame_index]

        # Comprueba si ha pasado suficiente tiempo para cambiar de fotograma
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            # Actualiza la marca de tiempo
            self.update_time = pygame.time.get_ticks()
            # Avanza al siguiente fotograma
            self.frame_index += 1

        # Si llega al final de la animación, vuelve al inicio
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        # ------------------ MOVIMIENTO ------------------
        # Mueve al enemigo en el eje x según la dirección (velocidad = 2)
        self.rect.x += self.direction * 2

        # Aplica el desplazamiento vertical si lo hay (scroll)
        self.rect.y += scroll

        # ------------------ ELIMINACIÓN SI SALE DE PANTALLA ------------------
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()  # Elimina el sprite del grupo al que pertenece