import turtle
from trafficJam import UserInput

class _KeyInput:
    def __init__(self, maze_solver):
        self._maze_solver = maze_solver
        self.extra_feature = None
        self.setup_keys()

    def setup_keys(self):
        screen = self._maze_solver.screen
        screen.listen()

        screen.onkey(turtle.bye, 'q')
        screen.onkey(turtle.bye, 'Q')

        screen.onkey(self._maze_solver._move_up, "Up")
        screen.onkey(self._maze_solver._move_down, "Down")
        screen.onkey(self._maze_solver._move_left, "Left")
        screen.onkey(self._maze_solver._move_right, "Right")

        screen.onkey(self._maze_solver._calculate_and_display_path, "F")
        screen.onkey(self._maze_solver._calculate_and_display_path, "f")

        screen.onkey(self._maze_solver._start_following_path, "G")
        screen.onkey(self._maze_solver._start_following_path, "g")

        screen.onkey(self._maze_solver._toggle_pause, "P")
        screen.onkey(self._maze_solver._toggle_pause, "p")

        screen.onkey(self._maze_solver._clear_path, "C")
        screen.onkey(self._maze_solver._clear_path, "c")

        screen.onkey(self._maze_solver._toggle_path_drawing, "H")
        screen.onkey(self._maze_solver._toggle_path_drawing, "h")

        screen.onkey(self._maze_solver._reset, "R")
        screen.onkey(self._maze_solver._reset, "r")

        # Additional keys for continue/pause functionality
        screen.onkey(self._maze_solver._continue_manual, "C")
        screen.onkey(self._maze_solver._continue_manual, "c")
        
       # for individual part
        screen.onkey(self.call_extra_feature, 's')

    def call_extra_feature(self):
        screen = self._maze_solver.screen
        self.extra_feature = UserInput(screen) #call extra feature with current screen

