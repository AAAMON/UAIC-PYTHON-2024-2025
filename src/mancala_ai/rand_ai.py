import random

class RandAi:
    @staticmethod
    def get_move(mancala):
        """ Picks a move randomly from the available pits """
        move = random.randint(8, 13)
        non_zero_elements = [index for index in range(8, 14) if mancala.board[index] != 0]
        random_index = -1
        if non_zero_elements:
            random_index = random.choice(non_zero_elements)
            print(f"Rand index: {random_index}, vall: {mancala.board[random_index]}")
        else:
            print("Error????")
        return random_index