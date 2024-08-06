import turtle

class EmployeeSecure:
    def __init__(self):
        self.load_users()  # Load existing users from the file
        self.logged_in = False

    def start(self):
        # Main loop for handling user input
        while not self.logged_in:
            choice = turtle.textinput("Login or Register", "Press A to login, B to register")
            if choice in ['A', 'a']:
                self.login()
            elif choice in ['B', 'b']:
                self.register()
            else:
                turtle.textinput("Invalid Option", "Please press A or B")

    def login(self):
        username = turtle.textinput("Login", "Enter username:")
        password = turtle.textinput("Login", "Enter password:")
        if username in self.users and self.users[username] == password:
            self.logged_in = True
            turtle.textinput("Login Success", "You are now logged in")
        else:
            turtle.textinput("Login Failed", "Invalid username or password")

    def register(self):
        username = turtle.textinput("Register", "Choose a username:")
        password = turtle.textinput("Register", "Choose a password:")
        if username not in self.users:
            self.users[username] = password
            with open('employee.txt', 'a') as file:
                file.write(f"{username},{password}\n")
            turtle.textinput("Registration Success", "You can now log in")
        else:
            turtle.textinput("Registration Failed", "Username already exists")

    def load_users(self):
        self.users = {}
        try:
            with open('employee.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        username, password = parts
                        self.users[username] = password
        except FileNotFoundError:
            print("employee.txt not found, starting with an empty user list.")
