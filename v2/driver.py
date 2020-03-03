from game import Game
from graphics import Graphics

BOARD_SIZE = 4
START_TILES = 2


class Driver:
    def __init__(self):
        self.game = None
        self.gui = Graphics()

    def start_game(self):
        self.game = Game(BOARD_SIZE, START_TILES)

# if __name__ == "__main__":
#     game = Game(BOARD_SIZE, START_TILES)
#     gui = Graphics()

