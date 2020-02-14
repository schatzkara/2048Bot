from board import Board
# from graphics import Graphics
import keyboard


class Game:
    def __init__(self, size, start_tiles):
        self.turn = 0
        self.score = 0
        self.board = Board(size, start_tiles)
        # self.gui = Graphics(self.board.get_grid())
        self.board.display()
        # self.play()

    def get_board(self):
        return self.board

    def take_turn(self, direction):
        self.turn += 1
        moved, turn_score = self.board.move(direction, self.turn)
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
                moved, turn_score = self.board.move(direction, self.turn)
                if moved:
                    self.board.add_tile()
                    self.score += turn_score
                self.board.display()
                # self.gui.display_board(self.board.get_grid())
            else:
                keyboard.read_key()
            alternate = not alternate

    def game_over(self):
        if self.board.dead():
            print("DEADDDDDD")
        return self.board.dead()


if __name__ == "__main__":
    g = Game(4, 2)
    g.play()
    # while not g.get_board().dead():
    #     g.take_turn()
