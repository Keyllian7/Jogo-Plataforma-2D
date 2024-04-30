import pygame

largura = 960
altura = 540

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
