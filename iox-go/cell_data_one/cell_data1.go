package cell_data_one

import (
	//"fmt"
	"../hdm_api"
	"regexp"

)

type Cellular_data struct {
	ID          string
	Type        string
	IMEI        string
	IMSI        string
	PhoneNumber string
	ISP         string
	Connected   string
	Band        string
	Channel     string
	SINR        string
	RSRQ        string
	RSRP        string
	RSSI        string
	Technology  string
	Carrier     string
	Roaming     string
	TXbytes     string
	RXbytes     string
}

type Cell_dict_data struct {
	CellularInterface Cellular_data
}



func cell_data_find(str string, dt string) (string) {
	orig_data := str
	reg := dt
	re := regexp.MustCompile(reg)
	var Data string
	preData := len(re.FindAllStringSubmatch(orig_data, -1))
	if (preData < 1){
		Data = ""
	}else {
		Data = re.FindAllStringSubmatch(orig_data, -1)[0][1]
	}

	return Data
}

func Cell_all(dt string) (*Cellular_data){
	// Cellular information variable definitions
	var ID string
	var Type string
	var IMEI string
	var IMSI string
	var PhoneNumber string
	var ISP string
	var Connected string
	var Band string
	var Channel string
	var SINR string
	var RSRQ string
	var RSRP string
	var RSSI string
	var Technology string
	var Carrier string
	var Carrier0 string
	var Carrier1 string
	var Roaming string
	var TXbytes string
	var RXbytes string

	var str = dt

	ID = "Cellular1/0"
	Type = "WWAN"

	//Data Cleaning for Cell Data

	IMEI = cell_data_find(str, `International\s+Mobile\s+Equipment\s+Identity\s+\(IMEI\)\s+=\s+(\S+)`)

	IMSI = cell_data_find(str, `International\s+Mobile\s+Subscriber\s+Identity\s+\(IMSI\)\s+=\s+(\S+)`)

	PhoneNumber = cell_data_find(str, `Digital\s+Network\-Number\s+\(MSISDN\)\s+=\s+(\S+)`)

	ISP = cell_data_find(str, `Carrier\s+=\s+(\S+)`)

	conn := cell_data_find(str, `Radio\s+power\s+mode\s+=\s+(\S+)`)
	if (conn == "online") {
		Connected = "Connected"
	} else {
		Connected = "Disconnected"
	}


	Band = cell_data_find(str, `LTE\s+Band\s+=\s+(\d+)`)

	Channel = cell_data_find(str, `LTE\s+Rx\s+Channel\s+Number\s+=\s+(\d+)`)

	SINR = cell_data_find(str, `Current\s+SNR\s+=\s+(\S+\d+)`)

	RSRQ = cell_data_find(str, `Current\s+RSRQ\s+=\s+(\S+\d+)`)

	RSRP = cell_data_find(str, `Current\s+RSRP\s+=\s+(\S+\d+)`)

	RSSI = cell_data_find(str, `Current\s+RSSI\s+=\s+(\S+\d+)`)

	Technology = cell_data_find(str, `Radio\s+Access\s+Technology\(RAT\)\s+Selected\s+=\s+(\S+)`)

	Carrier0 = cell_data_find(str, `Mobile\s+Country\s+Code\s+\(MCC\)\s+=\s+(\S+)`)

	Carrier1 = cell_data_find(str, `Mobile\s+Network\s+Code\s+\(MNC\)\s+=\s+(\S+)`)

	Carrier = Carrier0 + "-" + Carrier1

	Roaming = cell_data_find(str, `Current\s+Roaming\s+Status\s+=\s+(\S+)`)

	TXbytes = cell_data_find(str, `Data\s+Transmitted\s+=\s+(\S+)`)

	RXbytes = cell_data_find(str, `bytes,\s+Received\s+=\s+(\S+)`)

	c_data := Cellular_data{}

	// Save data to struct
	c_data.ID = ID
	c_data.Type = Type
	c_data.IMEI = IMEI
	c_data.IMSI = IMSI
	c_data.PhoneNumber = PhoneNumber
	c_data.ISP = ISP
	c_data.Connected = Connected
	c_data.Band = Band
	c_data.Channel = Channel
	c_data.SINR = SINR
	c_data.RSRQ = RSRQ
	c_data.RSRP = RSRP
	c_data.RSSI = RSSI
	c_data.Technology = Technology
	c_data.Carrier = Carrier
	c_data.Roaming = Roaming
	c_data.TXbytes = TXbytes
	c_data.RXbytes = RXbytes

	//fmt.Println(c_data)

	return &c_data


}

func Cell_data() (*Cell_dict_data){
	cmd_out := hdm_api.Show_cmd_ssh("show cell 1/0 all")
	final_cell_data := Cell_dict_data{}

	if (cmd_out == "Error") {
		return &final_cell_data
	}else {

		dt_out := *Cell_all(cmd_out)
		//fmt.Println(dt_out)

		final_cell_data.CellularInterface = dt_out

		//dt_out := Cell_all(cmd_out)
		//fmt.Println(dt_out)
		return &final_cell_data
	}
}