import re
import hdm_api
import time

ver_data = {}


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
        ver["HWVersion"] = "v0"

    return ver


def cell_sn_ver(dt):
    ver = {}

    data = dt

    # Cleaning the console data
    data1 = (re.search('Processor\s+board\s+ID\s+(\S+\d+)', data).group(1))

    if data1 != None:
        ver["DeviceID"] = data1

    return ver


# Logic for getting Version Data
def version_data():

    ver_data0 = hdm_api.show_cmd("show ver | include Version")
    time.sleep(0.1)
    ver_data1 = hdm_api.show_cmd("show ver | include revision")
    time.sleep(0.1)
    ver_data2 = hdm_api.show_cmd("show ver | include Processor")

    ver_data.update(cell_sw_ver(ver_data0))
    ver_data.update(cell_hw_ver(ver_data1))
    ver_data.update(cell_sn_ver(ver_data2))

    return ver_data


# print(version_data())

