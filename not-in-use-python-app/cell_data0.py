import hdm_api
import re

verbose = True
cellular_data0 = {}
cell_dict_data = {}


# Clean, Filter, and Parse Connection Data
def cell_connection(dt):

    conn = {}

    data = dt
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")

    data_clean_profiles = data_clean0.replace(",PacketSessionStatus", "")

    try:
        conn["TXbytes"] = re.search('Transmitted=(\d+)', data_clean1).group(1)
        conn["RXbytes"] = re.search('Received=(\d+)', data_clean1).group(1)
    except Exception:
        conn["TXbytes"] = "0"
        conn["RXbytes"] = "0"

    profiles = dict(re.findall(r'(Profile\S+)=(".*?"|\S+)', data_clean_profiles))

    active_prof = []
    for profile, status in profiles.items():
        if status == 'ACTIVE':
            active_prof.append(profile)

    return conn


# Clean, Filter, and Parse Network Data
def cell_network_lte(dt):

    network = {}

    data = dt
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")

    data1 = dict(re.findall(r'(\S+)=(".*?"|\S+)', data_clean1))

    network["Roaming"] = data1.get("CurrentRoamingStatus", "None")
    network["Carrier"] = data1.get("MobileCountryCode(MCC)", "None") + "-" + data1.get("MobileNetworkCode(MNC)", "None")

    return network


# Clean, Filter, and Parse Radio Data
def cell_radio(dt):

    radio = {}

    data = dt

    try:
        radio["Technology"] = (re.search('Radio\s+Access\s+Technology\(RAT\)\s+Selected\s+=\s+(\S+)', data).group(1))
    except Exception:
        pass
    try:
        radio["RSSI"] = (re.search('Current\s+RSSI\s+=\s+(\S+\d+)', data).group(1))
    except Exception:
        pass
    try:
        radio["RSRP"] = (re.search('Current\s+RSRP\s+=\s+(\S+\d+)', data).group(1))
    except Exception:
        pass
    try:
        radio["RSRQ"] = (re.search('Current\s+RSRQ\s+=\s+(\S+\d+)', data).group(1))
    except Exception:
        pass
    try:
        radio["SINR"] = (re.search('Current\s+SNR\s+=\s+(\S+\d+)', data).group(1))
    except Exception:
        pass
    try:
        radio["Channel"] = (re.search('LTE\s+Rx\s+Channel\s+Number\s+=\s+(\d+)', data).group(1))
    except Exception:
        pass
    try:
        radio["Band"] = (re.search('LTE\s+Band\s+=\s+(\d+)', data).group(1))
    except Exception:
        pass
    try:
        if (re.search('Radio\s+power\s+mode\s+=\s+(\S+)', data).group(1)) == "online":
            radio["Connected"] = "Connected"
        else:
            radio["Connected"] = "Disconnected"
    except Exception:
        radio["Connected"] = "Disconnected"

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
        hardware["ISP"] = (re.search('Carrier=(\S+)', data_clean1).group(1))
    except Exception:
        pass

    return hardware


# Logic for getting Cell Data
def cell_data():

    # Execute Show command over IOx HDM Service API
    all_data = hdm_api.show_cmd("show cell 0/0 all")

    cellular_data0.update({'ID': 'Cellular0/0'})
    cellular_data0.update({'Type': 'cellular'})
    cellular_data0.update(cell_hardware(all_data))
    cellular_data0.update(cell_network_lte(all_data))
    cellular_data0.update(cell_radio(all_data))

    cellular_data0.update(cell_connection(all_data))

    cd = [cellular_data0]

    cell_dict_data["CellularInterface"] = cd

    return cell_dict_data


# print(cell_data())

