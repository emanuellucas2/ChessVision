'''

Jogo Xadrez - Projeto Especializado - Programa principal

'''
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 ##Tamanho pixels tab, dimensão do tabuleiro
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'] ##carrega as imagens
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+ piece + ".png"), (SQ_SIZE,SQ_SIZE))


def main():
    p.init() #inicia pygame
    screen = p.display.set_mode((WIDTH, HEIGHT)) ##define tela e clock
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    loadImages()  # carrega as peças no tabuleiro
    running = True


#####################################################################################################################
    sqSelected = ()
    playerClicks = []  # track dos cliques na tela

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False ##sair do jogo

                ######só para manter 2 cliques do mouse, remover isso pelo botão pressionado
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()


                col = location[0] // SQ_SIZE  ##linha e coluna selecionada
                row = location[1] // SQ_SIZE
                sqSelected = (row, col)
                playerClicks.append(sqSelected)  ##acrescenta o quadrado selecionado
                if len(playerClicks) == 2:  # depois do 2o clique

                    ##passa a tabela nova vinda do algoritmo de visão
                    ##exemplo da 2 cliques
                    tabela = [
                    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "wp", "--", "--", "--", "--", "--"],
                    ["--", "--", "wp", "--", "--", "--", "--", "--"],
                    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                    gs.makeMove(tabela)

                    sqSelected = ()  ##reseta as escolhar
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()  # reseta jogo

"""
Gráfico do jogo
"""

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

"""
Desenho dos quadrados no tabuleiro
"""
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("darkgreen")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board): ##desenho das imagens
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c] #peça com base na posição inicial dela
            if piece != "--":  # quadrado nao vazio
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#if __name__ == "__main__":
#    main()
