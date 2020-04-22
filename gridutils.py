def num_monotonic(grid):
    size = len(grid)
    count = 0
    for i in range(size):
        # row
        if monotonic(grid[i]):
            count += 1
        # col
        if monotonic([grid[j][i] for j in range(size)]):
            count += 1

    return count


def monotonic(list):
    return monotonic_increasing(list) or monotonic_decreasing(list)


def monotonic_increasing(list):
    for i in range(1, len(list)):
        if list[i] is not None and list[i - 1] is not None and list[i].get_value() <= list[i - 1].get_value():
            return False
    return True


def monotonic_decreasing(list):
    for i in range(1, len(list)):
        if list[i] is not None and list[i - 1] is not None and list[i].get_value() >= list[i - 1].get_value():
            return False
    return True


def get_highest_tile(grid):
    size = len(grid)
    highest = 0
    for row in range(size):
        for col in range(size):
            if grid[row][col] is not None and grid[row][col].get_value() > highest:
                highest = grid[row][col].get_value()

    return highest


def value_in_corner(grid, value):
    size = len(grid)
    if grid[0][0] is not None and grid[0][0].get_value() == value:
        return True
    elif grid[size - 1][0] is not None and grid[size - 1][0].get_value() == value:
        return True
    elif grid[0][size - 1] is not None and grid[0][size - 1].get_value() == value:
        return True
    elif grid[size - 1][size - 1] is not None and grid[size - 1][size - 1].get_value() == value:
        return True
    else:
        return False


def value_in_top_left(grid, value):
    return grid[0][0] is not None and grid[0][0].get_value() == value


def value_in_top_right(grid, value):
    size = len(grid)
    return grid[0][size - 1] is not None and grid[0][size - 1].get_value() == value


def value_in_bottom_left(grid, value):
    size = len(grid)
    return grid[size - 1][0] is not None and grid[size - 1][0].get_value() == value


def value_in_bottom_right(grid, value):
    size = len(grid)
    return grid[size - 1][size - 1] is not None and grid[size - 1][size - 1].get_value() == value


def value_near_empty_space(grid, value):
    size = len(grid)
    count = 0
    for row in range(size):
        for col in range(size):
            if grid[row][col] is None:
                # check left
                if row - 1 > 0 and grid[row - 1][col] is not None and grid[row - 1][col].get_value() == value:
                    count += 1
                # check right
                if row + 1 < size and grid[row + 1][col] is not None and grid[row + 1][col].get_value() == value:
                    count += 1
                # check up
                if col - 1 > 0 and grid[row][col - 1] is not None and grid[row][col - 1].get_value() == value:
                    count += 1
                # check down
                if col + 1 < size and grid[row][col + 1] is not None and grid[row][col + 1].get_value() == value:
                    count += 1

    return count


def num_available_merges(grid):
    size = len(grid)
    count = 0
    for row in range(size):
        for col in range(size):
            if grid[row][col] is not None:
                value = grid[row][col].get_value()
                # check left
                if row - 1 > 0 and grid[row - 1][col] is not None and grid[row - 1][col].get_value() == value:
                    count += 1
                # check right
                if row + 1 < size and grid[row + 1][col] is not None and grid[row + 1][col].get_value() == value:
                    count += 1
                # check up
                if col - 1 > 0 and grid[row][col - 1] is not None and grid[row][col - 1].get_value() == value:
                    count += 1
                # check down
                if col + 1 < size and grid[row][col + 1] is not None and grid[row][col + 1].get_value() == value:
                    count += 1

    return count // 2
