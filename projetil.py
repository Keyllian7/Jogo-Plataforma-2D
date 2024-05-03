import math

class Flecha:
    def __init__(self, imagem, x, y, angle):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.angle = angle

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)