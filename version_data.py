from paramiko import SSHClient as SSHClient
import paramiko
import re
import time
import config as config
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

verbose = True
ver_data = {}


class sshClient(SSHClient):  #Extends the paramiko.SSHClient Class for code re-use
    AutoAddPolicy = paramiko.AutoAddPolicy()


def terminal_command(conn, command, sleepTime = 1):  # function to drive terminal commands
    conn.send(command + '\n')
    time.sleep(sleepTime)
    output = conn.recv(65535)
    if verbose == True:
        return output
    else:
        return "No output"


def show_version_api():

    url = "https://173.166.54.195:9999/api/v1/mw/hdmrpc/showcmd"

    payload = "show ver | include Version"
    headers = {"Authorization": "Bearer VupYy0Zm4xq1y082VBd8BdGNOiVl88", "Content-Type": "text/plain"}

    response = requests.post(url, data=payload, headers=headers, verify=False)

    resp_text = response.text

    # print(resp_text)

    resp_data = json.loads(resp_text)

    cmd_out = resp_data["output"]

    return cmd_out


def show_revision_api():

    url = "https://173.166.54.195:9999/api/v1/mw/hdmrpc/showcmd"

    payload = "show ver | include revision"
    headers = {"Authorization": "Bearer VupYy0Zm4xq1y082VBd8BdGNOiVl88", "Content-Type": "text/plain"}

    response = requests.post(url, data=payload, headers=headers, verify=False)

    resp_text = response.text

    # print(resp_text)

    resp_data = json.loads(resp_text)

    cmd_out = resp_data["output"]

    return cmd_out


# Clean, Filter, and Parse software version Data
def cell_sw_ver(dt):

    ver = {}

    data = dt

    # Cleaning the console data
    data_clean0 = data.replace(", ", ",")
    data_clean1 = data_clean0.replace(" ", ":")
    data_clean2 = data_clean1.replace(",", " ")
    data1 = dict(re.findall(r'(\S+):(".*?"|\S+)', data_clean2))

    ver["FWVersion"] = data1.get("Version", "None")

    #print("Data from Show Ver SW: \n{0}".format(data1))

    return ver


# Clean, Filter, and Parse HW version Data
def cell_hw_ver(dt):

    ver = {}

    data = dt

    # Cleaning the console data
    data1 = re.findall(r'Cisco\ (.*?)\ with', data)

    try:
        ver["HWVersion"] = data1[0]
    except Exception:
        ver["HWVersion"] = "None"
    #print("Data from Show Ver HW: \n{0}".format(data1))

    return ver


# Logic for getting Version Data
def version_data():

    """# credentials for the router
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
    terminal_command(ir_conn, '')"""

    ver_data0 = show_version_api()
    ver_data1 = show_revision_api()

    #print("Version Data\n")
    ver_data.update(cell_sw_ver(ver_data0))
    ver_data.update(cell_hw_ver(ver_data1))
    #print(ver_data)
    #print("\n")

    # ir_client.close()

    return ver_data


# print(version_data())

