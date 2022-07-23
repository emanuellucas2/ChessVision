import numpy as np
from cv2 import *
from threading import *         
import time 
import homografia2
import homografia4
import serial
import cv2
import ChessEngine
import pygame as p

sem = Semaphore(0)  
l = []
gs = ChessEngine.GameState() ## inicializa jogo

WIDTH = HEIGHT = 1024##Tamanho pixels tab, dimensão do tabuleiro
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'] ##carrega as imagens
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+ piece + ".png"), (SQ_SIZE,SQ_SIZE))


def Main():
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


def squares(table,ti,matrix):


	tf = np.empty((8,8), dtype=str)
	count = 0

	for i in range(8):
		for j in range(8):

			img = table[int(100*i):int(100*(i+1)),int(100*j):int(100*(j+1))]

			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			blur = cv2.medianBlur(hsv ,7)
			
			#black
			lower = np.array([0,0,0])
			upper = np.array([185,201,48])

			mask = cv2.inRange(blur, lower, upper)

			#orange
			lower = np.array([0,253,176])
			upper = np.array([179,255,255])

			mask2 = cv2.inRange(blur, lower, upper)

			if mask.any():
				cv2.imwrite("squares" + str(1) + "/" + str(i) + str(j) + "preta.png",img)
			elif mask2.any:
				cv2.imwrite("squares" + str(1) + "/" + str(i) + str(j) + "branca.png",img)
			else:
				cv2.imwrite("squares" + str(1) + "/" + str(i) + str(j) + "vazia.png",img)

			if mask.any():
				tf[i][j] = "b"
			elif mask2.any():
				tf[i][j] = "w"
			else:
				tf[i][j] = "l"


			if(ti[i][j] != tf[i][j]):
				count += 1

	if(count == 0):
		return tf
	elif(count == 2):
		
		for i in range(8):
			for j in range(8):
				if(ti[i][j] != tf[i][j]):
					if(tf[i][j]=="l"):
						piece = matrix[i][j]
						matrix[i][j] = "--" 
					else:
						x = i
						y = j
						
		matrix[x][y] = piece
		gs.makeMove(matrix)
		return tf
	elif(count == 3):
		k = 0
		for i in range(8):
			for j in range(8):
				if(ti[i][j] != tf[i][j]):
					if(tf[i][j]=="l" and k == 0):
						piece1 = matrix[i][j]
						k = 1
						matrix[i][j] = "--"
						x1 = i
						y1 = j
					elif(tf[i][j]=="l" and k == 1): 
						piece2 = matrix[i][j]
						matrix[i][j] = "--"
						k == 2
						x2 = i
						y2 = j
					else:
						x = i
						y = j
		if(y!=y1):
			matrix[x][y] = piece1
		else:
			matrix[x][y] = piece2	
		gs.makeMove(matrix)

	elif(count == 4):
		k = 0
		for i in range(8):
			for j in range(8):
				if(ti[i][j] != tf[i][j]):
					if(tf[i][j]=="l" and k == 0):
						k = 1
						matrix[i][j] = "--"
						x1 = i
						y1 = j
					elif(tf[i][j]=="l" and k == 1): 
						matrix[i][j] = "--"
						k == 2
						x2 = i
						y2 = j

		if(abs(y1-y2)==3):
			if(x1==0):
				matrix[0][6] = "bK"
				matrix[0][5] = "bR"
			else:
				matrix[7][6] = "wK"
				matrix[7][5] = "wR"
		else:
			if(x1==0):
				matrix[0][2] = "bK"
				matrix[0][3] = "bR"
			else:
				matrix[7][2] = "wK"
				matrix[7][3] = "wR"

		gs.makeMove(matrix)
		return tf	

def init_squares(table):


	tf = np.empty((8,8), dtype=str)

	for i in range(8):
		for j in range(8):

			img = table[int(100*i):int(100*(i+1)),int(100*j):int(100*(j+1))]

			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			blur = cv2.medianBlur(hsv ,7)
			
			#black
			lower = np.array([0,0,6])
			upper = np.array([165,191,28])

			mask = cv2.inRange(blur, lower, upper)

			#orange
			lower = np.array([0,230,146])
			upper = np.array([199,255,255])

			mask2 = cv2.inRange(blur, lower, upper)

			if mask.any():
				tf[i][j] = "b"
			elif mask2.any():
				tf[i][j] = "w"
			else:
				tf[i][j] = "l"

	return tf	

def TakePhotos():

	ser = serial.Serial('/dev/ttyACM0', 115200)
	cam_port = 0
	cam = VideoCapture(cam_port)
	focus = 100
	cam.set(28, focus)
	cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
	while(1==1):

		#input("Press Enter to continue...")
		ser.read()

		cam.set(28, focus)
		result, image = cam.read()
		
		l.insert(0,image)
		sem.release()

def ProcessImage():

	t = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

	sem.acquire()
	image = l.pop()

	pts = homografia2.find_pixels(image)
	#pts = np.array([[1185 ,808],[588 ,799],[1192 , 206],[592 , 205]])
	#print(pts)
	img = homografia2.homografia(pts,image)

	ti = init_squares(img)

	while(1==1):

		sem.acquire()
		image = l.pop()

		img = homografia2.homografia(pts,image)

		ti = squares(img,ti,t)


t1 = Thread(target = TakePhotos)
t2 = Thread(target = ProcessImage)
t3 = Thread(target = Main)

t1.start()
t2.start()
t3.start()
