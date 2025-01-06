import pygame
import sys
from pygame.locals import *

class GUI:
    def __init__(self):
        self.COL_BACKGROUND  = ( 50,  50,  50)
        self.COL_TEXT_B      = (  4,   8,  10)
        self.COL_TEXT_W      = (223, 237, 243)
        self.COL_PRIMARY     = (240, 210,  50)
        self.COL_SECONDARY   = (100,  50,  50)
        self.COL_ACCENT      = ( 90, 220, 200)
        self.FONT_M = None
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.DISPLAYSURF = None
        self.WINDOW_TITLE = "Mancala"
        self.WINDOW_PADDING = 30 # px
        self.FPS = 60
        self.FRAME_PER_SEC = pygame.time.Clock()

    def init_gui(self):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.WINDOW_TITLE)
        self.FRAME_PER_SEC.tick(self.FPS)
        self.FONT_M = pygame.font.SysFont('Corbel', 22)

    def handle_events(self, game_state):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            """ IN GAME """
            if event.type == pygame.MOUSEBUTTONDOWN and game_state.menu == "GAME":
                mousee = pygame.mouse.get_pos()
                print(mousee)
                """ Player 0 picks a move """
                if game_state.turn == 0:
                    for i in range(1, 7):
                        if (self.SCREEN_WIDTH / 2 - 685 + i*178 < mousee[0] < self.SCREEN_WIDTH / 2 - 685 + (i + 1)*178
                                and self.SCREEN_HEIGHT / 2 + 31 < mousee[1] < self.SCREEN_HEIGHT / 2 + 100):
                            game_state.apply_move(i, self)
                """ Player 1 picks move (only possible in a 2 player game) """
                if game_state.turn == 1 and game_state.opponent == "HUMAN":
                    for i in range(1, 7):
                        if (self.SCREEN_WIDTH / 2 - 685 + i*178 < mousee[0] < self.SCREEN_WIDTH / 2 - 685 + (i + 1)*178
                                and self.SCREEN_HEIGHT / 2 - 153 < mousee[1] < self.SCREEN_HEIGHT / 2 - 90):
                            game_state.apply_move(14-i, self)
                if 250 < mousee[0] < 450 and 250 < mousee[1] < 320:
                    game_state.menu = "MAIN_MENU"
            """ MAIN MENU """
            if event.type == pygame.MOUSEBUTTONDOWN and game_state.menu == "MAIN_MENU":
                mousee = pygame.mouse.get_pos()
                """ quit button """
                if 717 < mousee[0] < 1175 and 766 < mousee[1] < 879:
                    pygame.quit()
                    sys.exit()
                """ duo game button """
                if 717 < mousee[0] < 1175 and 631 < mousee[1] < 744:
                    game_state.menu = "GAME"
                    game_state.opponent = "HUMAN"
                    game_state.reset_board()
                """ solo game button """
                if 717 < mousee[0] < 1175 and 497 < mousee[1] < 616:
                    game_state.menu = "GAME"
                    game_state.opponent = "AI"
                    game_state.reset_board()
    def update_game_gui(self, game_state):
        self.DISPLAYSURF.fill(self.COL_BACKGROUND)
        if game_state.menu == 'MAIN_MENU':
            self.draw_main_menu()
        elif game_state.menu == 'GAME':
            self.draw_board()
            self.draw_seeds(game_state)
            self.draw_info(game_state)

        """ always leave these last """
        pygame.display.update()
        self.FRAME_PER_SEC.tick(self.FPS)
    def draw_board(self):
        board = pygame.image.load("assets/board.png")
        scaled_board = pygame.transform.scale(board, (1400, 400))
        self.DISPLAYSURF.blit(scaled_board, (self.SCREEN_WIDTH/2-700, self.SCREEN_HEIGHT/2-200))
        pygame.draw.rect(self.DISPLAYSURF, self.COL_SECONDARY,
                         [250, 250,
                          200, 70])
        text = self.FONT_M.render("QUIT GAME", True, self.COL_TEXT_W)
        self.DISPLAYSURF.blit(text, [270, 275])
    def draw_seeds(self, game_state):
        seed = [pygame.image.load("assets/seed1.png"),
                pygame.image.load("assets/seed2.png"),
                pygame.image.load("assets/seed3.png"),
                pygame.image.load("assets/seed4.png"),
                pygame.image.load("assets/seed5.png"),
                pygame.image.load("assets/seed6.png"),
                pygame.image.load("assets/seed7.png"),
                pygame.image.load("assets/seed8.png")]

        """
        When displaying seeds, i only did images for up to 8 seeds. So if a player
        has more than 8 seeds in a place, we will use the same image. 
        There is also a number indicating the number of seeds for each pit.
        """
        for i in range (1, 7):
            seeds_num = game_state.board[i]
            if seeds_num >= 8:
                self.DISPLAYSURF.blit(seed[7],(self.SCREEN_WIDTH / 2 - 685 + i * 178, self.SCREEN_HEIGHT / 2 + 31))
            else:
                if seeds_num != 0:
                    self.DISPLAYSURF.blit(seed[seeds_num-1], (self.SCREEN_WIDTH / 2 - 685 + i*178, self.SCREEN_HEIGHT / 2 + 31))

            text = self.FONT_M.render(str(seeds_num), True, self.COL_TEXT_B)
            self.DISPLAYSURF.blit(text, [self.SCREEN_WIDTH / 2 - 685 + i * 178, self.SCREEN_HEIGHT / 2 + 161])

        for i in range (8, 14):
            seeds_num = game_state.board[i]
            if seeds_num >= 8:
                self.DISPLAYSURF.blit(seed[7],
                                      (self.SCREEN_WIDTH / 2 + 381 - (i-8)*178, self.SCREEN_HEIGHT / 2 - 153))
            else:
                if seeds_num != 0:
                    self.DISPLAYSURF.blit(seed[seeds_num-1], (self.SCREEN_WIDTH / 2 + 381 - (i-8)*178, self.SCREEN_HEIGHT / 2 - 153))
            text = self.FONT_M.render(str(seeds_num), True, self.COL_TEXT_B)
            self.DISPLAYSURF.blit(text, [self.SCREEN_WIDTH / 2 + 381 - (i-8)*178, self.SCREEN_HEIGHT / 2 - 180])

        """ 0 and 7 are the position for the big pits. """
        if game_state.board[0] != 0:
            print(game_state.board[0])
            seeds_num = game_state.board[0]
            if seeds_num >= 8:
                self.DISPLAYSURF.blit(seed[7],
                                      (self.SCREEN_WIDTH / 2 - 680, self.SCREEN_HEIGHT / 2 - 65))
            else:
                self.DISPLAYSURF.blit(seed[game_state.board[0] - 1],(self.SCREEN_WIDTH / 2 - 680, self.SCREEN_HEIGHT / 2 - 65))
        text = self.FONT_M.render(str(game_state.board[0]), True, self.COL_TEXT_B)
        self.DISPLAYSURF.blit(text, [self.SCREEN_WIDTH / 2 - 680,  self.SCREEN_HEIGHT / 2 + 161])
        if game_state.board[7] != 0:
            print(game_state.board[7])
            seeds_num = game_state.board[7]
            if seeds_num >= 8:
                self.DISPLAYSURF.blit(seed[7],
                                      (self.SCREEN_WIDTH / 2 + 530, self.SCREEN_HEIGHT / 2 - 65))
            else:
                self.DISPLAYSURF.blit(seed[game_state.board[7] - 1],(self.SCREEN_WIDTH / 2 + 530, self.SCREEN_HEIGHT / 2 - 65))
        text = self.FONT_M.render(str(game_state.board[7]), True, self.COL_TEXT_B)
        self.DISPLAYSURF.blit(text, [self.SCREEN_WIDTH / 2 + 530, self.SCREEN_HEIGHT / 2 + 161])
    def draw_info(self, game_state):
        pygame.draw.rect(self.DISPLAYSURF, self.COL_SECONDARY,
                         [250, 150,
                          200, 70])
        if game_state.add_turn == 1:
            label = "EXTRA TURN"
        else:
            if game_state.opponent == 'HUMAN':
                if game_state.turn == 0:
                    label = "Turn: Player 0"
                else:
                    label = "Turn: Player 1"
            else:
                if game_state.turn == 0:
                    label = "Turn: YOU"
                else:
                    label = "Turn: COMPUTER"
        if game_state.winner != "none":
            label = game_state.winner + " has won!"
        text = self.FONT_M.render(label, True, self.COL_TEXT_W)
        self.DISPLAYSURF.blit(text, [270,175])
    def draw_main_menu(self):
        menu = pygame.image.load("assets/mainMenu.png")
        scaled_menu = pygame.transform.scale(menu, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))  # New width, height
        self.DISPLAYSURF.blit(scaled_menu, (0, 0))