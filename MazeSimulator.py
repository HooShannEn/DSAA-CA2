import turtle
from draw import _Draw
from drone import Drone
from maze import _Maze
from path_finder import _PathFinder

class MazeSimulator:
    def __init__(self, maze_data, box_size=30):
        self._maze = _Maze(maze_data)
        self._path_finder = _PathFinder(self._maze)
        self.box_size = box_size
        self._draw = _Draw(box_size)
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=800)
        #changed offset
        self.x_offset = (len(self._maze.grid[0]) *60 - len(self._maze.grid[0]) * box_size) / 2
        self.y_offset = (len(self._maze.grid) *60- len(self._maze.grid) * box_size) / 2

        self.color_map = {
            'X': '#C6C4C5',
            '.': 'white',
            's': '#84FD85',
            'e': '#7DFBFA'
        }
        
        start_pos = self._maze.get_start_position()
        self.drone = Drone(box_size, start_pos, self.x_offset, self.y_offset, len(self._maze.grid))


        self.following_path = False
        self.paused = False
        self.path_index = 0
        self.path_drawn = False
        self.path_cal = False
        self.count = 0

        # starting text
        self._draw.draw_text("DRONE STATUS = Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)")


    def _activate_continuekeys(self):
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self._continue_manual, "C")
        self.screen.onkey(self._continue_manual, "c")

    def _continue_manual(self):
        self.following_path = False
        self._activate_allkeys()
        self._clear_path()

    def _activate_allkeys(self):
        # Listen for key press to move drone
        self.screen.listen()
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self._move_up, "Up")
        self.screen.onkey(self._move_down, "Down")
        self.screen.onkey(self._move_left, "Left")
        self.screen.onkey(self._move_right, "Right")
        self.screen.onkey(self._calculate_and_display_path, "F")  # upper and lower case
        self.screen.onkey(self._calculate_and_display_path, "f")
        self.screen.onkey(self._start_following_path, "G")
        self.screen.onkey(self._start_following_path, "g")
        self.screen.onkey(self._toggle_pause, "P")
        self.screen.onkey(self._toggle_pause, "p")
        self.screen.onkey(self._clear_path, "C")
        self.screen.onkey(self._clear_path, "c")
        self.screen.onkey(self._toggle_path_drawing, "H")
        self.screen.onkey(self._toggle_path_drawing, "h")
        self.screen.onkey(self._reset, "R")
        self.screen.onkey(self._reset, "r")

    def _activate_pausedkeys(self):
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self._move_up, "Up")
        self.screen.onkey(self._move_down, "Down")
        self.screen.onkey(self._move_left, "Left")
        self.screen.onkey(self._move_right, "Right")
        self.screen.onkey(self._toggle_pause, "P")
        self.screen.onkey(self._toggle_pause, "p")
        self.screen.onkey(self._reset, "R")
        self.screen.onkey(self._reset, "r")

    def _deactivate_keys(self):
        self.screen.onkey(None, "Up")
        self.screen.onkey(None, "Down")
        self.screen.onkey(None, "Left")
        self.screen.onkey(None, "Right")
        self.screen.onkey(None, "F")  # upper and lower case
        self.screen.onkey(None, "f")
        self.screen.onkey(None, "C")
        self.screen.onkey(None, "c")
        self.screen.onkey(None, "H")
        self.screen.onkey(None, "h")
        self.screen.onkey(None, "R")
        self.screen.onkey(None, "r")

    def _recheck_path(self):
        if not self.paused:
            if self.path_cal and self.path_drawn:
                self._clear_path()
                self.count = 0
            if self.path_cal:
                self._clear_path()
            if self.path_drawn:
                self.count = 0
                self._clear_path()
                self._toggle_path_drawing()

    def _toggle_path_drawing(self):
        self.path_drawn = True
        if self.count % 2 == 0:
            self._draw_shortest_path()
        else:
            self._clear_path()
        self.count += 1

    def draw_maze(self):
        self._draw.draw_maze(self._maze.grid, self.color_map, self.x_offset, self.y_offset)

    def can_move(self, x, y):
        return self._maze.is_passable(x, y)

    def _move_up(self):
        x, y = self.drone.position
        if self.can_move(x, y - 1):
            self.drone.update_position('up')
            self.drone.set_heading('up')
            turtle.update()
            self._recheck_path()

    def _move_down(self):
        x, y = self.drone.position
        if self.can_move(x, y + 1):
            self.drone.update_position('down')
            self.drone.set_heading('down')
            turtle.update()
            self._recheck_path()

    def _move_left(self):
        x, y = self.drone.position
        if self.can_move(x - 1, y):
            self.drone.update_position('left')
            self.drone.set_heading('left')
            turtle.update()
            self._recheck_path()

    def _move_right(self):
        x, y = self.drone.position
        if self.can_move(x + 1, y):
            self.drone.update_position('right')
            self.drone.set_heading('right')
            turtle.update()
            self._recheck_path()

    def _bfs_shortest_path(self):
        return self._path_finder.bfs_shortest_path(self.drone.position)
    
    def _draw_shortest_path(self):
        self.shortest_path = self._bfs_shortest_path()

        if self.shortest_path:
            self._draw.draw_shortest_path(self.shortest_path, self.box_size, self.x_offset, self.y_offset, len(self._maze.grid))
        else:
            print("No path found!")


    def _calculate_and_display_path(self):
        self.path_cal = True
        self._draw_shortest_path()
        self._update_text("DRONE STATUS = Automatic Pilot: Press 'g' to follow pre-calculated path")

    def _start_following_path(self):
        if self.path_cal:
            self.path_index = 0
            self._update_text("DRONE STATUS = Automatic Pilot: Following pre-calculated path. Press 'p' to toggle pause/resume")
            self._deactivate_keys()
            self._follow_path()

    def _follow_path(self):
        if self.shortest_path and not self.paused:
            self.following_path = True
            if self.path_index < len(self.shortest_path):
                x, y = self.shortest_path[self.path_index]
                current_x, current_y = self.drone.position  # Use drone's current position

                # Determine the direction and set heading
                if x > current_x:
                    self.drone.set_heading('right')
                elif x < current_x:
                    self.drone.set_heading('left')
                elif y > current_y:
                    self.drone.set_heading('down')
                elif y < current_y:
                    self.drone.set_heading('up')

                self.drone.penup()  # Ensure the turtle doesn't leave a trail when moving
                # Move drone to the next position following the path
                self.drone.move_to((x, y))
                self.path_index += 1  # Move to the next step

                turtle.update()
                self.screen.ontimer(self._follow_path, 500)  # Move speed, each step takes 500 ms
            else:
                # Reached the end
                destination = self.shortest_path[-1]
                steps = len(self.shortest_path) - 1  # Initial point not counted
                dest_x, dest_y = destination[1], destination[0]  # Switch x and y, if not the destination is opposite
                self._update_text(f"DRONE STATUS = Automatic Pilot: Destination ({dest_x}, {dest_y}) reached in {steps} steps. Press 'c' to continue")
                self._activate_continuekeys()
        elif self.paused:
            self._activate_pausedkeys()
            self.screen.ontimer(self._follow_path, 100)  # Check every 100 ms if paused

    def _toggle_pause(self):
        if self.following_path:
            self.paused = not self.paused
            if self.paused:
                self._activate_pausedkeys()
                print("Paused")
            else:
                self._deactivate_keys()
                print("Resumed")

    def _clear_path(self):
        # same as def draw_shortest_path()
        # if path exist
        # loop the box position in path
        # redraw everything (self._draw)
        # if position is s or e, clear
        # else if position not s and e, clear the rest of the path
        # aft redraw the box, update screen, it will clear all the path
        if hasattr(self, 'shortest_path') and self.shortest_path:
            for x, y in self.shortest_path:
                if self._maze.grid[y][x] == 's' or self._maze.grid[y][x] == 'e':
                    self._draw.draw_box(x * self.box_size - self.x_offset, 
                                       (len(self._maze.grid) - y) * self.box_size - self.y_offset, 
                                       self.color_map[self._maze.grid[y][x]], letter=[self._maze.grid[y][x], '#3B79C3' if self._maze.grid[y][x] == 'e' else '#28AD45'])
                else:
                    self._draw.draw_box(x * self.box_size - self.x_offset, 
                                       (len(self._maze.grid) - y) * self.box_size - self.y_offset, 
                                       self.color_map[self._maze.grid[y][x]])
            turtle.update()
        self.path_drawn = False
        self.path_cal = False
        self._update_text("DRONE STATUS = Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)")

    def _draw_text(self, text):
        self._text_turtle.clear()  # clean previous text
        self._text_turtle.penup()
        self._text_turtle.goto(0, 350)  # text position
        self._text_turtle.write("COFFEE~GO~DRONE: Done by Shann En & Zehua DAAA/2A/01", align="center", font=("Arial", 16, "bold"))
        self._text_turtle.goto(0, 320)
        self._text_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self._text_turtle.hideturtle()

    def _update_text(self, text):
        self._draw.draw_text(text)

    def _reset(self):
        self.drone.move_to(self._maze.get_start_position())
        self.drone.set_heading('up')
        turtle.update()

