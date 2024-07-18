import turtle

class DrawBox:
    def __init__(self, box_size=30):
        self.box_size = box_size
        self.t = turtle.Turtle()
    
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
