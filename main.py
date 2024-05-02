import pygame, os , math, random
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
vampiro_direita = pygame.image.load(os.path.join(diretorio_imagens, 'VampiroDireita.png')).convert_alpha()
vampiro_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'VampiroEsquerda.png')).convert_alpha()
lobo_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
lobo_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()

# Criação do personagem
personagem = Masculino(spritesheet_andar_direita, spritesheet_andar_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

## Lista para armazenar os inimigos
inimigos = []

# Variável para controle do respawn de inimigos
tempo_para_respawn = 10 
ultimo_respawn_lobo = pygame.time.get_ticks()  
ultimo_respawn_vampiro = pygame.time.get_ticks()

# Lista para armazenar as plataformas
plataformas = []

# Criação das plataformas
imagem_plataforma = pygame.image.load(os.path.join(diretorio_imagens, 'Plataforma.png')).convert_alpha()
plataforma1 = Plataforma(imagem_plataforma, 200, 400)
plataforma2 = Plataforma(imagem_plataforma, 500, 300)
plataforma3 = Plataforma(imagem_plataforma, 700, 200)
plataformas.extend([plataforma1, plataforma2, plataforma3])

acelecacao_x = 0
aceleracao_y_inimigos = 0
aceleracao_y_player = 0

pulou = False

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
    aceleracao_y_inimigos += F
    aceleracao_y_player += F

    personagem.rect.y += aceleracao_y_player
    
    # Desenha as plataformas na tela
    for plataforma in plataformas:
        tela.blit(plataforma.image, plataforma.rect)
    
    # Atualiza a posição dos inimigos em relação ao personagem
    for lobo in inimigos:
        if not personagem.rect.colliderect(lobo.rect): 
            direcao_x = personagem.rect.x - lobo.rect.x
            direcao_y = personagem.rect.y - lobo.rect.y
            distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
            
            direcao_x /= distancia
            direcao_y /= distancia
            
            velocidade = 2
            
            lobo.rect.x += direcao_x * velocidade


        if lobo.rect.x < personagem.rect.x:
            lobo.direction = 'right'
        else:
            lobo.direction = 'left'
        lobo.update()

        lobo.rect.y += aceleracao_y_inimigos

        if lobo.rect.y > 513:
            lobo.rect.y = 513
            




    # Desenha os inimigos na tela
    for lobo in inimigos:
        tela.blit(lobo.image, lobo.rect)

    # Verifica se é hora de fazer o respawn de um novo lobo
    tempo_atual_lobo = pygame.time.get_ticks()
    if tempo_atual_lobo - ultimo_respawn_lobo > tempo_para_respawn * 700:
        novo_lobo = Lobisomem(lobo_direita, lobo_esquerda, (0, 0))  # Posição inicial temporária
        novo_lobo.rect.x = random.choice([0, largura - novo_lobo.rect.width])
        novo_lobo.rect.y = random.randint(altura // 2, altura - novo_lobo.rect.height)
        inimigos.append(novo_lobo)
        ultimo_respawn_lobo = tempo_atual_lobo
    

    # Atualiza a posição dos inimigos em relação ao personagem
    for vampiro in inimigos:
        if not personagem.rect.colliderect(vampiro.rect): 
            direcao_x = personagem.rect.x - vampiro.rect.x
            direcao_y = personagem.rect.y - vampiro.rect.y
            distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        
            direcao_x /= distancia
            direcao_y /= distancia
        
            velocidade = 1
        
            vampiro.rect.x += direcao_x * velocidade
            vampiro.rect.y += direcao_y * velocidade

        if vampiro.rect.x < personagem.rect.x:
            vampiro.direction = 'right'
        else:
            vampiro.direction = 'left'
        
        vampiro.update()


    # Desenha os vampiros na tela
    for vampiro in inimigos:
        tela.blit(vampiro.image, vampiro.rect)

    # Verifica se é hora de fazer o respawn de um novo vampiro
    tempo_atual_vampiro = pygame.time.get_ticks()
    if tempo_atual_vampiro - ultimo_respawn_vampiro > tempo_para_respawn * 1000:
        novo_vampiro = Vampiro(vampiro_direita, vampiro_esquerda, (0, 0))  # Posição inicial temporária
        novo_vampiro.rect.x = random.randint(0, largura - novo_vampiro.rect.width)
        novo_vampiro.rect.y = 0
        inimigos.append(novo_vampiro)
        ultimo_respawn_vampiro = tempo_atual_vampiro

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
    
    if teclas_press[K_SPACE] and not pulou:
        aceleracao_y_player = - 10
        pulou = True

    if personagem.rect.y > 513:
        personagem.rect.y = 513
        aceleracao_y_player = 0
        fps = pygame.time.Clock()
        pulou = False


    for plataforma in plataformas:
        if personagem.rect.colliderect(plataforma.rect):
            personagem.rect.bottom = plataforma.rect.top
            pulou = False
        

    # Desenha o personagem na tela
    sprites_personagem.draw(tela)

    # Atualiza a tela
    pygame.display.flip()
    pygame.display.update()
