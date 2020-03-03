from game import Game
import random
import copy
import keyboard


class Bot(Game):
    def __init__(self, size, start_tiles):
        super().__init__(size, start_tiles)
        # self.game = Game(size, start_tiles)
        self.directions = ["left", "right", "up", "down"]

    def play(self):
        while not self.game_over():
            direction = self.choose_move()
            self.take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def take_turn(self, dummy):
        if not self.game_over():
            direction = self.choose_move()
            super().take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def move_options(self):
        moves = {}
        boards = [copy.deepcopy(self.get_board()) for x in range(len(self.directions))]
        for i in range(len(self.directions)):
            movesMades, score, board = boards[i].move(self.directions[i], self.get_turn())
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

    def sort_moves(self, move_dict, descending=True):
        sorted_moves = []
        values = move_dict.values()
        for move in self.directions:
            if descending:
                largest = self.find_largest(values)
                sorted_moves.append(largest)
                values.remove(largest)
            else:
                smallest = self.find_smallest(values)
                sorted_moves.append(smallest)
                values.remove(smallest)
        return sorted_moves

    def find_largest(self, list):
        if len(list) == 0:
            return None
        else:
            largest = list[0]
            for elem in list:
                if elem > largest:
                    largest = elem
            return largest

    def find_smallest(self, list):
        if len(list) == 0:
            return None
        else:
            smallest = list[0]
            for elem in list:
                if elem < smallest:
                    smallest = elem
            return smallest


if __name__ == "__main__":
    bot = Bot(4, 2)
    bot.play()
