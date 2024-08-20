######################################################################
#                                                                    #
#      _____              _                    _    ____   ____      #
#     |  ___| __ ___  ___| |__   _____  __    / \  |  _ \ / ___|     #
#     | |_ | '__/ _ \/ _ \ '_ \ / _ \ \/ /   / _ \ | |_) | |         #
#     |  _|| | |  __/  __/ |_) | (_) >  <   / ___ \|  __/| |___      #
#     |_|  |_|  \___|\___|_.__/ \___/_/\_\ /_/   \_\_|    \____|     #
#      ____         __ _                                             #
#     / ___|  ___  / _| |___      ____ _ _ __ ___                    #
#     \___ \ / _ \| |_| __\ \ /\ / / _` | '__/ _ \                   #
#      ___) | (_) |  _| |_ \ V  V / (_| | | |  __/                   #
#     |____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|                   #
#                                                                    #
######################################################################
# --------------------------------------------------
# Name: Freebox Anti Parental Control Software (a.k.a: Freebox APC Software)
# Author: Romain SEBASTIANI <romain07022007seb@gmail.com> <https://github.com/R0M107/>
# Description: This app can bypass the parental control from the Freebox
Version = "0.1.0"
# --------------------------------------------------





# Importing libs
from colorama import Fore # type: ignore
import ctypes
import sys
import re
import os
import shutil
from alive_progress import alive_bar

# Importing files
from functions import is_admin
import logger, bypass

# Main function
if __name__ == '__main__':
    log = logger.Logger()
    log.write("Starting...", Fore.GREEN, "MAIN")
    print("")

    if not is_admin():
        log.write("You need admin privileges !", Fore.RED, "MAIN")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    while True:
        log.write("######################################################################", Fore.GREEN, "MAIN")
        log.write("#                                                                    #", Fore.GREEN, "MAIN")
        log.write("#      _____              _                    _    ____   ____      #", Fore.GREEN, "MAIN")
        log.write("#     |  ___| __ ___  ___| |__   _____  __    / \\  |  _ \\ / ___|     #", Fore.GREEN, "MAIN")
        log.write("#     | |_ | '__/ _ \\/ _ \\ '_ \\ / _ \\ \\/ /   / _ \\ | |_) | |         #", Fore.GREEN, "MAIN")
        log.write("#     |  _|| | |  __/  __/ |_) | (_) >  <   / ___ \\|  __/| |___      #", Fore.GREEN, "MAIN")
        log.write("#     |_|  |_|  \\___|\\___|_.__/ \\___/_/\\_\\ /_/   \\_\\_|    \\____|     #", Fore.GREEN, "MAIN")
        log.write("#      ____         __ _                                             #", Fore.GREEN, "MAIN")
        log.write("#     / ___|  ___  / _| |___      ____ _ _ __ ___                    #", Fore.GREEN, "MAIN")
        log.write("#     \\___ \\ / _ \\| |_| __\\ \\ /\\ / / _` | '__/ _ \\                   #", Fore.GREEN, "MAIN")
        log.write("#      ___) | (_) |  _| |_ \\ V  V / (_| | | |  __/                   #", Fore.GREEN, "MAIN")
        log.write("#     |____/ \\___/|_|  \\__| \\_/\\_/ \\__,_|_|  \\___|                   #", Fore.GREEN, "MAIN")
        log.write("#                                                                    #", Fore.GREEN, "MAIN")
        log.write("######################################################################", Fore.GREEN, "MAIN")
        log.write("Version : " + Version, Fore.GREEN, "MAIN")
        print("")

        log.write("Choose an option :", Fore.GREEN, "MAIN")
        log.write("1 - Change the MAC Address of an interface", Fore.GREEN, "MAIN")
        log.write("2 - Get MAC Address change history", Fore.GREEN, "MAIN")
        log.write("3 - Delete logs files", Fore.GREEN, "MAIN")
        
        print("")
        selected_menu_id = input("What you want to do ? ")
        print("")

        try:
            selected_menu_id = int(selected_menu_id)
        except ValueError as e:
            log.write(str(e), Fore.RED, "ValueError")
            sys.exit()

        ByPasser = bypass.Bypass()

        if selected_menu_id == 1:
            interfaces = ByPasser.get_interfaces()

            id_space = (len(str(max(interfaces["id"]))) - len("ID")) * " "
            code_space = (len(str(max(interfaces["code"]))) - len("CODE")) * " "
            name_space = (len(max(interfaces["name"], key=len)) - len("NAME")) * " "

            log.write("ID" + id_space + Fore.MAGENTA + " | CODE" + code_space + " | NAME" + name_space + " | MAC", Fore.RED)
            
            for i, interface in enumerate(interfaces["code"]):
                id_space = (len(str(max(interfaces["id"]))) - len(str(interfaces["id"][i]))) * " "
                code_space = (len(str(max(interfaces["code"]))) - len(str(interfaces["code"][i]))) * " "
                name_space = (len(max(interfaces["name"], key=len)) - len(interfaces["name"][i])) * " "
                log.write(str(interfaces["id"][i]) + id_space + Fore.MAGENTA + " | " + str(interfaces["code"][i]) + code_space + " | " + str(interfaces["name"][i]) + name_space + " | " + str(interfaces["macAddress"][i]), Fore.RED)

            print("")
            selected_interface_id = input("Select the ID of the interface you want to change the MAC Address : ")
            
            try:
                selected_interface_id = int(selected_interface_id)
            except ValueError as e:
                log.write(str(e), Fore.RED, "ValueError")
                sys.exit()
            
            if len(interfaces["id"]) < selected_interface_id:
                log.write("ID out of range", Fore.RED, "ValueError")
                sys.exit()

            print("")
            log.write(str(interfaces["id"][selected_interface_id]) + Fore.MAGENTA + " | " + str(interfaces["code"][selected_interface_id]) + " | " + str(interfaces["name"][selected_interface_id]) + " | " + str(interfaces["macAddress"][selected_interface_id]), Fore.RED)

            print("")
            log.write("Choose an option :", Fore.GREEN, "MAIN")
            log.write("1 - Set your MAC Address", Fore.GREEN, "MAIN")
            log.write("2 - Set a random MAC Address", Fore.GREEN, "MAIN")
            log.write("3 - Delete MAC Address", Fore.GREEN, "MAIN")

            print("")
            selected_mac_menu_id = input("What you want to do ? ")
            print("")

            try:
                selected_mac_menu_id = int(selected_mac_menu_id)
            except ValueError as e:
                log.write(str(e), Fore.RED, "ValueError")
                sys.exit()

            if selected_mac_menu_id == 1:
                input_mac_address = input("Please enter a MAC Address (A0-B1-C2-D3-E4-F5) : ")
                
                if not re.match("[0-9A-F]{2}([-])[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$", input_mac_address):
                    log.write("Invalid Mac Address !", Fore.RED, "ERROR")
                    sys.exit()

                result = ByPasser.set_mac_address(interfaces["code"][selected_interface_id], input_mac_address)

                if not result:
                    log.write("Can't change MAC Address", Fore.RED, "ERROR")
                else:
                    log.write("MAC Address successfuly updated", Fore.GREEN, "INFO")
            elif selected_mac_menu_id == 2:
                macAddress = ByPasser.random_mac_address()

                if not macAddress or macAddress is None:
                    log.write("Can't generate random MAC Address", Fore.RED, "ERROR")

                log.write("New MAC Address : " + macAddress, Fore.MAGENTA, "INFO")

                result = ByPasser.set_mac_address(interfaces["code"][selected_interface_id], macAddress)

                if not result:
                    log.write("Can't change MAC Address", Fore.RED, "ERROR")
                else:
                    log.write("MAC Address successfuly updated", Fore.GREEN, "INFO")
            elif selected_mac_menu_id == 3:
                result = ByPasser.delete_mac_address(interfaces["code"][selected_interface_id])

                if not result:
                    log.write("Can't delete MAC Address", Fore.RED, "ERROR")
                else:
                    log.write("MAC Address successfuly deleted", Fore.GREEN, "INFO")
            else:
                log.write("This option doesn't exist", Fore.RED, "ValueError")
                sys.exit()
        elif selected_menu_id == 2:
            log.write("MAC Address history :", Fore.GREEN, "MAIN")

            mac_history = ByPasser.get_mac_history()
            lines = mac_history.readlines()

            for line in lines:
                print(line)
        elif selected_menu_id == 3:
            log.write("Deleting log files :", Fore.BLUE, "INFO")

            folder = './logs/'
            with alive_bar(len(os.listdir(folder))) as bar:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        log.write("Failed to delete log file " + file_path, Fore.RED, "ERROR")
                        log.write(str(e), Fore.RED, "ERROR")
                    bar()

            log.write("PLEASE NOTE THAT ONE THE FILE CAN'T BE DELETED BECAUSE IT IS USED BY THIS PROGRAM !" + file_path, Fore.YELLOW, "INFO")
        else:
            log.write("This option doesn't exist", Fore.RED, "ValueError")
            sys.exit()

        print("")
        print("")
        print("")
        print("")
        print("")