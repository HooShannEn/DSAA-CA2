import turtle
from collections import deque
from draw_box import DrawBox


class MazeAlgo:
    def __init__(self, maze, box_size=30):
        self.maze = maze
        self.box_size = box_size
        self.draw_box = DrawBox(box_size)
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=800)
        self.x_offset = (800 - len(maze[0]) * box_size) / 3
        self.y_offset = (800 - len(maze) * box_size) / 6
        
        self.color_map = {
            'X': '#C6C4C5',
            '.': 'white',
            's': '#84FD85',
            'e': '#7DFBFA'
            ##30B34B
        }
        
        self.drone = turtle.Turtle()
        self.drone.fillcolor("red")
        self.drone.setheading(90)
        self.drone_pos = self.find_drone_start()
        
        self.following_path=False
        self.paused = False
        self.path_index = 0
        self.path_drawn=False
        self.path_cal=False
        self.count=0
        self.text_turtle = turtle.Turtle()  # turtle for text
        self.text_turtle.hideturtle()
        # starting text
        self.draw_text("DRONE STATUS = Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)")
    def activate_continuekeys(self):
       self.screen.onkey(turtle.bye, 'q')
       self.screen.onkey(turtle.bye, 'Q')
       self.screen.onkey(self.continue_manual, "C")
       self.screen.onkey(self.continue_manual, "c")
    def continue_manual(self):
        self.following_path=False
        self.activate_allkeys()
        self.clear_path()
    def activate_allkeys(self):
         #listen for key press to move drone
        self.screen.listen()
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self.move_up, "Up")
        self.screen.onkey(self.move_down, "Down")
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")
        self.screen.onkey(self.calculate_and_display_path, "F") #upper and lower case
        self.screen.onkey(self.calculate_and_display_path, "f")
        self.screen.onkey(self.start_following_path, "G")
        self.screen.onkey(self.start_following_path, "g")
        self.screen.onkey(self.toggle_pause, "P")
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.onkey(self.clear_path, "C")
        self.screen.onkey(self.clear_path, "c")
        self.screen.onkey(self.toggle_path_drawing, "H")
        self.screen.onkey(self.toggle_path_drawing, "h")
        self.screen.onkey(self.reset, "R")
        self.screen.onkey(self.reset, "r")
    def activate_pausedkeys(self):
        self.screen.onkey(turtle.bye, 'q')
        self.screen.onkey(turtle.bye, 'Q')
        self.screen.onkey(self.move_up, "Up")
        self.screen.onkey(self.move_down, "Down")
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")
        self.screen.onkey(self.toggle_pause, "P")
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.onkey(self.reset, "R")
        self.screen.onkey(self.reset, "r")
        
    def deactivate_keys(self):
        self.screen.onkey(None, "Up")
        self.screen.onkey(None, "Down")
        self.screen.onkey(None, "Left")
        self.screen.onkey(None, "Right")
        self.screen.onkey(None, "F") #upper and lower case
        self.screen.onkey(None, "f")
        self.screen.onkey(None, "C")
        self.screen.onkey(None, "c")
        self.screen.onkey(None, "H")
        self.screen.onkey(None, "h")
        self.screen.onkey(None, "R")
        self.screen.onkey(None, "r")
    def recheck_path(self):
        if not self.paused:
            if self.path_cal and self.path_drawn:
                self.clear_path()
                self.count=0
            if self.path_cal:
                self.clear_path()
            if self.path_drawn:
                self.count=0
                self.clear_path()
                self.toggle_path_drawing()
       
    def toggle_path_drawing(self):
        self.path_drawn=True
        if self.count % 2 == 0:
            self.draw_shortest_path()
        else:
            self.clear_path()
        self.count += 1

    def find_drone_start(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 's':
                    self.drone.goto(x * self.box_size - self.x_offset + (0.5 * self.box_size), (len(self.maze) - y) * self.box_size - (0.5 * self.box_size) - self.y_offset)
                    return (x, y)
        return (0, 0)

    def drawMaze(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                char = self.maze[y][x]
                color = self.color_map.get(char)
                if char == 'e':
                    # self.draw_box is refer to the DrawBox class.
                    # self.draw_box.draw_box is calling the draw_box method of the DrawBox class
                    self.draw_box.draw_box(x * self.box_size - self.x_offset, (len(self.maze) - y) * self.box_size - self.y_offset, color, letter=[char, '#3B79C3'])
                elif char == 's':
                    self.draw_box.draw_box(x * self.box_size - self.x_offset, (len(self.maze) - y) * self.box_size - self.y_offset, color, letter=[char, '#28AD45'])
                else:
                    self.draw_box.draw_box(x * self.box_size - self.x_offset, (len(self.maze) - y) * self.box_size - self.y_offset, color)

        self.draw_box.t.hideturtle() # just hide the arrow that use to draw box
        turtle.update() # after the drawing, refresh screen to update the newest drawing 

    def can_move(self, x, y):
        if x < 0 or x >= len(self.maze[0]) or y < 0 or y >= len(self.maze):
            return False
        return self.maze[y][x] not in ['X']

    def move_up(self):
        x, y = self.drone_pos
        if self.can_move(x, y - 1):
            self.drone_pos = (x, y - 1)
            self.drone.setheading(90)
            self.drone.sety(self.drone.ycor() + self.box_size)
            turtle.update()
            self.recheck_path()

    def move_down(self):
        x, y = self.drone_pos
        if self.can_move(x, y + 1):
            self.drone_pos = (x, y + 1)
            self.drone.setheading(270)
            self.drone.sety(self.drone.ycor() - self.box_size)
            turtle.update()
            self.recheck_path()

    def move_left(self):
        x, y = self.drone_pos
        if self.can_move(x - 1, y):
            self.drone_pos = (x - 1, y)
            self.drone.setheading(180)
            self.drone.setx(self.drone.xcor() - self.box_size)
            turtle.update()
            self.recheck_path()

    def move_right(self):
        x, y = self.drone_pos
        if self.can_move(x + 1, y):
            self.drone_pos = (x + 1, y)
            self.drone.setheading(0)
            self.drone.setx(self.drone.xcor() + self.box_size)
            turtle.update()
            self.recheck_path()

    def bfs_shortest_path(self):
        start_x, start_y = self.drone_pos # get current position
        queue = deque([(start_x, start_y)])
        visited = set([(start_x, start_y)]) # set to keep track of visited positions
        parent = {} # store parent-child for path reconstruction

        while queue:
            x, y = queue.popleft() # # dequeue the current position

            if self.maze[y][x] == 'e': # if the current position is the end position 'e'
                # found the end position, reconstruct the path
                path = []
                while (x, y) != (start_x, start_y):
                    path.append((x, y))
                    x, y = parent[(x, y)] # use previouse parent dictionary to reconstruct the path
                path.append((start_x, start_y))
                path.reverse() # reverse the path to get it from start to end
                return path

            # explore the map (up, down, left, right)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                # if boxs not visited and able to move to the position
                if (nx, ny) not in visited and self.can_move(nx, ny):
                    visited.add((nx, ny)) # mark the postion visited
                    queue.append((nx, ny))
                    parent[(nx, ny)] = (x, y) #set current position as parent

        # if no path found
        return None

    def draw_shortest_path(self):
        self.shortest_path = self.bfs_shortest_path() # use Breadth First Search algorithm to find the shortest way

        if self.shortest_path: # if shortest path is found 
            for x, y in self.shortest_path: #each box position in the path
                # draw black circle for outline
                self.draw_box.draw_circle('black', x * self.box_size - self.x_offset + self.box_size / 2, 
                                          (len(self.maze) - y) * self.box_size - self.y_offset - self.box_size / 2, 
                                          radius=self.box_size // 2 - 4, fill=False, outline_thickness=3)
                # draw yellow circle for inner color
                self.draw_box.draw_circle('#FFFF00', x * self.box_size - self.x_offset + self.box_size / 2, 
                                          (len(self.maze) - y) * self.box_size - self.y_offset - self.box_size / 2, 
                                          fill=True, outline_thickness=0)
            turtle.update()
        else:
            print("No path found!")

    def calculate_and_display_path(self):
        self.path_cal = True
        self.draw_shortest_path()
        self.update_text("DRONE STATUS = Automatic Pilot: Press 'g' to follow pre-calculated path")

    def start_following_path(self):
        if self.path_cal:
            self.path_index = 0 # reset the path index as begining
            self.update_text("DRONE STATUS = Automatic Pilot: Following pre-calculated path. Press 'p' to toggle pause/resume")
            self.deactivate_keys()
            self.follow_path()

    def follow_path(self):
        if self.shortest_path and not self.paused:
            self.following_path = True
            if self.path_index < len(self.shortest_path):
                x, y = self.shortest_path[self.path_index]
                current_x, current_y = self.drone_pos

                # 4 directions
                if x > current_x:
                    self.drone.setheading(0)  # R
                elif x < current_x:
                    self.drone.setheading(180)  # L
                elif y > current_y:
                    self.drone.setheading(270)  # D
                elif y < current_y:
                    self.drone.setheading(90)  # U


                self.drone.penup() #need pen up here so when move the drone no trail behind it
                # move drone to the next position follow the path
                self.drone.goto(x * self.box_size - self.x_offset + (0.5 * self.box_size), 
                                (len(self.maze) - y) * self.box_size - (0.5 * self.box_size) - self.y_offset)
                self.drone_pos = (x, y) #update drone current position
                self.path_index += 1 # add 1 to the path index to move to the next step

                turtle.update()
                self.screen.ontimer(self.follow_path, 500)  # moving speed, each step take 500 ms to move
            else:
                # reached the end
                destination = self.shortest_path[-1]
                steps = len(self.shortest_path) - 1  # initial point not counted
                dest_x, dest_y = destination[1], destination[0]  # switch x and y, if not the destination is opposite
                self.update_text(f"DRONE STATUS = Automatic Pilot: Destination ({dest_x}, {dest_y}) reached in {steps} steps. Press 'c' to continue")
                self.activate_continuekeys()
        elif self.paused:
            self.activate_pausedkeys()
            self.screen.ontimer(self.follow_path, 100)  # check every 100 ms if paused

    def toggle_pause(self):
        if self.following_path:
            self.paused = not self.paused
            if self.paused:
                self.activate_pausedkeys()
                print("Paused")
            else:
                self.deactivate_keys()
                print("Resumed")

    def clear_path(self):
         # same as def draw_shortest_path()
         #if path exist
         #loop the box position in path
         #redraw everything (self.draw_box)
         #if position is s or e, clear
         #else if position not s and e, clear the rest of the path
         #aft redraw the box, update screen, it will clear all the path
        if hasattr(self, 'shortest_path') and self.shortest_path:
            for x, y in self.shortest_path:
                if self.maze[y][x] == 's' or self.maze[y][x] == 'e':
                    self.draw_box.draw_box(x * self.box_size - self.x_offset, 
                                           (len(self.maze) - y) * self.box_size - self.y_offset, 
                                           self.color_map[self.maze[y][x]], letter=[self.maze[y][x], '#3B79C3' if self.maze[y][x] == 'e' else '#28AD45'])
                else:
                    self.draw_box.draw_box(x * self.box_size - self.x_offset, 
                                           (len(self.maze) - y) * self.box_size - self.y_offset, 
                                           self.color_map[self.maze[y][x]])
            turtle.update()
        self.path_drawn=False
        self.path_cal=False
        self.update_text("DRONE STATUS = Manual Mode: Use arrow keys to navigate (press 'f' to calculate shortest path)")

    def draw_text(self, text):
        self.text_turtle.clear() #clean previous text
        self.text_turtle.penup()
        self.text_turtle.goto(0, 350)  # text position
        self.text_turtle.write("COFFEE~GO~DRONE: Done by Shann En & Zehua DAAA/2A/01", align="center", font=("Arial", 16, "bold"))
        self.text_turtle.goto(0, 320)
        self.text_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self.text_turtle.hideturtle()

    def update_text(self, text):
        self.draw_text(text)

    def reset(self):
        x,y = self.find_drone_start()
        self.drone_pos = x,y
        self.drone.setheading(90)
        turtle.update() 