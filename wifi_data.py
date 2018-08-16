from paramiko import SSHClient as SSHClient
import paramiko
import re
import time
import config as config

verbose = True


class sshClient(SSHClient):  #Extends the paramiko.SSHClient Class for code re-use
    AutoAddPolicy = paramiko.AutoAddPolicy()


def terminal_command(conn, command, sleepTime = 1.5):  # function to drive terminal commands
    conn.send(command + '\n')
    time.sleep(sleepTime)
    output = conn.recv(65535)
    if verbose == True:
        return output
    else:
        return "No output"


def ap_ip_extract(dt):
    # print(dt)
    ap_ip_data = dt.decode('utf-8')
    try:
        ap_ip = re.search('IP address: (\d.+)', ap_ip_data).group(1)
    except Exception:
        ap_ip = "None"

    return ap_ip


def wifi_data0_parse(dt):
    wifi_info = {}
    wifi0 = dt.decode('utf-8')
    #print(wifi0)

    # BAS 8-15 - Added ID field from AP Name
    if (re.search('Name\s+: (\S+)', wifi0)) != None:
        ID = re.search('Name\s+: (\S+)', wifi0).group(1)
    else:
        ID = "None"
    if (re.search('SSID\s+: (\S+)', wifi0)) != None:
        SSID = re.search('SSID\s+: (\S+)', wifi0).group(1)
    else:
        SSID = "None"
    if (re.search('Address\s+: (\S+)', wifi0)) != None:
        BSSID = re.search('Address\s+: (\S+)', wifi0).group(1)
    else:
        BSSID = "None"
    if (re.search('Key Mgmt type\s+: (\S+ +\S+)', wifi0)) != None:
        Authentication = re.search('Key Mgmt type\s+: (\S+ +\S+)', wifi0).group(1)
    else:
        Authentication = "None"
    if (re.search('Signal Strength\s+: (\S+)', wifi0)) != None:
        RSSI = re.search('Signal Strength\s+: (\S+)', wifi0).group(1)
    else:
        RSSI = "None"
    if (re.search('Signal to Noise\s+: (\S+)', wifi0)) != None:
        SNR = re.search('Signal to Noise\s+: (\S+)', wifi0).group(1)
    else:
        SNR = "None"
    if (re.search('Encryption\s+: (\S+)', wifi0)) != None:
        Encryption = re.search('Encryption\s+: (\S+)', wifi0).group(1)
    else:
        Encryption = "None"


    # BAS 8-15 - Added ID field from AP Name
    wifi_info["ID"] = ID
    wifi_info["SSID"] = SSID
    wifi_info["BSSID"] = BSSID
    wifi_info["Authentication"] = Authentication
    wifi_info["RSSI"] = RSSI
    wifi_info["SNR"] = SNR
    wifi_info["Encryption"] = Encryption

    # BAS 8-15 - Added Signal to match the language from Netmotion API and other calls
    Signal = 0

    try:
        if int(RSSI) >= -50:
            Signal = 100
        elif int(RSSI) <= -100:
            Signal = 0
        else:
            Signal = 2 * (int(RSSI) + 100)
    except Exception:
        Signal = 0

    wifi_info["Signal"] = str(Signal)

    return wifi_info


def wifi_data1_parse(dt):
    wifi1 = dt.decode('utf-8')

    rx_tx = {}

    try:
        rxpackdict = list(map(int, (re.findall(r'Rx Packets:\s+\S+ / (\d+)', wifi1))))
        rxpack = max(rxpackdict)
        rxrate = (re.search('(\S+)\r\nRx Packets:\s+\S+ / %s' % rxpack, wifi1).group(1))
        rx_tx["RxRate"] = rxrate
    except Exception:
        rx_tx["RxRate"] = "None"
    try:
        txpackdict = list(map(int, (re.findall(r'Tx Packets:\s+\S+ / (\d+)', wifi1))))
        txpack = max(txpackdict)
        txrate = (re.search('(\S+)\r\nRx Packets:\s+\S+ / \S+\s+Tx Packets:\s+\S+ / %s' % txpack, wifi1).group(1))
        rx_tx["TxRate"] = txrate
    except Exception:
        rx_tx["TxRate"] = "None"

    return rx_tx


    # Logic for getting WiFi Data
def wifi_data():
    wgb0 = {
            "WGB WiFi Status": "NA",
            "ID": "NA",
            "Signal": "NA",
            "RSSI": "NA",
            "SSID": "NA",
            "BSSID": "NA",
            "TxRate": "NA",
            "RxRate": "NA",
            "Authentication": "NA",
            "Encryption": "NA"
            }

    ir_router = config.cfg.get("ir_router_info", "IP")

    ir_port = config.cfg.get("ir_router_info", "port")

    ir_user = config.cfg.get("ir_router_info", "user")

    ir_passwd = config.cfg.get("ir_router_info", "pass")

    ap_user = config.cfg.get("ap_info", "user")

    ap_passwd = config.cfg.get("ap_info", "pass")

    # setting up the terminal connection to the router
    ir_client = sshClient()
    ir_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ir_client.connect(ir_router, port=ir_port, username=ir_user, password=ir_passwd, look_for_keys=False,
                      allow_agent=False)

    # setting up the shell to issue commands
    ir_conn = ir_client.invoke_shell()

    ap_hostname = config.cfg.get("ap_info", "host") + "." + config.cfg.get("ir_router_info", "domain")

    terminal_command(ir_conn, '')
    ap_data = terminal_command(ir_conn, "show cdp entry %s" % ap_hostname)

    ap_ip = ap_ip_extract(ap_data)

    if ap_ip == "None":
        wgb0 = {
            "WGB WiFi Status": "Unavailable",
            "ID": "None",
            "Signal": "None",
            "RSSI": "None",
            "SSID": "None",
            "BSSID": "None",
            "TxRate": "None",
            "RxRate": "None",
            "Authentication": "None",
            "Encryption": "None"
        }

        wd = [wgb0]

        ir_client.close()

    else:
        ## This Next section is commented out
        ## Not being used because current access is remote
        ## ir_client.close()
        #
        ## setting up the terminal connection to the Wifi AP
        # wifi_client = sshClient()
        # wifi_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # wifi_client.connect(ir_router, port=ir_port, username=ir_user, password=ir_passwd, look_for_keys=False,
        #                  allow_agent=False)

        # setting up the shell to issue commands
        # wifi_conn = wifi_client.invoke_shell()

        ## Remote AP Access
        terminal_command(ir_conn, 'ssh -l %s %s' % (ap_user, ap_ip))
        time.sleep(2)
        terminal_command(ir_conn, ap_passwd + "\r\n")

        wifi_data0 = terminal_command(ir_conn, "show dot11 associations all-client interface Dot11Radio 1\n  ", 1.5)
        wifi_data1 = terminal_command(ir_conn, "show controllers dot11Radio 1 radio-stats\n  \n  \n", 1.5)

        #print(wifi_data0.decode('utf-8'))
        #print(wifi_data1.decode('utf-8'))

        wgb0.update(wifi_data0_parse(wifi_data0))
        wgb0.update(wifi_data1_parse(wifi_data1))
        wgb0.update({"WGB WiFi Status": "Connected"})
        wgb0.update({"Technology": "802.11n"})

        wd = [wgb0]

    final_wifi_data = {"WifiInterface": wd}

    ir_client.close()

    return final_wifi_data

#print(wifi_data())
