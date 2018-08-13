from paramiko import SSHClient as SSHClient
import paramiko
import re
import time
import config as config


verbose = True
ver_data = {}


class sshClient(SSHClient):  #Extends the paramiko.SSHClient Class for code re-use
    AutoAddPolicy = paramiko.AutoAddPolicy()


def terminal_command(conn, command):  # function to drive terminal commands
    conn.send(command + '\n')
    time.sleep(1)
    output = conn.recv(65535)
    if verbose == True:
        return output
    else:
        return "No output"


# Clean, Filter, and Parse software version Data
def cell_sw_ver(dt):

    ver = {}

    data = dt

    # Cleaning the console data
    data_clean0 = data.replace(", ", ",")
    data_clean1 = data_clean0.replace(" ", ":")
    data_clean2 = data_clean1.replace(",", " ")
    data1 = dict(re.findall(r'(\S+):(".*?"|\S+)', data_clean2))

    ver["SWVersion"] = data1.get("Version", "None")

    #print("Data from Show Ver SW: \n{0}".format(data1))

    return ver


# Clean, Filter, and Parse HW version Data
def cell_hw_ver(dt):

    ver = {}

    data = dt

    # Cleaning the console data
    data1 = re.findall(r'Cisco\ (.*?)\ with', data)

    ver['HWVersion'] = data1[0]
    #print("Data from Show Ver HW: \n{0}".format(data1))

    return ver


# Logic for getting Version Data
def version_data():
    # credentials for the router
    ir_router = config.cfg.get("ir_router_info", "IP")

    ir_port = config.cfg.get("ir_router_info", "port")

    ir_user = config.cfg.get("ir_router_info", "user")

    ir_passwd = config.cfg.get("ir_router_info", "pass")

    # setting up the terminal connection to the router
    ir_client = sshClient()
    ir_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ir_client.connect(ir_router, port=ir_port, username=ir_user, password=ir_passwd, look_for_keys=False, allow_agent=False)

    # setting up the shell to issue commands
    ir_conn = ir_client.invoke_shell()

    # terminal commands to gather cell int 0 and cell int 1 data
    # and GPS Data
    terminal_command(ir_conn, '')
    ver_data0 = (terminal_command(ir_conn, 'show ver | include Version').decode("utf-8"))
    ver_data1 = (terminal_command(ir_conn, 'show ver | include revision').decode("utf-8"))

    #print("Version Data\n")
    ver_data.update(cell_sw_ver(ver_data0))
    ver_data.update(cell_hw_ver(ver_data1))
    #print(ver_data)
    #print("\n")

    ir_client.close()

    return ver_data



