from flask import Flask
from flask_socketio import SocketIO, emit
from backend.global_vars_setting import *
from backend.functions import *
import json

# ----------DO NOT REMOVE THIS LINE!!!---------- #
from engineio.async_drivers import gevent

from backend.functions import *

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
@socketio.on('login attempt')
def handle_message(user_name_deatils):    # transfer to switch-case function
    data = json.loads(user_name_deatils)
    username = data["username"]
    password = data["password"]
    permission = arbitrator(username, password)
    if permission == -3:
        emit('invalid username and password')
    elif permission == -2:
        emit('invalid username')
    elif permission == -1:
        emit('invalid password')
    elif permission == 0:
        emit('username and password do not match')
    elif permission == 1:
        emit('simple user successfully logged in')
    elif permission == 2:
        emit('developer user successfully logged in')
    elif permission == 3:
        emit('administrator user successfully logged in')


# ========================= main window functions ========================= #

# ----- update program functions ----- #

# activate after pressing the button to show the available com ports
@socketio.on('get_list_of_ports')
def handle_message():
    portslist = get_ports_list()
    emit(json.dumps(portslist))


# activate after pressing the button to show the available controllers
@socketio.on('get_list_of_controllers')
def handle_message():
    controllerlist = get_controllers_list()
    emit(json.dumps(controllerlist))


# activate after pressing the button to show the available commands
@socketio.on('get_list_of_commands')
def handle_message():
    commandslist = get_commands_list()
    emit(json.dumps(commandslist))


# activate after choosing port, controller, command, and update(if necessary)
# and pressing the update program button
#port_name, controller_name, command_No, additonal_par
@socketio.on('execute command')
def handle_message(details):  # transfer to switch-case function
    data = json.loads(details)
    port_name = data["port name"]
    controller_name = data["controller name"]
    command_No = data["command number"]
    authorization_code = data["authorization code"]
    additional_par = data["additional parameters"]
    if authorization_code == 1 & command_No != 8:
        emit("unauthorized command for simple user")
    # the additional parameters is a json list of all the additional parameters the current function demands,
    # for example, if some command demands additional parameters than the global fields(port name, cont num...),
    # like number of sectors, or list of something or file address to upload from directory.
    # example for json file with additional parameters- {port name: "COM3",
    #                           controller name: "controller_1"
    #                           command number: "9"
    #                           authorization code: "2"
    #                           additional parameters: ["6", "00x4", "["3","7","0"]", "user_app.bin"]}
    result = do_command(port_name, controller_name, command_No, authorization_code, additional_par)
    if result == 0x00:
        emit("Flash_HAL_OK")
    elif result == 0x01:
        emit("Flash_HAL_ERROR")
    elif result == 0x02:
        emit("Flash_HAL_BUSY")
    elif result == 0x03:
        emit("Flash_HAL_TIMEOUT")
    elif result == 0x04:
        emit("Flash_HAL_INV_ADDR")
    elif result == -2:
        emit("TimeOut : No response from the bootloader, reset the board and Try Again !")


# ----- user management functions ----- #

# activate after pressing the user management button- only for administrator
@socketio.on('user_management')
def handle_message():
    if authorization_code == 3:
        emit("administrator confirmed")
    else:
        emit("unauthorized user")


# create new user - add to database after filing details and pressing register
@socketio.on('register_user')
def handle_message(new_user_details):    # transfer to switch-case function
    data = json.loads(new_user_details)
    new_username = data["new user name"]
    new_password = data["new password"]
    author_code = data["authorization code"]
    if author_code != 3:
        emit("unauthorized user")
    else:
        result = create_new_user(new_username, new_password, author_code)
        if result == 0:
            emit('username already in use')
        elif result == 1:
            emit('password already in use')
        elif result == 2:
            emit('username and password already in use')
        elif result == 3:
            emit('new user registered to system')


@socketio.on('get_table_of_users_to_delete')
def handle_message():
    emit(json.dumps(table_of_users))  # problem because of the new class i wrote!

@socketio.on('delete_user')
def handle_message(username_to_del):
    data = json.loads(username_to_del)
    us_to_del = data["username"]
    author_code = data["authorization code"]
    if author_code != 3:
        emit("unauthorized user")
    else:
        result = delete_user(us_to_del)
        if result == 0:
            emit('user is not in list')
        else:
            emit('user is out of the system')


@socketio.on('change_user_authorization')
def handle_message(details):
    data = json.loads(details)
    username = data["username"]
    author_code = data["authorization code"]
    if author_code != 3:
        emit("unauthorized user")
    else:
        new_author_code = data["additional parameters"]["new authorization code"]
        result = change_user_authorization(username, new_author_code)
        if result == 0:
            emit('user is not in list')
        elif result == 1:
            emit('user authorization changed')


@socketio.on('change_user_name')
def handle_message(details):
    data = json.loads(details)
    username = data["username"]
    author_code = data["authorization code"]
    if author_code != 3:
        emit("unauthorized user")
    else:
        new_user_name = data["additional parameters"]["new user name"]
        result = change_user_name(username, new_user_name)
        if result == 0:
            emit('user is not in list')
        elif result == 1:
            emit('user name changed')


@socketio.on('change_user_password')
def handle_message(details):
    data = json.loads(details)
    username = data["username"]
    new_password = data["new password"]
    result = change_user_name(username, new_password)
    if result == 0:
        emit('user is not in list')
    elif result == 1:
        emit('password changed')


# ----- logout functions ----- #

# activate after pressing the 'Logout' button, and the 'confirm Logout button'
@socketio.on('logout_attempt')
def handle_message():
    raise SystemExit


if __name__ == '__main__':
    print('running on port 5000')
    socketio.run(app)
    init()
