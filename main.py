import pygame
from player import Personagem
from pygame.locals import *
from sys import exit


pygame.init()

largura = 960
altura = 540

preto = (0, 0, 0)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Animação')

todas_sprites = pygame.sprite.Group()
personagem = Personagem()
todas_sprites.add(personagem)

imagem_fundo = pygame.image.load('Jogo-Plataforma-2D\Assets\Background.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

fps = pygame.time.Clock()

while True:
    fps.tick(60)
    tela.fill(preto)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                personagem.direita = True
            if event.key == K_a:
                personagem.esquerda = True
            if event.key == K_SPACE:
                personagem.jump()
        elif event.type == KEYUP:
            if event.key == K_d:
                personagem.direita = False
            if event.key == K_a:
                personagem.esquerda = False

    tela.blit(imagem_fundo, (0, 0))
    todas_sprites.draw(tela)
    todas_sprites.update()
    pygame.display.flip()


