from flask import Flask
#from flask_socketio import Flask-SocketIO, emit
from flask_socketio import SocketIO, emit
from functions import *
import json

"""
create py_server.exe with: pyinstaller py_server.py -n py-server.py
to create electron app go to dist/py-server and copy content to GUI's public library
than to pack everything to app command: npm run dep-win->for Windows.. (look in package.json for more)
"""
# ----------DO NOT REMOVE THIS SCOPE!!!---------- #
from engineio.async_drivers import gevent

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# ---------UNTIL HERE!!!!! ---------------------- #


# ========================= login window functions ========================= #

# activate after pressing the 'Login' button
@socketio.on('login_attempt')
def handle_message(user_name_details):
    data = json.dumps(user_name_details)
    data = json.loads(data)
    username = data["username"]
    password = data["password"]
    permission = arbitrator(username, password)
    if permission == -3:
        emit('login_response', {'success': 'false', 'message': 'invalid_username_and_password'})
    elif permission == -2:
        emit('login_response', {'success': 'false', 'message': 'invalid_username'})
    elif permission == -1:
        emit('login_response', {'success': 'false', 'message': 'invalid_password'})
    elif permission == 0:
        emit('login_response', {'success': 'false', 'message': 'username_and_password_do_not_match'})
    else:  # successful login
        if permission == 1:
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
    emit('list_of_ports_response', json.dumps(portslist))


# activate after pressing the button to show the available controllers
@socketio.on('get_list_of_controllers')
def handle_message():
    controllerlist = get_controllers_list()
    emit('list_of_controllers_response', json.dumps(controllerlist))


# activate after pressing the button to show the available commands
@socketio.on('get_list_of_commands')
def handle_message():
    commandslist = get_commands_list()
    emit('list_of_commands_response', json.dumps(commandslist))


@socketio.on('get_list_of_users')
def handle_message():
    userslist = get_users_list()
    emit('list_of_users_response', json.dumps(userslist))


# activate after choosing port, controller, command, and update(if necessary)
# and pressing the update program button
# port_name, controller_name, command_No, additional_par
@socketio.on('execute_command')
def handle_message(details):
    # translating arguments from GUI, from JSON to list of strings.
    data = json.dumps(details)
    data = json.loads(data)
    port_name = data["port_name"]
    # if the controller_name field is an empty string (""), so the user send the command to one default controller,
    # else, this field contains the ID of the target controller.
    controller_ID = data["controller_name"]
    command_name = data["command_name"]
    command_No = convert_to_number(command_name)  # input as the command nickname, output as a string number
    additional_par = data["additional_parameters"]

    """ the additional parameters is a dictionary of all the additional parameters the current function demands,
         for example, if some command demands additional parameters than the global fields(port name, cont num...),
         like number of sectors, or list of something or file address to upload from a directory.
         example for json file with additional parameters-
                                   {port name: "COM3",
                                   controller name: "controller_1"
                                   command number: "9"
                                   authorization code: "2"
                                   additional parameters: {"address": "6", "list_of_sectors": ["3","7","0"], "file_name": "user_app.bin"}"""

    # all the sets arguments are groups of commands numbers
    set0 = ['0', '6', '10', '12']
    # simple user tries to execute unauthorized command. server side secure
    if functions.my_authorization == '1' and command_No != '8':
        emit('execute_command_response', {'success': 'false', 'message': 'unauthorized_command_for_simple_user'})
    elif command_No in set0:
        emit('execute_command_response', {'success': 'false', 'message': 'This command is not supported'})
        return
    else:  # all set for executing the command
        socketio.sleep(0)
        result = do_command(port_name, controller_ID, command_No, additional_par, socketio)
        if result == -10:  # unable to connect this port
            emit('execute_command_response', {'success': 'false', 'message': 'port_configuration_error'})
            return
        socketio.sleep(0)
        bootloader_message = json.dumps(functions.bootloader_reply)  # converting the list to JSON
        socketio.sleep(0)

        # all commands in set1 required different types of visual structure to display to the user.
        # each one of the emit functions 'emitting' the correct process details back to the GUI
        set1 = ['1', '2', '3', '4', '11', '13', '14']
        if command_No in set1:
            emit1()
        elif command_No == '5':
            emit2()
        elif command_No == '7':
            emit3()
        elif command_No == '8':
            emit4()
        elif command_No == '9':
            emit5()

        socketio.sleep(0)

        # the down below scopes are required for emitting the bootloader reply back to the GUI.
        if 'Invalid_command_code' in functions.bootloader_reply[0]:
            emit('execute_command_bootloader_response', {'success': 'false', 'message': 'Invalid_command_code'})
        elif 'CRC_FAIL' in functions.bootloader_reply[0]:
            emit('execute_command_bootloader_response', {'success': 'false', 'message': 'CRC_FAIL'})
        elif 'Timeout' in functions.bootloader_reply[0]:
            emit('execute_command_bootloader_response',
                 {'success': 'false', 'message': 'Timeout:_Bootloader_not_responding'})
        elif 'CRC:_SUCCESS' in functions.bootloader_reply[0]:
            emit('execute_command_bootloader_response', {'success': 'true', 'message': bootloader_message})

        clean_process_reply()
        clean_bootloader_reply()


# ------------------- assistance functions for execute command, for emitting the correct message -----------
def emit1():
    emit('execute_command_process_response', {'length': functions.process_reply[0],
                                              'command_code': functions.process_reply[1],
                                              'CRC': functions.process_reply[2]})


def emit2():
    emit('execute_command_process_response', {'length': functions.process_reply[0],
                                              'command_code': functions.process_reply[1],
                                              'memory_address(LE)': functions.process_reply[2],
                                              'CRC': functions.process_reply[3]})


def emit3():
    emit('execute_command_process_response', {'length': functions.process_reply[0],
                                              'command_code': functions.process_reply[1],
                                              'sector_number': functions.process_reply[2],
                                              'number_of_sectors': functions.process_reply[3],
                                              'CRC': functions.process_reply[4]})


def emit4():
    socketio.sleep(0)
    emit('execute_command_process_response', {'length': functions.process_reply[0],
                                              'command_code': functions.process_reply[1],
                                              'base_memory_address(LE)': functions.process_reply[2],
                                              'payload_length': functions.process_reply[3],
                                              'payload': functions.process_reply[4],
                                              'CRC': functions.process_reply[5]})


def emit5():
    emit('execute_command_process_response', {'length': functions.process_reply[0],
                                              'command_code': functions.process_reply[1],
                                              'sector_details': functions.process_reply[2],
                                              'protection_mode': functions.process_reply[3],
                                              'CRC': functions.process_reply[4]})


def convert_to_number(command_name):
    if functions.my_authorization == '1':
        if command_name == 'BL_MEM_WRITE':
            return '8'
    else:
        counter = 1
        list_of_commands = get_commands_list()
        for x in list_of_commands:
            if x['name'] == command_name:
                return str(counter)
            counter += 1


@socketio.on('get_fields')
def handle_message(command_name):
    data = json.dumps(command_name)
    data = json.loads(data)
    name = data['name']
    fields = get_command_fields(name)
    data = json.dumps(fields)
    emit('get_fields_response', data)


@socketio.on('discover_controllers_status_by_port')
def handle_message(port_to_check):
    data = json.dumps(port_to_check)
    data = json.loads(data)
    port = data["port"]
    list_of_connected_controllers = discover_controllers_status_by_port(port, socketio)
    data = {port: list_of_connected_controllers}
    emit('discover_controllers_status_by_port_response', json.dumps(data))


@socketio.on('discover_controllers_status_all_ports')
def handle_message():
    map_of_connected_controllers = discover_controllers_status_all_ports(socketio)
    data = json.dumps(map_of_connected_controllers)
    emit('discover_controllers_status_all_ports_response', data)


# activate after pressing the user management button- only for administrator
@socketio.on('user_management')
def handle_message():
    if my_authorization == 3:
        emit('user_management_response', {'success': 'true', 'message': 'administrator_confirmed'})
    else:
        emit('user_management_response', {'success': 'false', 'message': 'unauthorized_user'})


# create new user - add to database after filling details and pressing register
@socketio.on('register_user')
def handle_message(new_user_details):
    data = json.dumps(new_user_details)
    data = json.loads(data)
    new_username = data["new_user_name"]
    new_password = data["new_password"]
    new_author_code = data["new_authorization_code"]
    if new_author_code != 1 and new_author_code != 2 and new_author_code != 3:
        emit('register_response', {'success': 'false', 'message': 'illegal_authorization_code'})
    else:
        result = create_new_user(new_username, new_password, new_author_code)
        if result == -1:
            emit('register_response', {'success': 'false', 'message': 'unauthorized_command'})
        elif result == 0:
            emit('register_response', {'success': 'false', 'message': 'username_already_in_use'})
        elif result == 1:
            emit('register_response', {'success': 'false', 'message': 'password_already_in_use'})
        elif result == 2:
            emit('register_response', {'success': 'false', 'message': 'username_and_password_already_in_use'})
        elif result == 3:
            emit('register_response', {'success': 'true', 'message': 'new_user_registered_to_system'})


@socketio.on('delete_user')
def handle_message(username_to_del):
    data = json.dumps(username_to_del)
    data = json.loads(data)
    us_to_del = data["username_to_delete"]
    result = delete_user(us_to_del)
    if result == -1:
        emit('delete_user_response', {'success': 'false', 'message': 'unauthorized_command'})
    if result == 0:
        emit('delete_user_response', {'success': 'false', 'message': 'user_is_not_in_list'})
    else:
        emit('delete_user_response', {'success': 'true', 'message': 'user_is_out_of_the_system'})


@socketio.on('change_user_authorization')
def handle_message(details):
    data = json.dumps(details)
    data = json.loads(data)
    username = data["username"]  # the one you want to change
    new_author_code = data["new_authorization"]
    if new_author_code != '1' and new_author_code != '2' and new_author_code != '3':
        emit('change_authorization_response', {'success': 'false', 'message': 'illegal_authorization_code'})
    else:
        result = change_user_authorization(username, new_author_code)
        if result == -1:
            emit('change_authorization_response', {'success': 'false', 'message': 'unauthorized_command'})
        elif result == 0:
            emit('change_authorization_response', {'success': 'false', 'message': 'user_is_not_in_list'})
        elif result == 1:
            emit('change_authorization_response', {'success': 'true', 'message': 'user_authorization_changed'})


@socketio.on('change_user_name')
def handle_message(details):
    data = json.dumps(details)
    data = json.loads(data)
    username = data["username"]  # the one you want to change
    new_user_name = data["new_username"]
    result = change_user_name(username, new_user_name)
    if result == -1:
        emit('change_username_response', {'success': 'false', 'message': 'unauthorized_command'})
    elif result == 0:
        emit('change_username_response', {'success': 'false', 'message': 'user_is_not_in_list'})
    elif result == 1:
        emit('change_username_response', {'success': 'true', 'message': 'user_name_changed'})


@socketio.on('change_password')
def handle_message(details):
    data = json.dumps(details)
    data = json.loads(data)
    username = data["username"]  # the one you want to change
    new_password = data["new_password"]
    result = change_user_password(username, new_password)
    if result == -1:
        emit('change_password_response', {'success': 'false', 'message': 'unauthorized_command'})
    elif result == 0:
        emit('change_password_response', {'success': 'false', 'message': 'user_is_not_in_list'})
    elif result == 1:
        emit('change_username_response', {'success': 'true', 'message': 'password_changed'})


@socketio.on('my_profile')
def handle_message():
    my_profile = {'username': functions.my_username,
                  'password': functions.my_password, 'authorization': functions.my_authorization}
    emit('my_profile_response', json.dumps(my_profile))


@socketio.on('logout_attempt')
def handle_message():
    init_my_profile()
    Close_serial_port()


@socketio.on('reset_ports')
def handle_message():
    purge_serial_port()
    Close_serial_port()


@socketio.on('is_connected')
def handle_message():
    if functions.my_authorization == "":
        emit('is_connected_response', {'success': 'false'})
    else:
        emit('is_connected_response', {'success': 'true'})


def emit_port_configuration_message(port_configuration_message):
    emit('port_configuration_response', {'message': port_configuration_message})
    return


if __name__ == '__main__':
    init_my_profile()
    print('running on port 5000')  # default port of flask is 5000
    socketio.run(app)
