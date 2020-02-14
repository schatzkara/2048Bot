from board import Board
import keyboard


class Game:
    def __init__(self, size, start_tiles, window):
        self.turn = 0
        self.score = 0
        self.board = Board(size, start_tiles, window)
        self.window = window
        self.board.display()
        # self.play()
        # print("here")

    def get_board(self):
        return self.board

    def take_turn(self, direction):
        # print('taking turn')
        # while not self.board.dead():
        # if keyboard.is_pressed("enter"):
        #     break
        # if alternate:
        # print('readin move')
        self.turn += 1
        # if keyboard.is_pressed("left"):
        #   self.board.move("left")
        # direction = keyboard.read_key()
        moved, turn_score = self.board.move(direction, self.turn)
        if moved:
            self.board.add_tile()
            self.score += turn_score
        self.board.display()
        # else:
        # keyboard.read_key()
        # alternate = not alternate

    def play(self):
        alternate = True
        while not self.board.dead():
            if keyboard.is_pressed("enter"):
                break
            if alternate:
                # print('readin move')
                self.turn += 1
                # if keyboard.is_pressed("left"):
                  #   self.board.move("left")
                direction = keyboard.read_key()
                moved, turn_score = self.board.move(direction, self.turn)
                if moved:
                    self.board.add_tile()
                    self.score += turn_score
                self.board.display()
            else:
                keyboard.read_key()
            alternate = not alternate
        # print("yah")


if __name__ == "__main__":
    g = Game(4, 2, None)
    g.play()
    # while not g.get_board().dead():
    #     g.take_turn()
