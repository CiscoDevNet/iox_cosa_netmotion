from flask import Flask,request, jsonify

import cell_data
import wifi_data
import active_int
import time

app = Flask(__name__)

cd = {}
wd = {}
wan = {}

thread0 = None
thread1 = None
thread2 = None


def bg_cell():
    global cd

    while True:
        cd = cell_data.cell_data()

        time.sleep(2)


def bg_wifi():
    global wd

    while True:
        wd = wifi_data.wifi_data()

        time.sleep(2)


def bg_act_int():
    global wan

    while True:
        wan = active_int.active_int()

        time.sleep(2)


@app.route('/all')
def cosa():
    cd = cell_data.cell_data()
    wd = wifi_data.wifi_data()
    wan = active_int.active_int()

    iox_data = {
        "Manufacturer": "Cisco",
        "Model": "IR829",
        "HWVersion": "NA",
        "FWVersion": "NA"
    }

    iox_data.update(cd)
    iox_data.update(wd)
    iox_data.update(wan)

    return jsonify(iox_data)


if "__main__" == __name__:
    """print("starting background data thread")
    if thread0 is None:
        thread0 = Thread(target=bg_cell)
        thread0.daemon = True
        thread0.start()
    if thread1 is None:
        thread1 = Thread(target=bg_wifi)
        thread1.daemon = True
        thread1.start()
    if thread2 is None:
        thread2 = Thread(target=bg_act_int)
        thread2.daemon = True
        thread2.start()
    print("starting API app for Cisco GW data")"""
    app.run(host="0.0.0.0", port="8000", debug=True)

