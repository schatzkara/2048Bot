import tkinter as tk
from game import Game
from bot import Bot
import constants as c
import time

# WINDOW_HEIGHT = 400
# WINDOW_WIDTH = 400
# BOARD_SIZE = 4
# INIT_TILES = 2
# LOOK_AHEAD = 1
#
# RANDOM = 0
# HIGHSCORE = 1
# MOSTMERGES = 2
#
# text_color_dict = {0: '#BDAD9E',
#                    2: '#BDAD9E',
#                    4: '#ede0c8',
#                    8: '#f9f6f2',
#                    16: '#f9f6f2',
#                    32: '#f9f6f2',
#                    64: '#f9f6f2',
#                    128: '#f9f6f2',
#                    256: '#f9f6f2',
#                    512: '#f9f6f2',
#                    1024: '#f9f6f2',
#                    2048: '#f9f6f2'
#                    }
#
# tile_color_dict = {0: '#BDAD9E',
#                    2: '#eee4da',
#                    4: '#ede0c8',
#                    8: '#f2b179',
#                    16: '#f59563',
#                    32: '#f67c5f',
#                    64: '#f65e3b',
#                    128: '#edcf72',
#                    256: '#edcc61',
#                    512: '#edc850',
#                    1024: '#edc53f',
#                    2048: '#edc22e'
#                    }


class Graphics(tk.Tk):
    def __init__(self, bot):
        super().__init__()
        # window
        # self.window = tk.Tk()
        self.title("2048")
        # self.grid = grid
        self.game = None  # Game(4, 2)
        self.bot = bot

        # labels
        label = tk.Label(self, text="2048", font=("Arial", 30))
        label.grid(column=0, row=0)

        # key binding
        # self.bind("<Key>", self.take_turn)

        self.grid_tiles = []
        self.background = tk.Frame(self, bg='#776e65',
                                   width=c.WINDOW_WIDTH,
                                   height=c.WINDOW_HEIGHT)

        self.init_board()

        # buttons
        self.start_button = tk.Button(self, text="Start Game", command=self.start)
        self.start_button.grid(column=0, row=1)

        self.game_over_frame = tk.Frame(self.background, bg='#776e65',
                                        width=c.WINDOW_WIDTH,
                                        height=c.WINDOW_HEIGHT)

        self.game_over = tk.Label(self.game_over_frame,
                                  text='GAME OVER',
                                  bg='#776e65',
                                  justify=tk.CENTER,
                                  font=("Arial", 40),
                                  width=6,
                                  height=4)

        self.background.grid()

        # start the window running
        self.mainloop()

    def init_board(self):

        for row in range(c.BOARD_SIZE):
            row_tiles = []
            for col in range(c.BOARD_SIZE):
                tile = tk.Frame(self.background, bg='#BDAD9E',
                                width=c.WINDOW_WIDTH / c.BOARD_SIZE,
                                height=c.WINDOW_HEIGHT / c.BOARD_SIZE)
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
        self.game_over_frame.place_forget()
        self.game_over.configure(text='')

        self.game = Bot(c.BOARD_SIZE, c.INIT_TILES, c.LOOK_AHEAD, c.HIGHSCORE, True) if self.bot else Game(c.BOARD_SIZE, c.INIT_TILES)
        self.display_board(self.game.get_board().get_grid())
        # key binding
        self.bind("<Key>", self.take_turn)
        # self.play(g)
        if self.bot:
            self.game.take_turn(None)

    def display_board(self, grid):
        for row in range(c.BOARD_SIZE):
            for col in range(c.BOARD_SIZE):
                if grid[row][col] is not None:
                    value = grid[row][col].get_value()
                    self.grid_tiles[row][col].configure(text=str(value), bg=c.tile_color_dict[value])
                else:
                    self.grid_tiles[row][col].configure(text='', bg=c.tile_color_dict[0])
        self.update_idletasks()

    def take_turn(self, event):
        direction = event.keysym.lower()
        # time.sleep(0.5)
        self.game.take_turn(direction)
        self.display_board(self.game.get_board().get_grid())
        if self.game.game_over():
            self.end_game()

    def end_game(self):
        print('here')

        self.game_over_frame.place(relheight=1 / 4, relwidth=3 / 4,
                                   relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.game_over_frame.lift()
        # value.place(anchor=tk.CENTER)
        self.game_over.configure(text='GAME OVER')
        self.game_over.place(relheight=1, relwidth=1,
                             relx=0.5, rely=0.5, anchor=tk.CENTER)
        # value.grid()


if __name__ == "__main__":
    Graphics(bot=True)

# ADD IN THE TERMINATING CONDITION NOW
# deactivate the start button when appropriate
# don't read key clicks until the game has been started
