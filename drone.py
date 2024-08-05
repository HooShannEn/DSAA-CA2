import turtle

class Drone:
    def __init__(self, box_size, start_pos, x_offset, y_offset, maze_height):
        self.box_size = box_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.maze_height = maze_height
        self.turtle = turtle.Turtle()
        self.turtle.fillcolor("red")
        self.turtle.setheading(90)
        self.turtle.penup()
        self.position = start_pos
        self.goto_position(start_pos)

    def goto_position(self, pos):
        x, y = pos
        # Correct the y-coordinate by subtracting from maze height
        corrected_y = self.maze_height - y
        self.turtle.goto(x * self.box_size - self.x_offset + (0.5 * self.box_size),
                         (corrected_y * self.box_size - (0.5 * self.box_size)) - self.y_offset)

    def move_to(self, pos):
        self.position = pos
        self.goto_position(pos)

    def set_heading(self, direction):
        headings = {'up': 90, 'down': 270, 'left': 180, 'right': 0}
        self.turtle.setheading(headings[direction])

    def update_position(self, direction):
        x, y = self.position
        move_map = {'up': (x, y - 1), 'down': (x, y + 1),
                    'left': (x - 1, y), 'right': (x + 1, y)}
        new_pos = move_map[direction]
        self.move_to(new_pos)

    def penup(self):
        self.turtle.penup()

    def pendown(self):
        self.turtle.pendown()
