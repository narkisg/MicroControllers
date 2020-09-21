from backend.STM32_Programmer_V1 import *

# ============== fields and builders ============== #
port_name = None
controller_name = None
command_number = None
authorization_code = 0
# 0- unauthorized
# 1- simple user
# 2- developer
# 3- administrator


def fill_list_of_users():
    userslist = dict()  # keys for user names, values for password, Respectively
    for x in range(31):
        userslist['user_' + str(x)] = '767' + str(x)
    return userslist


def fill_list_of_controllers():
    list_of_controllers = list()
    for x in range(1000):
        list_of_controllers.insert('controller_' + str(x))
    return list_of_controllers


def fill_list_of_ports():
    return serial_ports()


def fill_list_of_commands():
    if authorization_code == 3:
        list_of_commands == ()
    elif authorization_code == 2:
        list_of_commands == ()
    else:
        list_of_commands == ()


"""
the variables bellow (dictionaries/lists) are the hard-coded data bases of the user authorization system
- user 0 is the administrator
- users 1-15 (include) are the developers
- users 16-30 are the simple user
"""


list_of_users = fill_list_of_users()
list_of_controllers = fill_list_of_controllers()
list_of_ports = fill_list_of_ports()
list_of_commands = list()
#

# ============== functions ============== #


def do_command():
    if port_name is not None and controller_name is not None and command_number is not None:
        result = execute_command(port_name, controller_name, command_number, authorization_code)
        return result


def arbitrator(username, password):
    for (x, y) in list_of_users:
        if (username, password) == (x, y):
            if username == 'user_o':
                global authorization_code
                global list_of_commands
                authorization_code = 3
                fill_list_of_commands()
                return 3
            for i in range(1, 16):
                x = list_of_users.items(i)
                y = list_of_users.values(i)
                if (x, y) == (username, password):
                    global authorization_code
                    authorization_code = 2
                    return 2
            for i in range(16, 31):
                x = list_of_users.items(i)
                y = list_of_users.values(i)
                if (x, y) == (username, password):
                    global authorization_code
                    authorization_code = 1
                    return 1
    return 0


def get_ports_list():
    global list_of_ports
    list_of_ports = fill_list_of_ports()
    return list_of_ports


def choose_port(portName):
    global port_name
    if portName in list_of_ports:
        port_name = portName
        return port_name
    else:
        EnvironmentError('Unsupported platform')


def get_controllers_list():
    global list_of_controllers
    list_of_controllers = fill_list_of_controllers()
    return list_of_controllers


def choose_controller(controllerName):
    global controller_name
    controller_name = controllerName


def get_commands_list():
    return list_of_commands


def choose_command(commandNo):
    global command_number
    command_number = commandNo


def exit_system():
    return decode_menu_command_code(command=0)


def list_of_commands():
    return List_Of_Commands


def list_of_ports():
    return List_Of_Ports
""" undone
def create_new_user(new_username, new_password, author_code):
    global list_of_users
    list_of_users.
    """