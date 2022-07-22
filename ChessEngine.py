'''

Jogo Xadrez - Projeto Especializado - Engine - responsável por configurações do jogo

'''
import numpy as np
table = np.empty((8, 8), dtype=str)

table = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


class GameState():
    def __init__(self):

        self.board = table
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, tabela):
        self.board = tabela
