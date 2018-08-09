from flask import Flask,request, jsonify

import cell_data
import gps_data
import wifi_data
import active_int

app = Flask(__name__)


@app.route('/all')
def cosa():
    iox_data = {
        "Manufacturer": "Cisco",
        "Model": "IR829",
        "HWVersion": "v2.0",
        "FWVersion": "v1.7"
    }

    cd = cell_data.cell_data()
    wd = wifi_data.wifi_data()
    gps = gps_data.gps_data()
    wan = active_int.active_int()

    iox_data["CellularInterface"] = cd
    iox_data["WifiInterface"] = wd
    iox_data["Location"] = gps
    iox_data["ActiveInterface"] = wan

    return jsonify(iox_data)


if "__main__" == __name__:
    app.run(host="0.0.0.0", port="5100", debug=True)

