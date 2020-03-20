
class State:
    def __init__(self, board, direction, score, merges):
        self.board = board
        self.direction_moved = direction
        self.score = score
        self.merges = merges

    def get_board(self):
        return self.board

    def get_direction(self):
        return self.direction_moved

    def get_score(self):
        return self.score

    def get_merges(self):
        return self.merges