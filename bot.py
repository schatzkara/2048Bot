from game import Game
from state import State
from tree import Tree
from node import Node
import constants as c
import random
import copy
import keyboard


class Bot(Game):
    def __init__(self, size, start_tiles, look_ahead, heuristic=c.RANDOM, log=False):
        super().__init__(size, start_tiles)
        self.size = size
        self.start_tiles = start_tiles
        self.look_ahead = look_ahead
        self.heuristic = heuristic
        self.log = log
        if self.log:
            self.log_file = 'log_0000.txt'

        self.directions = ["left", "right", "up", "down"]
        # self.heuristics = {0: self.choose_move_random(),
        #                    1: self.choose_move_score(),
        #                    2: self.choose_move_merges()}

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
            if self.heuristic == c.RANDOM:
                direction = self.choose_move_random()
            elif self.heuristic == c.HIGHSCORE:
                direction = self.choose_move_score()
            elif self.heuristic == c.MOSTMERGES:
                direction = self.choose_move_merges()
            else:
                direction = self.choose_move_random()

            self.log_line(str(super().get_turn()) + ': ' + direction)
            super().take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def move_options(self, board_to_move):
        moves = {}
        boards = [copy.deepcopy(board_to_move) for x in range(len(self.directions))]
        for i in range(len(self.directions)):
            moves_made, merges, score, board = boards[i].move(self.directions[i], self.get_turn()+1)
            if moves_made:
                moves[self.directions[i]] = State(board, self.directions[i], score, merges)  # {'merges': merges, 'score': score, 'board': board}
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
        moves = self.move_options(self.get_board())
        # evals = self.evaluate_moves(moves)
        move = random.randint(0, len(moves) - 1)
        direction = list(moves.keys())[move]
        return direction

    # def choose_move_score(self):
    #     moves = self.move_options()
    #     best_move = list(moves.keys())[0]
    #     highest = moves[best_move]['score']
    #     # highest.insert(index=0, object="left")
    #     for move in moves.keys():
    #         print(move, moves[move]['score'])
    #         if moves[move]['score'] > highest:
    #             highest = moves[move]['score']
    #             best_move = move
    #     # sorted_moves = self.sort_moves(moves)
    #     print(best_move)
    #     return best_move

    def choose_move_score(self):
        # print('here')
        moves = self.move_options(self.get_board())
        best_moves = []  # [list(moves.keys())[0]]
        highest = 0  # moves[best_moves[0]].get_score()  # ['score']
        # highest.insert(index=0, object="left")
        for move in moves.keys():
            print(move, moves[move].get_score())  # ['score'])
            if moves[move].get_score() > highest:  #  moves[move]['score'] > highest:
                highest = moves[move].get_score()  # ['score']
                best_moves = [move]
            elif moves[move].get_score() == highest:
                best_moves.append(move)
        # sorted_moves = self.sort_moves(moves)
        print(best_moves)

        move = random.randint(0, len(best_moves) - 1)
        direction = best_moves[move]
        print(direction)
        # return best_moves
        return direction

    def make_tree(self):
        # tree = Tree(State(self.get_board(), 0, 0))
        current_level_nodes = []
        root = Node(label="", value=State(self.get_board(), "", 0, 0), sum=0)
        current_level_nodes.append(root)
        for i in range(self.look_ahead):
            next_level_nodes = []
            for node in current_level_nodes:
                moves = self.move_options(node.get_value().get_board())
                for move in moves.keys():
                    state = moves[move]
                    n = Node(label=move, value=state,
                             sum=node.get_sum()+state.get_score(), parent=node)
                    node.add_child(n)
                    next_level_nodes.append(n)
            current_level_nodes = next_level_nodes

        best_node = current_level_nodes[0]
        best_score = best_node.get_sum()
        for node in current_level_nodes:
            if node.get_sum() > best_score:
                best_node = node
                best_score = node.get_sum()

        while best_node.get_parent().get_parent() is not None:
            best_node = best_node.get_parent()

        move = best_node.get_value().get_direction()

        return move

        # return Tree(root)

    # def make_branch(self, node, look_ahead):
    #     if look_ahead > 0:
    #         moves = self.move_options(node.get_value().get_board())
    #         root = Node(label="", value=State(self.get_board(), "", 0, 0))
            # for move in moves.keys():
            #     n = Node(label=move, value=moves[move], parent=node)
            #     node.add_child(n)

    def choose_move_score_tree(self):
        return self.make_tree()

    def choose_move_merges(self):
        moves = self.move_options(self.get_board())
        best_move = list(moves.keys())[0]
        highest = moves[best_move].get_merges()  # ['merges']
        for move in moves.keys():
            print(move, moves[move].get_merges())  # ['merges'])
            if moves[move].get_merges() > highest:  # moves[move]['merges'] > highest:
                highest = moves[move].get_merges()  # ['merges']
                best_move = move
        # sorted_moves = self.sort_moves(moves)
        print(best_move)
        return best_move

    def high_corner(self):
        moves = self.move_options(self.get_board())
        best_move = list(moves.keys())[0]
        for move in moves.keys():
            print(move, moves[move].get_board())  # ['board'])
            if self.value_in_corner(moves[move].get_board(), self.get_highest_tile(moves[move].get_board())):  # self.value_in_corner(moves[move]['board'], self.get_highest_tile(moves[move]['board'])):
                best_move = move
        print(best_move)
        return best_move

    def get_highest_tile(self, grid):
        highest = 0
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] is not None and grid[row][col].get_value() > highest:
                    highest = grid[row][col].get_value()

        return highest

    def value_in_corner(self, grid, value):
        if grid[0][0] is not None and grid[0][0].get_value() == value:
            return True
        elif grid[self.size-1][0] is not None and grid[self.size-1][0].get_value() == value:
            return True
        elif grid[0][self.size-1] is not None and grid[0][self.size-1].get_value() == value:
            return True
        elif grid[self.size-1][self.size-1] is not None and grid[self.size-1][self.size-1].get_value() == value:
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
    bot = Bot(4, 2, 1)
    bot.play()
