import requests


# Logic for getting GPS Data
def gps_data():
    gps = {
        "Status": "tracking",
        "Latitude": "47.6097",
        "Longitude": "-122.3331",
        "Accuracy": "73",
        "HDOP": "1.2"
    }

    return gps
