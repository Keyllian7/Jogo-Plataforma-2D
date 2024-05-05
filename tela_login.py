import pygame, os, time
from pygame.locals import *
from player import Masculino, Feminino
import subprocess

# Inicialize o Pygame
pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

musica_de_fundo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'musica de fundo.mp3'))

iniciar_jogo_efeito = pygame.mixer.Sound(os.path.join(diretorio_sons, 'iniciar-jogo.wav'))

caminho_main = os.path.join(os.path.dirname(__file__), "main.py")


musica_de_fundo.play()
musica_de_fundo.set_volume(0.10)


# Defina as cores
preto = (0, 0, 0)

# Diretorios de arquivos para o codigo
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')

# Defina a largura e a altura da tela
largura = 960
altura = 540
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Unp Survival - Login')


# Titulo do jogo
unp_survival = pygame.image.load(os.path.join(diretorio_imagens, 'Titulo UNP.png')).convert_alpha()
unp_survival = pygame.transform.scale(unp_survival, (500, 125))

# Imagem do Nome "Usuario"
Usuario_Login = pygame.image.load(os.path.join(diretorio_imagens, 'Usuário UNP.png'))
Usuario_Login = pygame.transform.scale(Usuario_Login, (150, 46))

# Caixa do nome do Usuario:

caixa_login = pygame.image.load(os.path.join(diretorio_imagens, 'Caixa.png')).convert_alpha()

# Imagem do botão "Iniciar Jogo"
iniciar_Jogo = pygame.image.load(os.path.join(diretorio_imagens, 'Iniciar Jogo UNP.png'))
iniciar_Jogo = pygame.transform.scale(iniciar_Jogo, (150, 56))

# Criação do botão iniciar
iniciar_Jogo_rect = iniciar_Jogo.get_rect()
iniciar_Jogo_rect.center = (483, 372)

# Background da tela 
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Sprite Personagem e Inimigos do jogo
spritesheet_andar_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
spritesheet_andar_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()

# Personagem do jogo
personagem_M = Masculino(spritesheet_andar_direita, spritesheet_andar_esquerda)
personagem_M.rect.center = (480, 500)
sprites_personagem_M = pygame.sprite.Group()
sprites_personagem_M.add(personagem_M)

personagem_F = Feminino(spritesheet_andar_direita, spritesheet_andar_esquerda)
personagem_F.rect.center = (430, 500)
sprites_personagem_F = pygame.sprite.Group()
sprites_personagem_F.add(personagem_F)

# Defina a fonte para o texto
fonte_usuario = pygame.font.Font(None, 25)

# Função do click
clicked = False

# Variável para armazenar o nome do usuário
nome_usuario = ""

# Loop principal do jogo
rodando = True
while rodando:
    # Tratar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            # Verificar se uma tecla foi pressionada enquanto o campo de texto está ativo
            if evento.key == pygame.K_BACKSPACE:
                # Apagar o último caractere do nome do usuário
                nome_usuario = nome_usuario[:-1]
            elif evento.key == pygame.K_RETURN:
                # Se pressionar Enter, armazene o nome do usuário onde desejar
                nome_do_jogador = nome_usuario
                print("Nome do jogador:", nome_do_jogador)
                time.sleep(1)
                pygame.quit()
                subprocess.Popen(["python", caminho_main, nome_usuario])
            else:
                # Adicionar caracteres digitados ao nome do usuário
                nome_usuario += evento.unicode
        # Função do Iniciar jogo
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if iniciar_Jogo_rect.collidepoint(evento.pos):
                clicked = True

    # Movimentar o fundo
    tela.blit(imagem_de_fundo, (0, 0))
    mov_tela = altura % imagem_de_fundo.get_rect().width
    tela.blit(imagem_de_fundo, (mov_tela - imagem_de_fundo.get_rect().width, 0))
    if mov_tela < 960:
        tela.blit(imagem_de_fundo, (mov_tela, 0))
    altura -= 1

    # Desenhar o título do jogo
    tela.blit(unp_survival, (230, 0))

    # Desenhar o campo de entrada de texto
    texto_nome = fonte_usuario.render(nome_usuario, True, preto)
    tela.blit(caixa_login, (0, -25))
    tela.blit(texto_nome, (405, 220))

    # Desenhar o texto "Digite seu nome"
    tela.blit(Usuario_Login, (405, 175))

    # Desenhar o botão de iniciar o jogo
    tela.blit(iniciar_Jogo, iniciar_Jogo_rect)

    #Mostra persongaem na tela
    sprites_personagem_F.update()
    sprites_personagem_F.draw(tela)

    # Atualizar a tela
    pygame.display.flip()

    # Abrir o Jogo ao clicar no "Iniciar Jogo"
    if clicked:
        iniciar_jogo_efeito.play()
        time.sleep(1)
        pygame.quit()
        subprocess.Popen(["python", "Jogo-Plataforma-2D\main.py"])
        clicked = False

# Finalizar o Pygame
pygame.quit()
