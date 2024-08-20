import winreg
import re
import subprocess
import random

class Bypass():
    def __init__(self):
        self.registry_key = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
        self.mac_history = open("mac_history.txt", "a+")
        self.mac_history_read = open("mac_history.txt", "r+")

    def get_subkeys(self):
        subkeys = []
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.registry_key) as key:
                index = 0
                while True:
                    subkey_name = winreg.EnumKey(key, index)
                    subkeys.append(subkey_name)
                    index += 1
        except OSError:
            pass
        return subkeys
    
    def get_registry_value(self, subkey, value_name):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"{self.registry_key}\{subkey}") as key:
                value, _ = winreg.QueryValueEx(key, value_name)
                return value
        except (OSError, FileNotFoundError, winreg.error) as e:
            return False
    
    def create_registry_value(self, subkey, value_name, value):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"{self.registry_key}\{subkey}", 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
                return True
        except (OSError, FileNotFoundError, winreg.error) as e:
            return False

    def update_registry_value(self, subkey, value_name, new_value):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"{self.registry_key}\{subkey}", 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value)
                return True
        except (OSError, FileNotFoundError, winreg.error) as e:
            return False

    def delete_registry_value(self, subkey, value_name):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"{self.registry_key}\{subkey}", 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
                return True
        except (OSError, FileNotFoundError, winreg.error) as e:
            return False

    def get_interfaces(self):
        interfaceskeys = self.get_subkeys()

        if not interfaceskeys:
            return False
        else:
            interfaces = []

            for keys in interfaceskeys:
                if len(keys) == 4 and keys.isdigit():
                    interfaces.append(keys)
        
        interfaces_list = {"id": [], "code": [], "name": [], "macAddress": []}

        for i, interface in enumerate(interfaces):
            driverdesc = self.get_registry_value(interface, "driverDesc")
            macAddress = self.get_registry_value(interface, "NetworkAddress")

            if not driverdesc:
                return False

            interfaces_list["id"].append(i)
            interfaces_list["code"].append(interface)
            interfaces_list["name"].append(driverdesc)

            if macAddress:
                interfaces_list["macAddress"].append(macAddress)
            else:
                interfaces_list["macAddress"].append(None)

        return interfaces_list

    def set_mac_address(self, interface, macAddress):
        interfaces = self.get_interfaces()

        if not interface or interface is None or interface not in interfaces["code"]:
            return False
        
        if not macAddress or macAddress is None or not re.match("[0-9A-F]{2}([-])[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$", macAddress):
            return False
        
        registry_value_exist = self.get_registry_value(interface, "NetworkAddress")

        interface_index = interfaces["code"].index(interface)

        if not registry_value_exist:
            self.mac_history.write(str(interfaces["code"][interface_index]) + ": None --> " + macAddress + "\n")
            result = self.create_registry_value(interface, "NetworkAddress", macAddress)
            
            # Restarting the network interface
            command = "wmic path win32_networkadapter where \"Name='$interfaceName$'\" call ".replace("$interfaceName$", interfaces["name"][interface_index])

            p = subprocess.Popen(rf'{command}disable', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            (output, err) = p.communicate()

            p2 = subprocess.Popen(rf'{command}enable', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p2.wait()
            (output2, err2) = p2.communicate()

            return result
        else:
            self.mac_history.write(str(interfaces["code"][interface_index]) + ": " + str(interfaces["macAddress"][interface_index]) + " --> " + macAddress + "\n")
            result = self.update_registry_value(interface, "NetworkAddress", macAddress)

            # Restarting the network interface
            command = "wmic path win32_networkadapter where \"Name='$interfaceName$'\" call ".replace("$interfaceName$", interfaces["name"][interface_index])

            p = subprocess.Popen(rf'{command}disable', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            (output, err) = p.communicate()

            p2 = subprocess.Popen(rf'{command}enable', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p2.wait()
            (output2, err2) = p2.communicate()

            return result

        return False
    
    def random_mac_address(self):
        myhexdigits = []
        for x in range(6):
            a = random.randint(0,255)
            hex = '%02x' % a
            myhexdigits.append(hex)
        return '-'.join(myhexdigits).upper()
    
    def delete_mac_address(self, interface):
        interfaces = self.get_interfaces()

        if not interface or interface is None or interface not in interfaces["code"]:
            return False
        
        interface_index = interfaces["code"].index(interface)
        
        self.mac_history.write(str(interfaces["code"][interface_index]) + ": " + str(interfaces["macAddress"][interface_index]) + " --> None\n")
        result = self.delete_registry_value(interface, "NetworkAddress")

        return result
    
    def get_mac_history(self):
        return self.mac_history_read