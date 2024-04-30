#Importação de bibliotecas
import pygame
from pygame.locals import *
from sys import exit
from player import Personagem
import os

import pygame.locals

# Diretórios dos arquivos
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

pygame.init()

# Tamanho da matriz de pixels em que o jogo será reproduzido.
largura = 960
altura = 540

# Criação da variável e argumentos para a execução da matriz.
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('UNP')

# Variáveis que contém valores RGB.
branco = (255, 255, 255)

#Imagem de fundo
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Carregar sprites
spritesheet_andar_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
spritesheet_andar_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()


# Criação do personagem
personagem = Personagem(spritesheet_andar_direita, spritesheet_andar_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

#Variavel para o pulo do player
pulando = False
velocidade_do_pulo = -20

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
