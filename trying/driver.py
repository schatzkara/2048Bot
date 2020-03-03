from game import Game
from graphics import Graphics
import keyboard

BOARD_SIZE = 4
START_TILES = 2


class Driver:
    def __init__(self):
        self.game = Game(BOARD_SIZE, START_TILES)
        self.gui = Graphics(self.game.get_board(), self.play)
        self.gui.mainloop()
        # self.play()

    def play(self):
        while not self.game.game_over():
            direction = keyboard.read_key()
            self.game.take_turn(direction)
            self.gui.display_board(self.game.get_board())

    def start_game(self):
        self.game = Game(BOARD_SIZE, START_TILES)


if __name__ == "__main__":
    Driver()
#     game = Game(BOARD_SIZE, START_TILES)
#     gui = Graphics()

