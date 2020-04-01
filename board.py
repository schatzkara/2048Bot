import random
from tile import Tile


class Board:
    """
    Constructor for Board objects.
    Board objects have the following fields:
        size: the number of tiles in each row and column of the board
        start_tiles: the number of tiles that the board starts with
        grid: a 2D array representing the board
    """
    def __init__(self, size, start_tiles):
        self.size = size
        self.start_tiles = start_tiles
        self.grid = [[None for x in range(self.size)] for y in range(self.size)]
        """ randomly put 2 tiles (either 2 or 4) on the board """
        # self.init_grid()
        # self.display()

    """
    Accessor method for the grid
    @return the field grid
    """
    def get_grid(self):
        return self.grid

    """
    Determines the value of the highest tile in the grid.
    @return the value of the highest tile
    """
    def get_highest_tile(self):
        highest = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is not None and self.grid[row][col].get_value() > highest:
                    highest = self.grid[row][col].get_value()

        return highest

    """ 
    Initializes the grid. Adds start_tiles tiles to the board.
    """
    def init_grid(self):
        # add the correct number of tiles for the starting board
        for i in range(self.start_tiles):
            self.add_tile()

    """
    Adds a new tile to the board.
    Adds either a 2-tile or a 4-tile with probability 0.9 and 0.1, respectively
    """
    def add_tile(self):
        # generate a 2 or a 4 with correct probability
        value = random.randint(0, 9)
        value = 2 if value < 9 else 4

        # generate a random tile position to place the tile
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)

        # make sure that the tile position isn't already filled
        while self.grid[x][y] is not None:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

        # place the tile
        self.grid[x][y] = Tile(value, x, y)

    """
    Prints the grid to the console in a readable way.
    """
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

    """
    Moves all the tiles on the board in the designated direction. 
    @param direction - the direction to move, can only be "left", "right", "up", "down"
    @param turn - the turn number that the board is on 
    @return a 3-tuple (movesMade, score, self.grid) representing the following:
        movesMade: true if at least one tile was moved, false otherwise
        score: the number of points earned during the turn
        self.grid: the grid
    """
    def move(self, direction, turn):
        score = 0
        movesMade = False
        mergesMade = 0
        """ direction can be "left", "right", "up", "down" """
        if direction == "left":
            for row in range(self.size):
                for col in range(self.size):
                    # if self.grid[row][col] is not None:
                    moved, merges, score_delta = self.move_tile_left(tile=self.grid[row][col], turn=turn)
                    # self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    mergesMade += merges
                    score += score_delta
        elif direction == "right":
            for row in range(self.size):
                for col in range(self.size-1, -1, -1):
                    # if self.grid[row][col] is not None:
                    moved, merges, score_delta = self.move_tile_right(tile=self.grid[row][col], turn=turn)
                    # self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    mergesMade += merges
                    score += score_delta
        elif direction == "up":
            for col in range(self.size):
                for row in range(self.size):
                    # if self.grid[row][col] is not None:
                    moved, merges, score_delta = self.move_tile_up(tile=self.grid[row][col], turn=turn)
                    # self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    mergesMade += merges
                    score += score_delta
        elif direction == "down":
            for col in range(self.size):
                for row in range(self.size-1, -1, -1):
                    # if self.grid[row][col] is not None:
                    moved, merges, score_delta = self.move_tile_down(tile=self.grid[row][col], turn=turn)
                    # self.move_tile(tile=self.grid[row][col], direction=direction, turn=turn)
                    if moved:
                        movesMade = True
                    mergesMade += merges
                    score += score_delta
        else:
            print("poop")

        return movesMade, mergesMade, score

    def move_tile_left(self, tile, turn):
        moved = False
        merges = 0
        score = 0
        if tile is not None:
            row, col = tile.get_position()
            i = col - 1  # col to move to
            #  find furthest left spot we can move to (that's i)
            while i >= 0 and self.grid[row][i] is None:
                i -= 1
            new_col = i + 1
            # case: we can merge
            if i >= 0 and self.can_merge_tiles(tile1=tile, tile2=self.grid[row][i], turn=turn):
                # move tile from old position
                self.grid[row][col] = None
                # merge tiles
                score += tile.merge(turn)
                # put tile in new position
                tile.set_position(row, i)
                self.grid[row][i] = tile
                # reflect that tiles were merged
                moved = True
                merges += 1
            # case: we can't merge
            else:
                # case: we can move
                if col != new_col:
                    # move tile from old position
                    self.grid[row][col] = None
                    # put tile in new position
                    tile.set_position(row, new_col)
                    self.grid[row][new_col] = tile
                    # reflect that the tile was moved
                    moved = True

        return moved, merges, score

    def move_tile_right(self, tile, turn):
        moved = False
        merges = 0
        score = 0
        if tile is not None:
            row, col = tile.get_position()
            i = col + 1  # col to move to
            #  find furthest right spot we can move to (that's i)
            while i < self.size and self.grid[row][i] is None:
                i += 1
            new_col = i - 1
            # case: we can merge
            if i < self.size and self.can_merge_tiles(tile1=tile, tile2=self.grid[row][i], turn=turn):
                self.grid[row][col] = None
                score += tile.merge(turn)
                tile.set_position(row, i)
                self.grid[row][i] = tile
                moved = True
                merges += 1
            # we can't merge
            else:
                if col != new_col:
                    self.grid[row][col] = None
                    tile.set_position(row, new_col)
                    self.grid[row][new_col] = tile
                    moved = True

        return moved, merges, score

    def move_tile_up(self, tile, turn):
        moved = False
        merges = 0
        score = 0
        if tile is not None:
            row, col = tile.get_position()
            i = row - 1  # row to move to
            #  find furthest up spot we can move to (that's i)
            while i >= 0 and self.grid[i][col] is None:
                i -= 1
            new_row = i + 1
            # case: we can merge
            if i >= 0 and self.can_merge_tiles(tile1=tile, tile2=self.grid[i][col], turn=turn):
                self.grid[row][col] = None
                score += tile.merge(turn)
                tile.set_position(i, col)
                self.grid[i][col] = tile
                moved = True
                merges += 1
            # we can't merge
            else:
                if row != new_row:
                    self.grid[row][col] = None
                    tile.set_position(new_row, col)
                    self.grid[new_row][col] = tile
                    moved = True

        return moved, merges, score

    def move_tile_down(self, tile, turn):
        moved = False
        merges = 0
        score = 0
        if tile is not None:
            row, col = tile.get_position()
            i = row + 1  # row to move to
            #  find furthest down spot we can move to (that's i)
            while i < self.size and self.grid[i][col] is None:
                i += 1
            new_row = i - 1
            # case: we can merge
            if i < self.size and self.can_merge_tiles(tile1=tile, tile2=self.grid[i][col], turn=turn):
                self.grid[row][col] = None
                score += tile.merge(turn)
                tile.set_position(i, col)
                self.grid[i][col] = tile
                moved = True
                merges += 1
            # we can't merge
            else:
                if row != new_row:
                    self.grid[row][col] = None
                    tile.set_position(new_row, col)
                    self.grid[new_row][col] = tile
                    moved = True

        return moved, merges, score

    # def move_tile(self, tile, direction, turn):
    #     moved = False
    #     merges = 0
    #     score = 0
    #     if tile is not None:
    #         if direction == "left":
    #             row, col = tile.get_position()
    #             i = col - 1  # col to move to
    #             #  find furthest left spot we can move to (that's i)
    #             while i >= 0 and self.grid[row][i] is None:
    #                 i -= 1
    #                 # print(i)
    #             new_col = i + 1
    #             # case: we can merge
    #             # if i >= 0 and self.grid[row][i] is not None and self.grid[row][i].get_value() == tile.get_value()
    #             # and tile.get_last_merged() != turn and self.grid[row][i].get_last_merged() != turn:
    #             if i >= 0 and self.can_merge_tiles(tile1=tile, tile2=self.grid[row][i], turn=turn):
    #                 # move tile from old position
    #                 self.grid[row][col] = None
    #                 # merge tiles
    #                 score += tile.merge(turn)
    #                 # put tile in new position
    #                 tile.set_position(row, i)
    #                 self.grid[row][i] = tile
    #                 # reflect that tiles were merged
    #                 moved = True
    #                 merges += 1
    #             # case: we can't merge
    #             else:
    #                 # case: we can move
    #                 if col != new_col:
    #                     # move tile from old position
    #                     self.grid[row][col] = None
    #                     # put tile in new position
    #                     tile.set_position(row, new_col)
    #                     self.grid[row][new_col] = tile
    #                     # reflect that tiles were merged
    #                     moved = True
    #
    #         elif direction == "right":
    #             # print(tile.get_position())
    #             row, col = tile.get_position()
    #             i = col + 1
    #             #  find furthest left spot we can move to (that's i)
    #             while i < self.size and self.grid[row][i] is None:
    #                 i += 1
    #                 # print(i)
    #             new_col = i - 1
    #             # print(new_col)
    #             # we can merge
    #             if i < self.size and self.grid[row][i] is not None and self.grid[row][i].get_value() == tile.get_value() and tile.get_last_merged() != turn and self.grid[row][i].get_last_merged() != turn:
    #                 self.grid[row][col] = None
    #                 score += tile.merge(turn)
    #                 tile.set_position(row, i)
    #                 self.grid[row][i] = tile
    #                 moved = True
    #                 merges += 1
    #                 # print('we mergin')
    #             # we can't merge
    #             else:
    #                 # we can't merge sowwy
    #                 # shift = i - 1
    #                 if col != new_col:
    #                     self.grid[row][col] = None
    #                     tile.set_position(row, new_col)
    #                     self.grid[row][new_col] = tile
    #                     moved = True
    #             # print('done')
    #
    #         elif direction == "up":
    #             # print(tile.get_position())
    #             row, col = tile.get_position()
    #             i = row - 1
    #             #  find furthest left spot we can move to (that's i)
    #             while i >= 0 and self.grid[i][col] is None:
    #                 i -= 1
    #                 # print(i)
    #             new_row = i + 1
    #             # print(new_y)
    #             # we can merge
    #             if i >= 0 and self.grid[i][col] is not None and self.grid[i][col].get_value() == tile.get_value() and tile.get_last_merged() != turn and self.grid[i][col].get_last_merged() != turn:
    #                 self.grid[row][col] = None
    #                 score += tile.merge(turn)
    #                 tile.set_position(i, col)
    #                 self.grid[i][col] = tile
    #                 moved = True
    #                 merges += 1
    #                 # print('we mergin')
    #             # we can't merge
    #             else:
    #                 # we can't merge sowwy
    #                 # shift = i - 1
    #                 if row != new_row:
    #                     self.grid[row][col] = None
    #                     tile.set_position(new_row, col)
    #                     self.grid[new_row][col] = tile
    #                     moved = True
    #             # print('done')
    #
    #         elif direction == "down":
    #             # print(tile.get_position())
    #             row, col = tile.get_position()
    #             i = row + 1
    #             #  find furthest left spot we can move to (that's i)
    #             while i < self.size and self.grid[i][col] is None:
    #                 i += 1
    #                 # print(i)
    #             new_row = i - 1
    #             # print(new_y)
    #             # we can merge
    #             if i < self.size and self.grid[i][col] is not None and self.grid[i][col].get_value() == tile.get_value() and tile.get_last_merged() != turn and self.grid[i][col].get_last_merged() != turn:
    #                 self.grid[row][col] = None
    #                 score += tile.merge(turn)
    #                 tile.set_position(i, col)
    #                 self.grid[i][col] = tile
    #                 moved = True
    #                 merges += 1
    #                 # print('we mergin')
    #             # we can't merge
    #             else:
    #                 # we can't merge sowwy
    #                 # shift = i - 1
    #                 if row != new_row:
    #                     self.grid[row][col] = None
    #                     tile.set_position(new_row, col)
    #                     self.grid[new_row][col] = tile
    #                     moved = True
    #             # print('done')
    #     return moved, merges, score

    def can_merge_tiles(self, tile1, tile2, turn):
        return tile1 is not None and tile2 is not None and tile1.get_value() == tile2.get_value() and tile1.get_last_merged() != turn and tile2.get_last_merged() != turn

    def mergeable(self, tile, turn):
        return tile is not None and tile.get_last_merged() != turn

    def empty_rowcol(self, arr):
        for i in range(len(arr)):
            if arr[i] is not None:
                return False
        return True

    def full_rowcol(self, arr):
        for i in range(len(arr)):
            if arr[i] is None:
                return False
        return True

    def no_merges_rowcol(self, arr):
        for i in range(len(arr)):
            for j in range(i, len(arr)):
                if arr[j] is not None:
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
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is not None:
                    if col + 1 < self.size and self.grid[row][col+1] is not None:
                        if self.grid[row][col].get_value() == self.grid[row][col+1].get_value():
                            return False
                    if row + 1 < self.size and self.grid[row+1][col] is not None:
                        if self.grid[row][col].get_value() == self.grid[row+1][col].get_value():
                            return False
        return True

    def dead(self):
        return self.full_board() and self.no_merges_board()
