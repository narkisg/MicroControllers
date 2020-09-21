from flask import Flask
from flask_socketio import SocketIO, emit

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
def handle_message(username, password):
    permission = arbitrator(username, password)
    if permission == 1:
        emit('simple user successfully logged in')
    elif permission == 2:
        emit('developer user successfully logged in')
    elif permission == 3:
        emit('administrator user successfully logged in')
    else:
        emit('invalid username or password')


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
    emit(port+" chosen")


# activate after pressing the button to show the available controllers
@socketio.on('get_list_of_controllers')
def handle_message():
    controllerlist = get_controllers_list()
    emit(controllerlist)


# activate after choosing controller from list
@socketio.on('choose_controller')
def handle_message(controller_name):
    choose_controller(controller_name)
    emit(controller_name+" chosen")


# activate after pressing the button to show the available commands
@socketio.on('get_list_of_commands')
def handle_message():
    commandslist = get_commands_list()
    emit(commandslist)


# activate after choosing command from list
@socketio.on('choose_command')
def handle_message(command_No):
    choose_command(command_No)
    emit(command_No+" chosen")


# activate after choosing port, controller, command, and update(if necessary)
# and pressing the upload button
@socketio.on('upload')
def handle_message():
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


# ----- user management functions ----- #

# activate after pressing the user management button- only for administrator
@socketio.on('user_management')
def handle_message():
    if authorization_code == 3:
        pass
    else:
        raise OSError("Unauthorized action")

""" undone
@socketio.on('create_new_user')
def handle_message(new_username, new_password, author_code):
   result = create_new_user(new_username, new_password, author_code)
   if result....
   emit()"""


@socketio.on('delete_user')
def handle_message():
   pass


@socketio.on('change_user_authorization')
def handle_message():
   pass


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