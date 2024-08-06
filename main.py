######  uncomment to test normal maze  #######


# import turtle
# from filehandler import FileHandler
# from MazeSimulator import MazeSimulator
# from key_input import _KeyInput
# from employeeSecure import EmployeeSecure

# turtle.tracer(False)


# maze_data = FileHandler().check_maze_dimensions('./city2.txt')

# if maze_data:
#     # Proceed with loading or using the maze data
#     print('Maze dimensions are valid.')
#     # Create the MazeSimulator object
#     maze_solver = MazeSimulator(maze_data)

#     # Draw the maze
#     maze_solver.draw_maze()

#     # Initialize KeyInput with the maze solver to manage key events
#     key_input = _KeyInput(maze_solver)

#     # Keep the turtle window open
#     turtle.done()

# else:
#     print('Maze dimensions are invalid.')





# ZehuaTest

# def start_maze_simulation():
#     maze_data = FileHandler().check_maze_dimensions('./city2.txt')

#     if maze_data:
#         # Proceed with loading or using the maze data
#         print('Maze dimensions are valid.')
#         # Create the MazeSimulator object
#         maze_solver = MazeSimulator(maze_data)

#         # Draw the maze
#         maze_solver.draw_maze()

#         # Initialize KeyInput with the maze solver to manage key events
#         key_input = _KeyInput(maze_solver)

#         # Keep the turtle window open
#         turtle.done()
#     else:
#         print('Maze dimensions are invalid.')

# # Initialize the EmployeeSecure class and start the login/register process
# employee_secure = EmployeeSecure()

# def main_start():
#     # Start the employee secure process first
#     employee_secure.start()
#     # After successful login, start the maze simulation
#     if employee_secure.logged_in:
#         start_maze_simulation()

# # Run the program
# if __name__ == "__main__":
#     main_start()

import sys
import turtle
from filehandler import FileHandler
from MazeSimulator import MazeSimulator
from key_input import _KeyInput
from employeeSecure import EmployeeSecure

def start_maze_simulation(maze_file):
    maze_data = FileHandler().check_maze_dimensions(maze_file)

    if maze_data:
        print('Maze dimensions are valid.')
        maze_solver = MazeSimulator(maze_data)
        maze_solver.draw_maze()
        key_input = _KeyInput(maze_solver)
        turtle.done()
    else:
        print('Maze dimensions are invalid.')

def main():
    employee_secure = EmployeeSecure()
    employee_secure.start()

    # Once logged in, proceed to start the maze simulation
    if employee_secure.logged_in:
        # Check if a maze file is provided as a command-line argument
        if len(sys.argv) > 1:
            maze_file = sys.argv[1]
        else:
            maze_file = './city.txt'  # Default maze file

        start_maze_simulation(maze_file)

# Run the program
if __name__ == "__main__":
    main()
