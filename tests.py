import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols,)
        self.assertEqual(len(m1._cells[0]), num_rows,)

        # Test with a smaller maze
        m2 = Maze(0, 0, 5, 5, 10, 10)
        self.assertEqual(len(m2._cells), 5)
        self.assertEqual(len(m2._cells[0]), 5)

        # Test with a larger maze
        m3 = Maze(0, 0, 20, 15, 10, 10)
        self.assertEqual(len(m3._cells), 15)
        self.assertEqual(len(m3._cells[0]), 20)

    def test_break_entrance_and_exit(self):
        # Setup - create a maze with a few rows and columns
        num_rows = 3
        num_cols = 3
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        
        # Before breaking walls, check that entrance and exit have walls
        self.assertTrue(maze._cells[0][0].has_top_wall)
        self.assertTrue(maze._cells[num_cols-1][num_rows-1].has_bottom_wall)
        
        # Call the method we're testing
        maze._break_entrance_and_exit()
        
        # After breaking walls, check that entrance and exit don't have walls
        self.assertFalse(maze._cells[0][0].has_top_wall)
        self.assertFalse(maze._cells[num_cols-1][num_rows-1].has_bottom_wall)

if __name__ == "__main__":
    unittest.main()