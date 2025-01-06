import time


class Mancala:
    def __init__(self):
        """
        The places on the board are labeled as shown below
          __13 12 11 10 9 8__  player 1
         |  | O O O O O O |  |
         |__| O O O O O O |__|
          0   1 2 3 4 5 6   7  player 0
        """
        self.board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
        self.turn = 0
        """
        if the last seed goes into the store of
        the player taking the turn, they make an additional turn
        """
        self.add_turn = 0
        """ 'AI' or 'HUMAN' """
        self.opponent = "AI"
        """ 'MAIN_MENU' or 'GAME' """
        self.menu = "MAIN_MENU"
        """ when player leaves the game prematurely """
        self.exit = False
        """ so the gui knows what message to display """
        self.winner = "none"
    def game_is_finished(self):
        """
        game is finished when one of the players has all their places
        on the board empty.
        Player 0 has places 1 to 6, and Player 1 has 8 to 13
        """
        ok = 1
        for i in range(1, 6):
            if self.board[i] != 0:
                ok = 0
                break
        if ok == 1:
            return True, 0
        ok = 1
        for i in range(8, 13):
            if self.board[i] != 0:
                ok = 0
                break
        if ok == 1:
            return True, 1
    def apply_move(self, init_pos, gui):
        """
        move is an integer 1-6 or 8-13 which means from which place
        the player wants to move the seeds form
        """
        print("APPLY MOVE:", init_pos, " TURN:", self.turn)
        steps = self.board[init_pos]
        self.board[init_pos] = 0
        position = init_pos
        for step in range(1, steps+1):
            if position == 13:
                position = 0
            else:
                position = position + 1
            """ dont put seeds in opponents store """
            if self.turn == 0 and position == 0:
                position = position + 1
                print("DONT PUT")
            if self.turn == 1 and position == 7:
                position = position + 1
                print("DONT PUT")
            """ add turn after last seed falls in store """
            if step == steps and self.turn == 0 and position == 7:
                self.add_turn = 1
            if step == steps and self.turn == 1 and position == 0:
                self.add_turn = 1
            """ take opponents seed if last seed lands on YOUR empty """
            if step == steps and self.turn == 0 and 7 > position > 0 == self.board[position]:
                self.board[7] = self.board[7] + self.board[position+(14-2*position)]
                self.board[position + (14 - 2 * position)] = 0
            if step == steps and self.turn == 1 and 14 > position > 7 and 0 == self.board[position]:
                self.board[7] = self.board[7] + self.board[position - (14 - 2 * (position-7))]
                self.board[position - (14 - 2 * (position-7))] = 0
            self.board[position] = self.board[position] + 1
            gui.update_game_gui(self)
            time.sleep(1)
        self.update_turn()
    def update_turn(self):
        if self.game_is_finished():
            if self.board[7] > self.board[0]:
                if self.opponent == "AI":
                    self.winner = "YOU"
                else:
                    self.winner = "PLAYER 0"
            else:
                if self.opponent == "AI":
                    self.winner = "COMPUTER"
                else:
                    self.winner = "PLAYER 1"
        else:
            if self.add_turn == 1:
                self.add_turn = 0
            else:
                if self.turn == 1:
                    self.turn = 0
                else:
                    self.turn = 1
    def reset_board(self):
        self.board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
        self.turn = 0
        self.add_turn = 0
        self.exit = False
        self.winner = "none"