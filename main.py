#Importação de bibliotecas
import pygame
from pygame.locals import *
from sys import exit
import os

import pygame.locals

# Diretórios dos arquivos
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

pygame.init()

# Resolução da tela
largura = 960
altura = 540

# Cores
branco = (255, 255, 255)

# Criação da tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('UNP')

#Imagem de funfo
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Carregar sprites
spritesheet_andar_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
spritesheet_andar_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()

# Classe do Personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.andar_direita = []
        self.andar_esquerda = []
        for i in range(8):
            img = spritesheet_andar_direita.subsurface((i * 64, 0), (64, 47))
            self.andar_direita.append(img)
            img = spritesheet_andar_esquerda.subsurface((i * 64, 0), (64, 47))
            self.andar_esquerda.append(img)

        self.index_lista = 0
        self.image = self.andar_direita[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.direction = 'right'

        #Tamanho do personagem
        self.image = pygame.transform.scale(self.image, (int(64*1.5), int(47*1.5)))

        #Posição do personagem na tela
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 460

    # Atualiza a imagem do personagem de acordo com a direção do movimento
    def update(self):
        self.index_lista += 0.25
        if self.index_lista >= len(self.andar_direita):
            self.index_lista -= len(self.andar_direita)
        if self.direction == 'right':
            self.image = self.andar_direita[int(self.index_lista)]
        elif self.direction == 'left':
            self.image = self.andar_esquerda[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image, (int(64*1.5), int(47*1.5)))

# Criação do personagem
personagem = Personagem()
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

#Variavel para o pulo do player
pulando = False
velocidade_do_pulo = -10

# Controle de FPS
fps = pygame.time.Clock()

# Loop Principal do jogo
while True:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Verifica as teclas pressionadas para movimentar o personagem
    teclas_press = pygame.key.get_pressed()
    if teclas_press[K_d] and personagem.rect.right < largura + 30:
        personagem.rect.x += 5
        personagem.direction = 'right'
        personagem.update()

    if teclas_press[K_a] and personagem.rect.left > -30:
        personagem.rect.x -= 5
        personagem.direction = 'left'
        personagem.update()

    #Comando de pulo do personagem
    if teclas_press[K_SPACE] and not pulando:
        pulando = True

    if pulando:
        personagem.rect.y += velocidade_do_pulo
        velocidade_do_pulo += 1

        # Verifica se o personagem atingiu o chão e reinicia o comando
        if personagem.rect.y >= 460:
            pulando = False
            velocidade_do_pulo = -10

    # Desenha o personagem na tela
    sprites_personagem.draw(tela)

    # Atualiza a tela
    pygame.display.flip()
