from flask import Flask, request, jsonify

import cell_data0
import cell_data1
import gps_data
import wifi_data
import active_int
import version_data
import time
from threading import Thread

app = Flask(__name__)

cd0 = {}
cd1 = {}
gps = {}
wd = {}
wan = {}
ver = {}

thread0 = None
thread1 = None
thread2 = None
thread3 = None
thread4 = None
thread5 = None

cd0_first = 0
cd1_first = 0
gps_first = 0
wd_first = 0
wan_first = 0
ver_first = 0


"""def bg_cell0():
    global cd0, cd0_first

    while True:
        cd0 = cell_data0.cell_data()
        time.sleep(3)
        cd0_first = 1


def bg_cell1():
    global cd1, cd1_first

    while True:
        cd1 = cell_data1.cell_data()
        time.sleep(3)
        cd1_first = 1


def bg_gps():
    global gps, gps_first

    while True:
        gps = gps_data.gps_data()
        time.sleep(3)
        gps_first = 1


def bg_ver():
    global ver, ver_first

    while True:
        ver = version_data.version_data()
        time.sleep(3)
        ver_first = 1"""


def api_calls():
    global gps, gps_first
    global ver, ver_first
    global cd0, cd0_first
    global cd1, cd1_first
    global wan, wan_first

    while True:
        cd0_first = 1
        cd1_first = 1
        gps_first = 1
        ver_first = 1
        wan_first = 1

        try:
            ver = version_data.version_data()
        except BaseException as e:
            print(e)
        try:
            gps = gps_data.gps_data()
        except BaseException as f:
            print(f)
        try:
            cd0 = cell_data0.cell_data()
        except BaseException as g:
            print(g)
        try:
            cd1 = cell_data1.cell_data()
        except BaseException as h:
            print(h)
        try:
            wan = active_int.active_int()
        except BaseException as i:
            print(i)

        time.sleep(0.5)


def bg_wifi():
    global wd, wd_first

    while True:
        wd = wifi_data.wifi_data()
        time.sleep(2)
        wd_first = 1


"""def bg_act_int():
    global wan, wan_first

    while True:
        wan = active_int.active_int()
        time.sleep(2)
        wan_first = 1"""


@app.route('/cisco_gwdata')
def cosa():
    """cd = cell_data.cell_data()
    wd = wifi_data.wifi_data()
    wan = active_int.active_int()
    ver = version_data.version_data()"""

    global cd0
    global cd1
    global gps
    global wd
    global wan
    global ver

    iox_data = {
        "Manufacturer": "Cisco",
        "Model": "IR829"
    }

    all_run = cd0_first + cd1_first + gps_first + wd_first + wan_first + ver_first

    while all_run < 6:
        all_run = cd0_first + cd1_first + gps_first + wd_first + wan_first + ver_first

    interfaces = list(cd0['CellularInterface'])
    #print(interfaces)

    interfaces.append(cd1['CellularInterface'])
    interfaces.append(wd)

    #print(interfaces)

    iox_data.update(ver)
    #iox_data.update(cd)
    #iox_data.update(wd)
    iox_data.update({'Interface': interfaces})
    iox_data.update({'Location': gps['Location']})
    iox_data.update(wan)

    return jsonify({'Data': iox_data})


if __name__ == "__main__":
    print("starting background data thread")
    if thread0 is None:
        thread0 = Thread(target=api_calls)
        thread0.daemon = True
        thread0.start()
    if thread1 is None:
        thread1 = Thread(target=bg_wifi)
        thread1.daemon = True
        thread1.start()
    print("starting API app for Cisco GW data")
    app.run(host="0.0.0.0", port="8000", debug=True)

