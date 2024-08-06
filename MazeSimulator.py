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
        #changed offset up to triple
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

        # zehua
        # Initialize battery level
        self.battery_level = 100
        # Create separate turtle objects for status and battery text
        self.status_turtle = turtle.Turtle()
        self.status_turtle.hideturtle()
        self.status_turtle.penup()
        self.status_turtle.goto(0, 350)
        self.battery_turtle = turtle.Turtle()
        self.battery_turtle.hideturtle()
        self.battery_turtle.penup()
        self.battery_turtle.goto(0, 300)
        start_pos = self._maze.get_start_position()
        self.start_pos = start_pos


        # starting text
        self._draw.draw_text("DRONE STATUS = Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)")
        # zehua
        self._draw_battery_status()

    # zehua
    def _draw_battery_status(self, reached_return_point=False):
        self.battery_turtle.clear()
        self.battery_turtle.goto(0, 300)  # Position for battery status
        battery_text = f"Battery: {self.battery_level}%"
        if self.battery_level == 0:
            current_x, current_y = self.drone.position
            battery_text = f"Battery: 0% - Position ({current_x}, {current_y}) - Press 'r' to restart"
        elif reached_return_point:
            battery_text += " - Press 'r' to reset drone battery"
        elif self.battery_level < 30:
            battery_text += " - Low Battery! Returning to Start..."
        self.battery_turtle.write(battery_text, align="center", font=("Arial", 12, "normal"))

    def _draw_status_text(self, text):
        self.status_turtle.clear()  # Clear only the status text
        self.status_turtle.goto(0, 350)  # Position for status text
        self.status_turtle.write(text, align="center", font=("Arial", 12, "normal"))

    def _update_battery(self):
        self.battery_level = max(0, self.battery_level - 1)
        self._draw_battery_status()
        # Only trigger the return if not already returning and battery is low
        if self.battery_level < 30 and not self.following_path:
            self._return_to_start()
        elif self.battery_level == 0:
            self._activate_reset_key  # Freeze all keys except reset battery
            self.following_path = False  # Stop any automatic movement


    def _activate_continuekeys(self):
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self._continue_manual, "C")
        self.screen.onkey(self._continue_manual, "c")

    def _continue_manual(self):
        self.following_path = False
        self._activate_allkeys()
        self._clear_path()
        # zehua
        self._draw_battery_status()  # Redraw battery status to ensure it's visible

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

    def _activate_reset_key(self):
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self._reset, "R")
        self.screen.onkey(self._reset, "r")


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
            self._update_battery()  # zehua: Decrease battery level
            self._recheck_path()

            # Check battery level and initiate return to start if necessary
            if self.battery_level < 30:
                self._return_to_start()

    def _move_down(self):
        x, y = self.drone.position
        if self.can_move(x, y + 1):
            self.drone.update_position('down')
            self.drone.set_heading('down')
            turtle.update()
            self._update_battery()  # zehua: Decrease battery level
            self._recheck_path()
            # Check battery level and initiate return to start if necessary
            if self.battery_level < 30:
                self._return_to_start()

    def _move_left(self):
        x, y = self.drone.position
        if self.can_move(x - 1, y):
            self.drone.update_position('left')
            self.drone.set_heading('left')
            turtle.update()
            self._update_battery()  # zehua: Decrease battery level
            self._recheck_path()
            # Check battery level and initiate return to start if necessary
            if self.battery_level < 30:
                self._return_to_start()

    def _move_right(self):
        x, y = self.drone.position
        if self.can_move(x + 1, y):
            self.drone.update_position('right')
            self.drone.set_heading('right')
            turtle.update()
            self._update_battery()  # zehua: Decrease battery level
            self._recheck_path()
            # Check battery level and initiate return to start if necessary
            if self.battery_level < 30:
                self._return_to_start()

    def _bfs_shortest_path(self):
        return self._path_finder.bfs_shortest_path(self.drone.position)
    
    def _draw_shortest_path(self):
        self.shortest_path = self._bfs_shortest_path()

        if self.shortest_path:
            self._draw.draw_shortest_path(self.shortest_path, self.box_size, self.x_offset, self.y_offset, len(self._maze.grid))
        else:
            print("No path found!")

    # zehua
    def _return_to_start(self):
        # if not self.following_path:  # Ensure this is only triggered once
            # print("AAAAAAA")
            # Use the modified pathfinder to find the path back to the start position
            self._clear_path()
            self.shortest_path = self._path_finder.bfs_shortest_path(self.drone.position, self.start_pos)
            if self.shortest_path:
                self._deactivate_keys()  # Prevent user input during return
                self.following_path = True
                self.paused = False  # Make sure the drone is not paused
                self._path_index = 0
                self._follow_return_path()



    def _follow_return_path(self):
        if self.following_path and self._path_index < len(self.shortest_path):
            x, y = self.shortest_path[self._path_index]
            current_x, current_y = self.drone.position

            if x > current_x:
                self.drone.set_heading('right')
            elif x < current_x:
                self.drone.set_heading('left')
            elif y > current_y:
                self.drone.set_heading('down')
            elif y < current_y:
                self.drone.set_heading('up')

            self.drone.penup()
            self.drone.move_to((x, y))
            self._path_index += 1
            self._update_battery()  # Decrease battery level
            turtle.update()
            self.screen.ontimer(self._follow_return_path, 500)
        else:
            self.following_path = False
            # self._activate_continuekeys()
            self._activate_reset_key()
            self._draw_battery_status(reached_return_point=True)


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
            if self.battery_level < 30: 
                self._return_to_start()
                return
            self.following_path = True

            # Interrupt path following if battery is low
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
                self._update_battery() # zehua: Decrease battery level

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
        self.status_turtle.clear()  # Clean previous text
        self.status_turtle.penup()
        self.status_turtle.goto(0, 350)  # Text position
        self.status_turtle.write("COFFEE~GO~DRONE: Done by Shann En & Zehua DAAA/2A/01", align="center", font=("Arial", 16, "bold"))
        self.status_turtle.goto(0, 320)
        self.status_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self.status_turtle.hideturtle()


    def _update_text(self, text):
        self._draw.draw_text(text)

    def _reset(self):
        self.drone.move_to(self._maze.get_start_position())
        self.drone.set_heading('up')
        self.battery_level = 100  # Reset battery level
        self._draw_battery_status()  # Update battery status display
        self._activate_allkeys()  # Reactivate all keys
        turtle.update()

