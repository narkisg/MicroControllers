from flask import Flask
from flask_socketio import SocketIO, emit

#---------DO NOT REMOVE THIS LINE!!--------#
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


@socketio.on('choose_port')
def handle_message(port_name):
    choose_port(port_name)
    emit(port_name+" chosen")


@socketio.on('choose_controller')
def handle_message(controller_name):
    choose_controller(controller_name)
    emit(controller_name+" chosen")


@socketio.on('choose_command')
def handle_message(command_No):
    choose_command(command_No)
    # add if statements for each command separately
    emit(command_No+" chosen")


@socketio.on('list_of_commands')
def handle_message():
    emit(List_Of_Commands)


@socketio.on('list_of_ports')
def handle_message():
    emit(list_of_ports)


@socketio.on('upload')
def handle_message():
    do_command()
    emit("update has been uploaded successfully")


"""
@socketio.on('exit')
def handle_message():
    exit_system()
    emit('exit')


@socketio.on('get_ver')
def handle_message():
    get_ver()
    emit('get_ver_done')


@socketio.on('get_help')
def handle_message():
    get_help()
    emit('')


@socketio.on('get_cid')
def handle_message():
    get_cid()
    emit('get_cid_done')


@socketio.on('get_status')
def handle_message():
    get_status()
    emit('get_status_done')


@socketio.on('go_to_address')
def handle_message():
    go_to_addr()
    emit('')


@socketio.on('flash_erase')
def handle_message():
    flash_erase()
    emit('flash_erase_done')


@socketio.on('mem_write')
def handle_message():
    mem_write()
    emit('mem_write_done')


@socketio.on('en_r_w_protect')
def handle_message():
    en_r_w_protect()
    emit('en_r_w_is_protected')


@socketio.on('mem_read')
def handle_message():
    mem_read()
    emit('')


@socketio.on('read_sector_status')
def handle_message():
    read_sector_status()
    emit('')


@socketio.on('opt_read')
def handle_message():
    opt_read()
    emit('')


@socketio.on('dis_r_w_protect')
def handle_message():
    dis_r_w_protect()
    emit('dis_r_w_done')


@socketio.on('my_new_command')
def handle_message():
    my_new_command()
    emit('your new command executed')
"""


if __name__ == '__main__':
    print('running on port 5000')
    socketio.run(app)