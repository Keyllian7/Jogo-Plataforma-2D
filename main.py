import pygame
from pygame.locals import *
from sys import exit
pygame.init()

largura = 960
altura = 540

preto = (0, 0, 0)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Animação')

class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita1.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita2.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita3.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita4.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita5.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita6.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita7.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita8.png'))
        self.sprites.append(pygame.image.load('Jogo-Plataforma-2D\PassosDireita\PassoDireita9.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (int(38*1.5), int(48*1.5)))

        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 460

        self.animar = False
        self.direita = False
        self.esquerda = False
        self.pulando = False
        self.velocidade_y = 0
        self.double_jump = False  
        self.last_jump_time = 0  

    def andar_frente(self):
        self.animar = True

    def update(self):
        if self.animar:
            self.atual += 0.25
            if self.atual >= len(self.sprites):
                self.atual = 0
                self.animar = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (int(38*1.5), int(48*1.5)))

        if self.direita and self.rect.right < largura:
            self.rect.x += 5
            self.andar_frente()

        if self.esquerda and self.rect.left > 0:
            self.rect.x -= 5
            self.andar_frente()
            self.image = pygame.transform.flip(self.image, True, False)

        if self.pulando:
            if self.rect.top > 0:  
                self.rect.y -= self.velocidade_y
                self.velocidade_y -= 1
                if self.rect.y >= 460:
                    self.rect.y = 460
                    self.pulando = False
                    self.double_jump = True  

    def jump(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_jump_time < 200:  
            if self.double_jump:
                self.pulando = True
                self.velocidade_y = 15
                self.double_jump = False
        else:
            if not self.pulando:
                self.pulando = True
                self.velocidade_y = 15
        self.last_jump_time = current_time

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


