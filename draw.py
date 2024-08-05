import turtle

class Draw:
    def __init__(self, box_size=30):
        self.box_size = box_size
        self.t = turtle.Turtle()
        self.text_turtle = turtle.Turtle()  # Turtle for text
        self.text_turtle.hideturtle()
    
    def draw_letter(self, char, x, y):
        self.letter = turtle.Turtle()
        self.letter.penup()
        self.letter.goto(x, y)  # Starting position for 'e'
        self.letter.pendown()
        self.letter.write(char, font=("Arial", 16, "bold"))
        self.letter.hideturtle()

    def draw_circle(self, color, x, y, radius=None, fill=False, outline_thickness=3):
        # if radius is not provid (None), it calculates the radius based on box size.
        if radius is None:
            radius = self.box_size // 2 - 5

        # Draw circle outline
        self.letter.penup()
        self.letter.goto(x, y - radius)  # Adjusted position for the circle outline
        self.letter.pendown()
        self.letter.setheading(0)  # Ensure facing right
        self.letter.pensize(outline_thickness)
        self.letter.color(color)
        if fill:
            self.letter.begin_fill() #fill color for the path circle
        self.letter.circle(radius)  # Radius adjusted to fit around the letter
        if fill:
            self.letter.end_fill()#fill color for the path circle
        self.letter.hideturtle()

    def draw_box(self, x, y, color, letter=None):
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        self.t.begin_fill()
        self.t.fillcolor(color)
        for _ in range(4):
            self.t.forward(self.box_size)
            self.t.right(90)
        self.t.end_fill()
        if letter is not None:
            self.draw_letter(letter[0], x + self.box_size * 0.35, y - self.box_size * 0.85)
            circle_color = letter[1]
            self.draw_circle(circle_color, x + self.box_size * 0.5, y - self.box_size * 0.5, 12)
    
    def draw_maze(self, maze, color_map, x_offset, y_offset):
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                char = maze[y][x]
                color = color_map.get(char, 'white')
                if char in ['s', 'e']:
                    letter_color = '#3B79C3' if char == 'e' else '#28AD45'
                    self.draw_box(x * self.box_size - x_offset, (len(maze) - y) * self.box_size - y_offset, color, letter=[char, letter_color])
                else:
                    self.draw_box(x * self.box_size - x_offset, (len(maze) - y) * self.box_size - y_offset, color)

        self.t.hideturtle()
        turtle.update()
    
    def draw_shortest_path(self, path, box_size, x_offset, y_offset, maze_height):
        for x, y in path:
            # Draw black circle for outline
            self.draw_circle('black', x * box_size - x_offset + box_size / 2,
                             (maze_height - y - 1) * box_size - y_offset + box_size / 2,
                             radius=box_size // 2 - 4, fill=False, outline_thickness=3)
            # Draw yellow circle for inner color
            self.draw_circle('#FFFF00', x * box_size - x_offset + box_size / 2,
                             (maze_height - y - 1) * box_size - y_offset + box_size / 2,
                             fill=True, outline_thickness=0)
        turtle.update()
    
    def draw_text(self, text):
        self.text_turtle.clear()  # clean previous text
        self.text_turtle.penup()
        self.text_turtle.goto(0, 350)  # text position
        self.text_turtle.write("COFFEE~GO~DRONE: Done by Shann En & Zehua DAAA/2A/01", align="center", font=("Arial", 16, "bold"))
        self.text_turtle.goto(0, 320)
        self.text_turtle.write(text, align="center", font=("Arial", 12, "normal"))
        self.text_turtle.hideturtle()