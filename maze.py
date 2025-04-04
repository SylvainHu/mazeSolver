from graphics import Cell
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for row in range(self._num_rows)] for col in range(self._num_cols)]
        for j in range(self._num_cols):
            for i in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is not None:
            c = self._cells[j][i]
            x1 = self._x1 + j * self._cell_size_x
            y1 = self._y1 + i * self._cell_size_y
            x2 = x1 + self._cell_size_x
            y2 = y1 + self._cell_size_y

            c.draw(x1, y1, x2, y2)
            self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(0, 0)

        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)