import hdm_api
import re

verbose = True
cell_gps_data = {}


# Function to convert Location data to decimal location data
def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd


# Clean, Filter, and Parse GPS Data
def cell_gps(dt):

    gps = {}

    data = dt

    # Cleaning the console data
    data_clean0 = data.replace(" ", "")
    data_clean1 = data_clean0.replace("\n", " ")
    # adding another clean for later detail lines that are seperated by commas instead of linebreaks or spaces
    data_clean2 = data_clean1.replace(",", " ")
    data1 = dict(re.findall(r'(\S+):(".*?"|\S+)', data_clean2))

    # Parse Directional Data
    try:
        dmsNS = (re.split('[DegMinSecorth]+', data1["Latitude"]))[:4]
        dmsEW = (re.split('[DegMinSecest]+', data1["Longitude"]))[:4]
    except Exception:
        dmsNS = "None"
        dmsEW = "None"

    try:
        gps["Latitude"] = dms2dd(*dmsNS)
        gps["Longitude"] = dms2dd(*dmsEW)
    except Exception:
        gps["Latitude"] = "Incomplete"
        gps["Longitude"] = "Incomplete"

    gps["Status"] = data1.get("GPSautotrackingstatus", "None")
    gps["HDOP"] = data1.get("HDOP", "None")

    return gps


# Logic for getting GPS Data
def gps_data():

    all_data = hdm_api.show_cmd("show cell 0/0 gps detail")

    gps = cell_gps(all_data)

    cell_gps_data["Location"] = gps

    return cell_gps_data


# print(gps_data())

