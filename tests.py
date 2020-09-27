
from backend.global_vars_setting import *
from backend.functions import *
from backend.STM32_Programmer_V1 import *


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
        print('\n simple user successfully logged in!')
        print("\n what do you want to do now?")
        print("\n your only option is:   BL_MEM_WRITE        --> 8")

        command = str(input("\n insert your command here :"))
        port = str(input("\n insert your port name here :"))
        cont = str(input("\n from controller 1-1000,\n insert your controller name here :"))
        file = str(input("\n insert your the directory name here :"))



    elif permission == 2:
        print('\n developer user successfully logged in!')
        print("\n what do you want to do now?")
        print("\n your options are:")
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
        print("   MENU_EXIT                             --> 0")


    elif permission == 3:
        print('\n administrator user successfully logged in!')
        print("\n what do you want to do now? \n")
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
        print("   MENU_EXIT                             --> 0")


        action = str(input("\n insert your username here :"))
        ans2 = False
        for x in global_vars_setting.table_of_users:
            curr2 = user_card(x).password
            if curr2 == password:
                ans2 = True
                break
        if not curr2:
            print("username is not found in database")
            print("\n   Please Input valid username")


