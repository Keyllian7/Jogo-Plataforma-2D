import pygame, os, mysql.connector
from pygame.locals import *

# Inicialização da conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    port = 3306,
    user="root",
    password="batatadoce0552",
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
def renderizar_nome(pontuacao_final, pos_y):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (395, pos_y))

# Função para renderizar a pontuação final do jogador
def renderizar_pontuacao(pontuacao_final, pos_y):
    texto_pontuacao_final = fonte_fim_jogo.render(pontuacao_final, True, preto)
    tela.blit(texto_pontuacao_final, (585, pos_y))

# Loop Principal do jogo
rodando = True
while rodando:
    fps.tick(60)
    tela.blit(imagem_de_fundo, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            rodando = False

    # Exibir os resultados
    if resultados:
        for i, resultado in enumerate(resultados):
            nome_jogador = resultado[0]
            pontos_jogador = resultado[1]
            renderizar_nome(nome_jogador, 210 + i * 62)
            renderizar_pontuacao(str(pontos_jogador), 210 + i * 62)
    else:
        print("Não há jogadores suficientes na tabela.")

    pygame.display.flip()

# Fechar a conexão com o banco de dados
conn.close()
