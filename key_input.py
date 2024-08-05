import turtle

class KeyInput:
    def __init__(self, maze_solver):
        self.maze_solver = maze_solver
        self.setup_keys()

    def setup_keys(self):
        screen = self.maze_solver.screen
        screen.listen()

        screen.onkey(turtle.bye, 'q')
        screen.onkey(turtle.bye, 'Q')

        screen.onkey(self.maze_solver.move_up, "Up")
        screen.onkey(self.maze_solver.move_down, "Down")
        screen.onkey(self.maze_solver.move_left, "Left")
        screen.onkey(self.maze_solver.move_right, "Right")

        screen.onkey(self.maze_solver.calculate_and_display_path, "F")
        screen.onkey(self.maze_solver.calculate_and_display_path, "f")

        screen.onkey(self.maze_solver.start_following_path, "G")
        screen.onkey(self.maze_solver.start_following_path, "g")

        screen.onkey(self.maze_solver.toggle_pause, "P")
        screen.onkey(self.maze_solver.toggle_pause, "p")

        screen.onkey(self.maze_solver.clear_path, "C")
        screen.onkey(self.maze_solver.clear_path, "c")

        screen.onkey(self.maze_solver.toggle_path_drawing, "H")
        screen.onkey(self.maze_solver.toggle_path_drawing, "h")

        screen.onkey(self.maze_solver.reset, "R")
        screen.onkey(self.maze_solver.reset, "r")

        # Additional keys for continue/pause functionality
        screen.onkey(self.maze_solver.continue_manual, "C")
        screen.onkey(self.maze_solver.continue_manual, "c")

