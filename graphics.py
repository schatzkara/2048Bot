import tkinter as tk
from game import Game

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BOARD_SIZE = 4
INIT_TILES = 2


class Graphics(tk.Tk):
    def __init__(self):
        super().__init__()
        # window
        # self.window = tk.Tk()
        self.title("2048")
        self.game = None  # Game(4, 2)

        # labels
        label = tk.Label(self, text="2048", font=("Arial", 30))
        label.grid(column=0, row=0)

        # buttons
        start_button = tk.Button(self, text="Start Game", command=self.start)
        start_button.grid(column=0, row=1)

        # key binding
        self.bind("<Key>", self.take_turn)

        self.grid_tiles = []
        self.init_board()

        # start the window running
        self.mainloop()

    def init_board(self):
        background = tk.Frame(self, bg='#776e65',
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
            self.grid_tiles.append(row_tiles)

    def start(self):
        self.game = Game(4, 2)
        self.display_board(self.game.get_board().get_grid())
        # self.play(g)

    def display_board(self, grid):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if grid[row][col] is not None:
                    self.grid_tiles[row][col].configure(text=str(grid[row][col].get_value()))
                else:
                    self.grid_tiles[row][col].configure(text='')
        self.update_idletasks()

    def take_turn(self, event):
        direction = event.keysym.lower()
        self.game.take_turn(direction)
        self.display_board(self.game.get_board().get_grid())
        if self.game.game_over():
            self.end_game()

    def end_game(self):
        print('here')
        background = tk.Frame(self, bg='#776e65',
                              width=WINDOW_WIDTH,
                              height=WINDOW_HEIGHT)
        background.grid()
        value = tk.Label(background,
                         text='GAME OVER',
                         bg='#BDAD9E',
                         justify=tk.CENTER,
                         font=("Arial", 40),
                         width=4,
                         height=2)
        value.grid()


if __name__ == "__main__":
    Graphics()

# ADD IN THE TERMINATING CONDITION NOW
# deactivate the start button when appropriate
# don't read key clicks until the game has been started
