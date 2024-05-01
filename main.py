import pygame, os , math
from pygame.locals import *
from sys import exit
from player import Personagem, Masculino, Feminino
from inimigos import Inimigo, Vampiro, Lobisomem, Zumbi
from plataformas import Plataforma


pygame.init()

G = 20.807

# Diretórios dos arquivos
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

# Tamanho da matriz de pixels em que o jogo será reproduzido.
largura = 1000
altura = 600

# Criação da variável e argumentos para a execução da matriz.
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('UNP Survival')
fps = pygame.time.Clock()

# Variáveis que contém valores RGB.
branco = (255, 255, 255)

#Imagem de fundo
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background_Gameplay.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Carregar sprites
spritesheet_andar_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
spritesheet_andar_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()
sprite_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosVampiroDireita.png')).convert_alpha()
sprite_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosVampiroEsquerda.png')).convert_alpha()


# Criação do personagem
personagem = Masculino(spritesheet_andar_direita, spritesheet_andar_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

## Lista para armazenar os inimigos
inimigos = []

# Variável para controle do respawn de vampiros
tempo_para_respawn = 10 
ultimo_respawn = pygame.time.get_ticks()  

# Lista para armazenar as plataformas
plataformas = []

# Criação das plataformas
imagem_plataforma = pygame.image.load(os.path.join(diretorio_imagens, 'Plataforma.png')).convert_alpha()
plataforma1 = Plataforma(imagem_plataforma, 200, 400)
plataforma2 = Plataforma(imagem_plataforma, 500, 300)
plataforma3 = Plataforma(imagem_plataforma, 700, 200)
plataformas.extend([plataforma1, plataforma2, plataforma3])

acelecacao_x = 0
aceleracao_y = 0

ultimo_salto = pygame.time.get_ticks()

# Loop Principal do jogo
while True:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    T = fps.get_time() / 1000
    F = G * T
    aceleracao_y += F

    personagem.rect.y += aceleracao_y
    
    if personagem.rect.y > 513:
        personagem.rect.y = 513
        aceleracao_y = 0
        fps = pygame.time.Clock()



    # Desenha as plataformas na tela
    for plataforma in plataformas:
        tela.blit(plataforma.image, plataforma.rect)
    
    # Atualiza a posição dos inimigos em relação ao personagem
    for vampiro in inimigos:
        if not personagem.rect.colliderect(vampiro.rect): 
            direcao_x = personagem.rect.x - vampiro.rect.x
            direcao_y = personagem.rect.y - vampiro.rect.y
            distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
            
            direcao_x /= distancia
            direcao_y /= distancia
            
            velocidade = 2
            
            vampiro.rect.x += direcao_x * velocidade
            vampiro.rect.y += direcao_y * velocidade


            if vampiro.rect.bottom > 513:
                vampiro.rect.bottom = 513

        if vampiro.rect.x < personagem.rect.x:
            vampiro.direction = 'right'
        else:
            vampiro.direction = 'left'
        vampiro.update()

    # Desenha os inimigos na tela
    for vampiro in inimigos:
        tela.blit(vampiro.image, vampiro.rect)

    # Verifica se é hora de fazer o respawn de um novo vampiro
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_respawn > tempo_para_respawn * 1000:
        novo_vampiro = Vampiro(sprite_direita, sprite_esquerda)
        inimigos.append(novo_vampiro)
        ultimo_respawn = tempo_atual

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
    
    if teclas_press[K_SPACE]:
        aceleracao_y = -9
        fps = pygame.time.Clock()


    for plataforma in plataformas:
        if personagem.rect.colliderect(plataforma.rect):
            personagem.rect.bottom = plataforma.rect.top 
        

    # Desenha o personagem na tela
    sprites_personagem.draw(tela)

    # Atualiza a tela
    pygame.display.flip()
    pygame.display.update()
    fps.tick(60)
