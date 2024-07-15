import turtle
from filehandler import FileHandler
turtle.tracer(False)
class mazeAlgo:
    def __init__(self, maze, box_size=30):
        self.maze = maze
        self.files = FileHandler()
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=800)
        self.x_offset = (800 - len(maze[0]) * box_size)/3
        self.y_offset = (800 - len(maze) * box_size) /6
        
        self.box_size = box_size
        self.t = turtle.Turtle()
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
        
        #listen for key press to move drone
        self.screen.listen()
        self.screen.onkey(self.move_up, "Up")
        self.screen.onkey(self.move_down, "Down")
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")
    

    def find_drone_start(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 's':
                    self.drone.goto(x * self.box_size -self.x_offset +(0.5*self.box_size),  (len(self.maze)-y)* self.box_size -(0.5*self.box_size)  - self.y_offset )
                    return (x, y)
        return (0, 0)
    def draw_letter(self,char,x,y):
        self.letter.penup()
        self.letter.width(60)

        self.letter.goto(x,y)   # Starting position for 'e'
        self.letter.pendown()
        self.letter.write(char,font=("Arial", 16, "bold"))
        
        
    def draw_circle(self,color,x,y):
    
        # Draw circle outline
        self.letter.penup()
        self.letter.goto(x, y)  # Adjusted position for the circle outline
        self.letter.pendown()
        self.letter.setheading(0)  # Ensure facing right
        self.letter.pensize(3)
        self.letter.color(color)
        self.letter.circle(12)  # Radius adjusted to fit around the letter
        self.letter.hideturtle()

    def drawBox(self, x, y, color, letter=None):
        self.t.penup()
        self.t.goto(x , y )
        self.t.pendown()
        self.t.begin_fill()
        self.t.fillcolor(color)
        for _ in range(4):
            self.t.forward(self.box_size)
            self.t.right(90)
        self.t.end_fill()
        if letter != None:
            self.letter = turtle.Turtle()
            self.draw_letter(letter[0],x+self.box_size*0.35,y-self.box_size*0.85)
            circle_color = letter[1]
            
            self.draw_circle(circle_color,x+self.box_size*0.5,y-self.box_size*0.9)

    def drawMaze(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                char = self.maze[y][x]
                color = self.color_map.get(char)
                if char == 'e':
                     self.drawBox(x * self.box_size -self.x_offset, (len(self.maze)-y) * self.box_size - self.y_offset, color,letter=[char,'#3B79C3'])
                elif char == 's':
                    self.drawBox(x * self.box_size -self.x_offset, (len(self.maze)-y) * self.box_size - self.y_offset, color,letter=[char,'#28AD45'])
                else:
                    self.drawBox(x * self.box_size -self.x_offset, (len(self.maze)-y) * self.box_size - self.y_offset, color)
                    
                     

        self.t.hideturtle()
        turtle.update()

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

    def move_down(self):
        x, y = self.drone_pos
        if self.can_move(x, y + 1):
            self.drone_pos = (x, y + 1)
            self.drone.setheading(270)
            self.drone.sety(self.drone.ycor() - self.box_size)
            turtle.update()

    def move_left(self):
        x, y = self.drone_pos
        if self.can_move(x -1,y):
            self.drone_pos = (x - 1, y)
            self.drone.setheading(180)
            self.drone.setx(self.drone.xcor() - self.box_size)
            turtle.update()

    def move_right(self):
        x, y = self.drone_pos
        if self.can_move(x + 1, y):
            self.drone_pos = (x + 1, y)
            self.drone.setheading(0)
            self.drone.setx(self.drone.xcor() + self.box_size)
            turtle.update()

# Create the maze list
maze = FileHandler().read_file(inpfilepath='./city.txt').split('\n')
print(maze)# Create the mazeAlgo object
maze_solver = mazeAlgo(maze)
maze_solver.drawMaze()

# Keep the turtle window open
turtle.done()
