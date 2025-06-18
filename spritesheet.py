import pygame

class SpriteSheet:
    def __init__(self, image):
        # Constructor: recibe la imagen de la hoja de sprites y la guarda como atributo
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        """
        Extrae un 'frame' (subimagen) de la hoja de sprites.
        Parámetros:
          - frame: el número de frame a extraer (posición horizontal)
          - width, height: dimensiones del frame en la hoja de sprites
          - scale: factor de escala para redimensionar la imagen
          - color: color a considerar como transparente
        """
        # Crea una nueva superficie transparente del tamaño del frame
        image = pygame.Surface((width, height)).convert_alpha()

        # Copia el frame deseado de la hoja de sprites a la nueva superficie
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))

        # Escala la imagen extraída
        image = pygame.transform.scale(image, (width * scale, height * scale))

        # Establece el color transparente (colorkey) para la imagen extraída
        image.set_colorkey(color)

        return image  # Devuelve la imagen lista para usar
