from STM32_Programmer_V1 import *
import json
from py_server import emit_port_configuration_message

# ============== global variables ============== #

my_username = ""  # holds current user username
my_password = ""  # holds current user password
my_authorization = ""  # holds current user authorization
process_reply = []  # holds current command process arguments
bootloader_reply = []  # holds current command bootloader reply
is_connected_to_port = ""  # holds current port connection- empty string for not connected, name of port for connected

# ============== functions ============== #

# initializing global variables
def init_my_profile():
    global my_username
    my_username = ""

    global my_password
    my_password = ""

    global my_authorization
    my_authorization = ""

    global process_reply
    process_reply = []

    global bootloader_reply
    bootloader_reply = []

    global is_connected_to_port
    is_connected_to_port = ""


def clean_process_reply():
    process_reply.clear()


def clean_bootloader_reply():
    bootloader_reply.clear()


def do_command(port_name, controller_name, command_No, additional_par, socket):
    result = execute_command(port_name, controller_name, command_No, additional_par, socket)
    return result


# assistant functions for arbitrator
def check_user_name(user_to_check):
    with open('database.json') as f:
        data = json.load(f)
        for x in data['users']:
            if x['name'] == user_to_check:
                return 1
        return 0


# assistant functions for arbitrator
def check_password(pass_to_check):
    with open('database.json') as f:
        data = json.load(f)
        for x in data['users']:
            if x['password'] == pass_to_check:
                return 1
        return 0


def check_authorization(username, password):
    output = ""
    with open('database.json') as f:
        data = json.load(f)
        for x in data['users']:
            curr1 = x['name']
            curr2 = x['password']
            if curr1 == username and curr2 == password:
                output = x['authorization']
    return output


# assistant functions for arbitrator
def check_match(username, password):
    output = 0
    with open('database.json') as f:
        data = json.load(f)
        for x in data['users']:
            curr1 = x['name']
            curr2 = x['password']
            if curr1 == username and curr2 == password:
                output = 1
    return output


# the arbitrator function is called only from login attempt
def arbitrator(username, password):
    output = 0  # Default value
    u_n_c = check_user_name(username)
    p_w_c = check_password(password)
    c_m = check_match(username, password)
    if u_n_c == 0:
        if p_w_c == 0:
            output = -3
        else:
            output = -2
    elif u_n_c == 1:
        if p_w_c == 0:
            output = -1
        elif c_m == 0:
            output = 0
        else:
            output = check_authorization(username, password)
            global my_username
            my_username = username
            global my_password
            my_password = password
            global my_authorization
            my_authorization = output
    return int(output)


def discover_controllers_status_by_port(port_to_check, socket):
    list_of_connected_controllers = []
    for i in range(32):
        current_controller = i+1
        result = execute_command(port_to_check, str(current_controller), 1, '',socket)
        if result == 0 | result == -1:
            list_of_connected_controllers.append(current_controller)


def discover_controllers_status_all_ports(socket):
    map_of_connected_controllers = {}
    available_ports = get_ports_list()
    for i in range(len(available_ports)):
        current_port = available_ports[i]
        map_of_connected_controllers[current_port]=[]
        for j in range(32):
            current_controller = j+1
            result = execute_command(current_port, str(current_controller), 1, '', socket)
            if result == 0 | result == -1:
                map_of_connected_controllers[current_port].append(str(current_controller))
    return map_of_connected_controllers


def get_controllers_list():
    output = []
    for i in range(32):
        controller = 'controller' + str(i+1)
        output.append(controller)
    return output


def get_commands_list():
    if my_authorization == '1':
        output = [{'name': 'BL_MEM_WRITE', 'fields': []}]
    else:
        output = [{'name': 'BL_GET_VER', 'fields': []}, {'name': 'BL_GET_HLP', 'fields': []},
                  {'name': 'BL_GET_CID', 'fields': []}, {
                      'name': 'BL_GET_RDP_STATUS', 'fields': []},
                  {'name': 'BL_GO_TO_ADDR', 'fields': ['address']}, {
                      'name': 'BL_FLASH_MASS_ERASE', 'fields': []},
                  {'name': 'BL_FLASH_ERASE', 'fields': [
                      'sector_number', 'number_of_sectors_to_erase']},
                  {'name': 'BL_MEM_WRITE', 'fields': ['file_name', 'address']},
                  {'name': 'BL_EN_R_W_PROTECT', 'fields': [
                      'total_sector', 'list_of_sector_numbers', 'mode']},
                  {'name': 'BL_MEM_READ', 'fields': []}, {
                      'name': 'BL_READ_SECTOR_P_STATUS', 'fields': []},
                  {'name': 'BL_OTP_READ', 'fields': []}, {
                      'name': 'BL_DIS_R_W_PROTECT', 'fields': []},
                  {'name': 'BL_MY_NEW_COMMAND', 'fields': []}]
    return output


def get_command_fields(name):
    output = {'list': []}
    if name == 'BL_GO_TO_ADDR':
        output = {'list': ['address']}

    elif name == 'BL_FLASH_ERASE':
        output = {'list': ['sector_number', 'number_of_sectors_to_erase']}

    elif name == 'BL_MEM_WRITE':
        output = {'list': ['file_name', 'address']}

    elif name == 'BL_EN_R_W_PROTECT':
        output = {'list': ['total_sector', 'list_of_sector_numbers', 'mode']}

    return output


def get_ports_list():
    return serial_ports()


def get_users_list():
    with open('database.json') as f:
        output = []
        data = json.load(f)
        for x in data['users']:
            output.append(x['name'])
    return output


def get_number_of_users():
    counter = 0
    with open('database.json') as f:
        data = json.load(f)
        for x in data['users']:
            counter += 1
    return counter


def exit_system():
    raise SystemExit


# checks that username and password is not in use
# add new user to data base
def create_new_user(new_username, new_password, new_author_code):
    # if my_authorization != '3':
    # return -1  # not suppose to happen
    output = -1
    # for user name check- 0 if the name not in list, 1 if it is
    u_n_c = check_user_name(new_username)
    # for password check 0 if the password not in list, 1 if it is
    p_w_c = check_password(new_password)
    if u_n_c == 1:
        if p_w_c == 1:
            output = 2
        elif p_w_c == 0:
            output = 0
    elif u_n_c == 0:
        if p_w_c == 1:
            output = 1
        elif p_w_c == 0:
            output = 3
            with open('database.json', 'r+') as f:
                data = json.load(f)
                data['users'].append(
                    {"name": new_username, "password": new_password, "authorization": new_author_code})
                data = json.dumps(data)
                f.seek(0)
                f.write(data)
                f.truncate()
            f.close()
    return output


def delete_user(username):
    if my_authorization != '3':
        return -1  # not suppose to happen
    output = 0
    u_n_c = check_user_name(username)
    if u_n_c == 0:
        output = 0
    else:
        output = 1
        with open('database.json', 'r+') as f:
            data = json.load(f)
            for x in data['users']:
                if x['name'] == username:
                    password = x['password']
                    authorization = x['authorization']
                    data['users'].remove(
                        {"name": username, "password": password, "authorization": authorization})
                    break
            data = json.dumps(data)
            f.seek(0)
            f.write(data)
            f.truncate()
        f.close()
    return output


def change_user_authorization(username, new_author_code):
    if my_authorization != '3':
        return -1  # not suppose to happen
    output = 0
    with open('database.json', 'r+') as f:
        data = json.load(f)
        for x in data['users']:
            if x['name'] == username:
                x['authorization'] = new_author_code
                output = 1
                break
        data = json.dumps(data)
        f.seek(0)
        f.write(data)
        f.truncate()
    f.close()
    return output


def change_user_name(username, new_user_name):
    if my_authorization != '3':
        return -1  # not suppose to happen
    output = 0
    with open('database.json', 'r+') as f:
        data = json.load(f)
        for x in data['users']:
            if x['name'] == username:
                x['name'] = new_user_name
                output = 1
                break
        data = json.dumps(data)
        f.seek(0)
        f.write(data)
        f.truncate()
    f.close()
    return output


def change_user_password(username, new_password):
    if my_authorization != '3':
        return -1  # not suppose to happen
    output = 0
    with open('database.json', 'r+') as f:
        data = json.load(f)
        for x in data['users']:
            if x['name'] == username:
                x['password'] = new_password
                output = 1
                break
        data = json.dumps(data)
        f.seek(0)
        f.write(data)
        f.truncate()
    f.close()
    return output


def print_process_nevo(result):
    functions.process_reply.append(result)


def print_bootloader_nevo(result):
    functions.bootloader_reply.append(result)

def port_configuration_message(port_configuration_message):
    emit_port_configuration_message(port_configuration_message)
    return

