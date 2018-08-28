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
cell_gps_data = {}


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


def show_all_api():

    url = "https://173.166.54.195:9999/api/v1/mw/hdmrpc/showcmd"

    payload = "show cell 0/0 all"
    headers = {"Authorization": "Bearer VupYy0Zm4xq1y082VBd8BdGNOiVl88", "Content-Type": "text/plain"}

    response = requests.post(url, data=payload, headers=headers, verify=False)

    resp_text = response.text

    # print(resp_text)

    resp_data = json.loads(resp_text)

    cmd_out = resp_data["output"]

    return cmd_out


# Function to convert Location data to decimal location data
def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd


# Clean, Filter, and Parse GPS Data
def cell_gps(dt):

    gps = {}

    data = dt

    # Cleaning the console data
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")
    #adding another clean for later detail lines that are seperated by commas instead of linebreaks or spaces
    data_clean2 = data_clean1.replace(","," ")
    data1 = dict(re.findall(r'(\S+):(".*?"|\S+)', data_clean2))

    test_dict = {"value": "1"}

    test_dict.update(data1)

    # Parse Directional Data
    try:
        dmsNS = (re.split('[DegMinSecorth]+', data1["Latitude"]))[:4]
        dmsEW = (re.split('[DegMinSecest]+', data1["Longitude"]))[:4]
    except Exception:
        dmsNS = "None"
        dmsEW = "None"

    try:
        gps["Latitude"] = dms2dd(*dmsNS)
        gps["Longitude"] = dms2dd(*dmsEW)
    except Exception:
        gps["Latitude"] = "Incomplete"
        gps["Longitude"] = "Incomplete"

    gps["Status"] = data1.get("GPSautotrackingstatus", "None")
#    gps["Accuracy"] = "NA"
    gps["HDOP"] = data1.get("HDOP", "None")

    return gps


# Logic for getting GPS Data
def gps_data():

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

    # terminal commands to gather GPS Data
    gps_data = (terminal_command(ir_conn, 'show cell 0/0 gps detail').decode("utf-8"))
    terminal_command(ir_conn, "\x03").decode("utf-8")"""

    all_data = show_all_api()

    #print("GPS Data\n")
    gps = cell_gps(all_data)
    #print(gps)
    #print("\n")

    cell_gps_data["Location"] = gps
    #print(cell_gps_data)

    # ir_client.close()

    return cell_gps_data


# print(gps_data())

