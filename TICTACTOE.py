#Focussing on programming pythonic (mainly snake_case en cool shortcuts)
import math
import random
import pygame
class Board:
    global board, board_dimensions, board_height, board_width
    board_dimensions = board_height, board_width = (3,3)
    board = [[0 for x in range(board_width)] for y in range(board_height)] 
    # 0 = nothing, -1 circle, 1 Square
    def UpdateBoard(board_position, player):
        if board[board_position[1]][board_position[0]] == 0:
            board[board_position[1]][board_position[0]] = player
            Game.SwitchPlayer()
class Render:
    global screen, window_size, window_width, window_height, blue
    window_size = window_width, window_height = (800,800)
    pygame.display.init()
    screen = pygame.display.set_mode(window_size)
    blue = (0,0,255)
    def RenderBoard():
        #render Vertical
        for i in range(1,board_width):
            pygame.draw.line(screen,(blue), (((window_width/board_width)*i),0), (((window_width/board_width)*i), window_height))
        #render Horizontal
        for i in range(1,board_height):
            pygame.draw.line(screen,(blue), (0,((window_height/board_height)*i)), (window_height,((window_height/board_height)*i)))
    def RenderPositions():
        for y,row in enumerate(board):
            for x, value in enumerate(row):
                
                if value == -1:
                    pos = (((window_width/board_width)*(x+1))-(window_width/board_width)/2)-40,(((window_height/board_height)*(y+1))-(window_height/board_height)/2)-40
                    pygame.draw.rect(screen,blue, pos+(80,80), 10)
                if value == 1:
                    pos = (((window_width/board_width)*(x+1))-(window_width/board_width)/2),(((window_height/board_height)*(y+1))-(window_height/board_height)/2)
                    pygame.draw.circle(screen, blue, pos, 80, 20)
    def UpdateDisplay():
        pygame.display.update()
class Game:
    is_running = True
    player = -1
    winner = 0
    def Main():
        Render.RenderBoard()
        Render.RenderPositions()
        Render.UpdateDisplay()
    def CheckEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.is_running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                Game.MousePositionToBoardPosition(pygame.mouse.get_pos())
                Game.CheckWinners()
    def MousePositionToBoardPosition(mouse_position):
        x = math.floor((board_width/window_width)*mouse_position[0])
        y = math.floor((board_height/window_height)*mouse_position[1])
        Board.UpdateBoard((x,y), Game.player)
    def SwitchPlayer():
        if Game.player == -1: Game.player = 1
        elif Game.player == 1: Game.player = -1
    def CheckWinners():
        Game.winner = Game.player
        #check horizontal
        for row in board:
            if abs(sum(row)) == board_width: Game.is_running = False
        #check vertical
        board_adjusted_to_columns = zip(*board)
        for column in board_adjusted_to_columns:
            if abs(sum(column)) == board_height: Game.is_running = False
        #check diagonal programmed not really nice
        board_adjusted_to_diagonal = [[],[]]
        for i in range(max(board_width, board_height)):
            board_adjusted_to_diagonal[0].append(board[i][i])
        for i in range(max(board_width, board_height)):
            board_adjusted_to_diagonal[1].append(board[i][board_height-i-1])
        for diagonal in board_adjusted_to_diagonal: 
            if abs(sum(diagonal)) == max(board_width, board_height): Game.is_running = False
        #check Draw
        board_without_zeros = [x for x in board if 0 in x]
        if len(board_without_zeros) == 0: 
            Game.is_running = False
            Game.winner = 0
while Game.is_running:
    Game.Main()
    Game.CheckEvents()
print("Tie") if Game.winner == 0 else print(Game.winner, "won")