import random
import turtle
import time
import tkinter as tk
from tkinter import messagebox
import yagmail#module to send emails
import subprocess

class EmailNotification:
    def __init__(self, email_user, email_password):
        self.yag = yagmail.SMTP(email_user, email_password)

    def send_email(self, recipient, subject, body):
        self.yag.send(
            to=recipient,
            subject=subject,
            contents=body
        )

#notify user via email and close turtle screen
def notify_user(name, email, total_time, num_orders):
    email_user = 'hoo.shannen@gmail.com'  #email address
    email_password = 'kqhl mwdv haip cgof'  #user app pass created in google
    subject = "Coffee Delivery Completion Notification"
    body = (f"Dear {name},\n\n"
            f"Time taken to Complete Delivery: {total_time:.2f} seconds\n"
            f"Number of Coffee(s) Delivered: {num_orders}\n\n"
            "Best regards,\n"
            "Coffee~Go~Drone")
    email_notifier = EmailNotification(email_user, email_password)
    email_notifier.send_email(email, subject, body)

class _Draw:
    def __init__(self, box_size=40):
        self.box_size = box_size
        self.t = turtle.Turtle()
        self.t.hideturtle()
    
    def draw_box(self, x, y, color):
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        self.t.color('black', color)
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(self.box_size)
            self.t.right(90)
        self.t.end_fill()


class cityGame:
    def __init__(self, cityw, cityh, num_drone, num_aero, drone_len, aero_len, email, user):
        self.cityw = cityw
        self.cityh = cityh
        self.num_aero = num_aero
        self.num_drone = num_drone
        self.drone_len = drone_len
        self.aero_len = aero_len
        self.vehicle = {}
        self.visited_pos = []
        self.pieces = []
        self.level = 1
        self.count_goal = 0
        self.time_limit = 40#40 seconds
        self.draw = _Draw()
        self.color_map = {
            'a': 'blue',
            'd': 'red',
            '.': 'white',
            'G': 'yellow'
        }
        self.distance = 2
        self.box_size = 40 #size of each cell in the maze
        self.emp_name = user
        self.emp_email = email
        
    
    #generating city
    def check_hori_emp(self, city, randomx, randomy, piece):
        if randomx + piece > self.cityw:
            return False
        return all(city[randomy][randomx + i] == '.' for i in range(piece))

    def check_vert_emp(self, city, randomx, randomy, piece):
        if randomy + piece > self.cityh:
            return False
        return all(city[randomy + i][randomx] == '.' for i in range(piece))


    def place_vert(self, city, randomx, randomy, chosen_piece, chosen_name):
        for i in range(randomy, randomy + chosen_piece):
            city[i][randomx] = chosen_name
        self.vehicle[chosen_name] = ((randomy, randomx), (randomy + chosen_piece - 1, randomx), chosen_piece, 'V')
        self.pieces.remove(chosen_piece)
        self.piece_name.remove(chosen_name)
        self.visited_pos.append((randomx, randomy))
        return city

    def place_hori(self, city, randomx, randomy, chosen_piece, chosen_name):
        for i in range(randomx, randomx + chosen_piece):
            city[randomy][i] = chosen_name
        
        self.vehicle[chosen_name] = ((randomy, randomx), (randomy, randomx + chosen_piece - 1), chosen_piece, 'H')
        self.pieces.remove(chosen_piece)
        self.piece_name.remove(chosen_name)
        self.visited_pos.append((randomx, randomy))
        return city
    
    def get_random_pos(self):
        x_random = random.randint(0, self.cityw -1)
        y_random = random.randint(0, self.cityh -1)
        return x_random, y_random

    def randomcity(self):
        self.city = [list('.'*self.cityw) for _ in range(self.cityh)]
        self.visited_pos = []
        self.piece_name = []
        self.pieces = []
        for i in range(self.num_drone):
            self.piece_name.append('d' + str(i))
            self.pieces.append(self.drone_len)
        for d in range(self.num_aero):
            self.piece_name.append('a' + str(d))
            self.pieces.append(self.aero_len)
        
        while self.pieces and len(self.visited_pos) < self.cityw * self.cityh:  #if pieces not placed finished or checked all possible pos
            chosen_index = random.randint(0, len(self.pieces) - 1)
            chosen_piece = self.pieces[chosen_index]
            chosen_name = self.piece_name[chosen_index]
            random_pos = self.get_random_pos() #get random position on the board
            randomx, randomy = random_pos
            if (randomx, randomy) not in self.visited_pos:  # if not already checked
                random_hv = self.random_align()
                try: #need check not out of range
                    if random_hv:#if horizontal
                        if self.check_hori_emp(self.city, randomx, randomy, chosen_piece):  # if horizontal empty
                            self.city = self.place_hori(self.city, randomx, randomy, chosen_piece, chosen_name)
                        else:
                            self.visited_pos.append((randomx, randomy))
                    else: #if vertical
                        if self.check_vert_emp(self.city, randomx, randomy, chosen_piece):  # if vertical empty
                            self.city = self.place_vert(self.city, randomx, randomy, chosen_piece, chosen_name)
                        else:
                            self.visited_pos.append((randomx, randomy))

                except IndexError:#if index error
                    self.visited_pos.append((randomx, randomy))
        self.x_offset = ((self.cityw*120) -self.cityw * self.box_size) / 3
        self.y_offset = ((self.cityh*110) - self.cityh * self.box_size) / 3
        print('city generated:', self.city)
        if self.count_goal == 0:#record time started only at 0 orders (first city map generated)
            self.time_started = time.time()
        self.auto_mode = False#set auto to false first
        self.countA = 0
        self.start_game()#start game

    #draw city board with city generated
    def drawMaze(self):
        if not self.auto_mode:
            turtle.tracer(0, 0)#turn animation off
        for y in range(len(self.city)):
            for x in range(len(self.city[y])):
                char = self.city[y][x]
                color = self.color_map.get(char[0], 'white')
                self.draw.draw_box(x * self.box_size - self.x_offset, (len(self.city) - y) * self.box_size - self.y_offset, color)
        self.draw_outline()
        self.draw_goal_box(self.goal_pos[1],self.goal_pos[0])
        self.veh_name = list(self.vehicle.keys())[self.cveh]
        turtle.update() #update screen with the newest drawing
        turtle.hideturtle()
    #colliding with other drones
    def check_collide(self, drone, direction):
        try:
            (start_pos, end_pos, length_veh, orientation) = self.vehicle[drone]
            y2, x2 = end_pos
            if direction == 'down':
                collide_y, collide_x = y2 + 1, x2
            elif direction == 'up':
                collide_y, collide_x = start_pos[0] - 1, x2
            elif direction == 'left':
                collide_y, collide_x = y2, start_pos[1] - 1
            elif direction == 'right':
                collide_y, collide_x = y2, end_pos[1] + 1
            if self.city[collide_y][collide_x] != '.':
                bumped_drone = self.city[collide_y][collide_x]
                print(f"{drone} is interefering with {bumped_drone}, controlling {bumped_drone} now!")
                self.veh_name = bumped_drone
                self.cveh = list(self.vehicle.keys()).index(bumped_drone)
                self.goal_pos = self.get_goal_pos()
                if not self.auto_mode:#only if manual mode the check for switch keys
                    self.check_switch_keys()
                return bumped_drone#change to this drone after this
        except IndexError:
            print('out of maze')
    
    def remove_car(self):#remove car from board when win
        (start_pos, end_pos, length_veh, orientation) = list(self.vehicle.values())[self.cveh]  # get current car details
        y2, x2 = end_pos
        y1, x1 = start_pos
        #check orientation
        if orientation == 'H':
            for x in range(x1, x2 + 1):
                self.city[y1][x] = '.'
        elif orientation == 'V':
            for y in range(y1, y2 + 1):
                self.city[y][x1] = '.'
    def display_time_and_level(self):
        #keep drawing white box to overlap text
        self.draw.t.showturtle()
        self.draw.t.penup()
        self.draw.t.goto(-self.x_offset-10, -self.y_offset -20)
        self.draw.t.pendown()
        self.draw.t.color('white')
        self.draw.t.begin_fill()
        self.extra_length_box = len(self.emp_name)*20
        for _ in range(2):
            self.draw.t.forward(600+self.extra_length_box)#width of the box
            self.draw.t.right(90)
            self.draw.t.forward(20)#height of box
            self.draw.t.right(90)
        self.draw.t.end_fill()
        #prepare to write text
        self.draw.t.penup()
        self.draw.t.goto(-self.x_offset, -self.y_offset-40)
        self.draw.t.pendown()
        #color for text
        self.draw.t.color('black')
        #calculate elapsed time and remaining time
        elapsed_time = time.time() - self.time_started
        self.remaining_time = max(0, self.time_limit - elapsed_time)
        #time and level
        if not self.auto_mode:
            self.draw.t.write(f'Drone Operator: {self.emp_name} | Time left: {self.remaining_time:.1f} seconds | Camera: {self.level} | Orders: {self.count_goal}', font=('Arial', 14, 'normal'))
        else:
             self.draw.t.write(f'Drone Operator: Auto | Time left: {self.remaining_time:.1f} seconds | Camera: {self.level} | Orders: {self.count_goal}', font=('Arial', 14, 'normal'))
        self.draw.t.hideturtle()
        
    def check_win(self,start,end):#checking for removing of drone upon hit goal and if all drones reached destination, generate new harder city (level2,level3 etc.)
        if self.goal_pos in (start,end):
            self.remove_car()
            del self.vehicle[self.veh_name]
            self.cveh=0
            if 'a' in self.veh_name:
                self.count_goal+=2
            else:
                self.count_goal+=1
            self.veh_name = list(self.vehicle.keys())[self.cveh]#change name to the new drone
            
            self.goal_pos = self.get_goal_pos()
            if not self.auto_mode:
                self.check_switch_keys()
            self.drawMaze()#redraw the maze
            return True
    def check_timer(self):
        elapsed_time = time.time() - self.time_started
        self.remaining_time = max(0, self.time_limit - elapsed_time)
        if self.remaining_time <= 0:
            turtle.bye()#go back to main
            try:
                subprocess.run(["python", "main.py"])
            except Exception as e:
                print(f"Failed to execute main.py: {e}")
            notify_user(self.emp_name, self.emp_email, elapsed_time, self.count_goal)
            #once time up, send notification to user on total time taken to deliver, how many total orders delivered and kill screen
        else:
            if len(self.vehicle)==0:
                print('Cleared all orders, changing to next camera!')
                turtle.clearscreen()
                self.level += 1 #increment level upon winning (replicate camera)
                self.time_limit= self.time_limit+15 #updated here increased the time limit for the next level (by remaining time +15)
                self.deactivate_vert()
                self.deactivate_hori()
                self.num_drone+=3
                self.num_aero+=2
                return self.randomcity()
            self.display_time_and_level()
            turtle.ontimer(self.check_timer, 1000)
    def check_switch_keys(self):#switch keys based on vehicle alignment (only for manual mode)
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        self.deactivate_hori()
        self.deactivate_vert()
        if orientation == 'H':
            self.activate_hori()
        else:
            self.activate_vert()
    
    #activate auto mode
    def activate_auto_mode(self):
        self.auto_mode = True#set auto to true
        self.deactivate_hori()
        self.deactivate_vert()
        self.auto_move()#move automaticlly
    #decativate auto mode
    def deactivate_auto_mode(self):
        self.auto_mode = False#changing back to manual control
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        if orientation == 'H':
            self.activate_hori()
        else:
            self.activate_vert()

    def auto_move(self):#for auto pilot
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        y2, x2 = end_pos
        y1, x1 = start_pos
        goal_y, goal_x = self.goal_pos
        moved=False
        if orientation == 'H':
            if goal_x > x2 and self.can_move(x2 + 1, y2):
                self.move_right()
                moved = 'right'
            elif goal_x < x1 and self.can_move(x1 - 1, y1):
                self.move_left()
                moved = 'left'
        else:#orientation == v
            if goal_y > y2 and self.can_move(x2, y2 + 1):
                self.move_down()
                moved = 'down'
            elif goal_y < y1 and self.can_move(x1, y1 - 1):
                self.move_up()
                moved = 'up'
        if not moved:#get previous move (one more press to change drone since can_move(+1))
            if orientation == 'V':
                if goal_y > y2:
                    moved = 'down'
                else:
                    moved = 'up'
            else:
                if goal_x > x2:
                    moved = 'right'
                else:
                    moved='left'
            if not self.check_win(start_pos, end_pos):#check if it is goal pos
                bumped_drone = self.check_collide(self.veh_name, moved)#if not check for collision wth another drone
                if bumped_drone:#check if there's a collision 
                    self.drawMaze()
        turtle.update()
        if self.auto_mode:#if still in auto mode
            turtle.ontimer(self.auto_move, 500)

    #movements
    def can_move(self, x, y):
        if x < 0 or x >= len(self.city[0]) or y < 0 or y >= len(self.city):
            return False
        return self.city[y][x] == '.'
    def move_down(self):
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        y2,x2 = end_pos
        y1,x1 = start_pos
        if self.can_move(x2, y2 + 1):#move vertically if cell above is empty
            self.city[y1][x1] = '.'
            self.city[y2+1][x2] = self.veh_name
            self.vehicle[self.veh_name] = ((y1+ 1, x1), (y2 + 1, x1), length_veh, orientation)
            self.drawMaze()
        else:#if not empty
            if not self.check_win(start_pos, end_pos):#check if it is goal pos
                bumped_drone = self.check_collide(self.veh_name, 'down')#if not check for collision wth another drone
                if bumped_drone:#check if there's a collision 
                    self.drawMaze()
    def move_up(self):
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        y2,x2 = end_pos
        y1,x1 = start_pos
        if self.can_move(x1, y1 - 1):#move cell up only if empty
            self.city[y2][x2] = '.'
            self.city[y1-1][x1] = self.veh_name
            self.vehicle[self.veh_name] = ((y1-1, x1), (y2-1, x2), length_veh, orientation)
            self.drawMaze()
        else:
            if not self.check_win(start_pos, end_pos):
                bumped_drone = self.check_collide(self.veh_name, 'up')
                if bumped_drone:#check if there's a collision (check collide return so)
                    self.drawMaze()
    def move_left(self):
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        y2,x2 = end_pos
        y1,x1 = start_pos
        if self.can_move(x1-1,y1):
            self.city[y2][x2] = '.'
            self.city[y1][x1-1] = self.veh_name
            self.vehicle[self.veh_name] = ((y1, x1-1), (y2,x2-1), length_veh, orientation)
            self.drawMaze()
        else:
            if not self.check_win(start_pos, end_pos):
                bumped_drone = self.check_collide(self.veh_name, 'left')
                if bumped_drone:
                    self.drawMaze()
    def move_right(self):
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        y2,x2 = end_pos
        y1,x1 = start_pos
        if self.can_move(x2+1, y2):
            #move horizontally across the length of the vehicle
            self.city[y1][x1] = '.'
            self.city[y2][x2+1] = self.veh_name
            self.vehicle[self.veh_name] = ((y1,x1+1), (y2,x2+1), length_veh, orientation)
            self.drawMaze()
        else:
            if not self.check_win(start_pos, end_pos):
                bumped_drone = self.check_collide(self.veh_name, 'right')
                if bumped_drone:
                    self.drawMaze()

    def random_align(self):#randomly align (used in goal position and generation of drones/aeroplanes)
        return random.randint(0, 1)
    #outline for vehicles under control
    def draw_outline(self):
        vehicle_info = list(self.vehicle.values())[self.cveh]
        (i1, j1), (i2, j2), length_veh, orientation = vehicle_info
        turtle.color('#84FD85') #draw outline for vehicles
        turtle.width(5)
        turtle.penup()
        if orientation == 'H':
            for j in range(j1, j1 + length_veh):
                self.draw_box_outline(i1, j)
        elif orientation == 'V':
            for i in range(i1, i1 + length_veh):
                self.draw_box_outline(i, j1)
    def draw_box_outline(self, i, j):
        x = j * self.box_size - self.x_offset
        y = (len(self.city) - i) * self.box_size - self.y_offset
        turtle.goto(x, y)
        turtle.pendown()
        for _ in range(4):
            turtle.forward(self.box_size)
            turtle.right(90)
        turtle.penup()
    
    #draw and get goals
    def get_goal_pos(self):
        ((i1, j1), (i2, j2), length_veh, orientation) = self.vehicle[list(self.vehicle.keys())[self.cveh]]
        end_or_start = self.random_align()
        if orientation == 'H':
            if end_or_start:#if horizontal, end
                return i1,self.cityw-1
            else:#if start
                return i1,0
        else:
            if end_or_start:#if vertical, end
                return self.cityh-1,j1
            else:#if start
                return 0,j1
    def draw_goal_box(self, x, y):
        turtle.color('black', '#7DFBFA')
        turtle.penup()
        turtle.goto(x * self.box_size - self.x_offset, (len(self.city) - y) * self.box_size - self.y_offset)
        turtle.pendown()
        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(self.box_size)
            turtle.right(90)
        turtle.end_fill()  
        turtle.hideturtle()
    
    #adding distance to vehicles coordinates
    def change_vehicle(self):
        for car,((i1, j1), (i2, j2), length_veh, orientation) in self.vehicle.items():
            self.vehicle[car] = ((i1+self.distance, j1+self.distance), (i2+self.distance, j2+self.distance), length_veh, orientation)
    #activate and deactivate keys based on user presses
    def activate_hori(self):
        turtle.listen()
        turtle.onkey(lambda: self.move_left(), "Left")
        turtle.onkey(lambda: self.move_right(), "Right")
    def activate_vert(self):
        turtle.listen() 
        turtle.onkey(lambda: self.move_up(), "Up")
        turtle.onkey(lambda: self.move_down(), "Down")
    def deactivate_hori(self):
        turtle.listen() 
        turtle.onkey(None, "Left")
        turtle.onkey(None, "Right")
    def deactivate_vert(self):
        turtle.listen()
        turtle.onkey(None, "Up")
        turtle.onkey(None, "Down")

    #for auto mode
    def check_auto(self):
        turtle.listen()
        turtle.onkey(self.toggle_auto_mode, "a")
    def toggle_auto_mode(self):
        self.countA += 1
        if self.countA % 2 == 1:
            self.activate_auto_mode()
        else:
            self.deactivate_auto_mode()
    def activate_auto_mode(self):
        self.deactivate_hori()
        self.deactivate_vert()
        self.auto_mode = True
        self.auto_move()
    def deactivate_auto_mode(self):
        self.auto_mode = False
        (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
        if orientation == 'H':
            self.activate_hori()
        else:
            self.activate_vert()

    #initalizing the game (comes after creating city)
    def start_game(self):
        turtle.tracer(1, 10)#animation
        self.cveh=0#set index of vehicle to 0 first (actually could jus use either countveh or vehname)
        new_city = []
        #adding outer border
        for i in range(self.distance):
            new_city.append(list('.'*(self.cityw+(self.distance*2))))
        for y in range(len(self.city)):
            new = []
            for i in range(self.distance):
                new.append('.')
            for x in range(len(self.city[y])):
                new.append(self.city[y][x])
            for i in range(self.distance):
                new.append('.')
            new_city.append(new)
        for i in range(self.distance):
            new_city.append(list('.'*(self.cityw+(self.distance*2))))
        
        self.city = new_city
        #add (distance) to current coords of vehicle
        self.change_vehicle()
        self.cityw=self.cityw+(self.distance*2)
        self.cityh=self.cityh+(self.distance*2)
        print('new city generated:',self.city)
        #initalizing game like set goal_pos, drawmaze, timer, based on current car activate horizontal/vertical keys
        self.goal_pos = self.get_goal_pos()
        self.drawMaze()
        self.check_timer()
        self.check_auto()
        if not self.auto_mode:
            (start_pos, end_pos, length_veh, orientation) = self.vehicle[self.veh_name]
            if orientation == 'H':
                self.activate_hori()
            else:
                self.activate_vert()

#tkinter for user input (employee name & employee email)
class UserInput:
    def __init__(self,prevscreen):
        self.prevscreen = prevscreen

        self.window = tk.Tk()
        self.window.title("User Information")

        self.name_label = tk.Label(self.window, text="Enter Employer Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack()

        self.email_label = tk.Label(self.window, text="Enter Email Address:")
        self.email_label.pack()

        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit)
        self.submit_button.pack()

        self.window.mainloop()

    def submit(self):
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        if self.validate_email(self.email):
            messagebox.showinfo("Info", "Information submitted successfully!")
            self.window.destroy()
            self.prevscreen.clearscreen()#clear previous screen
            #start game after submitting
            game = cityGame(cityw=6, cityh=6, num_drone=4, num_aero=3, drone_len=2, aero_len=3, email=self.email, user=self.name)
            game.randomcity()
            turtle.done()
        else:
            messagebox.showerror("Error", "Invalid email address!")
    #validate email for user input
    def validate_email(self, email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
