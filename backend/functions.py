from backend import global_vars_setting
from backend.global_vars_setting import *
from backend.STM32_Programmer_V1 import *


# ============== functions ============== #


def do_command(port_name, controller_name, command_No, additional_par):
    result = execute_command(port_name, controller_name, command_No, additional_par)
    return result


# assistant functions for arbitrator
def check_user_name(user_to_check):
    for usercard in global_vars_setting.table_of_users.values():
        if usercard.username == user_to_check:
            return 1
    return 0


# assistant functions for arbitrator
def check_password(pass_to_check):
    for usercard in global_vars_setting.table_of_users.values():
        if usercard.password == pass_to_check:
            return 1
    return 0


# assistant functions for arbitrator
def check_match(user_to_check, pass_to_check):
    for usercard in global_vars_setting.table_of_users.values():
        curr1 = usercard.username
        curr2 = usercard.password
        if curr1 == user_to_check and curr2 == pass_to_check:
            return 1
    return 0


# the arbitrator function is called only from login attempt
def arbitrator(username, password):
    global_vars_setting.init2(username, password)
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
            output = global_vars_setting.chek_authorization(username, password)
    return output


def get_controllers_list():
    return global_vars_setting.list_of_controllers


def get_commands_list():
    return global_vars_setting.list_of_commands


def get_ports_list():
    return global_vars_setting.list_of_ports


def exit_system():
    raise SystemExit


# checks that username and password is not in use
# add new user to data base
def create_new_user(new_username, new_password, author_code):
    u_n_c = 1  # for user name check- 1 for good, 0 for bad
    p_w_c = 1  # for password check 1 for good, 0 for bad
    output = -1
    for x in global_vars_setting.table_of_users.values():
        tmp_1 = x.username
        tmp_2 = x.password
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
            NEW_USER = global_vars_setting.user_card(new_username, new_password, author_code)
            i = len(global_vars_setting.table_of_users)
            global_vars_setting.table_of_users['user_No.'+str(i)] = NEW_USER
    return output


def delete_user(username):
    if global_vars_setting.my_authorization != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    output = 0
    for key, usercard in global_vars_setting.table_of_users.items():
        current = usercard.username
        if current == username:
            del (global_vars_setting.table_of_users[key])
            output = 1
            break
    return output


def change_user_authorization(username, new_author_code):
    if global_vars_setting.my_authorization != 3:
        raise OSError("Unauthorized action")  # not suppose to happen
    output = 0
    for x in global_vars_setting.table_of_users.values():
        current = x.username
        if current == username:
            x.authorization = new_author_code
            output = 1
    return output


def change_user_name(username, new_user_name):
    output = 0
    for x in global_vars_setting.table_of_users.values():
        current = x.username
        if current == username:
            x.username = new_user_name
            output = 1
    return output


def change_user_password(username, new_password):
    output = 0
    for x in global_vars_setting.table_of_users.values():
        current = x.username
        if current == username:
            x.password = new_password
            output = 1
    return output
