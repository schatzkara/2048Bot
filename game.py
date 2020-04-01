from board import Board
import keyboard


class Game:
    def __init__(self, size, start_tiles):
        self.turn = 0
        self.score = 0
        self.size = size
        self.start_tiles = start_tiles
        self.board = Board(size, start_tiles)
        self.init_board()
        self.board.display()

    def init_board(self):
        self.board.init_grid()

    def get_board(self):
        return self.board

    def get_score(self):
        return self.score

    def get_turn(self):
        return self.turn

    def take_turn(self, direction):
        self.turn += 1
        moved, merges, turn_score = self.board.move(direction, self.turn)
        if moved:
            self.board.add_tile()
            self.score += turn_score
        self.board.display()

    def play(self):
        alternate = True
        while not self.game_over():
            if keyboard.is_pressed("enter"):
                break
            if alternate:
                self.turn += 1
                direction = keyboard.read_key()
                moved, merges, turn_score = self.board.move(direction, self.turn)
                if moved:
                    self.board.add_tile()
                    self.score += turn_score
                self.board.display()
            else:
                keyboard.read_key()
            alternate = not alternate

    def game_over(self):
        # if self.board.dead():
        #     print("DEADDDDDD")
        return self.board.dead()


if __name__ == "__main__":
    g = Game(4, 2)
    g.play()
    # while not g.get_board().dead():
    #     g.take_turn()
