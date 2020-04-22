from game import Game
from state import State
from tree import Tree
from node import Node
import gridutils as utils
import constants as c
import random
import copy
import keyboard


class Bot(Game):
    def __init__(self, size, start_tiles, look_ahead, trials=0, heuristic=c.RANDOM, log=False):
        super().__init__(size, start_tiles)
        self.size = size
        self.start_tiles = start_tiles
        self.look_ahead = look_ahead
        self.trials = trials
        self.heuristic = heuristic
        self.log = log
        if self.log:
            self.log_file = c.LOG_FILES[heuristic]  # 'log_0000.txt'
        print(self.log_file)
        self.directions = ["left", "right", "up", "down"]

    def __del__(self):
        self.log_game()

    def log_game(self):
        self.log_line('look_ahead:{} trials:{} moves:{} highest_tile:{} score:{}'.format(self.look_ahead,
                                                                                         self.trials,
                                                                                         super().get_turn(),
                                                                                         super().get_board().get_highest_tile(),
                                                                                         super().get_score()))

    def log_line(self, line):
        if self.log:
            with open(self.log_file, 'a') as f:
                f.write(line + '\n')

    def play(self):
        while not self.game_over():
            # direction = self.choose_direction()
            self.take_turn(None)
            # keyboard.press(str(direction))
            # keyboard.release(str(direction))

    def take_turn(self, _):
        if not self.game_over():
            direction = self.choose_direction()
            # self.log_line(str(super().get_turn()) + ': ' + direction)
            super().take_turn(direction)
            keyboard.press(str(direction))
            keyboard.release(str(direction))

    def choose_direction(self):
        # if self.heuristic == c.RANDOM:
        #     direction = self.choose_move_random()
        # elif self.heuristic == c.HIGHSCORE:
        #     direction = self.choose_move_score_tree()
        # elif self.heuristic == c.MOSTMERGES:
        #     direction = self.choose_move_merges()
        # elif self.heuristic == c.MOSTMERGESAVAIL:
        #     direction = self.choose_move_merges_avail()
        # else:
        #     direction = self.choose_move_random()
        direction = self.run_trials()

        return direction

    def run_trials(self):
        runs = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
        for x in range(self.trials):
            direction = self.make_tree()
            runs[direction] = runs[direction] + 1

        best = ''
        most = 0
        for direction in list(runs.keys()):
            if runs[direction] > most:
                best = direction
                most = runs[direction]

        return best

    def make_tree(self):
        # tree = Tree(State(self.get_board(), 0, 0))
        current_level_nodes = []
        root = Node(label="", value=State(self.get_board(), "", 0, 0, self.get_turn()), points=0)
        current_level_nodes.append(root)

        next_level_possible = False

        # make the tree look_ahead levels deep
        for i in range(self.look_ahead):
            next_level_nodes = []
            # build each node one level deeper
            for node in current_level_nodes:
                moves = self.determine_move_options(node.get_value().get_board(), turn_difference=i + 1)
                if len(moves) > 0:
                    next_level_possible = True
                # make each new move a child
                for move in moves.keys():
                    state = moves[move]
                    n = Node(label=move, value=state,
                             points=node.get_points() + self.get_points(state), parent=node)
                    node.add_child(n)
                    next_level_nodes.append(n)
            if next_level_possible:
                current_level_nodes = next_level_nodes
                next_level_possible = False
            else:
                break

        # print(current_level_nodes)

        best_nodes = []  # current_level_nodes[0]
        best_score = -1  # best_node.get_points()
        for node in current_level_nodes:
            if node.get_points() > best_score:
                best_nodes = [node]
                best_score = node.get_points()
            elif node.get_points() == best_score:
                best_nodes.append(node)

        best_node = best_nodes[random.randint(0, len(best_nodes) - 1)]

        while best_node.get_parent().get_parent() is not None:
            best_node = best_node.get_parent()

        move = best_node.get_value().get_direction()

        return move

        # return Tree(root)

    def get_points(self, state):
        if self.heuristic == c.RANDOM:
            # print("random")
            points = 0
        elif self.heuristic == c.HIGHSCORE:
            # print("high score")
            points = state.get_score()
        elif self.heuristic == c.MOSTMERGES:
            # print("most merges")
            points = state.get_merges()
        elif self.heuristic == c.MOSTMERGESAVAIL:
            # print("most merges avail")
            points = utils.num_available_merges(grid=state.get_board().get_grid())
        elif self.heuristic == c.HIGHCORNER:
            # print("high corner")
            points = int(utils.value_in_corner(grid=state.get_board().get_grid(),
                                               value=utils.get_highest_tile(state.get_board().get_grid())))
        elif self.heuristic == c.TOPLEFT:
            points = int(utils.value_in_top_left(grid=state.get_board().get_grid(),
                                                 value=utils.get_highest_tile(state.get_board().get_grid())))
        elif self.heuristic == c.TOPRIGHT:
            points = int(utils.value_in_top_right(grid=state.get_board().get_grid(),
                                                  value=utils.get_highest_tile(state.get_board().get_grid())))
        elif self.heuristic == c.BOTTOMLEFT:
            points = int(utils.value_in_bottom_left(grid=state.get_board().get_grid(),
                                                    value=utils.get_highest_tile(state.get_board().get_grid())))
        elif self.heuristic == c.BOTTOMRIGHT:
            points = int(utils.value_in_bottom_right(grid=state.get_board().get_grid(),
                                                     value=utils.get_highest_tile(state.get_board().get_grid())))
        elif self.heuristic == c.MONOTONIC:
            points = utils.num_monotonic(state.get_board().get_grid())
        elif self.heuristic == c.TWONEAREMPTY:
            points = utils.value_near_empty_space(grid=state.get_board().get_grid(), value=2)
        elif self.heuristic == c.MULTIATTRIBUTE:
            # print("multi attribute")
            points = self.score_board_state(state)
        elif self.heuristic == c.MULTIATTRIBUTE_TURN:
            points = self.score_board_state_turn(state)
        else:
            print("rut ro")
            points = 0

        return points

    def determine_move_options(self, board_to_move, turn_difference):
        # print(board_to_move)
        move_options = {}  # key: direction, value: game state with moved board
        boards = [copy.deepcopy(board_to_move) for x in range(len(self.directions))]
        # move the current board in each possible direction
        for i in range(len(self.directions)):
            # move board
            moves_made, merges, score = boards[i].move(self.directions[i],
                                                       self.get_turn() + turn_difference)  # not + 1 so that tree can go further
            # if valid, store it as a move option
            if moves_made:
                boards[i].add_tile()
                move_options[self.directions[i]] = State(board=boards[i],
                                                         direction=self.directions[i],
                                                         score=score,
                                                         merges=merges,
                                                         turn=self.get_turn() + turn_difference)
        # print(move_options)

        return move_options

    def choose_move_random(self):
        moves = self.determine_move_options(self.get_board(), 0)
        # evals = self.evaluate_moves(moves)
        index = random.randint(0, len(moves) - 1)
        direction = list(moves.keys())[index]

        return direction

    def choose_move_score(self):
        moves = self.determine_move_options(self.get_board(), 0)
        best_moves = []
        highest = 0
        for move in moves.keys():
            print(move, moves[move].get_score())
            if moves[move].get_score() > highest:
                highest = moves[move].get_score()
                best_moves = [move]
            elif moves[move].get_score() == highest:
                best_moves.append(move)
        print(best_moves)

        # randomly choose one of the best moves
        index = random.randint(0, len(best_moves) - 1)
        direction = best_moves[index]
        print(direction)

        return direction

    def choose_move_score_tree(self):
        return self.make_tree()

    def choose_move_merges(self):
        moves = self.determine_move_options(self.get_board(), 0)
        best_moves = []  # list(moves.keys())[0]
        highest = 0  # moves[best_move].get_merges()  # ['merges']
        for move in moves.keys():
            print(move, moves[move].get_merges())  # ['merges'])
            if moves[move].get_merges() > highest:  # moves[move]['merges'] > highest:
                highest = moves[move].get_merges()  # ['merges']
                best_moves = [move]
            elif moves[move].get_merges() == highest:
                best_moves.append(move)
        print(best_moves)

        # randomly choose one of the best moves
        index = random.randint(0, len(best_moves) - 1)
        direction = best_moves[index]
        print(direction)

        return direction

    def choose_move_merges_tree(self):
        return self.make_tree()

    def score_board_state(self, state):
        score = 0
        grid = state.get_board().get_grid()
        s = state.get_score()

        # 1: score
        score += state.get_score()
        # 2: merges
        score += (state.get_merges() * (s // 2))
        # 3: monotonic
        score += (utils.num_monotonic(grid=grid) * (s // 2))
        # 4: merges avail
        score += (utils.num_available_merges(grid=grid) * (s // 2))
        # 5: two near empty space
        score += (utils.value_near_empty_space(grid=grid, value=2) * (s // 2))
        # 6: high corner
        score += int(utils.value_in_corner(grid=grid,
                                           value=utils.get_highest_tile(grid))) * (s // 2)

        return score

    def score_board_state_turn(self, state):
        score = 0
        grid = state.get_board().get_grid()
        s = state.get_score()

        # 1: score
        score += state.get_score()
        # 2: merges
        score += (state.get_merges() * (state.get_turn()))
        # 3: monotonic
        score += (utils.num_monotonic(grid=grid) * (state.get_turn()))
        # 4: merges avail
        score += (utils.num_available_merges(grid=grid) * (state.get_turn()))
        # 5: two near empty space
        score += (utils.value_near_empty_space(grid=grid, value=2) * (state.get_turn()))
        # 6: high corner
        score += int(utils.value_in_corner(grid=grid,
                                           value=utils.get_highest_tile(grid))) * (state.get_turn())

        return score

    def high_corner(self):
        moves = self.determine_move_options(self.get_board(), turn_difference=1)
        best_moves = []  # list(moves.keys())[0]
        for move in moves.keys():
            print(move, moves[move].get_board())  # ['board'])
            if utils.value_in_corner(grid=moves[move].get_board(),
                                     value=utils.get_highest_tile(moves[move].get_board())):
                # self.value_in_corner(moves[move]['board'], self.get_highest_tile(moves[move]['board'])):
                best_moves.append(move)
        # print(best_moves)

        index = random.randint(0, len(best_moves) - 1)
        direction = best_moves[index]
        # print(direction)

        return direction

    def game_over(self):
        if self.board.dead():
            # self.log_line('highest tile: ' + str(super().get_board().get_highest_tile()))
            # self.log_line('score: ' + str(super().get_score()))
            # self.log_game()
            return True
        else:
            return False


if __name__ == "__main__":
    bot = Bot(4, 2, 1)
    bot.play()
