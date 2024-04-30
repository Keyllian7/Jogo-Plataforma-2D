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

    def update(self, personagem):
        # Calcula o vetor de direção entre o inimigo e o personagem
        direcao_x = personagem.rect.x - self.rect.x
        direcao_y = personagem.rect.y - self.rect.y
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        
        # Verifica se a distância é maior que zero para evitar divisão por zero
        if distancia > 0:
            # Normaliza o vetor de direção
            direcao_x /= distancia
            direcao_y /= distancia
            
            # Define a velocidade de movimento do inimigo
            velocidade = 3
            
            # Move o inimigo na direção do personagem
            self.rect.x += direcao_x * velocidade
            self.rect.y += direcao_y * velocidade
