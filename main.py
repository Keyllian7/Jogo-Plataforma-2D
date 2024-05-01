import pygame, os , math
from pygame.locals import *
from sys import exit
from player import Personagem, Masculino, Feminino
from inimigos import Inimigo, Vampiro, Lobisomem, Zumbi
from plataformas import Plataforma

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
sprite_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosVampiroDireita.png')).convert_alpha()
sprite_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosVampiroEsquerda.png')).convert_alpha()


# Criação do personagem
personagem = Masculino(spritesheet_andar_direita, spritesheet_andar_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

## Lista para armazenar os inimigos
inimigos = []

# Variável para controle do respawn de vampiros
tempo_para_respawn = 10  # Tempo em segundos para o próximo respawn
ultimo_respawn = pygame.time.get_ticks()  # Último momento de respawn

#Variavel para o pulo do player
pulando = False
velocidade_do_pulo = -15

# Controle de FPS
fps = pygame.time.Clock()


#definindo a gravidade do jogo
velocidade_vertical = 0
aceleracao_gravidade = 0.1

# Lista para armazenar as plataformas
plataformas = []

# Criação das plataformas
imagem_plataforma = pygame.image.load(os.path.join(diretorio_imagens, 'java.png')).convert_alpha()
plataforma1 = Plataforma(imagem_plataforma, 200, 400)
plataforma2 = Plataforma(imagem_plataforma, 500, 300)
plataforma3 = Plataforma(imagem_plataforma, 700, 200)
plataformas.extend([plataforma1, plataforma2, plataforma3])

# Loop Principal do jogo
while True:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

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

            velocidade_vertical += aceleracao_gravidade
            vampiro.rect.y += velocidade_vertical

            if vampiro.rect.bottom > altura:
                vampiro.rect.bottom = altura

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

    #Comando de pulo do personagem
    if teclas_press[K_SPACE] and not pulando:
        pulando = True

    if pulando:
        personagem.rect.y += velocidade_do_pulo
        velocidade_do_pulo += 1

        # Verifica se o personagem atingiu o chão e reinicia o comando
        if personagem.rect.y >= 460:
            pulando = False
            velocidade_do_pulo = -15

    for plataforma in plataformas:
        if personagem.rect.colliderect(plataforma.rect) and velocidade_do_pulo > 0:
            velocidade_do_pulo = 0  # Para o pulo
            personagem.rect.bottom = plataforma.rect.top  # Posiciona o personagem sobre a plataforma

    for vampiro in inimigos:
        if vampiro.rect.colliderect(plataforma.rect) and velocidade_do_pulo > 0:
            velocidade_do_pulo = 0  
            vampiro.rect.bottom = plataforma.rect.top  # Posiciona o vampiro sobre a plataforma

    # Desenha o personagem na tela
    sprites_personagem.draw(tela)

    # Atualiza a tela
    pygame.display.flip()
