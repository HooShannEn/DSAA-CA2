import turtle
from filehandler import FileHandler
from MazeSimulator import MazeSimulator
from key_input import _KeyInput

turtle.tracer(False)

maze_data = FileHandler().check_maze_dimensions('./city.txt')

if maze_data:
    # Proceed with loading or using the maze data
    print('Maze dimensions are valid.')
    # Create the MazeSimulator object
    maze_solver = MazeSimulator(maze_data)

    # Draw the maze
    maze_solver.draw_maze()

    # Initialize KeyInput with the maze solver to manage key events
    key_input = _KeyInput(maze_solver)

    # Keep the turtle window open
    turtle.done()

else:
    print('Maze dimensions are invalid.')

