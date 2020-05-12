import tkinter as tk
from game import Game
from bot import Bot
import constants as c
import time


class Graphics(tk.Tk):
    def __init__(self, bot, heuristic=c.RANDOM, look_ahead=0, trials=0, log=False):
        super().__init__()
        # window
        # self.window = tk.Tk()
        self.title("2048")
        # self.grid = grid
        self.game = None  # Game(4, 2)
        self.bot = bot
        self.heuristic = heuristic
        self.look_ahead = look_ahead
        self.trials = trials
        self.log = log

        # labels
        self.header = tk.Frame(self, bg=c.BOARD_COLOR,
                                   width=c.WINDOW_WIDTH,
                                   height=c.WINDOW_HEIGHT)
        self.header.grid(column=0, row=0)

        label = tk.Label(self.header, text="2048", font=c.TITLE_FONT)
        label.grid(column=0, row=0)

        dummy = tk.Label(self.header, text="                 ", font=c.TITLE_FONT)
        dummy.grid(column=1, row=0)
        dummy.grid(column=2, row=0)

        score_label = tk.Label(self.header, text="Score:", font=c.TITLE_FONT)
        score_label.grid(column=3, row=0)

        self.score_value = tk.Label(self.header, text="0".ljust(8), font=c.TITLE_FONT)
        self.score_value.grid(column=4, row=0)


        # key binding
        # self.bind("<Key>", self.take_turn)
        self.bind("<s>", self.start)

        self.grid_tiles = []
        self.background = tk.Frame(self, bg=c.BOARD_COLOR,
                                   width=c.WINDOW_WIDTH,
                                   height=c.WINDOW_HEIGHT)

        self.init_board()

        # buttons
        self.start_button = tk.Button(self, text="Start Game", command=self.start)
        self.start_button.grid(column=0, row=1)

        self.game_over_frame = tk.Frame(self.background, bg=c.BOARD_COLOR,
                                        width=c.WINDOW_WIDTH,
                                        height=c.WINDOW_HEIGHT)

        self.game_over = tk.Label(self.game_over_frame,
                                  text='GAME OVER',
                                  bg=c.BOARD_COLOR,
                                  justify=tk.CENTER,
                                  font=c.TILE_FONT,
                                  width=6,
                                  height=4)

        self.background.grid(column=0, row=2)

        # start the window running
        self.mainloop()

    def init_board(self):

        for row in range(c.BOARD_SIZE):
            row_tiles = []
            for col in range(c.BOARD_SIZE):
                tile = tk.Frame(self.background, bg=c.tile_color_dict[0],
                                width=c.WINDOW_WIDTH / c.BOARD_SIZE,
                                height=c.WINDOW_HEIGHT / c.BOARD_SIZE)
                tile.grid(row=row, column=col,
                          padx=c.TILE_PADX, pady=c.TILE_PADY)
                value = tk.Label(tile,
                                 text='',
                                 bg=c.tile_color_dict[0],
                                 justify=tk.CENTER,
                                 font=c.TILE_FONT,
                                 width=c.TILE_WIDTH,
                                 height=c.TILE_HEIGHT)
                value.grid()
                row_tiles.append(value)
            self.grid_tiles.append(row_tiles)

    def start(self, *args):
        print('here')
        self.unbind("<s>")
        self.start_button["state"] = "disable"

        # self.game_over.master.destroy()
        self.game_over.place_forget()
        self.game_over.configure(text=' ')
        # self.game_over.place(relheight=1, relwidth=1,
        #                      relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.game_over_frame.place_forget()

        if self.bot:
            self.game = Bot(size=c.BOARD_SIZE, start_tiles=c.INIT_TILES,
                            look_ahead=self.look_ahead, trials=self.trials, heuristic=self.heuristic,
                            log=self.log)
        else:
            self.game = Game(size=c.BOARD_SIZE, start_tiles=c.INIT_TILES)

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
                    self.grid_tiles[row][col].configure(text=str(value),
                                                        bg=c.tile_color_dict[value])
                                                        # fg=c.text_color_dict[value])
                else:
                    self.grid_tiles[row][col].configure(text='',
                                                        bg=c.tile_color_dict[0])
                                                        # fg=c.text_color_dict[0])
        self.update_idletasks()

    def update_score(self, score):
        self.score_value.configure(text=str(score).ljust(8))
        self.update_idletasks()

    def take_turn(self, event):
        direction = event.keysym.lower()
        # input("press enter to continue...")
        # time.sleep(1)
        try:
            self.game.take_turn(direction)
            self.display_board(self.game.get_board().get_grid())
            self.update_score(self.game.get_score())
            if self.game.game_over():
                self.end_game()
        except:
            print('game over')

    def end_game(self):
        print('here')
        del self.game

        self.game_over_frame.place(relheight=1 / 4, relwidth=3 / 4,
                                   relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.game_over_frame.lift()
        # value.place(anchor=tk.CENTER)
        self.game_over.configure(text='GAME OVER')
        self.game_over.place(relheight=1, relwidth=1,
                             relx=0.5, rely=0.5, anchor=tk.CENTER)
        # value.grid()

        self.bind("<s>", self.start)
        self.start_button["state"] = "normal"

# if __name__ == "__main__":
#     Graphics(bot=True, heuristic=c.HIGHSCORE)
