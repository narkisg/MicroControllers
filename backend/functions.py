from backend.STM32_Programmer_V1 import *
from backend.global_vars_setting import *

def fill_table_of_users():
    for i in range(30):
        if i == 0:
            user = user_card('user_'+str(i), '767'+str(i), 3)
            table_of_users.append(user)
        elif i < 16:
            user = user_card('user_' + str(i), '767' + str(i), 2)
            table_of_users.append(user)
        else:
            user = user_card('user_' + str(i), '767' + str(i), 1)
            table_of_users.append(user)


def fill_list_of_controllers():
    for x in range(1000):
        list_of_controllers.insert('controller_' + str(x))
    return list_of_controllers


def fill_list_of_ports():
    return serial_ports()

#UNDONE
def fill_list_of_commands():
    if authorization_code == 3:
        list_of_commands == ()
    elif authorization_code == 2:
        list_of_commands == ()
    else:
        list_of_commands == ()


# ============== functions ============== #


def do_command():
    if port_name is not None and controller_name is not None and command_number is not None:
        result = execute_command(port_name, controller_name, command_number, authorization_code)
        return result

# assistant functions for arbitrator
def check_user_name(user_to_check):
    for x in  table_of_users:
        if x == user_to_check:
            return 1
    return 0


# assistant functions for arbitrator
def check_password(pass_to_check):
    for x in table_of_users:
        for y in x:
            if y == pass_to_check:
                return 1
    return 0


# assistant functions for arbitrator
def check_match(user_to_check, pass_to_check):
    for x in table_of_users:
        for y in x:
            if x == user_to_check and y == pass_to_check:
                return 1
    return 0


# the arbitrator function is called only from login attempt
def arbitrator(username, password):
    output = 0   #Default value
    fill_table_of_users()
    fill_list_of_ports()
    fill_list_of_controllers()
    u_n_c = check_user_name(username)
    p_w_c = check_password(password)
    c_m = check_match(username, password)
    if u_n_c == 0:
        if p_w_c == 0:
            output = -3
        else: output = -2

    elif u_n_c == 1:
        if p_w_c == 0:
            output = -1
        elif c_m == 0:
            output = 0
        else:
            output = table_of_users([username][2])
    return output


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
    raise SystemExit

def list_of_commands():
    return List_Of_Commands


def list_of_ports():
    return List_Of_Ports

# checks that username and password is not in use
# add new user to data base
def create_new_user(new_username, new_password, author_code):
    if authorization_code != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    u_n_c = 1  # for user name check- 1 for good, 0 for bad
    p_w_c = 1  # for password check 1 for good, 0 for bad
    output = -1
    for x in table_of_users:
        tmp_1 = user_card(x).username
        tmp_2 = user_card(x).password
        if tmp_1 == new_username:
            u_n_c = 0
        if tmp_2 == new_password:
            p_w_c = 0
    if u_n_c == 0:
        if p_w_c == 0:
            output = 2
        elif p_w_c == 1:
            output = 0
    if u_n_c == 1:
        if p_w_c == 0:
            output = 1
        elif p_w_c == 1:
            output = 3
            NEW_USER = user_card(new_username, new_password, author_code)
            table_of_users.append(NEW_USER)
    return output


def delete_user(username):
    if authorization_code != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    output = 0
    for x in table_of_users:
        current = user_card(x).username
        if current == username:
            table_of_users.remove(x)
            output = 1
    return output


def change_user_authorization(username, new_author_code):
    if authorization_code != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    output = 0
    for x in table_of_users:
        current = user_card(x).username
        index = table_of_users.index(x)
        if current == username:
            user_card(table_of_users[index]).authorization = new_author_code
            output = 1
    return output


def change_user_name(username, new_user_name):
    if authorization_code != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    output = 0
    for x in table_of_users:
        current = user_card(x).username
        index = table_of_users.index(x)
        if current == username:
            user_card(table_of_users[index]).username = new_user_name
            output = 1
    return output


def change_user_password(username, new_password):
    if authorization_code != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    output = 0
    for x in table_of_users:
        current = user_card(x).username
        index = table_of_users.index(x)
        if current == username:
            user_card(table_of_users[index]).password = new_password
            output = 1
    return output


def update_address(address_num):
    address = address_num


def updater_sector_num(sec_num):
    sector_number = sec_num


def update_num_of_sector_to_erase(num_of_sec_to_erase):
    num_of_sector_to_erase = num_of_sec_to_erase