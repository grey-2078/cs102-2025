import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """grouping elements"""
    return [values[i : i + n] for i in range(0, len(values), n)]


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """grid maker"""
    digits = [c for c in puzzle if c in "123456789."]
    return group(digits, 9)


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """reads sudoku puzzle"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def display(grid: tp.List[tp.List[str]]) -> None:
    """displays the table"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if col in (2, 5) else "")
                for col in range(9)
            )
        )
        if row in (2, 5):
            print(line)
    print()


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """gets the row"""
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """gets the column"""
    _, col = pos
    return [grid[row][col] for row in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """gets the 3x3 block"""
    row, col = pos
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    return [
        grid[r][c]
        for r in range(start_row, start_row + 3)
        for c in range(start_col, start_col + 3)
    ]


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """finds empty positions"""
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):

            if value == ".":
                return row_index, col_index
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """finds possible values"""
    used = set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos))
    return {str(i) for i in range(1, 10)} - used


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """solves sudoku"""
    pos = find_empty_positions(grid)
    if pos is None:
        return grid

    row, col = pos

    for value in sorted(find_possible_values(grid, pos)):
        grid[row][col] = value
        if solve(grid):
            return grid
        grid[row][col] = "."

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """checks if solution is right"""
    digits = {str(i) for i in range(1, 10)}

    for i in range(9):
        if set(solution[i]) != digits:
            return False
        if set(solution[r][i] for r in range(9)) != digits:
            return False

    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            block = [solution[i][j] for i in range(r, r + 3) for j in range(c, c + 3)]
            if set(block) != digits:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """generates sudoku tabl"""
    grid = [["." for _ in range(9)] for _ in range(9)]
    solve(grid)

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    to_remove = max(0, 81 - N)
    for i in range(to_remove):
        r, c = cells[i]
        grid[r][c] = "."

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
