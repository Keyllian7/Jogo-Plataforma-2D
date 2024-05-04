import pygame, os , math, random
from pygame.locals import *
from sys import exit
from player import Masculino
from inimigos import Vampiro, Lobisomem, Zumbi
from projetil import Flecha
from plataformas import Plataforma


pygame.init()

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
vermelho = (255, 0, 0)

#Imagem de fundo
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background_Gameplay.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Carregar sprites
personagem_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
personagem_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()
vampiro_direita = pygame.image.load(os.path.join(diretorio_imagens, 'VampiroDireita.png')).convert_alpha()
vampiro_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'VampiroEsquerda.png')).convert_alpha()
lobo_direita = pygame.image.load(os.path.join(diretorio_imagens, 'Lobisomen_direita.png')).convert_alpha()
lobo_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'Lobisomen_esquerda.png')).convert_alpha()

# Criação do personagem
personagem = Masculino(personagem_direita, personagem_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)


# Variável para controle do respawn de inimigos
tempo_para_respawn = 10 
ultimo_respawn_lobo = pygame.time.get_ticks()  
ultimo_respawn_vampiro = pygame.time.get_ticks()

# Listaz para armazenar objetos
plataformas = []
inimigos = []
flechas = []

# Carregar sprite da flecha
flecha_imagem = pygame.image.load(os.path.join(diretorio_imagens, 'flecha.png')).convert_alpha()


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
flecha = None

vidas_personagem = 10
pontos_personagem = 0

# Fonte para o contador de vidas e pontos
fonte = pygame.font.Font(None, 36)

# Função para renderizar o contador de vidas
def renderizar_vidas():
    texto_vidas = fonte.render(f'Vidas: {vidas_personagem}', True, (vermelho))
    tela.blit(texto_vidas, (10, 10))

def renderizar_pontos():
    texto_pontos = fonte.render(f'Pontos: {pontos_personagem}', True, (branco))
    tela.blit(texto_pontos, (875, 10))
    

 # Variável para controlar o tempo de invencibilidade do jogador após uma colisão com um inimigo
tempo_invencibilidade = 0
tempo_invencibilidade_maximo = 3000 

G = 15.807

# Loop Principal do jogo
while True:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()

    T = fps.get_time() / 1000
    F = G * T
    aceleracao_y_inimigos += F
    aceleracao_y_player += F

    personagem.rect.y += aceleracao_y_player
    
    # Desenha as plataformas na tela
    for plataforma in plataformas:
        tela.blit(plataforma.image, plataforma.rect)

    # Atualiza a posição e a animação dos inimigos
    for inimigo in inimigos:
        inimigo.update_animation()
        inimigo.update_position()

        if isinstance(inimigo, Lobisomem):
            inimigo.rect.y += aceleracao_y_inimigos

        # Verifica se o inimigo atingiu o chão
        if inimigo.rect.y > 513:
            inimigo.rect.y = 513

        # Verifica colisões entre o personagem e os inimigos
        if tempo_invencibilidade <= 0 and personagem.rect.colliderect(inimigo.rect):
            # Reduz o número de vidas do personagem
            vidas_personagem -= 1
            # Define o tempo de invencibilidade do jogador
            tempo_invencibilidade = tempo_invencibilidade_maximo

            # Verifica se o personagem ainda tem vidas
            if vidas_personagem == 0:
                # Encerra o jogo se o personagem estiver sem vidas
                pygame.quit()
                exit()

    # Reduz o tempo de invencibilidade do jogador
    tempo_invencibilidade = max(0, tempo_invencibilidade - fps.get_time())

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

    # Verifica se é hora de fazer o respawn de um novo vampiro
    tempo_atual_vampiro = pygame.time.get_ticks()
    if tempo_atual_vampiro - ultimo_respawn_vampiro > tempo_para_respawn * 1000:
        if len(inimigos) < 2:
            novo_vampiro = Vampiro(vampiro_direita, vampiro_esquerda, (0, 0)) 
            novo_vampiro.rect.x = random.randint(0, largura - novo_vampiro.rect.width)
            novo_vampiro.rect.y = 0
            inimigos.append(novo_vampiro)
            ultimo_respawn_vampiro = tempo_atual_vampiro

    # Atualiza a posição do inimigo em relação ao personagem
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

    # Verifica se é hora de fazer o respawn de um novo lobo
    tempo_atual_lobo = pygame.time.get_ticks()
    if tempo_atual_lobo - ultimo_respawn_lobo > tempo_para_respawn * 700:
        novo_lobo = Lobisomem(lobo_direita, lobo_esquerda, (0, 0)) 
        novo_lobo.rect.x = random.choice([0, largura - novo_lobo.rect.width])
        novo_lobo.rect.y = random.randint(altura // 2, altura - novo_lobo.rect.height)
        inimigos.append(novo_lobo)
        ultimo_respawn_lobo = tempo_atual_lobo

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
        aceleracao_y_player = - 9
        pulou = True

    if pygame.mouse.get_pressed()[0]:
        angle = math.atan2(mouse_pos[1] - personagem.rect.y, mouse_pos[0] - personagem.rect.x)
        nova_flecha = Flecha(flecha_imagem, personagem.rect.x, personagem.rect.y, angle)
        flechas.append(nova_flecha)

    if personagem.rect.y > 513:
        personagem.rect.y = 513
        aceleracao_y_player = 0
        fps = pygame.time.Clock()
        pulou = False

    # Verifica colisões entre o personagem e as plataformas
    for plataforma in plataformas:
        if personagem.rect.colliderect(plataforma.rect):
            personagem.rect.bottom = plataforma.rect.top
            pulou = False

    # Atualiza a posição das flechas e verifica colisões com os inimigos
    for flecha in flechas:
        flecha.update()
        for inimigo in inimigos:
            if pygame.sprite.collide_rect(flecha, inimigo):
                flechas.remove(flecha)
                inimigos.remove(inimigo)
                pontos_personagem += 1
                break

    if flechas:
        for flecha in flechas:
            tela.blit(flecha.image, flecha.rect)
    
    # Desenha os sprites na tela
    sprites_personagem.draw(tela)

    for lobo in inimigos:
        tela.blit(lobo.image, lobo.rect)
    
    for vampiro in inimigos:
        tela.blit(vampiro.image, vampiro.rect)

    renderizar_vidas()
    renderizar_pontos()

    # Função para atualizar a tela 
    pygame.display.flip()
