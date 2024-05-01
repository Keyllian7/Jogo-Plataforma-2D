import pygame
import math

# Criação do inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
