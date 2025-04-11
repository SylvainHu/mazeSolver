from cells import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visted()


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
        self._draw_cell(self._num_rows - 1, self._num_cols - 1)

    def _break_walls_r(self, i, j):
        self._cells[j][i]._visited = True

        while True:
            to_visit = []
            # Check all adjacent cells
            if i > 0 and not self._cells[j][i - 1]._visited:  # Above
                to_visit.append((i - 1, j))
            if i < self._num_rows - 1 and not self._cells[j][i + 1]._visited:  # Below
                to_visit.append((i + 1, j))
            if j > 0 and not self._cells[j - 1][i]._visited:  # Left
                to_visit.append((i, j - 1))
            if j < self._num_cols - 1 and not self._cells[j + 1][i]._visited:  # Right
                to_visit.append((i, j + 1))

            if not to_visit:
                self._draw_cell(i, j)
                return
            
            next_i, next_j = random.choice(to_visit)
            if next_i < i:  # Moving up
                self._cells[j][i].has_top_wall = False
                self._cells[next_j][next_i].has_bottom_wall = False
            elif next_i > i:  # Moving down
                self._cells[j][i].has_bottom_wall = False
                self._cells[next_j][next_i].has_top_wall = False
            elif next_j < j:  # Moving left
                self._cells[j][i].has_left_wall = False
                self._cells[next_j][next_i].has_right_wall = False
            elif next_j > j:  # Moving right
                self._cells[j][i].has_right_wall = False
                self._cells[next_j][next_i].has_left_wall = False
            self._draw_cell(i, j)
            self._draw_cell(next_i, next_j)

            self._break_walls_r(next_i, next_j)
        
    def _reset_cells_visted(self):
        for col in self._cells:
            for cell in col:
                cell._visited = False

    def has_wall(self, j, i, direction):
        if direction == (-1, 0):  # Up
            return self._cells[j][i].has_top_wall
        elif direction == (0, 1):  # Right
            return self._cells[j][i].has_right_wall
        elif direction == (1, 0):  # Down
            return self._cells[j][i].has_bottom_wall
        elif direction == (0, -1):  # Left
            return self._cells[j][i].has_left_wall
        return True  # Default: wall exists (safety)

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, j, i):
        self._animate()
        
        self._cells[j][i]._visited = True
        
        # Check if we've reached the end
        if j == self._num_cols - 1 and i == self._num_rows - 1:
            return True
        
        # Define directions: Up, Right, Down, Left
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        direction_names = ["up", "right", "down", "left"]
        
        for idx, (dj, di) in enumerate(directions):
            new_j = j + dj
            new_i = i + di
            direction_name = direction_names[idx]
            
            # Check if the move is valid
            if (0 <= new_i < self._num_rows and 0 <= new_j < self._num_cols and 
                not self._cells[new_j][new_i]._visited):
                
                # Check for walls based on direction
                has_wall = False
                if direction_name == "up":
                    has_wall = self._cells[j][i].has_top_wall
                elif direction_name == "right":
                    has_wall = self._cells[j][i].has_right_wall
                elif direction_name == "down":
                    has_wall = self._cells[j][i].has_bottom_wall
                elif direction_name == "left":
                    has_wall = self._cells[j][i].has_left_wall
                
                if not has_wall:
                    self._cells[j][i].draw_move(self._cells[new_j][new_i])
                    
                    if self._solve_r(new_j, new_i):
                        return True
                    
                    self._cells[j][i].draw_move(self._cells[new_j][new_i], True)
        
        return False
