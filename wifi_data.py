import pysnmp


# Logic for getting WiFi Data
def wifi_data():
    wgb0 = {
            "ID": "WiFi1",
            "Signal": "67",
            "RSSI": "-80",
            "SSID": "Corporate-WiFi",
            "BSSID": "01:23:45:67:89:AB",
            "TxRate": "130000",
            "RxRate": "130000",
            "Authentication": "WPA2-Enterprise",
            "Encryption": "AES-128"
            }

    wd = [wgb0]

    return wd
