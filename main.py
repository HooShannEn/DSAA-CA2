import turtle
from filehandler import FileHandler
from maze_algo import MazeAlgo
turtle.tracer(False)

# Create the maze list
maze = FileHandler().read_file(inpfilepath='./city.txt').split('\n')
print(maze)  # Create the MazeAlgo object
maze_solver = MazeAlgo(maze)

maze_solver.drawMaze()

# Keep the turtle window open
turtle.done()
