from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    dirs = [(-2, 0), (0, 2)]
    dx, dy = choice(dirs)
    nx, ny = x + dx, y + dy

    if not (0 <= nx < rows and 0 <= ny < cols):
        dx, dy = dirs[0] if (dx, dy) == dirs[1] else dirs[1]
        nx, ny = x + dx, y + dy

    if 0 <= nx < rows and 0 <= ny < cols:
        wx, wy = x + dx // 2, y + dy // 2
        grid[wx][wy] = " "

    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = (
            randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        )
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                if i - 1 >= 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if i + 1 < rows and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if j - 1 >= 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if j + 1 < cols and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    x, y = exit_coord

    cell = grid[x][y]
    if not isinstance(cell, int):
        return None

    k = cell
    path = [(x, y)]
    rows = len(grid)
    cols = len(grid[0])

    while k != 1:
        if x - 1 >= 0 and isinstance(grid[x - 1][y], int) and grid[x - 1][y] == k - 1:
            x = x - 1
        elif (
            x + 1 < rows and isinstance(grid[x + 1][y], int) and grid[x + 1][y] == k - 1
        ):
            x = x + 1
        elif y - 1 >= 0 and isinstance(grid[x][y - 1], int) and grid[x][y - 1] == k - 1:
            y = y - 1
        elif (
            y + 1 < cols and isinstance(grid[x][y + 1], int) and grid[x][y + 1] == k - 1
        ):
            y = y + 1
        else:
            return None

        path.append((x, y))

        cell = grid[x][y]
        if not isinstance(cell, int):
            return None
        k = cell

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    if not (x == 0 or y == 0 or x == rows - 1 or y == cols - 1):
        return False

    ok = True
    if x - 1 >= 0 and grid[x - 1][y] != "■":
        ok = False
    if x + 1 < rows and grid[x + 1][y] != "■":
        ok = False
    if y - 1 >= 0 and grid[x][y - 1] != "■":
        ok = False
    if y + 1 < cols and grid[x][y + 1] != "■":
        ok = False

    return ok


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) <= 1:
        if exits:
            return grid, exits[0]
        return grid, None

    enter_coord = exits[0]
    exit_coord = exits[1]

    if encircled_exit(grid, enter_coord) or encircled_exit(grid, exit_coord):
        return grid, None

    work_grid = deepcopy(grid)
    for i, row in enumerate(work_grid):
        for j, cell in enumerate(row):
            if cell == " ":
                work_grid[i][j] = 0
            elif cell == "X":
                work_grid[i][j] = 0

    ex, ey = enter_coord
    work_grid[ex][ey] = 1

    k = 1
    while work_grid[exit_coord[0]][exit_coord[1]] == 0:
        zero_before = 0
        for r in work_grid:
            for c in r:
                if c == 0:
                    zero_before += 1

        work_grid = make_step(work_grid, k)
        k += 1

        zero_after = 0
        for r in work_grid:
            for c in r:
                if c == 0:
                    zero_after += 1

        if zero_after == zero_before:
            return work_grid, None

        if k > len(work_grid) * len(work_grid[0]) + 5:
            return work_grid, None

    path = shortest_path(work_grid, exit_coord)
    return work_grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
