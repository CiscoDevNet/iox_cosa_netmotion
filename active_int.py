import hdm_api
import re

verbose = True


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

    wan_data0 = hdm_api.show_cmd("show ip route 0.0.0.0")

    act_wan = cell_act_wan(wan_data0)

    if act_wan["ActiveInterface"] == "Vlan1":
        act_wan["ActiveInterface"] = "Wlan-GigabitEthernet0"

    active.update(act_wan)

    #print(wan_data0)

    # ir_client.close()

    return active

# print(active_int())

