import pygame
import sys

# Inicialize o Pygame
pygame.init()

# Defina as cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)

# Defina a largura e a altura da tela
largura_tela = 960
altura_tela = 540
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Menu Inicial')

imgagem_fundo = pygame.image.load('Jogo-Plataforma-2D/Assets Imagens/Background.png')
imgagem_fundo = pygame.transform.scale(imgagem_fundo, (largura_tela, altura_tela))

# Defina a fonte para o texto
fonte_usuario = pygame.font.Font(None, 25)
fonte = pygame.font.Font(None, 36)


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

    # Preencher a tela com a cor de fundo
    tela.blit(imgagem_fundo, (0,0))
    mov_tela = altura_tela % imgagem_fundo.get_rect().width
    tela.blit(imgagem_fundo, (mov_tela - imgagem_fundo.get_rect().width, 0))
    if mov_tela < 960:
        tela.blit(imgagem_fundo, (mov_tela,0))
    altura_tela-= 1

    # Desenhar o campo de entrada de texto
    pygame.draw.rect(tela, BRANCO, (380, 220, 200, 30), 2)
    texto_nome = fonte_usuario.render(nome_usuario, True, BRANCO)
    tela.blit(texto_nome, (385, 220))

    # Desenhar o texto "Digite seu nome"
    texto_instrucao = fonte.render("Digite o nome de Usuario:", True, BRANCO)
    tela.blit(texto_instrucao, (330, 180))

    # Desenhar o botão de iniciar o jogo
    pygame.draw.rect(tela, AZUL, (410, 350, 150, 30))
    texto_iniciar = fonte.render("Iniciar Jogo", True, BRANCO)
    tela.blit(texto_iniciar, (410, 350))

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
sys.exit()
