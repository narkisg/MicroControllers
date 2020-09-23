

"""
below there are global variables and hard-coded data structures.
the global vars are used to specified the commands that the user executes.

the data structures (numpy array/lists) are the data bases and the 
of the user authorization system.

the init() function called from main.py.

at the initializing:
- user 0 is the administrator
- users 1-15 (include) are the developers
- users 16-30 are the simple user
*Note that the administrator can change the database*
"""

# new object to store the details of the users
class user_card:
    def __init__(self, username, password, authorization):
        self.username = username
        self.password = password
        self.authorization = authorization

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def to_string(self):
        return  "["+self.username+", "+self.password+", "+self.authorization+"]"

    def print_user(self):
        print(self.to_string())

    def equals(self, object):
        if isinstance(object, self.__class__):
            if object.username == self.username and object.password == self.password and object.authorization == self.authorization:
                return True
        return False

authorization_code = 0
table_of_users = list(user_card)
list_of_controllers = list()
list_of_ports = list()
list_of_commands = list()

def init():
    global authorization_code
    authorization_code = 0
    # 0- unauthorized
    # 1- simple user
    # 2- developer
    # 3- administrator

    global table_of_users
    table_of_users = list()

    global list_of_controllers
    list_of_controllers = list()

    global list_of_ports
    list_of_ports = list()

    global list_of_commands
    list_of_commands = list()


