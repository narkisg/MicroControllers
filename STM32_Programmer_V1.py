import serial
import struct
import os
import sys
import glob
import functions

Flash_HAL_OK = 0x00
Flash_HAL_ERROR = 0x01
Flash_HAL_BUSY = 0x02
Flash_HAL_TIMEOUT = 0x03
Flash_HAL_INV_ADDR = 0x04

# BL Commands
COMMAND_BL_GET_VER = 0x51
COMMAND_BL_GET_HELP = 0x52
COMMAND_BL_GET_CID = 0x53
COMMAND_BL_GET_RDP_STATUS = 0x54
COMMAND_BL_GO_TO_ADDR = 0x55
COMMAND_BL_FLASH_ERASE = 0x56
COMMAND_BL_MEM_WRITE = 0x57
COMMAND_BL_EN_R_W_PROTECT = 0x58
COMMAND_BL_MEM_READ = 0x59
COMMAND_BL_READ_SECTOR_P_STATUS = 0x5A
COMMAND_BL_OTP_READ = 0x5B
COMMAND_BL_DIS_R_W_PROTECT = 0x5C
COMMAND_BL_MY_NEW_COMMAND = 0x5D

# len details of the command
COMMAND_BL_GET_VER_LEN = 6
COMMAND_BL_GET_HELP_LEN = 6
COMMAND_BL_GET_CID_LEN = 6
COMMAND_BL_GET_RDP_STATUS_LEN = 6
COMMAND_BL_GO_TO_ADDR_LEN = 10
COMMAND_BL_FLASH_ERASE_LEN = 8
COMMAND_BL_MEM_WRITE_LEN = 11
COMMAND_BL_EN_R_W_PROTECT_LEN = 8
COMMAND_BL_READ_SECTOR_P_STATUS_LEN = 6
COMMAND_BL_DIS_R_W_PROTECT_LEN = 6
COMMAND_BL_MY_NEW_COMMAND_LEN = 8

verbose_mode = 1
mem_write_active = 0


# ----------------------------- file ops----------------------------------------

def calc_file_len():
    size = os.path.getsize("user_app.bin")
    return size


def my_calc_file_len(file):
    size = os.path.getsize(file)
    return size


def open_the_file():
    global bin_file
    bin_file = open('user_app.bin', 'rb')
    # read = bin_file.read()
    # global file_contents = bytearray(read)


def my_open_the_file(file):
    global bin_file
    bin_file = open(file, 'rb')
    # read = bin_file.read()
    # global file_contents = bytearray(read)


def confirm_controller_ID(my_controller, controller_ID):
    controller_ID = hex(int(controller_ID, 16))
    return my_controller == controller_ID


def read_the_file():
    pass


def close_the_file():
    bin_file.close()


# ----------------------------- utilities----------------------------------------


def word_to_byte(addr, index, lowerfirst):
    value = (addr >> (8 * (index - 1)) & 0x000000FF)
    return value


def get_crc(buff, length, initial_index):
    Crc = 0xFFFFFFFF
    # print(length)
    for data in buff[initial_index:length]:
        Crc = Crc ^ data
        for i in range(32):
            if (Crc & 0x80000000):
                Crc = (Crc << 1) ^ 0x04C11DB7
            else:
                Crc = (Crc << 1)
    return Crc


# ----------------------------- Serial Port ----------------------------------------
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def Serial_Port_Configuration(port):
    global ser
    try:
        ser = serial.Serial(port, 115200, timeout=2)
    except:
        # print("\n   Oops! That was not a valid port")
        functions.port_configuration_message('Oops! That was not a valid port')

        port = serial_ports()
        if (not port):
            # print("\n   No ports Detected")
            functions.port_configuration_message('No ports Detected')
        else:
            # print("\n   Here are some available ports on your PC. Try Again!")
            functions.port_configuration_message('Here are some available ports on your PC. Try Again!')
            # print("\n   ", port)
        return -1
    if ser.is_open:
        # print("\n   Port Open Success")
        functions.port_configuration_message('Port Open Success connected to port: ' + port)
        functions.is_connected_to_port = port
    else:
        # print("\n   Port Open Failed")
        functions.port_configuration_message('Port Open Failed')

    return 0


def read_serial_port(length):
    read_value = ser.read(length)
    return read_value


def Close_serial_port():
    # pass
    ser.close()


def purge_serial_port():
    ser.reset_input_buffer()


def Write_to_serial_port(value, *length, socket):
    print("------------write to serial port-------------")
    data = struct.pack('>B', value)
    if (verbose_mode):
        value = bytearray(data)
        # print("   "+hex(value[0]), end='')
        # print("   "+"0x{:02x}".format(value[0]), end=' ')
        functions.print_process_args("0x{:02x}".format(value[0]))
    if (mem_write_active and (not verbose_mode)):
        # print("#", end=' ')
        functions.print_process_args("#")
    socket.sleep(0)
    print("start ser.write with data:")
    print(data)
    ser.write(data)
    print("done ser.write")
# ----------------------------- command processing----------------------------------------


def process_COMMAND_BL_MY_NEW_COMMAND(length):
    pass


def process_COMMAND_BL_GET_VER(length):
    ver = read_serial_port(1)
    value = bytearray(ver)
    # print("\n   Bootloader Ver. : ", hex(value[0]))
    functions.print_bootloader_args('Bootloader Ver. : ' + hex(value[0]))


def process_COMMAND_BL_GET_HELP(length):
    # print("reading:", length)
    value = read_serial_port(length)
    reply = bytearray(value)
    # print("\n   Supported Commands :", end=' ')
    boot_message = 'Supported Commands : '
    for x in reply:
        # print(hex(x), end=' ')
        boot_message = boot_message + ', ' + hex(x)
    # print()
    functions.print_bootloader_args(boot_message)


def process_COMMAND_BL_GET_CID(length):
    value = read_serial_port(length)
    ci = (value[1] << 8) + value[0]
    # print("\n   Chip Id. : ", hex(ci))
    functions.print_bootloader_args('Chip Id. : ' + hex(ci))


def process_COMMAND_BL_GET_RDP_STATUS(length):
    value = read_serial_port(length)
    rdp = bytearray(value)
    # print("\n   RDP Status : ", hex(rdp[0]))
    functions.print_bootloader_args('RDP Status : ' + hex(rdp[0]))


def process_COMMAND_BL_GO_TO_ADDR(length):
    addr_status = 0
    value = read_serial_port(length)
    addr_status = bytearray(value)
    # print("\n   Address Status : ", hex(addr_status[0]))
    functions.print_bootloader_args('Address Status : ' + hex(addr_status[0]))


def process_COMMAND_BL_FLASH_ERASE(length):
    erase_status = 0
    value = read_serial_port(length)
    if len(value):
        erase_status = bytearray(value)
        if (erase_status[0] == Flash_HAL_OK):
            # print("\n   Erase Status: Success  Code: FLASH_HAL_OK")
            functions.print_bootloader_args('Erase Status: Success  Code: FLASH_HAL_OK')
        elif (erase_status[0] == Flash_HAL_ERROR):
            # print("\n   Erase Status: Fail  Code: FLASH_HAL_ERROR")
            functions.print_bootloader_args('Erase Status: Fail  Code: FLASH_HAL_ERROR')
        elif (erase_status[0] == Flash_HAL_BUSY):
            # print("\n   Erase Status: Fail  Code: FLASH_HAL_BUSY")
            functions.print_bootloader_args('Erase Status: Fail  Code: FLASH_HAL_BUSY')
        elif (erase_status[0] == Flash_HAL_TIMEOUT):
            # print("\n   Erase Status: Fail  Code: FLASH_HAL_TIMEOUT")
            functions.print_bootloader_args('Erase Status: Fail  Code: FLASH_HAL_TIMEOUT')
        elif (erase_status[0] == Flash_HAL_INV_ADDR):
            # print("\n   Erase Status: Fail  Code: FLASH_HAL_INV_SECTOR")
            functions.print_bootloader_args('Erase Status: Fail  Code: FLASH_HAL_INV_SECTOR')
        else:
            # print("\n   Erase Status: Fail  Code: UNKNOWN_ERROR_CODE")
            functions.print_bootloader_args('Erase Status: Fai,  Code: UNKNOWN_ERROR_CODE')
    else:
        # print("Timeout: Bootloader is not responding")
        functions.print_bootloader_args('Timeout: Bootloader is not responding')


def process_COMMAND_BL_MEM_WRITE(length):
    write_status = 0
    value = read_serial_port(length)
    write_status = bytearray(value)
    if (write_status[0] == Flash_HAL_OK):
        # print("\n   Write_status: FLASH_HAL_OK")
        functions.print_bootloader_args('Write_status: FLASH_HAL_OK')
    elif (write_status[0] == Flash_HAL_ERROR):
        # print("\n   Write_status: FLASH_HAL_ERROR")
        functions.print_bootloader_args('FLASH_HAL_ERROR')
    elif (write_status[0] == Flash_HAL_BUSY):
        # print("\n   Write_status: FLASH_HAL_BUSY")
        functions.print_bootloader_args('FLASH_HAL_BUSY')
    elif (write_status[0] == Flash_HAL_TIMEOUT):
        # print("\n   Write_status: FLASH_HAL_TIMEOUT")
        functions.print_bootloader_args('FLASH_HAL_TIMEOUT')
    elif (write_status[0] == Flash_HAL_INV_ADDR):
        # print("\n   Write_status: FLASH_HAL_INV_ADDR")
        functions.print_bootloader_args('FLASH_HAL_INV_ADDR')
    else:
        # print("\n   Write_status: UNKNOWN_ERROR")
        functions.print_bootloader_args('UNKNOWN_ERROR')
    # print("\n")


def process_COMMAND_BL_FLASH_MASS_ERASE(length):
    pass


protection_mode = ["Write Protection",
                   "Read/Write Protection", "No protection"]


def protection_type(status, n):
    if (status & (1 << 15)):
        # PCROP is active
        if (status & (1 << n)):
            return protection_mode[1]
        else:
            return protection_mode[2]
    else:
        if (status & (1 << n)):
            return protection_mode[2]
        else:
            return protection_mode[0]


def process_COMMAND_BL_READ_SECTOR_STATUS(length):
    s_status = 0
    value = read_serial_port(length)
    s_status = bytearray(value)
    # s_status.flash_sector_status = (uint16_t)(status[1] << 8 | status[0] )
    # print("\n   Sector Status : ", s_status[0])
    # print("\n  ====================================")
    # print("\n  Sector                               \tProtection")
    # print("\n  ====================================")
    boot_message = "Sector Status : " + str(s_status[
                                                0]) + "\n  ====================================" + 'Sector                               \tProtection' + '\n  ===================================='
    functions.print_bootloader_args(boot_message)
    if (s_status[0] & (1 << 15)):
        # PCROP is active
        # print("\n  Flash protection mode : Read/Write Protection(PCROP)\n")
        functions.print_bootloader_args('Flash protection mode : Read/Write Protection(PCROP)')
    else:
        # print("\n  Flash protection mode :   \tWrite Protection\n")
        functions.print_bootloader_args('Flash protection mode :   \tWrite Protection')
    boot_message2 = ''
    for x in range(8):
        # print("\n   Sector{0}                               {1}".format(
        # x, protection_type(s_status[0], x)))
        boot_message2 = boot_message2 + 'Sector{0}                               {1}'.format(
            x, protection_type(s_status[0], x))
    functions.print_bootloader_args(boot_message2)


def process_COMMAND_BL_DIS_R_W_PROTECT(length):
    status = 0
    value = read_serial_port(length)
    status = bytearray(value)
    if (status[0]):
        # print("\n   FAIL")
        functions.print_bootloader_args('FAIL')
    else:
        # print("\n   SUCCESS")
        functions.print_bootloader_args('SUCCESS')


def process_COMMAND_BL_EN_R_W_PROTECT(length):
    status = 0
    value = read_serial_port(length)
    status = bytearray(value)
    if (status[0]):
        functions.print_bootloader_args('FAIL')
    else:
        functions.print_bootloader_args('SUCCESS')


def initialize_data_buf():
    output = []
    for i in range(255):
        output.append(0)
    return output


def convert_from_string(string):
    output = []
    for x in string:
        output.append(x)
    return output


def decode_menu_command_code(controller_ID, command, additional_par, socket):
    ret_value = 0
    data_buf = initialize_data_buf()
    command = int(command, 10)
    is_directed_to_specific_controller = True
    shift = 0
    if controller_ID == '':  # No controller is defined
        is_directed_to_specific_controller = False
        shift = 1
    else:
        controller_ID = int(controller_ID)

    if (command == 0):
        # print("\n   Exiting...!") this line is for manual debugging
        raise SystemExit

    elif (command == 1):
        print("start get version")
        COMMAND_BL_GET_VER_LEN = 6
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_GET_VER_LEN - 1
        data_buf[2] = COMMAND_BL_GET_VER
        crc32 = get_crc(data_buf, COMMAND_BL_GET_VER_LEN - 4, shift)
        crc32 = crc32 & 0xffffffff
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_GET_VER_LEN]:
            Write_to_serial_port(i, COMMAND_BL_GET_VER_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])


    elif (command == 2):
        COMMAND_BL_GET_HELP_LEN = 6
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_GET_HELP_LEN - 1
        data_buf[2] = COMMAND_BL_GET_HELP
        crc32 = get_crc(data_buf, COMMAND_BL_GET_HELP_LEN - 4, shift)
        crc32 = crc32 & 0xffffffff
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_GET_HELP_LEN]:
            Write_to_serial_port(i, COMMAND_BL_GET_HELP_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    elif (command == 3):
        COMMAND_BL_GET_CID_LEN = 6
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_GET_CID_LEN - 1
        data_buf[2] = COMMAND_BL_GET_CID
        crc32 = get_crc(data_buf, COMMAND_BL_GET_CID_LEN - 4, shift)
        crc32 = crc32 & 0xffffffff
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_GET_CID_LEN]:
            Write_to_serial_port(i, COMMAND_BL_GET_CID_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    elif (command == 4):
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_GET_RDP_STATUS_LEN - 1
        data_buf[2] = COMMAND_BL_GET_RDP_STATUS
        crc32 = get_crc(data_buf, COMMAND_BL_GET_RDP_STATUS_LEN - 4, shift)
        crc32 = crc32 & 0xffffffff
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_GET_RDP_STATUS_LEN]:
            Write_to_serial_port(i, COMMAND_BL_GET_RDP_STATUS_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    elif (command == 5):
        go_address = additional_par["address"]
        go_address = '0x0800A000'  # for debugging
        go_address = int(go_address, 16)
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_GO_TO_ADDR_LEN - 1
        data_buf[2] = COMMAND_BL_GO_TO_ADDR
        data_buf[3] = word_to_byte(go_address, 1, 1)
        data_buf[4] = word_to_byte(go_address, 2, 1)
        data_buf[5] = word_to_byte(go_address, 3, 1)
        data_buf[6] = word_to_byte(go_address, 4, 1)
        crc32 = get_crc(data_buf, COMMAND_BL_GO_TO_ADDR_LEN - 4, shift)
        data_buf[7] = word_to_byte(crc32, 1, 1)
        data_buf[8] = word_to_byte(crc32, 2, 1)
        data_buf[9] = word_to_byte(crc32, 3, 1)
        data_buf[10] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_GO_TO_ADDR_LEN]:
            Write_to_serial_port(i, COMMAND_BL_GO_TO_ADDR_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    # elif(command == 6):
    # print("\n   This command is not supported")

    elif (command == 7):
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_FLASH_ERASE_LEN - 1
        data_buf[2] = COMMAND_BL_FLASH_ERASE
        sector_num = additional_par["sector_number"]
        sector_num = int(sector_num, 16)
        nsec = ""
        if (sector_num != 0xff):
            nsec = additional_par["number_of_sectors_to_erase"]
            nsec = int(nsec, 16)
            # nsec = int(input("\n   Enter number of sectors to erase(max 8) here :"))

        data_buf[3] = sector_num
        data_buf[4] = nsec

        crc32 = get_crc(data_buf, COMMAND_BL_FLASH_ERASE_LEN - 4, shift)
        data_buf[5] = word_to_byte(crc32, 1, 1)
        data_buf[6] = word_to_byte(crc32, 2, 1)
        data_buf[7] = word_to_byte(crc32, 3, 1)
        data_buf[8] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_FLASH_ERASE_LEN]:
            Write_to_serial_port(i, COMMAND_BL_FLASH_ERASE_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    elif (command == 8):
        functions.port_configuration_message('memory write starts')
        bytes_remaining = 0
        t_len_of_file = 0
        bytes_so_far_sent = 0
        len_to_read = 0
        base_mem_address = 0
        data_buf[0] = controller_ID
        data_buf[2] = COMMAND_BL_MEM_WRITE

        # First get the total number of bytes in the .bin file.
        t_len_of_file = my_calc_file_len(additional_par['file_name'])
        my_open_the_file(additional_par["file_name"])
        bytes_remaining = t_len_of_file - bytes_so_far_sent
        base_mem_address = additional_par["address"]
        base_mem_address = '0x0800A000'  # for debugging
        base_mem_address = int(base_mem_address, 16)
        global mem_write_active
        while (bytes_remaining):
            socket.sleep(0)
            mem_write_active = 1
            if (bytes_remaining >= 128):
                len_to_read = 128
            else:
                len_to_read = bytes_remaining
            # get the bytes in to buffer by reading file
            for x in range(len_to_read):
                socket.sleep(0)
                file_read_value = bin_file.read(1)
                file_read_value = bytearray(file_read_value)
                data_buf[8 + x] = int(file_read_value[0])
            # read_the_file(&data_buf[7],len_to_read)
            # print("\n   base mem address = \n",base_mem_address, hex(base_mem_address))

            # populate base mem address
            data_buf[3] = word_to_byte(base_mem_address, 1, 1)
            data_buf[4] = word_to_byte(base_mem_address, 2, 1)
            data_buf[5] = word_to_byte(base_mem_address, 3, 1)
            data_buf[6] = word_to_byte(base_mem_address, 4, 1)
            data_buf[7] = len_to_read

            # /* 1 byte len + 1 byte command code + 4 byte mem base address
            # * 1 byte payload len + len_to_read is amount of bytes read from file + 4 byte CRC
            # */
            mem_write_cmd_total_len = COMMAND_BL_MEM_WRITE_LEN + len_to_read

            # first field is "len_to_follow"
            data_buf[1] = mem_write_cmd_total_len - 1

            crc32 = get_crc(data_buf, mem_write_cmd_total_len - 4, shift)
            data_buf[8 + len_to_read] = word_to_byte(crc32, 1, 1)
            data_buf[9 + len_to_read] = word_to_byte(crc32, 2, 1)
            data_buf[10 + len_to_read] = word_to_byte(crc32, 3, 1)
            data_buf[11 + len_to_read] = word_to_byte(crc32, 4, 1)

            # update base mem address for the next loop
            base_mem_address += len_to_read

            if not is_directed_to_specific_controller:  # one controller is connected
                data_buf.pop(0)  # removes the controller_ID from list

            Write_to_serial_port(data_buf[0], 1, socket=socket)
            socket.sleep(0)
            for i in data_buf[1:mem_write_cmd_total_len]:
                socket.sleep(0)
                Write_to_serial_port(i, mem_write_cmd_total_len - 1, socket=socket)
            socket.sleep(0)
            bytes_so_far_sent += len_to_read
            bytes_remaining = t_len_of_file - bytes_so_far_sent
            # print("\n   bytes_so_far_sent:{0} -- bytes_remaining:{1}\n".format(bytes_so_far_sent, bytes_remaining))
            functions.port_configuration_message(
                "bytes_so_far_sent:{0} -- bytes_remaining:{1}\n".format(bytes_so_far_sent, bytes_remaining))
            socket.sleep(0)
            ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1 + shift])
            if 'ERROR!' in functions.bootloader_reply[0]:
                break
        mem_write_active = 0

    elif (command == 9):
        total_sector = additional_par["total_sector"]
        total_sector = int(total_sector, 10)
        sector_numbers = [0, 0, 0, 0, 0, 0, 0, 0]
        sector_details = 0
        list_of_sector_numbers = convert_from_string(additional_par['list_of_sector_numbers'])
        for x in range(total_sector):
            sector_numbers[x] = int(list_of_sector_numbers[x].format(x + 1))
            sector_details = sector_details | (1 << sector_numbers[x])

        mode = additional_par["mode"]
        mode = int(mode)
        if (mode != 2 and mode != 1):
            functions.print_process_args("Invalid option : Command Dropped")
            return
        if (mode == 2):
            functions.print_process_args("This feature is currently not supported !")
            return

        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_EN_R_W_PROTECT_LEN - 1
        data_buf[2] = COMMAND_BL_EN_R_W_PROTECT
        data_buf[3] = sector_details
        data_buf[4] = mode
        crc32 = get_crc(data_buf, COMMAND_BL_EN_R_W_PROTECT_LEN - 4, shift)
        data_buf[5] = word_to_byte(crc32, 1, 1)
        data_buf[6] = word_to_byte(crc32, 2, 1)
        data_buf[7] = word_to_byte(crc32, 3, 1)
        data_buf[8] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_EN_R_W_PROTECT_LEN]:
            Write_to_serial_port(i, COMMAND_BL_EN_R_W_PROTECT_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    # elif(command == 10):
    # print("\n   Command == > COMMAND_BL_MEM_READ")
    # print("\n   This command is not supported")

    elif (command == 11):
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_READ_SECTOR_P_STATUS_LEN - 1
        data_buf[2] = COMMAND_BL_READ_SECTOR_P_STATUS

        crc32 = get_crc(data_buf, COMMAND_BL_READ_SECTOR_P_STATUS_LEN - 4, shift)
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)


        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_READ_SECTOR_P_STATUS_LEN]:
            Write_to_serial_port(i, COMMAND_BL_READ_SECTOR_P_STATUS_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    # elif(command == 12):
    # print("\n   Command == > COMMAND_OTP_READ")
    # print("\n   This command is not supported")

    elif (command == 13):
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_DIS_R_W_PROTECT_LEN - 1
        data_buf[2] = COMMAND_BL_DIS_R_W_PROTECT
        crc32 = get_crc(data_buf, COMMAND_BL_DIS_R_W_PROTECT_LEN - 4, shift)
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1)
        for i in data_buf[1:COMMAND_BL_DIS_R_W_PROTECT_LEN]:
            Write_to_serial_port(i, COMMAND_BL_DIS_R_W_PROTECT_LEN - 1)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    elif (command == 14):
        data_buf[0] = controller_ID
        data_buf[1] = COMMAND_BL_MY_NEW_COMMAND_LEN - 1
        data_buf[2] = COMMAND_BL_MY_NEW_COMMAND
        crc32 = get_crc(data_buf, COMMAND_BL_MY_NEW_COMMAND_LEN - 4, shift)
        data_buf[3] = word_to_byte(crc32, 1, 1)
        data_buf[4] = word_to_byte(crc32, 2, 1)
        data_buf[5] = word_to_byte(crc32, 3, 1)
        data_buf[6] = word_to_byte(crc32, 4, 1)

        if not is_directed_to_specific_controller:  # one controller is connected
            data_buf.pop(0)  # removes the controller_ID from list

        Write_to_serial_port(data_buf[0], 1, socket=socket)
        for i in data_buf[1:COMMAND_BL_MY_NEW_COMMAND_LEN]:
            Write_to_serial_port(i, COMMAND_BL_MY_NEW_COMMAND_LEN - 1, socket=socket)

        ret_value = read_bootloader_reply(shift, controller_ID, data_buf[1+shift])

    return ret_value


def read_bootloader_reply(shift, controller_ID, command_code):
    ret_value = -2
    ack = read_serial_port(2 + shift)
    if (len(ack)):
        if shift == 1:
            match = confirm_controller_ID(controller_ID, ack[0])
            if not match:
                functions.print_bootloader_args("MATCH ERROR! Controller " + str(
                    ack[0]) + " receives the command instead of controller " + controller_ID)
                return ret_value

        a_array = bytearray(ack)
        # print("read uart:",ack)
        if (a_array[0 + shift] == 0xA5):
            # CRC of last command was good .. received ACK and "len to follow"
            len_to_follow = a_array[1 + shift]
            # print("\n   CRC : SUCCESS Len :",len_to_follow)
            functions.print_bootloader_args("CRC:_SUCCESS,Len:_ " + str(len_to_follow))
            # print("command_code:",hex(command_code))
            if (command_code) == COMMAND_BL_GET_VER:
                process_COMMAND_BL_GET_VER(len_to_follow)

            elif (command_code) == COMMAND_BL_GET_HELP:
                process_COMMAND_BL_GET_HELP(len_to_follow)

            elif (command_code) == COMMAND_BL_GET_CID:
                process_COMMAND_BL_GET_CID(len_to_follow)

            elif (command_code) == COMMAND_BL_GET_RDP_STATUS:
                process_COMMAND_BL_GET_RDP_STATUS(len_to_follow)

            elif (command_code) == COMMAND_BL_GO_TO_ADDR:
                process_COMMAND_BL_GO_TO_ADDR(len_to_follow)

            elif (command_code) == COMMAND_BL_FLASH_ERASE:
                process_COMMAND_BL_FLASH_ERASE(len_to_follow)

            elif (command_code) == COMMAND_BL_MEM_WRITE:
                process_COMMAND_BL_MEM_WRITE(len_to_follow)

            elif (command_code) == COMMAND_BL_READ_SECTOR_P_STATUS:
                process_COMMAND_BL_READ_SECTOR_STATUS(len_to_follow)

            elif (command_code) == COMMAND_BL_EN_R_W_PROTECT:
                process_COMMAND_BL_EN_R_W_PROTECT(len_to_follow)

            elif (command_code) == COMMAND_BL_DIS_R_W_PROTECT:
                process_COMMAND_BL_DIS_R_W_PROTECT(len_to_follow)

            elif (command_code) == COMMAND_BL_MY_NEW_COMMAND:
                process_COMMAND_BL_MY_NEW_COMMAND(len_to_follow)

            else:
                # print("\n   Invalid command code\n")
                functions.print_bootloader_args("ERROR! Invalid_command_code")

            ret_value = 0

        elif a_array[0 + shift] == 0x7F:
            # CRC of last command was bad .. received NACK
            # print("\n   CRC: FAIL \n")
            functions.print_bootloader_args("ERROR! CRC_FAIL")
            ret_value = -1
    else:
        # print("\n   Timeout : Bootloader not responding")
        functions.print_bootloader_args("ERROR! Timeout:_Bootloader_not_responding")
    return ret_value


def execute_command(port_name, controller_ID, command_code, additional_par, socket):
    name = port_name
    if functions.is_connected_to_port != name:
        ret = Serial_Port_Configuration(name)
        if ret < 0:
            return -10
    result = decode_menu_command_code(controller_ID, command_code, additional_par, socket)
    purge_serial_port()
    return result


def check_flash_status():
    pass


def protection_type():
    pass
