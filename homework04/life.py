from __future__ import annotations

import pathlib
import random
import typing as tp

from typing_extensions import TypeAlias

Cell: TypeAlias = tp.Tuple[int, int]
Cells: TypeAlias = tp.List[int]
Grid: TypeAlias = tp.List[tp.List[int]]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        r, c = cell
        out: Cells = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    out.append(self.curr_generation[nr][nc])

        return out

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(randomize=False)
        for r in range(self.rows):
            for c in range(self.cols):
                alive = self.curr_generation[r][c] == 1
                neighbours = self.get_neighbours((r, c))
                alive_cnt = sum(neighbours)

                if alive:
                    new_grid[r][c] = 1 if alive_cnt in (2, 3) else 0
                else:
                    new_grid[r][c] = 1 if alive_cnt == 3 else 0

        return new_grid

    def step(self) -> None:
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        different = self.curr_generation != self.prev_generation
        has_alive = any(v == 1 for row in self.curr_generation for v in row)
        return different and has_alive

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        lines = filename.read_text(encoding="utf-8").splitlines()
        grid: Grid = [[1 if ch == "1" else 0 for ch in line.strip()] for line in lines if line.strip() != ""]
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        life = GameOfLife((rows, cols))
        life.prev_generation = life.create_grid(randomize=False)
        life.curr_generation = grid
        life.generations = 1
        return life

    def save(self, filename: pathlib.Path) -> None:
        text = "\n".join("".join(str(v) for v in row) for row in self.curr_generation) + "\n"
        filename.write_text(text, encoding="utf-8")
