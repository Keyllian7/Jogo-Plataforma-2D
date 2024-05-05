import pygame, os, math, random, time
from pygame.locals import *
from sys import exit
from player import Masculino
from inimigos import Vampiro, Lobisomem, Zumbi
from projetil import Flecha
from plataformas import Plataforma
import subprocess


pygame.init()

# Tamanho da matriz de pixels em que o jogo será reproduzido.
largura = 1000
altura = 600

# Criação da variável e argumentos para a execução da matriz.
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('UNP Survival')
fps = pygame.time.Clock()

# Diretórios dos arquivos
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

# Variáveis que contém valores RGB.
branco = (255, 255, 255)
vermelho = (255, 0, 0)

#Imagem de fundo
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background_Gameplay.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Carregar sprites
flecha_imagem = pygame.image.load(os.path.join(diretorio_imagens, 'flecha.png')).convert_alpha()
personagem_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
personagem_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()
vampiro_direita = pygame.image.load(os.path.join(diretorio_imagens, 'VampiroDireita.png')).convert_alpha()
vampiro_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'VampiroEsquerda.png')).convert_alpha()
lobo_direita = pygame.image.load(os.path.join(diretorio_imagens, 'Lobisomen_direita.png')).convert_alpha()
lobo_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'Lobisomen_esquerda.png')).convert_alpha()
zumbi_direita = pygame.image.load(os.path.join(diretorio_imagens, 'Zumbi_direita.png')).convert_alpha()
zumbi_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'Zumbi_esquerda.png')).convert_alpha()

#Musicas e efeitos sonoros
dano_ao_personagem = pygame.mixer.Sound(os.path.join(diretorio_sons, 'dano-personagem.wav'))
matou_o_inimigo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'matou-inimigo.wav'))
musica_de_fundo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'musica de fundo.mp3'))
efeito_de_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'pulo.wav'))
morte_personagem = pygame.mixer.Sound(os.path.join(diretorio_sons, 'morte_personagem.wav'))
efeito_flechas = pygame.mixer.Sound(os.path.join(diretorio_sons, 'flecha-efeito.wav'))

musica_de_fundo.play()
musica_de_fundo.set_volume(0.10)

# Listas para armazenar objetos
plataformas = []
inimigos = []
flechas = []

# Criação do personagem
personagem = Masculino(personagem_direita, personagem_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

# Criação das plataformas
imagem_plataforma = pygame.image.load(os.path.join(diretorio_imagens, 'Plataforma.png')).convert_alpha()
imagem_plataforma_menor = pygame.image.load(os.path.join(diretorio_imagens, 'Plataforma-menor.png')).convert_alpha()
plataforma1 = Plataforma(imagem_plataforma, -40, 365)
plataforma2 = Plataforma(imagem_plataforma, 200, 415)
plataforma3 = Plataforma(imagem_plataforma, 520, 365)
plataforma4 = Plataforma(imagem_plataforma_menor, 300, 285)
plataforma5 = Plataforma(imagem_plataforma_menor, 865, 285)
plataforma6 = Plataforma(imagem_plataforma, 750, 415)
plataformas.extend([plataforma1, plataforma2, plataforma3, plataforma4, plataforma5, plataforma6])

# Variável para controle do respawn de inimigos
tempo_para_respawn = 10 
ultimo_respawn_lobo = pygame.time.get_ticks()  
ultimo_respawn_vampiro = pygame.time.get_ticks()
ultimo_respawn_zumbi = pygame.time.get_ticks()

#variaveis para controle de movimento do zumbi
velocidade_zumbi = 1
direcao_zumbi = 1 
posicao_inicial_zumbi = [0, altura - 100]

aceleracao_y_inimigos = 0
aceleracao_y_personagem = 0

pulou = False
flecha = None

#variaveis para controle de vidas e pontos do personagem
vidas_personagem = 10
pontos_personagem = 0

#variaveis para controle do tempo de invencibilidade e tempo de disparos do personagem
ultimo_disparo_tempo = 0
tempo_entre_disparos = 2000
tempo_invencibilidade = 0
tempo_invencibilidade_maximo = 2000 

# Fonte para o contador de vidas e pontos
fonte = pygame.font.Font(None, 36)

# Função para renderizar o contador de vidas e pontos
def renderizar_vidas():
    texto_vidas = fonte.render(f'Vidas: {vidas_personagem}', True, (vermelho))
    tela.blit(texto_vidas, (10, 10))

def renderizar_pontos():
    texto_pontos = fonte.render(f'Pontos: {pontos_personagem}', True, (branco))
    tela.blit(texto_pontos, (875, 10))

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

    G = 15.807
    T = fps.get_time() / 1000
    F = G * T
    aceleracao_y_inimigos += F
    aceleracao_y_personagem += F

    personagem.rect.y += aceleracao_y_personagem

    # Atualiza a posição e a animação dos inimigos
    for inimigo in inimigos:
        inimigo.update_animation()
        inimigo.update_position()

        if isinstance(inimigo, Lobisomem,):
            inimigo.rect.y += aceleracao_y_inimigos

        # Verifica se o inimigo atingiu o chão
        if inimigo.rect.y > 513:
            inimigo.rect.y = 513

        # Verifica colisões entre o personagem e os inimigos
        if tempo_invencibilidade <= 0 and pygame.sprite.collide_mask(personagem, inimigo):
            dano_ao_personagem.play()
            vidas_personagem -= 1
            tempo_invencibilidade = tempo_invencibilidade_maximo

    tempo_invencibilidade = max(0, tempo_invencibilidade - fps.get_time())
    
    #controla a posição do inimigo
    for inimigo in inimigos:
        if isinstance(inimigo, Zumbi):
            inimigo.rect.x += velocidade_zumbi * direcao_zumbi
        
        if inimigo.rect.left <= 0 or inimigo.rect.right >= largura:
            direcao_zumbi *= -1

# Atualiza a posição e a animação do zumbi em relação ao personagem
    for inimigo in inimigos:
        if not isinstance(inimigo, Zumbi):
            inimigo.update_animation()
            inimigo.update_position()

# Atualiza a posição dos inimigos em relação ao personagem
    for inimigo in inimigos:
        if not pygame.sprite.collide_mask(personagem, inimigo): 
            direcao_x = personagem.rect.x - inimigo.rect.x
            direcao_y = personagem.rect.y - inimigo.rect.y
            distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        
            direcao_x /= distancia
            direcao_y /= distancia
        
            velocidade = inimigo.speed
        
            inimigo.rect.x += direcao_x * velocidade
            inimigo.rect.y += direcao_y * velocidade

        if inimigo.rect.x < personagem.rect.x:
            inimigo.direction = 'right'
        else:
            inimigo.direction = 'left'
        
        inimigo.update()

    # Verifica se é hora de fazer o respawn de um novo zumbi
    tempo_atual_zumbi = pygame.time.get_ticks()
    if tempo_atual_zumbi - ultimo_respawn_zumbi > tempo_para_respawn * 500:
            novo_zumbi = Zumbi(zumbi_direita, zumbi_esquerda, (0, 0)) 
            novo_zumbi.rect.x = random.choice([0, largura - novo_zumbi.rect.width])
            novo_zumbi.rect.y = random.randint(altura // 2, altura - novo_zumbi.rect.height)
            inimigos.append(novo_zumbi)
            ultimo_respawn_zumbi = tempo_atual_zumbi
    
    # Verifica se é hora de fazer o respawn de um novo vampiro
    tempo_atual_vampiro = pygame.time.get_ticks()
    if tempo_atual_vampiro - ultimo_respawn_vampiro > tempo_para_respawn * 1000:
            novo_vampiro = Vampiro(vampiro_direita, vampiro_esquerda, (0, 0)) 
            novo_vampiro.rect.x = random.randint(0, largura - novo_vampiro.rect.width)
            novo_vampiro.rect.y = 0
            inimigos.append(novo_vampiro)
            ultimo_respawn_vampiro = tempo_atual_vampiro

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
        aceleracao_y_personagem = - 9
        pulou = True
        efeito_de_pulo.play()

    if pygame.mouse.get_pressed()[0]:
        tempo_atual = pygame.time.get_ticks()
        
        if tempo_atual - ultimo_disparo_tempo >= tempo_entre_disparos:
            angle = math.atan2(mouse_pos[1] - personagem.rect.y, mouse_pos[0] - personagem.rect.x)
            nova_flecha = Flecha(flecha_imagem, personagem.rect.x, personagem.rect.y, angle)
            flechas.append(nova_flecha)
            efeito_flechas.play()
            ultimo_disparo_tempo = tempo_atual

    #monitora a posição y do player para evitar que ele caia da tela
    if personagem.rect.y > 513:
        personagem.rect.y = 513
        aceleracao_y_personagem = 0
        fps = pygame.time.Clock()
        pulou = False

    # Verifica colisões entre o personagem e as plataformas
    for plataforma in plataformas:
        if pygame.sprite.collide_mask(personagem, plataforma):
            personagem.rect.bottom = plataforma.rect.top
            pulou = False

    # Atualiza a posição das flechas, verifica colisões com os inimigos e da a pontuação de acord com cada inimigo eliminado
    for flecha in flechas:
        flecha.update()
        for inimigo in inimigos:
            if pygame.sprite.collide_mask(flecha, inimigo):
                flechas.remove(flecha)
                inimigos.remove(inimigo)
                pontos_personagem += 1
                matou_o_inimigo.play()
                break

    # Desenha os sprites na tela
    for plataforma in plataformas:
        tela.blit(plataforma.image, plataforma.rect)

    if flechas:
        for flecha in flechas:
            tela.blit(flecha.image, flecha.rect)
    
    sprites_personagem.draw(tela)

    for lobo in inimigos:
        tela.blit(lobo.image, lobo.rect)
    
    for vampiro in inimigos:
        tela.blit(vampiro.image, vampiro.rect)

    renderizar_vidas()
    renderizar_pontos()

    # Função para atualizar a tela a cada ciclo do loop.
    pygame.display.flip()

    if vidas_personagem == 0:
        morte_personagem.play() 
        time.sleep(1)
        # Encerra o jogo
        subprocess.Popen(["python", "Jogo-Plataforma-2D/tela_final.py", str(pontos_personagem)])
        pygame.quit()