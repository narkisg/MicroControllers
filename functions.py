from STM32_Programmer_V1 import *
import json

# ============== functions ============== #

my_username = ""
my_password = ""
my_authorization = ""
process_reply = []
bootloader_reply = []

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


def do_command(port_name, controller_name, command_No, additional_par):
    result = execute_command(port_name, controller_name, command_No, additional_par)
    return result


# assistant functions for arbitrator
def check_user_name(user_to_check):
    with open('database.json') as dta:
        data = json.load(dta)
        for x in data['users']:
            if x['name'] == user_to_check:
                return 1
        return 0


# assistant functions for arbitrator
def check_password(pass_to_check):
    with open('database.json') as dta:
        data = json.load(dta)
        for x in data['users']:
            if x['password'] == pass_to_check:
                return 1
        return 0


def check_authorization(username, password):
    output = ""
    with open('database.json') as dta:
        data = json.load(dta)
        for x in data['users']:
            curr1 = x['name']
            curr2 = x['password']
            if curr1 == username and curr2 == password:
                output = x['authorization']
    return output


# assistant functions for arbitrator
def check_match(username, password):
    output = 0
    with open('database.json') as dta:
        data = json.load(dta)
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
    return output


def get_controllers_list():
    output = []
    for i in range(24):
        controller = 'controller' + str(i)
        output.append(controller)
    return output


def get_commands_list():
    if my_authorization == 1:
        output = ['MEM_WRITE']
    else:
        output = [{'name': 'BL_GET_VER', "fields": ["address", "sectroer"]}, 'BL_GET_HLP', 'BL_GET_CID', 'BL_GET_RDP_STATUS', 'BL_GO_TO_ADDR',
                  'BL_FLASH_MASS_ERASE', 'BL_FLASH_ERASE', 'BL_MEM_WRITE', 'BL_EN_R_W_PROTECT',
                  'BL_MEM_READ', 'BL_READ_SECTOR_P_STATUS', 'BL_OTP_READ', 'BL_DIS_R_W_PROTECT', 'BL_MY_NEW_COMMAND']
    return output


def get_ports_list():
    return serial_ports()


def get_users_list():
    with open('database.json') as dta:
        output = []
        data = json.load(dta)
        for x in data.values():
            output.append(x['name'])
    return output


def get_number_of_users():
    counter = 0
    with open('database.json') as dta:
        data = json.load(dta)
        for x in data.values():
            counter += 1
    return counter


def exit_system():
    raise SystemExit


# checks that username and password is not in use
# add new user to data base
def create_new_user(new_username, new_password, new_author_code):
    if my_authorization != '3':
        return -1  # not suppose to happen
    output = -1
    u_n_c = check_user_name(new_username)  # for user name check- 0 if the name not in list, 1 if it is
    p_w_c = check_password(new_password)  # for password check 0 if the password not in list, 1 if it is
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
                data['users'].append({"name": new_username, "password": new_password, "authorization": new_author_code})
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
                    data['users'].remove({"name": username, "password": password, "authorization": authorization})
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


def trying():
    with open('database.json', 'r+') as f:
        data = json.load(f)
        data['users'].append({"name": "ziv", "ln": "levi", "author": "17"})
        data = json.dumps(data)
        f.seek(0)
        f.write(data)
        f.truncate()
    f.close()

