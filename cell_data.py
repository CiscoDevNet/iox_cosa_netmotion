import paramiko


# Logic for getting Cell Data
def cell_data():

    cell_int0 = {
        "ID": "WWAN0",
        "IMEI": "353776060002670",
        "IMSI": "325911480066607802",
        "PhoneNumber": "4255551212",
        "Connected": "Connected",
        "Technology": "CDMA 1xEV-DO Rev A",
        "Roaming": "Home",
        "SID": "6-12",
        "TXbytes": "546780",
        "RXbytes": "859300",
        "RSSI": "-68",
        "SINR": "30"
    }

    cell_int1 = {
        "ID": "WWAN1",
        "IMEI": "359225050020502",
        "IMSI": "32023699260",
        "PhoneNumber": "2065551212",
        "Connected": "Connected",
        "Technology": "LTE",
        "Roaming": "Home",
        "PLMN": "123-456",
        "TXbytes": "1560780",
        "RXbytes": "2879300",
        "RSSI": "-57",
        "RSRP": "-79",
        "RSRQ": "-9",
        "SINR": "30"
    }

    cd = [cell_int0, cell_int1]

    return cd
