import pygame, os , math
from pygame.locals import *
from sys import exit
from player import Personagem, Masculino, Feminino
from inimigos import Inimigo, Vampiro, Lobisomem, Zumbi
from plataformas import Plataforma
import subprocess

# Inicialize o Pygame
pygame.init()

# Defina as cores
BRANCO = (255, 255, 255)
#Diretorios de arquivos para o codigo
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

# Defina a largura e a altura da tela
largura = 960
altura = 540
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Unp Survival - Login')
#Titulo do jogo
unp_survival = pygame.image.load(os.path.join(diretorio_imagens,'Titulo UNP.png')).convert_alpha()
unp_survival = pygame.transform.scale(unp_survival, (500, 125.49))
#Imagem do Nome "Usuario"
Usuario_Login = pygame.image.load(os.path.join(diretorio_imagens,'Usuário UNP.png'))
Usuario_Login = pygame.transform.scale(Usuario_Login, (150, 46.4))
#Imagem do botão "Iniciar Jogo"
iniciar_Jogo = pygame.image.load(os.path.join(diretorio_imagens,'Iniciar Jogo UNP.png'))
iniciar_Jogo = pygame.transform.scale(iniciar_Jogo, (150, 56.4))
#Criação do botão iniciar
iniciar_Jogo_rect = iniciar_Jogo.get_rect()
iniciar_Jogo_rect.center = (483,372)
#Background da tela 
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Background.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))
#Sprite Personagem do jogo
spritesheet_andar_direita = pygame.image.load(os.path.join(diretorio_imagens, 'PassosDireita.png')).convert_alpha()
spritesheet_andar_esquerda = pygame.image.load(os.path.join(diretorio_imagens, 'PassosEsquerda.png')).convert_alpha()
#Personagem do jogo
personagem = Masculino(spritesheet_andar_direita, spritesheet_andar_esquerda)
sprites_personagem = pygame.sprite.Group()
sprites_personagem.add(personagem)

# Defina a fonte para o texto
fonte_usuario = pygame.font.Font(None, 25)
fonte = pygame.font.Font(None, 30)
#Função do click
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
                # Se pressionar Enter, pode-se iniciar o jogo ou fazer outra ação com o nome do usuário
                print("Nome do usuário:", nome_usuario)
                # Aqui você pode iniciar o jogo com o nome do usuário
            else:
                # Adicionar caracteres digitados ao nome do usuário
                nome_usuario += evento.unicode

        #Função do Iniciar jogo
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if iniciar_Jogo_rect.collidepoint(evento.pos):
                clicked = True

    #Movimentar o fundo
    tela.blit(imagem_de_fundo, (0,0))
    mov_tela = altura % imagem_de_fundo.get_rect().width
    tela.blit(imagem_de_fundo, (mov_tela - imagem_de_fundo.get_rect().width, 0))
    if mov_tela < 960:
        tela.blit(imagem_de_fundo, (mov_tela,0))
    altura-= 1/2
    # Desenhar o título do jogo
    tela.blit(unp_survival, (230,0))
    # Desenhar o campo de entrada de texto
    texto_nome = fonte_usuario.render(nome_usuario, True, BRANCO)
    tela.blit(texto_nome, (385, 220))

    # Desenhar o texto "Digite seu nome"
    tela.blit(Usuario_Login, (405, 175))

    # Desenhar o botão de iniciar o jogo
    tela.blit(iniciar_Jogo, iniciar_Jogo_rect,)
    # Desenhar o personagem
    sprites_personagem.draw(tela, (500, 460))



    # Atualizar a tela
    pygame.display.flip()
    #Abrir o Jogo ao clicar no "Iniciar Jogo"
    if clicked:
        subprocess.Popen(["python", "Jogo-Plataforma-2D\main.py"]) 
        pygame.quit()
        clicked = False

# Finalizar o Pygame
pygame.quit()

