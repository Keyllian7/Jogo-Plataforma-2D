import pygame
import math
import os
from pygame.locals import *
from sys import exit
from player import Personagem
from inimigos import Inimigo

pygame.init()

# Diretórios dos arquivos
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

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
sprite_inimigo = pygame.image.load(os.path.join(diretorio_imagens, 'Java.png')).convert_alpha()

# Redimensionar a imagem do inimigo
largura_inimigo = 50  
altura_inimigo = 50   
sprite_inimigo = pygame.transform.scale(sprite_inimigo, (largura_inimigo, altura_inimigo))

# Criação do personagem
personagem = Personagem(spritesheet_andar_direita, spritesheet_andar_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

# Criação do inimigo
inimigos = []
inimigos.append(Inimigo(sprite_inimigo, 100, 100))
inimigos.append(Inimigo(sprite_inimigo, 200, 200))

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

    # Atualiza a posição dos inimigos em relação ao personagem
    for inimigo in inimigos:
        direcao_x = personagem.rect.x - inimigo.rect.x
        direcao_y = personagem.rect.y - inimigo.rect.y
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        
        direcao_x /= distancia
        direcao_y /= distancia
        
        velocidade = 2
        
        inimigo.rect.x += direcao_x * velocidade
        inimigo.rect.y += direcao_y * velocidade

    # Desenha os inimigos na tela
    for inimigo in inimigos:
        tela.blit(inimigo.image, inimigo.rect)

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
            velocidade_do_pulo = -20

    # Desenha o personagem na tela
    sprites_personagem.draw(tela)

    mov_altura = altura % imagem_de_fundo.get_rect().width
    tela.blit(imagem_de_fundo, (imagem_de_fundo.get_rect().width), 0)
    if mov_altura < 960:
        tela.blit(imagem_de_fundo, (mov_altura, 0))

    altura-= 1/5

    # Atualiza a tela
    pygame.display.flip()
