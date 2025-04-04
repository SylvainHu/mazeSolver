from graphics import Window, Point, Line, Cell
from maze import Maze

def main():
    win = Window(800, 600)

    test_maze = Maze(50, 50, 10, 10, 40, 40, win)

    win.wait_for_close()



if __name__ == '__main__':
    main()
