from backend.functions import *

table_of_users = dict()
list_of_commands = dict()
list_of_controllers = dict()
list_of_ports = dict()
my_user_name = ""
my_password = ""
my_authorization = ""

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

    def __str__(self):
        return "[" + self.username + ", " + self.password + ", " + self.authorization + "]"

    def print_user(self):
        print(self.__str__())

    def __eq__(self, other):
        if isinstance(object, self.__class__):
            if object.username is self.username and object.password is self.password and object.authorization is self.authorization:
                return True
        return False


# after running the program
def init1():
    global table_of_users
    table_of_users = fill_table_of_users()


# after login, called from arbitrator function
def init2(username, password):
    global list_of_controllers
    list_of_controllers = fill_list_of_controllers()

    global list_of_ports
    list_of_ports = fill_list_of_ports()

    global my_user_name
    my_user_name = username

    global my_password
    my_password = password

    global my_authorization
    my_authorization = chek_authorization(username, password)

    global list_of_commands
    list_of_commands = fill_list_of_commands(my_authorization)


def fill_table_of_users():
    output = dict()
    for i in range(30):
        if i == 0:
            user = user_card('user_' + str(i), '767_' + str(i), 3)
            output["user_No."+ str(i)] = user
        elif i < 16:
            user = user_card('user_' + str(i), '767_' + str(i), 2)
            output["user_No."+ str(i)] = user
        else:
            user = user_card('user_' + str(i), '767_' + str(i), 1)
            output["user_No."+ str(i)] = user
    return output


def fill_list_of_controllers():
    output = dict()
    for x in range(30):
        output["cont_" + str(x)] = str(x)
    return output


def fill_list_of_ports():
    return {"port_1": "COM3"}
    # return serial_ports()


def fill_list_of_commands(authorization_code):
    output = dict()
    i = -1
    if authorization_code == 1:
        output = {'command_0': 'MEM_WRITE'}
    else:
        to_insert = ['GET_VER', 'GET_HELP', 'GET_CID', 'GET_RDP_STATUS', 'GO_TO_ADDR', 'FLASH_ERASE',
                     'MEM_WRITE', 'EN_R_W_PROTECT', 'MEM_READ', 'READ_SECTOR_P_STATUS', 'OTP_READ',
                     'DIS_R_W_PROTECT', 'MY_NEW_COMMAND']
        for x in to_insert:
            i += 1
            output["command_" + str(i)] = x
    return output


def chek_authorization(username, password):
    output = ""
    for x in table_of_users.values():
        if x.username == username and x.password == password:
            output = x.authorization
    return output


