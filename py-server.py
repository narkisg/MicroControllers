from flask import Flask
from flask_socketio import SocketIO, emit
import json
from backend.functions import *


# ----------DO NOT REMOVE THIS LINE!!!---------- #
from engineio.async_drivers import gevent

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


# example:
@socketio.on('getlist')
def handle_message(message):
    print(message)
    emit('list', {'controllers': ['cont-1', 'cont-2', 'cont-3', 'cont-4']})


# ========================= login window functions ========================= #

# activate after pressing the 'Login' button
@socketio.on('login_attempt')
def handle_message(user_name_deatils):  # transfer to switch-case function
    data = json.dumps(user_name_deatils)
    data = json.loads(data)
    username = data["username"]
    password = data["password"]
    permission = arbitrator(username, password)  # will call init2() later on
    if permission == -3:
        emit('login_response', {'success': 'false', 'message': 'invalid_username_and_password'})
    elif permission == -2:
        emit('login_response', {'success': 'false', 'message': 'invalid_username'})
    elif permission == -1:
        emit('login_response', {'success': 'false', 'message': 'invalid_password'})
    elif permission == 0:
        emit('login_response', {'success': 'false', 'message': 'username_and_password_do_not_match'})
    elif permission == 1:
        emit('login_response', {'success': 'true', 'message': 'simple_user_successfully_logged_in'})
    elif permission == 2:
        emit('login_response', {'success': 'true', 'message': 'developer_user_successfully_logged_in'})
    elif permission == 3:
        emit('login_response', {'success': 'true', 'message': 'administrator_user_successfully_logged_in'})


# ========================= main window functions ========================= #

# ----- update program functions ----- #

# activate after pressing the button to show the available com ports
@socketio.on('get_list_of_ports')
def handle_message():
    portslist = get_ports_list()
    emit('list_of_ports', json.dumps(portslist))


# activate after pressing the button to show the available controllers
@socketio.on('get_list_of_controllers')
def handle_message():
    controllerlist = get_controllers_list()
    emit('list_of_controllers', json.dumps(controllerlist))


# activate after pressing the button to show the available commands
@socketio.on('get_list_of_commands')
def handle_message():
    commandslist = get_commands_list()
    emit(json.dumps(commandslist))


# activate after choosing port, controller, command, and update(if necessary)
# and pressing the update program button
# port_name, controller_name, command_No, additional_par
@socketio.on('execute_command')
def handle_message(details):  # transfer to switch-case function
    data = json.dumps(details)
    data = json.loads(data)
    port_name = data["port_name"]
    controller_name = data["controller_name"]
    command_No = data["command_number"]
    additional_par = data["additional_parameters"]
    # the additional parameters is a json list of all the additional parameters the current function demands,
    # for example, if some command demands additional parameters than the global fields(port name, cont num...),
    # like number of sectors, or list of something or file address to upload from directory.
    # example for json file with additional parameters-
    #                           {port name: "COM3",
    #                           controller name: "controller_1"
    #                           command number: "9"
    #                           authorization code: "2"
    #                           additional parameters: ["6", "00x4", "["3","7","0"]", "user_app.bin"]}
    if global_vars_setting.my_authorization == 1 & command_No != 8:
        emit('execute_command_response', {'success': 'false', 'message': 'unauthorized_command_for_simple_user'})
    else:
        result = do_command(port_name, controller_name, command_No, additional_par)
        if result == 0x00:
            emit('execute_command_response', {'success': 'true', 'message': 'Flash_HAL_OK'})
        elif result == 0x01:
            emit('execute_command_response', {'success': 'false', 'message': 'Flash_HAL_ERROR'})
        elif result == 0x02:
            emit('execute_command_response', {'success': 'false', 'message': 'Flash_HAL_BUSY'})
        elif result == 0x03:
            emit('execute_command_response', {'success': 'false', 'message':  'Flash_HAL_TIMEOUT'})
        elif result == 0x04:
            emit('execute_command_response', {'success': 'false', 'message': 'Flash_HAL_INV_ADDR'})
        elif result == -2:
            emit('execute_command_response', {'success': 'false', 'message': 'TimeOut:_No_response_from_the_bootloader,_reset_the_board_and_try_Again_!'})


# ----- user management functions ----- #

# activate after pressing the user management button- only for administrator
@socketio.on('user_management')
def handle_message():
    if global_vars_setting.my_authorization == 3:
        emit('user_management_response', {'success': 'true', 'message': 'administrator_confirmed'})
    else:
        emit('user_management_response', {'success': 'false', 'message': 'unauthorized_user'})


# create new user - add to database after filing details and pressing register
@socketio.on('register_user')
def handle_message(new_user_details):  # transfer to switch-case function
    data = json.dumps(new_user_details)
    data = json.loads(data)
    new_username = data["new_user_name"]
    new_password = data["new_password"]
    author_code = data["authorization_code"]
    author_code = int(author_code, 10)
    if author_code != 1 and author_code != 2 and author_code != 3:
        emit('register_response', {'success': 'false', 'message': 'illegal_authorization_code'})
    else:
        result = create_new_user(new_username, new_password, author_code)
        if result == 0:
            emit('register_response', {'success': 'false', 'message': 'username_already_in_use'})
        elif result == 1:
            emit('register_response', {'success': 'false', 'message': 'password_already_in_use'})
        elif result == 2:
            emit('register_response', {'success': 'false', 'message': 'username_and_password_already_in_use'})
        elif result == 3:
            emit('register_response', {'success': 'true', 'message': 'new_user_registered_to_system'})


@socketio.on('get_table_of_users')
def handle_message():
    output = dict()
    i = 0
    for usercard in global_vars_setting.table_of_users.values():
        current = usercard.username
        output['user_No.'+str(i)] = current
        i += 1
    emit(json.dumps(output))


@socketio.on('delete_user')
def handle_message(username_to_del):
    data = json.dumps(username_to_del)
    data = json.loads(data)
    us_to_del = data["username_to_delete"]
    result = delete_user(us_to_del)
    if result == 0:
        emit('delete_user_response', {'success': 'false', 'message': 'user_is_not_in_list'})
    else:
        emit('delete_user_response', {'success': 'false', 'message': 'user_is_out_of_the_system'})


@socketio.on('change_user_authorization')
def handle_message(details):
    data = json.dumps(details)
    data = json.loads(data)
    username = data["username"]
    new_author_code = data["new_authorization"]
    if new_author_code != 1 and new_author_code != 2 and new_author_code != 3:
        emit('change_authorization_response', {'success': 'false', 'message': 'illegal_authorization_code'})
    else:
        result = change_user_authorization(username, new_author_code)
        if result == 0:
            emit('change_authorization_response', {'success': 'false', 'message': 'user_is_not_in_list'})
        elif result == 1:
            emit('change_authorization_response', {'success': 'true', 'message': 'user_authorization_changed'})


@socketio.on('change_user_name')
def handle_message(details):
    data = json.dumps(details)
    data = json.loads(data)
    username = data["username"]
    new_user_name = data["new_username"]
    result = change_user_name(username, new_user_name)
    if result == 0:
        emit('change_username_response', {'success': 'false', 'message': 'user_is_not_in_list'})
    elif result == 1:
        emit('change_username_response', {'success': 'true', 'message': 'user_name_changed'})


@socketio.on('change_user_password')
def handle_message(details):
    data = json.dumps(details)
    data = json.loads(data)
    username = data["username"]
    new_password = data["new_password"]
    result = change_user_password(username, new_password)
    if result == 0:
        emit('change_password_response', {'success': 'false', 'message': 'user_is_not_in_list'})
    elif result == 1:
        emit('change_username_response', {'success': 'true', 'message': 'password_changed'})


@socketio.on('my_profile')
def handle_message():
    my_profile = {'username': global_vars_setting.my_user_name,
                  'password': global_vars_setting.my_password, 'authorization': global_vars_setting.my_authorization}
    emit(json.dumps(my_profile))


# ----- logout function ----- #

# activate after pressing the 'Logout' button, and the 'confirm Logout button'
@socketio.on('logout_attempt')
def handle_message():
    raise SystemExit


if __name__ == '__main__':
    global_vars_setting.init1()
    #execute_command('COM3', 'CONT1', '4', "")
    print('running on port 5000')
    socketio.run(app)
