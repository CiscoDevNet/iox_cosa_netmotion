from flask import Flask, request, jsonify

import cell_data
import wifi_data
import active_int
import version_data
import time
from threading import Thread

app = Flask(__name__)

cd = {}
wd = {}
wan = {}
ver = {}

thread0 = None
thread1 = None
thread2 = None
thread3 = None

cd_first = 0
wd_first = 0
wan_first = 0
ver_first = 0


def bg_cell():
	global cd, cd_first

	while True:
		cd = cell_data.cell_data()
		time.sleep(2)
		cd_first = 1


def bg_wifi():
	global wd, wd_first

	while True:
		wd = wifi_data.wifi_data()
		time.sleep(2)
		wd_first = 1


def bg_act_int():
	global wan, wan_first

	while True:
		wan = active_int.active_int()
		time.sleep(2)
		wan_first = 1


def bg_ver():
	global ver, ver_first

	while True:
		ver = version_data.version_data()
		time.sleep(2)
		ver_first = 1


@app.route('/all')
def cosa():
	"""cd = cell_data.cell_data()
	wd = wifi_data.wifi_data()
	wan = active_int.active_int()
	ver = version_data.version_data()"""

	global cd
	global wd
	global wan
	global ver

	iox_data = {
		"Manufacturer": "Cisco",
		"Model": "IR829"
	}

	all_run = cd_first + wd_first + wan_first + ver_first

	while all_run < 4:
		all_run = cd_first + wd_first + wan_first + ver_first

	interfaces = list(cd['CellularInterface'])
	#print(interfaces)

	interfaces.append(wd)

	#print(interfaces)

	iox_data.update(ver)
	#iox_data.update(cd)
	#iox_data.update(wd)
	iox_data.update({'Interface': interfaces})
	iox_data.update(wan)

	return jsonify({'Data': iox_data})


if __name__ == "__main__":
	print("starting background data thread")
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
	if thread3 is None:
		thread3 = Thread(target=bg_ver)
		thread3.daemon = True
		thread3.start()
	print("starting API app for Cisco GW data")
	app.run(host="0.0.0.0", port="8000", debug=True)
