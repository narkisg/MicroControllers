from backend.STM32_Programmer_V1 import *

# ==============fields=================
port_name = None
controller_name = None
command_number = None

# ==============functions===============
def do_command():
    if port_name is not None and controller_name is not None and command_number is not None:
        execute_command(port_name, controller_name, command_number)

def choose_port(portName):
    port_name = portName
    ret = Serial_Port_Configuration(portName)


def choose_controller(controllerName):
    controller_name = controllerName


def choose_command(commandNo):
    command_number = commandNo


def exit_system():
    return decode_menu_command_code(command=0)


def list_of_commands():
    return List_Of_Commands


def list_of_ports():
    return List_Of_Ports


"""def get_ver():
    return decode_menu_command_code(command=1)


def get_help():
    return decode_menu_command_code(command=2)


def get_cid():
    return decode_menu_command_code(command=3)


def get_status():
    return decode_menu_command_code(command=4)


def go_to_addr():
    return decode_menu_command_code(command=5)


def flash_erase():
    return decode_menu_command_code(command=7)


def mem_write():
    return decode_menu_command_code(command=8)


def en_r_w_protect():
    return decode_menu_command_code(command=9)


def mem_read():
    return decode_menu_command_code(command=10)


def read_sector_status():
    return decode_menu_command_code(command=11)


def opt_read():
    return decode_menu_command_code(command=12)


def dis_r_w_protect():
    return decode_menu_command_code(command=13)


def my_new_command():
    return decode_menu_command_code(14)
"""


