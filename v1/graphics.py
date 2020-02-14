import tkinter as tk
from game import Game

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BOARD_SIZE = 4
INIT_TILES = 2


class Graphics:
    def __init__(self):
        # window
        self.window = tk.Tk()
        self.window.title("2048")
        self.game = Game(4, 2, None)

        # frame = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        # frame.grid()
        self.window.bind("<Key>", self.take_turn)
        # self.window.geometry('{}x{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        # labels
        label = tk.Label(self.window, text="2048", font=("Arial", 30))
        label.grid(column=0, row=0)

        # buttons
        start_button = tk.Button(self.window, text="Start Game", command=self.start)
        start_button.grid(column=0, row=1)

        self.grid_tiles = []

        self.init_board()

        # start the window running
        self.window.mainloop()

    def init_board(self):
        background = tk.Frame(self.window, bg='#776e65',
                              width=WINDOW_WIDTH,
                              height=WINDOW_HEIGHT)
        background.grid()
        for row in range(BOARD_SIZE):
            row_tiles = []
            for col in range(BOARD_SIZE):
                tile = tk.Frame(background, bg='#BDAD9E',
                                width=WINDOW_WIDTH / BOARD_SIZE,
                                height=WINDOW_HEIGHT / BOARD_SIZE)
                tile.grid(row=row, column=col, padx=5, pady=5)
                value = tk.Label(tile,
                                 text='',
                                 bg='#BDAD9E',
                                 justify=tk.CENTER,
                                 font=("Arial", 40),
                                 width=4,
                                 height=2)
                value.grid()
                row_tiles.append(value)
                # if grid[row][col] is not None:
                #     tile = tk.Label(background, text=str(grid[row][col].get_value()).ljust(4), font=("Arial", 20))
                #     tile.grid(column=col, row=row + 2)
            self.grid_tiles.append(row_tiles)

    def start(self):
        # self.g = Game(4, 2, None)
        self.display_board(self.game.get_board().get_board())
        # self.play(g)

        # while not g.get_board().dead():
        #     g.take_turn()
        #     self.display_board(g.get_board().get_board())
        # for i in range(4):
        #     tile = tk.Label(self.window, text='0')
        #     tile.grid(column=i, row=3)

    def take_turn(self, event):
        # print(event)
        # print(type(event))
        direction = event.keysym.lower()
        # print(type(direction))
        # while not g.get_board().dead():
        self.game.take_turn(direction)
        self.display_board(self.game.get_board().get_board())

    def display_board(self, grid):
        # background = tk.Frame(self.window, width=WINDOW_WIDTH-10, height=WINDOW_HEIGHT-10)
        # background.grid()
        for row in range(4):
            for col in range(4):
                if grid[row][col] is not None:
                    self.grid_tiles[row][col].configure(text=str(grid[row][col].get_value()))
                    # tile = tk.Label(background, text=str(grid[row][col].get_value()).ljust(4), font=("Arial", 20))
                    # tile.grid(column=col, row=row+2)
                else:
                    self.grid_tiles[row][col].configure(text='')
        self.window.update_idletasks()


if __name__ == "__main__":
    Graphics()

# ADD IN THE TERMINATING CONDITION NOW
# deactivate the start button when appropriate
# don't read key clicks until the game has been started
