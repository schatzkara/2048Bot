from game import Game
import random
import copy
import keyboard


class Bot(Game):
    def __init__(self, size, start_tiles, log=False):
        super().__init__(size, start_tiles)
        self.directions = ["left", "right", "up", "down"]
        self.log = log
        if self.log:
            self.log_file = 'log_0000.txt'

    # def play(self):
    #     while not self.game_over():
    #         direction = self.choose_move()
    #         self.take_turn(direction)
    #         keyboard.press(str(direction))
    #         keyboard.release(str(direction))

    def log_line(self, line):
        if self.log:
            with open(self.log_file, 'a') as f:
                f.write(line + '\n')

    def take_turn(self, dummy):
        if not self.game_over():
            direction = self.choose_move_merges()
            self.log_line(str(super().get_turn()) + ': ' + direction)
            super().take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def move_options(self):
        moves = {}
        boards = [copy.deepcopy(self.get_board()) for x in range(len(self.directions))]
        for i in range(len(self.directions)):
            moves_made, merges, score, board = boards[i].move(self.directions[i], self.get_turn()+1)
            if moves_made:
                moves[self.directions[i]] = {'merges': merges, 'score': score, 'board': board}
            for k in range(4):
                row = ""
                for j in range(4):
                    if board[k][j] is None:
                        row = row + str(0).ljust(4) + "  "
                    else:
                        row = row + str(board[k][j].get_value()).ljust(4) + "  "
                # print(row)
            # print()
        # return [boards[i].move(directions[i]) for i in range(len(self.directions))]
        print(moves)

        return moves

    def choose_move_random(self):
        moves = self.move_options()
        # evals = self.evaluate_moves(moves)
        move = random.randint(0, len(moves) - 1)
        direction = list(moves.keys())[move]
        return direction

    def choose_move_score(self):
        moves = self.move_options()
        best_move = list(moves.keys())[0]
        highest = moves[best_move]['score']
        # highest.insert(index=0, object="left")
        for move in moves.keys():
            print(move, moves[move]['score'])
            if moves[move]['score'] > highest:
                highest = moves[move]['score']
                best_move = move
        # sorted_moves = self.sort_moves(moves)
        print(best_move)
        return best_move

    def choose_move_merges(self):
        moves = self.move_options()
        best_move = list(moves.keys())[0]
        highest = moves[best_move]['merges']
        for move in moves.keys():
            print(move, moves[move]['merges'])
            if moves[move]['merges'] > highest:
                highest = moves[move]['merges']
                best_move = move
        # sorted_moves = self.sort_moves(moves)
        print(best_move)
        return best_move

    def high_corner(self):
        moves = self.move_options()
        best_move = list(moves.keys())[0]
        for move in moves.keys():
            print(move, moves[move]['board'])
            if self.value_in_corner(moves[move]['board'], self.get_highest_tile(moves[move]['board'])):
                best_move = move
        print(best_move)
        return best_move

    def get_highest_tile(self, grid):
        highest = 0
        for row in range(4):
            for col in range(4):
                if grid[row][col] is not None and grid[row][col].get_value() > highest:
                    highest = grid[row][col].get_value()

        return highest

    def value_in_corner(self, grid, value):
        if grid[0][0] is not None and grid[0][0].get_value() == value:
            return True
        elif grid[3][0] is not None and grid[3][0].get_value() == value:
            return True
        elif grid[0][3] is not None and grid[0][3].get_value() == value:
            return True
        elif grid[3][3] is not None and grid[3][3].get_value() == value:
            return True
        else:
            return False

    def game_over(self):
        # if self.board.dead():
        #     print("DEADDDDDD")
        if self.board.dead():
            self.log_line('highest tile: ' + str(super().get_board().get_highest_tile()))
            self.log_line('score: ' + str(super().get_score()))
            return True
        else:
            return False

    # def evaluate_moves(self, moves):
    #     evals = {}
    #     # moves = move_options()
    #     for direction in moves.keys():
    #         evals[direction] = self.heuristic(moves[direction])
    #     return evals
    #
    # def heuristic(self, board):
    #     return 0

    # def sort_moves(self, move_dict, descending=True):
    #     sorted_moves = []
    #     values = list(move_dict.values())
    #     keys = list(move_dict.keys())
    #     for i in range(len(move_dict.keys())):
    #         if descending:
    #             if i == 0:
    #                 sorted_moves.insert(0, keys[i])
    #             else:
    #                 j = len(move_dict.keys()) - 1
    #                 while move_dict[keys[i]] > move_dict[keys[j]]:
    #                     j -= 1
    #                 sorted_moves.insert(j, keys[i])
    #         else:
    #             if i == 0:
    #                 sorted_moves.insert(0, keys[i])
    #             else:
    #                 j = len(move_dict.keys()) - 1
    #                 while move_dict[keys[i]] < move_dict[keys[j]]:
    #                     j -= 1
    #                 sorted_moves.insert(j, keys[i])
    #     return sorted_moves


if __name__ == "__main__":
    bot = Bot(4, 2)
    bot.play()
