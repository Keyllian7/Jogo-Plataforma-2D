import pygame

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, sprite_direita, sprite_esquerda, posicao_inicial):
        pygame.sprite.Sprite.__init__(self)
        self.andar_direita = []
        self.andar_esquerda = []
        for i in range(8):
            img = sprite_direita.subsurface((i * 64, 0), (64, 47))
            self.andar_direita.append(img)
            img = sprite_esquerda.subsurface((i * 64, 0), (64, 47))
            self.andar_esquerda.append(img)

        self.index_lista = 0
        self.image = self.andar_direita[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = posicao_inicial
        self.direction = 'right'

        # Tamanho do personagem
        self.image = pygame.transform.scale(self.image, (int(64*1.5), int(47*1.5)))

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


class Vampiro(Inimigo):
    def __init__(self, vampiro_direita, vampiro_esquerda, posicao_inicial):
        super().__init__(vampiro_direita, vampiro_esquerda, posicao_inicial)

class Zumbi(Inimigo):
    def __init__(self, sprite_direita_zumbi, sprite_esquerda_zumbi, posicao_inicial):
        super().__init__(sprite_direita_zumbi, sprite_esquerda_zumbi, posicao_inicial)

class Lobisomem(Inimigo):
    def __init__(self, lobo_direita, lobo_esquerda, posicao_inicial):
        super().__init__(lobo_direita, lobo_esquerda, posicao_inicial)