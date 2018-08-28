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


class sshClient(SSHClient):  #Extends the paramiko.SSHClient Class for code re-use
    AutoAddPolicy = paramiko.AutoAddPolicy()


def terminal_command(conn, command, sleepTime=1):  # function to drive terminal commands
    conn.send(command + '\n')
    time.sleep(sleepTime)
    output = conn.recv(65535)
    if verbose == True:
        return output
    else:
        return "No output"


def show_vlan_api():

    url = "https://173.166.54.195:9999/api/v1/mw/hdmrpc/showcmd"

    payload = "show ip route 0.0.0.0"
    headers = {"Authorization": "Bearer VupYy0Zm4xq1y082VBd8BdGNOiVl88", "Content-Type": "text/plain"}

    response = requests.post(url, data=payload, headers=headers, verify=False)

    resp_text = response.text

    # print(resp_text)

    resp_data = json.loads(resp_text)

    cmd_out = resp_data["output"]

    return cmd_out


# Clean, Filter, and Parse software version Data
def cell_act_wan(dt):
    act_wan = {}

    data = dt

    # Cleaning the console data
    wan_search = re.search('\*.*?,\svia\s(\S+)', data)
    if wan_search != None:
        wan = wan_search.group(1)
        act_wan["ActiveInterface"] = wan

    # print("Data from Show Ver SW: \n{0}".format(data1))

    return act_wan


# Logic for getting Active WAN interface
def active_int():

    active = {}
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
    terminal_command(ir_conn, '')
    wan_data0 = (terminal_command(ir_conn, 'show ip route 0.0.0.0', 2)).decode("utf-8")"""

    wan_data0 = show_vlan_api()

    act_wan = cell_act_wan(wan_data0)

    if act_wan["ActiveInterface"] == "Vlan1":
        act_wan["ActiveInterface"] = "Wlan-GigabitEthernet0"

    active.update(act_wan)

    #print(wan_data0)

    # ir_client.close()

    return active

# print(active_int())

