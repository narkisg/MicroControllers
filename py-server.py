from flask import Flask
from flask_socketio import SocketIO, emit
from backend.global_vars_setting import *
from backend.functions import *

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
def handle_message(username, password):    # transfer to switch-case function
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
    emit(portslist)


# activate after choosing port from list
@socketio.on('choose_port')
def handle_message(port_name):
    port = choose_port(port_name)
    emit(port + " chosen")


# activate after pressing the button to show the available controllers
@socketio.on('get_list_of_controllers')
def handle_message():
    controllerlist = get_controllers_list()
    emit(controllerlist)


# activate after choosing controller from list
@socketio.on('choose_controller')
def handle_message(controller_name):
    choose_controller(controller_name)
    emit(controller_name + " chosen")


# activate after pressing the button to show the available commands
@socketio.on('get_list_of_commands')
def handle_message():
    commandslist = get_commands_list()
    emit(commandslist)


# activate after choosing command from list
@socketio.on('choose_command')
def handle_message(command_No):
    choose_command(command_No)
    emit(command_No + " chosen")


# activate after choosing port, controller, command, and update(if necessary)
# and pressing the upload button
@socketio.on('upload')
def handle_message():  # transfer to switch-case function
    result = do_command()
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


# ----- specific commands demands ----- #

@socketio.on('enter_address')
def handle_message(address):
    update_address(address)
    emit(address + " updated")


@socketio.on('enter_sector_num')
def handle_message(sector_num):
    updater_sector_num(sector_num)
    emit(sector_num + " updated")


@socketio.on('enter_num_of_sector_to_erase')
def handle_message(num_of_sector_to_erase):
    update_num_of_sector_to_erase(num_of_sector_to_erase)
    emit(num_of_sector_to_erase + " updated")


# ----- user management functions ----- #

# activate after pressing the user management button- only for administrator
@socketio.on('user_management')
def handle_message():
    if authorization_code == 3:
        emit("administrator confirmed")
    else:
        raise OSError("Unauthorized action")


# create new user - add to database after filing details and pressing register
@socketio.on('register_user')
def handle_message(new_username, new_password, author_code):    # transfer to switch-case function
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
    return table_of_users

@socketio.on('delete_user')
def handle_message(username):
    result = delete_user(username)
    if result == 0:
        emit('user is not in list')
    else:
        emit('user: '+username+", deleted")


@socketio.on('change_user_authorization')
def handle_message(username, new_author_code):
    result = change_user_authorization(username, new_author_code)
    if result == 0:
        emit('user is not in list')
    elif result == 1:
        emit('user authorization changed')


@socketio.on('change_user_name')
def handle_message(username, new_user_name):
    result = change_user_name(username, new_user_name)
    if result == 0:
        emit('user is not in list')
    elif result == 1:
        emit('user name changed')


@socketio.on('change_user_password')
def handle_message(username, new_password):
    result = change_user_name(username, new_password)
    if result == 0:
        emit('user is not in list')
    elif result == 1:
        emit('password changed')


# ----- add new update functions ----- #

@socketio.on('add_file')
def handle_message():
    pass


# ----- logout functions ----- #

# activate after pressing the 'Logout' button, and the 'confirm Logout button'
@socketio.on('logout_attempt')
def handle_message():
    raise SystemExit


if __name__ == '__main__':
    print('running on port 5000')
    socketio.run(app)
    init()
