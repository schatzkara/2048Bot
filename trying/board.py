import random
from tile import Tile
import tkinter as tk


class Board:
    def __init__(self, size, start_tiles):
        self.size = size
        self.start_tiles = start_tiles
        self.empty = None
        self.grid = [[self.empty for x in range(self.size)] for y in range(self.size)]
        """ randomly put 2 tiles (either 2 or 4) on the board """
        # self.init_grid()
        # self.display()

    def get_grid(self):
        return self.grid

    def init_grid(self):
        # self.grid[0][2] = Tile(2, 0, 2)
        for i in range(self.start_tiles):
            self.add_tile()

    def add_tile(self):
        # print('addin')
        value = random.randint(0, 9)
        value = 2 if value < 9 else 4

        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)

        while self.grid[x][y] is not self.empty:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

        # x = 0
        self.grid[x][y] = Tile(value, x, y)

    def display(self):
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if self.grid[i][j] is None:
                    row = row + str(0).ljust(4) + "  "
                else:
                    row = row + str(self.grid[i][j].get_value()).ljust(4) + "  "
            print(row)
        print()
        # print('done')
        # self.graphics_display()

    def graphics_display(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] is None:
                    # row = row + str(0).ljust(4) + "  "
                    tile = tk.Label(self.window, text='0')
                    tile.grid(column=j, row=i + 2)
                else:
                    # row = row + str(self.grid[i][j].get_value()).ljust(4) + "  "
                    tile = tk.Label(self.window, text=str(self.grid[i][j].get_value()).ljust(4))
                    tile.grid(column=j, row=i + 2)

    # MAKE SURE IT DON'T ADD NO NEW TILE IF YOU AIN'T GOT NONE TO MOVE
    def move(self, direction, turn):
        score = 0
        movesMade = False
        moved = False
        score_delta = 0
        """ direction can be "left", "right", "up", "down" """
        if direction == "left":
            for row in range(self.size):
                for col in range(self.size):
                    moved, score_delta = self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    score += score_delta
        elif direction == "right":
            for row in range(self.size):
                for col in range(self.size-1, -1, -1):
                    moved, score_delta = self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    score += score_delta
        elif direction == "up":
            for col in range(self.size):
                for row in range(self.size):
                    moved, score_delta = self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    score += score_delta
        elif direction == "down":
            for col in range(self.size):
                for row in range(self.size-1, -1, -1):
                    moved, score_delta = self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    score += score_delta
        else:
            print("poop")

        # if moved:
        #     movesMade = True
        # score += score_delta

        return movesMade, score, self.grid

    def move_tile(self, tile, direction, turn):
        moved = False
        score = 0
        if tile is not None:
            if direction == "left":
                # print(tile.get_position())
                row, col = tile.get_position()
                i = col - 1
                #  find furthest left spot we can move to (that's i)
                while i >= 0 and self.grid[row][i] is None:
                    i -= 1
                    # print(i)
                new_col = i + 1
                # print(new_col)
                # we can merge
                if i >= 0 and self.grid[row][i] is not None and self.grid[row][i].get_value() == tile.get_value() and tile.get_last_merged() != turn:
                    self.grid[row][col] = None
                    score += tile.merge(turn)
                    tile.set_position(row, i)
                    self.grid[row][i] = tile
                    moved = True
                    # print('we mergin')
                # we can't merge
                else:
                    # we can't merge sowwy
                    # shift = i - 1
                    if col != new_col:
                        self.grid[row][col] = None
                        tile.set_position(row, new_col)
                        self.grid[row][new_col] = tile
                        moved = True

                # print('done')

            elif direction == "right":
                # print(tile.get_position())
                row, col = tile.get_position()
                i = col + 1
                #  find furthest left spot we can move to (that's i)
                while i < self.size and self.grid[row][i] is None:
                    i += 1
                    # print(i)
                new_col = i - 1
                # print(new_col)
                # we can merge
                if i < self.size and self.grid[row][i] is not None and self.grid[row][i].get_value() == tile.get_value() and tile.get_last_merged() != turn:
                    self.grid[row][col] = None
                    score += tile.merge(turn)
                    tile.set_position(row, i)
                    self.grid[row][i] = tile
                    moved = True
                    # print('we mergin')
                # we can't merge
                else:
                    # we can't merge sowwy
                    # shift = i - 1
                    if col != new_col:
                        self.grid[row][col] = None
                        tile.set_position(row, new_col)
                        self.grid[row][new_col] = tile
                        moved = True
                # print('done')

            elif direction == "up":
                # print(tile.get_position())
                row, col = tile.get_position()
                i = row - 1
                #  find furthest left spot we can move to (that's i)
                while i >= 0 and self.grid[i][col] is None:
                    i -= 1
                    # print(i)
                new_row = i + 1
                # print(new_y)
                # we can merge
                if i >= 0 and self.grid[i][col] is not None and self.grid[i][col].get_value() == tile.get_value() and tile.get_last_merged() != turn:
                    self.grid[row][col] = None
                    score += tile.merge(turn)
                    tile.set_position(i, col)
                    self.grid[i][col] = tile
                    moved = True
                    # print('we mergin')
                # we can't merge
                else:
                    # we can't merge sowwy
                    # shift = i - 1
                    if row != new_row:
                        self.grid[row][col] = None
                        tile.set_position(new_row, col)
                        self.grid[new_row][col] = tile
                        moved = True
                # print('done')

            elif direction == "down":
                # print(tile.get_position())
                row, col = tile.get_position()
                i = row + 1
                #  find furthest left spot we can move to (that's i)
                while i < self.size and self.grid[i][col] is None:
                    i += 1
                    # print(i)
                new_row = i - 1
                # print(new_y)
                # we can merge
                if i < self.size and self.grid[i][col] is not None and self.grid[i][col].get_value() == tile.get_value() and tile.get_last_merged() != turn:
                    self.grid[row][col] = None
                    score += tile.merge(turn)
                    tile.set_position(i, col)
                    self.grid[i][col] = tile
                    moved = True
                    # print('we mergin')
                # we can't merge
                else:
                    # we can't merge sowwy
                    # shift = i - 1
                    if row != new_row:
                        self.grid[row][col] = None
                        tile.set_position(new_row, col)
                        self.grid[new_row][col] = tile
                        moved = True
                # print('done')
        return moved, score

    def empty_rowcol(self, arr):
        for i in range(len(arr)):
            if arr[i] is not self.empty:
                return False
        return True

    def full_rowcol(self, arr):
        for i in range(len(arr)):
            if arr[i] is self.empty:
                return False
        return True

    def no_merges_rowcol(self, arr):
        for i in range(len(arr)):
            for j in range(i, len(arr)):
                if arr[j] is not self.empty:
                    if arr[i] == arr[j]:
                        return False
                    else:
                        break
        return True

    def full_board(self):
        # for row in range(self.size):
        #     if not self.full_rowcol(self.grid[row]):
        #         return False
        # return True
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is None:
                    return False
        return True

    def no_merges_board(self):
        # for row in range(self.size):
        #     if not self.no_merges_rowcol(self.grid[row]):
        #         return False
        # for col in range(self.size):
        #     if not self.no_merges_rowcol([row[col] for row in self.board]):
        #         return False
        # return True
        for row in range(self.size-1):
            for col in range(self.size-1):
                if self.grid[row][col].get_value() == self.grid[row][col+1].get_value():
                    return False
                if self.grid[row][col].get_value() == self.grid[row+1][col].get_value():
                    return False
        return True

    def dead(self):
        return self.full_board() and self.no_merges_board()
