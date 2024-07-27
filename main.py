import turtle
from filehandler import FileHandler
from maze_algo import MazeAlgo
turtle.tracer(False)

# Create the maze list
maze = FileHandler().read_file(inpfilepath='./city2.txt').split('\n')
print(maze)  # Create the MazeAlgo object
maze_solver = MazeAlgo(maze)

maze_solver.drawMaze()
maze_solver.activate_allkeys()

# Keep the turtle window open
turtle.done()
