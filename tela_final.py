import pygame
import os
from pygame.locals import *
from sys import exit, argv

pygame.init()

# Definição das cores
preto = (0, 0, 0)

# Definição das dimensões da tela
largura = 960
altura = 540

# Criação da tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('UNP Survival - FIM')
fps = pygame.time.Clock()

# Diretórios dos arquivos
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'Assets Imagens')
diretorio_sons = os.path.join(diretorio_principal, 'Assets Sons')

# Carregamento da imagem de fundo
imagem_de_fundo = pygame.image.load(os.path.join(diretorio_imagens, 'Tela_Final.png'))
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura, altura))

# Definição da fonte para o texto
fonte_fim_jogo = pygame.font.Font(None, 36)

# Variável para armazenar a pontuação atual do jogador
pontuacao_atual = 0

# Verifica se há argumentos na linha de comando
if len(argv) > 1:
    pontuacao_atual = int(argv[1])

# Função para renderizar a pontuação final do jogador
def renderizar_pontuacao_final(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (593, 210))


nome_player = "Tiago"

# Loop Principal do jogo
while True:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Renderiza a pontuação final do jogador
    pontuacao_final = f"{pontuacao_atual}"
    renderizar_pontuacao_final(pontuacao_final)

    pygame.display.flip()