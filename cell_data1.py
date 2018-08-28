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
cellular_data1 = {}
cell_dict_data = {}


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

    payload = "show cell 1/0 all"
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


# Clean, Filter, and Parse Connection Data
def cell_connection(dt):

    conn = {}

    data = dt
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")

    data_clean_profiles = data_clean0.replace(",PacketSessionStatus", "")

    #print('data_clean_profiles: \n{}'.format(data_clean_profiles))

    try:
        conn["TXbytes"] = re.search('Transmitted=(\d+)', data_clean1).group(1)
        conn["RXbytes"] = re.search('Received=(\d+)', data_clean1).group(1)
    except Exception:
        conn["TXbytes"] = "0"
        conn["RXbytes"] = "0"

    profiles = dict(re.findall(r'(Profile\S+)=(".*?"|\S+)', data_clean_profiles))

    #print('profiles: \n{}'.format(profiles))

    active_prof = []
    for profile, status in profiles.items():
        if status == 'ACTIVE':
            active_prof.append(profile)

    #conn['ActiveProfiles'] = active_prof

    return conn


# Clean, Filter, and Parse Network Data
def cell_network_lte(dt):

    network = {}

    data = dt
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")

    data1 = dict(re.findall(r'(\S+)=(".*?"|\S+)', data_clean1))

    network["Roaming"] = data1.get("CurrentRoamingStatus", "None")
    network["PLMN"] = data1.get("MobileCountryCode(MCC)", "None") + "-" + data1.get("MobileNetworkCode(MNC)", "None")

    return network


# Clean, Filter, and Parse Radio Data
def cell_radio(dt):

    radio = {}

    data = dt
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")

    data1 = dict(re.findall(r'(\S+)=(".*?"|\S+)', data_clean1))

    radio["Technology"] = data1.get("RadioAccessTechnology(RAT)Selected", "None")
    radio["RSSI"] = data1.get("CurrentRSSI", "None")
    radio["RSRP"] = data1.get("CurrentRSRP", "None")
    radio["RSRQ"] = data1.get("CurrentRSRQ", "None")
    radio["SINR"] = data1.get("CurrentSNR", "None")
    radio["Connected"] = data1.get("Radiopowermode", "None")

    return radio


# Clean, Filter, and Parse Hardware Data
def cell_hardware(dt):

    hardware = {}

    data = dt
    data_clean0 = data.replace(" ", "")
    #print(data_clean0)
    data_clean1 = data_clean0.replace("\n", " ")

    data1 = dict(re.findall(r'(\S+)=(".*?"|\S+)', data_clean1))
    #print(data1)

    hardware["IMEI"] = data1.get("InternationalMobileEquipmentIdentity(IMEI)", "None")
    hardware["IMSI"] = data1.get("InternationalMobileSubscriberIdentity(IMSI)", "None")
    hardware["PhoneNumber"] = data1.get("DigitalNetwork-Number(MSISDN)", "None")

    try:
        hardware["Carrier"] = (re.search('Carrier=(\S+)', data_clean1).group(1))
    except Exception:
        hardware["Carrier"] = "None"

    return hardware


def rtr_hostname(dt, cellInt):

    hostname = {}

    #Split the 3 lines (0-command entry, 1-actual response, 2-next open prompt)
    data = dt.split('\n')
    data_clean0 = data[1].replace(" ", "=")

    #print('hostname data: {0}'.format(data_clean0))

    data0 = dict(re.findall(r'(\S+)=(".*?"|\S+)', data_clean0))

    try:
        hostname['ID'] = 'Cellular1/0'
    except Exception:
        hostname['ID'] = cellInt

    #print('hostname: {0}'.format(hostname))

    return hostname


# Logic for getting Cell Data
def cell_data():

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

    all_data = show_all_api()

    hw_data1 = (terminal_command(ir_conn, 'show cell 1/0 hardware').decode("utf-8"))
    radio_data1 = (terminal_command(ir_conn, 'show cell 1/0 radio').decode("utf-8"))
    network_data1 = (terminal_command(ir_conn, 'show cell 1/0 network').decode("utf-8"))
    connection_data1 = (terminal_command(ir_conn, 'show cell 1/0 connection').decode("utf-8"))

    gps_data = (terminal_command(ir_conn, 'show cell 0/0 gps detail').decode("utf-8"))
    terminal_command(ir_conn, "\x03").decode("utf-8")

    # Had to adjust the terminal command to allow for variable sleep timing,
    # Searching the running config takes a bit longer
    host_data = (terminal_command(ir_conn, 'show run | include hostname', 3).decode("utf-8"))"""

    all_data = show_all_api()

    #print("Cell Interface 1 Data\n")
    # cellular_data1.update(rtr_hostname(all_data, 'Cellular1/0'))
    cellular_data1.update({'ID': 'Cellular1/0'})
    cellular_data1.update(cell_hardware(all_data))
    cellular_data1.update(cell_network_lte(all_data))
    cellular_data1.update(cell_radio(all_data))
    cellular_data1.update(cell_connection(all_data))
    #print(cellular_data1)
    #print("\n")

    #print("Combined Cell Data")
    cd = [cellular_data1]
    #print(cd)

    #print("Cell and GPS Data combined")
    #cell_gps_data["CellularInterface"] = cd
    cell_dict_data["CellularInterface"] = cd
    #print(cell_gps_data)

    # ir_client.close()

    return cell_dict_data


# print(cell_data())
# print(show_all_api())

