from game import Game
import random
import copy
import keyboard
import time


SLEEP_TIME = 2


class Bot:
    def __init__(self, size, start_tiles):
        self.game = Game(size, start_tiles)
        self.directions = ["left", "right", "up", "down"]

    def get_game(self):
        return self.game

    def play(self):
        while not self.game.game_over():
            # time.sleep(SLEEP_TIME)
            direction = self.choose_move()
            self.game.take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def take_turn(self):
        if not self.game.game_over():
            direction = self.choose_move()
            self.game.take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def move_options(self):
        moves = {}
        boards = [copy.deepcopy(self.game.get_board()) for x in range(len(self.directions))]
        for i in range(len(self.directions)):
            movesMades, score, board = boards[i].move(self.directions[i], self.game.get_turn())
            moves[self.directions[i]] = board
            for k in range(4):
                row = ""
                for j in range(4):
                    if board[k][j] is None:
                        row = row + str(0).ljust(4) + "  "
                    else:
                        row = row + str(board[k][j].get_value()).ljust(4) + "  "
                print(row)
            print()
        # return [boards[i].move(directions[i]) for i in range(len(self.directions))]
        print(moves)

        return moves

    def evaluate_moves(self, moves):
        evals = {}
        # moves = move_options()
        for direction in self.directions:
            evals[direction] = self.heuristic(moves[direction])
        return evals

    def heuristic(self, board):
        return 0

    def choose_move(self):
        moves = self.move_options()
        evals = self.evaluate_moves(moves)
        move = random.randint(0, len(self.directions) - 1)
        direction = self.directions[move]
        return direction


if __name__ == "__main__":
    bot = Bot(4, 2)
    bot.play()
