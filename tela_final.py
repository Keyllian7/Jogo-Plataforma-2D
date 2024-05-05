import pygame, os, mysql.connector
from pygame.locals import *
from sys import exit, argv

# Inicialização da conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="2031",
    database="survival"
)

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

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

# Consulta SQL para recuperar os três primeiros valores da tabela
sql = "SELECT nome_jogador, pontos_jogador FROM resultado ORDER BY pontos_jogador DESC LIMIT 3"

# Executar o comando SQL
cursor.execute(sql)

# Recuperar os resultados da consulta
resultados = cursor.fetchall()

# Fechar o cursor, mas manter a conexão aberta
cursor.close()

# Função para renderizar o Nome do jogador
def renderizar_nome_1(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (395, 210))
def renderizar_nome_2(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (395, 272))
def renderizar_nome_3(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (395, 335))

#Função para renderizar a pontuação final do jogador
def renderizar_pontuacao_1(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (585, 210))
def renderizar_pontuacao_2(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (585, 272))
def renderizar_pontuacao_3(pontuacao_final):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (585, 335))

# Verificar se há pelo menos três resultados
if len(resultados) >= 3:
    # Recuperar os nomes e pontos dos três primeiros jogadores
    nome_jogador_1 = resultados[0][0]
    pontos_jogador_1 = resultados[0][1]

    nome_jogador_2 = resultados[1][0]
    pontos_jogador_2 = resultados[1][1]

    nome_jogador_3 = resultados[2][0]
    pontos_jogador_3 = resultados[2][1]

    # Exibir os nomes e pontos dos três primeiros jogadores
    print(f"Nome do jogador 1: {nome_jogador_1}, Pontos: {pontos_jogador_1}")
    print(f"Nome do jogador 2: {nome_jogador_2}, Pontos: {pontos_jogador_2}")
    print(f"Nome do jogador 3: {nome_jogador_3}, Pontos: {pontos_jogador_3}")
else:
    print("Não há jogadores suficientes na tabela.")

# Loop Principal do jogo
while True:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Renderiza a pontuação final do jogador
    pontuacao_final = f"{nome_jogador_1}"
    renderizar_nome_1(pontuacao_final)
    pontuacao_final = f"{nome_jogador_2}"
    renderizar_nome_2(pontuacao_final)
    pontuacao_final = f"{nome_jogador_3}"
    renderizar_nome_3(pontuacao_final)
    pontuacao_final = f"{pontos_jogador_1}"
    renderizar_pontuacao_1(pontuacao_final)
    pontuacao_final = f"{pontos_jogador_2}"
    renderizar_pontuacao_2(pontuacao_final)
    pontuacao_final = f"{pontos_jogador_3}"
    renderizar_pontuacao_3(pontuacao_final)
    

    pygame.display.flip()

# Fechar a conexão com o banco de dados
    conn.close()
