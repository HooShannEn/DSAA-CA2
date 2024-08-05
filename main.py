import turtle
from filehandler import FileHandler
from MazeSimulator import MazeSimulator
from key_input import KeyInput

turtle.tracer(False)

# Create the maze list
maze_data = FileHandler().read_file(inpfilepath='./city.txt').split('\n')
print(maze_data)  

# Create the MazeSimulator object
maze_solver = MazeSimulator(maze_data)

# Draw the maze
maze_solver.draw_maze()

# Initialize KeyInput with the maze solver to manage key events
key_input = KeyInput(maze_solver)

# Keep the turtle window open
turtle.done()
