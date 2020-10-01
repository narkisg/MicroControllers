
from backend.global_vars_setting import *
from backend.functions import *
from backend.STM32_Programmer_V1 import *


def permission_1():
    while True:
        print('\n simple user successfully logged in!')
        print("\n what do you want to do now?\n")
        print("\n  your only options are:")
        print("\n   BL_MEM_WRITE        --> 8")
        print("   VIEW MY PROFILE     --> 16")
        print("   LOGOUT              --> 0")
        print("   GO BACK             --> -1")

        command = int(input("\n insert your command from above here :"))
        if command != 8 and command != 0 and command != 16 and command != -1:
            print('unauthorized command maddafacka!')
        elif command == 0:
            do_command("", "", 0, "")
        elif command == 16:
            my_profile()
        elif command == -1:
            break
        else:
            port = str(input("\n insert your port name here :"))
            cont = str(input("\n from controller 1-1000,\n insert your controller name here :"))
            file = str(input("\n insert your the directory name here :"))
            do_command(port, cont, command, file, "")

def permission_2():
    while True:
        print('\n developer user successfully logged in!')
        print("\n what do you want to do now?")
        print("\n your options are:\n")
        print("   GO BACK                               --> -1")
        print("   LOGOUT                                --> 0")
        print("   BL_GET_VER                            --> 1")
        print("   BL_GET_HLP                            --> 2")
        print("   BL_GET_CID                            --> 3")
        print("   BL_GET_RDP_STATUS                     --> 4")
        print("   BL_GO_TO_ADDR                         --> 5")
        print("   BL_FLASH_MASS_ERASE                   --> 6")
        print("   BL_FLASH_ERASE                        --> 7")
        print("   BL_MEM_WRITE                          --> 8")
        print("   BL_EN_R_W_PROTECT                     --> 9")
        print("   BL_MEM_READ                           --> 10")
        print("   BL_READ_SECTOR_P_STATUS               --> 11")
        print("   BL_OTP_READ                           --> 12")
        print("   BL_DIS_R_W_PROTECT                    --> 13")
        print("   BL_MY_NEW_COMMAND                     --> 14")
        print("   VIEW MY PROFILE                       --> 16")

        command = int(input("\n please insert your command here :"))
        if not is_legal(command):
            print("\n illegal command!")
        elif command == -1:
            break
        elif command == 0:
            do_command("", "", 0, "")
        elif command == 15:
            print('unauthorized command maddafacka!')
        elif command == 16:
            my_profile()
        else:
            port = str(input("\n insert your port name here :"))
            cont = str(input("\n from controller 1-1000,\n insert your controller name here :"))
            additional_par = ""
            if command == 5 or command == 8:
                address = str(input("\n this command demands address.\n please insert your address here: "))
                additional_par = {"address": address}
            do_command(port, cont, command, additional_par)

            if command == 7:
                print("\n this command demands more info from user\n")
                sector_number = str(input("\n insert sector number here: (0-8 decimal)"))
                nsec = str(input("\n insert number of sectors to erase here: (0-7 decimal)"))
                additional_par = {"sector number": sector_number, "number of sectors to erase": nsec}
                do_command(port, cont, command, additional_par)

            elif command == 9:
                print("\n this command demands more info from user\n")
                total_sector = str(input("\n insert number of sectors to protect here: (0-8 decimal)"))
                n = int(total_sector, 10)
                list_of_sector_numbers = list(input('\n insert list of sector numbers,\n'
                                                    'with' + str(
                    n) + ' numbers, no intervals (2567...) here: '))
                additional_par = {"number of sectors to protect": n,
                                  "list of sector numbers": list_of_sector_numbers}
                do_command(port, cont, command, additional_par)

def permission_3():
    while True:
        print('\n administrator user successfully logged in!')
        print("\n what do you want to do now?")
        print("\n your options are:\n")
        print("   GO BACK                               --> -1")
        print("   LOGOUT                                --> 0")
        print("   BL_GET_VER                            --> 1")
        print("   BL_GET_HLP                            --> 2")
        print("   BL_GET_CID                            --> 3")
        print("   BL_GET_RDP_STATUS                     --> 4")
        print("   BL_GO_TO_ADDR                         --> 5")
        print("   BL_FLASH_MASS_ERASE                   --> 6")
        print("   BL_FLASH_ERASE                        --> 7")
        print("   BL_MEM_WRITE                          --> 8")
        print("   BL_EN_R_W_PROTECT                     --> 9")
        print("   BL_MEM_READ                           --> 10")
        print("   BL_READ_SECTOR_P_STATUS               --> 11")
        print("   BL_OTP_READ                           --> 12")
        print("   BL_DIS_R_W_PROTECT                    --> 13")
        print("   BL_MY_NEW_COMMAND                     --> 14")
        print("   USER_MANAGEMENT                       --> 15")
        print("   VIEW MY PROFILE                       --> 16")

        command = int(input("\n please insert your command here :"))
        if not is_legal(command):
            print("\n illegal command!")

        elif command == -1:
            break

        elif command == 0:
            do_command("", "", 0, "")

        elif command == 15:
            user_management()

        elif command == 16:
            my_profile()

        else:
            port = input("\n insert your port name here :")
            cont = input("\n from controller 1-1000,\n insert your controller name here :")
            additional_par = ""
            if command == 5 or command == 8:
                address = input("\n this command demands address.\n please insert your address here: ")
                additional_par = {"address": address}
                do_command(port, cont, command, additional_par)

            elif command == 7:
                print("\n this command demands more info from user\n")
                sector_number = input("\n please insert sector number here: (0-8 decimal)")
                nsec = str(input("\n insert number of sectors to erase here: (0-7 decimal)"))
                additional_par = {"sector number": sector_number, "number of sectors to erase": nsec}
                do_command(port, cont, command, additional_par)

            elif command == 9:
                print("\n this command demands more info from user\n")
                total_sector = str(input("\n insert number of sectors to protect here: (0-8 decimal)"))
                n = int(total_sector, 10)
                list_of_sector_numbers = list(input('\n insert list of sector numbers,\n'
                                                    'with' + str(
                    n) + ' numbers, no intervals (2567...) here: '))
                additional_par = {"number of sectors to protect": n,
                                  "list of sector numbers": list_of_sector_numbers}
                do_command(port, cont, command, additional_par)
            else:
                do_command(port, cont, command, additional_par)

def user_management():
    while True:
        print("\n what do you want to do now? \n"
              "those are your options:\n")
        print("    CREATE NEW USER    --> 1")
        print("    DELETE USER        --> 2")
        print("    EDIT USERS         --> 3")
        print("    GO BACK            --> -1")
        command = int(input("\n insert your command here: (-1/1/2/3) "))
        if command == -1:
            break
        elif command != 1 and command != 2 and command != 3:
            print("\n   Please Input valid command code shown above")
        elif command == 1:
            create_user()

        elif command == 2:
            del_user()

        elif command == 3:
            edit_users()

def create_user():
    while True:
        back = int(input("\n if you want to go back type -1, else type any key"))
        if back == -1:
            break
        new_username = str(input("\n please insert new username here: "))
        new_password = str(input("\n please insert new password here: "))
        new_authorization = str(input("\n please insert new authorization code here: "))
        if new_authorization != 1 and new_authorization != 2 and new_authorization != 3:
            print('illegal authorization code')
            break
        result = create_new_user(new_username, new_password, new_authorization)
        if result == 0:
            print('\n username already in use')
        elif result == 1:
            print('\n password already in use')
        elif result == 2:
            print('\n username and password already in use')
        elif result == 3:
            print('\n new user registered to system')

def del_user():
    while True:
        back = int(input("\n if you want to go back type -1, else type any key"))
        if back == -1:
            break
        user_to_delete = str(input("\n please insert username to delete: "))
        result = delete_user(user_to_delete)
        if result == 0:
            print('\n user is not in list')
        else:
            print('\n user is out of the system')

def edit_users():
    while True:
        print("\n what do you want to do now? \n"
              "those are your options:\n")
        print("    CHANGE USER NAME      --> 1")
        print("    CHANGE PASSWORD       --> 2")
        print("    CHANGE AUTHORIZATION  --> 3")
        print("    GO BACK               --> -1")
        command = int(input("\n please insert your command here: "))
        if command == -1:
            break
        if command != 1 and command != 2 and command != 3:
            print("\n   Please Input valid code shown above")
        elif command == 1:
            change_us_name()

        elif command == 2:
            change_us_password()

        elif command == 3:
            change_us_authorization()

def change_us_name():
    while True:
        user_to_edit = str(input("\n please insert username you want to edit: \n"))
        new_username = str(input("\n please insert new username here: "))
        result = change_user_name(user_to_edit, new_username)
        if result == 0:
            print('\n user is not in list')
            next_move = str(input("\n if you want to try again type 1, else type 0"))
            if next_move == 0:
                break
            elif next_move == 1:
                pass
        elif result == 1:
            print('\n user name changed')
            break

def change_us_password():
    while True:
        user_to_edit = str(input("\n please insert username you want to edit: \n"))
        new_password = str(input("\n please insert new password here: "))
        result = change_user_password(user_to_edit, new_password)
        if result == 0:
            print('\n user is not in list')
            next_move = str(input("\n if you want to try again type 1, else type 0"))
            if next_move == 0:
                break
        elif result == 1:
            print('\n password changed')
            break

def change_us_authorization():
    while True:
        user_to_edit = str(input("\n please insert username you want to edit: \n"))
        new_author = int(input("\n please insert new authorization code here: (1/2/3)"))
        if new_author != 1 and new_author != 2 and new_author != 3:
            print("\n   Please insert valid authorization code shown above")
        else:
            result = change_user_authorization(user_to_edit, str(new_author))
            if result == 0:
                print('\n user is not in list')
                next_move = str(input("\n if you want to try again type 1, else type 0"))
                if next_move == 0:
                    break
                elif next_move == 1:
                    pass
            elif result == 1:
                print('\n authorization changed')
                break

def my_profile():
    print('\n my username is: ' + str(global_vars_setting.my_user_name))
    print('\n my password is: ' + str(global_vars_setting.my_password))
    print('\n my authorization: ' + str(global_vars_setting.my_authorization))

def is_legal(command):
    a = ["-1"]
    for i in range(17):
        a.append(str(i))
    for x in a:
        if x == str(command):
            return True
    return False


# ======================================== STARTS FROM HERE ======================================== #
global_vars_setting.init1()
while True:
    print("\n +==========================================+")
    print(" |           test generator                 |")
    print(" |            Netafim App                   |")
    print(" +==========================================+")

    username = str(input("\n insert your username here :"))
    password = str(input("\n insert your password here :"))
    permission = arbitrator(username, password)
    if permission == -3:
        print('\n #####Sorry!  invalid username and password  #####')
    elif permission == -2:
        print('#####Sorry!  invalid username  #####')
    elif permission == -1:
        print('#####Sorry!  invalid password  #####')
    elif permission == 0:
        print('#####Sorry!  username and password do not match  #####')

    elif permission == 1:
        permission_1()

    elif permission == 2:
        permission_2()

    elif permission == 3:
        permission_3()










