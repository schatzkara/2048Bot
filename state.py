
class State:
    def __init__(self, board, direction, score, merges, turn):
        self.board = board
        self.direction_moved = direction
        self.score = score
        self.merges = merges
        self.turn = turn

    def get_board(self):
        return self.board

    def get_direction(self):
        return self.direction_moved

    def get_score(self):
        return self.score

    def get_merges(self):
        return self.merges

    def get_turn(self):
        return self.turn