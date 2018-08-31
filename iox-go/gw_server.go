package main

import (
	"./cell_data_zero"
	"./cell_data_one"
	"./gps_data"
	"./version_data"
	"./act_int_data"
	"./wifi_data"
	"fmt"
	"encoding/json"
	"time"
	"github.com/julienschmidt/httprouter"
	"net/http"
	"log"
	"bytes"
)


type CiscoGW struct {
	ActiveInterface     string
	ID                  string
	FWVersion           string
	HWVersion           string
	Interface           []interface{}
	Location            gps_data.Gps
	Manufacturer        string
	Model               string

}

var all_data CiscoGW
var gw_json  string
var cell0 cell_data_zero.Cellular_data
var cell1 cell_data_one.Cellular_data
var wifi_int wifi_data.Wifi_struct


func JSONMarshalIndent(v interface{}, safeEncoding bool) ([]byte, error) {
	b, err := json.MarshalIndent(v, "", "    ")

	if safeEncoding {
		b = bytes.Replace(b, []byte("\\u003c"), []byte("<"), -1)
		b = bytes.Replace(b, []byte("\\u003e"), []byte(">"), -1)
		b = bytes.Replace(b, []byte("\\u0026"), []byte("&"), -1)
	}
	return b, err
}

func gps() {
	for {
		gps := *gps_data.Gps_data()

		all_data.Location = gps.Location

		time.Sleep(500 * time.Millisecond)

	}

}

func cellular0() {
	for {
		cell0 = cell_data_zero.Cellular_data(cell_data_zero.Cell_data().CellularInterface)
		time.Sleep(500 * time.Millisecond)
	}
}

func cellular1() {
	for {
		cell1 = cell_data_one.Cellular_data(cell_data_one.Cell_data().CellularInterface)
		time.Sleep(500 * time.Millisecond)
	}
}

func wifi() {
	wifi_int = wifi_data.Wifi_struct(wifi_data.Wifi_data().WifiInterface)
	time.Sleep(500 * time.Millisecond)
}

func act_int() {
	for {
		act := act_int_data.Active_int()
		all_data.ActiveInterface = act.ActiveInterface
		time.Sleep(500 * time.Millisecond)
	}
}

func version() {
	vers := version_data.Version_data()


	all_data.Manufacturer = "Cisco"
	all_data.Model = "IR829"

	all_data.ID = vers.DeviceID
	all_data.FWVersion = vers.FWVersion
	all_data.HWVersion = vers.HWVersion
}

func interfaces() {
	for {
		all_data.Interface = append([]interface{}{cell0, cell1, wifi_int})
		time.Sleep(500 * time.Millisecond)
	}
}

func json_proc() {
	for {
		read_data := all_data
		cisco_json, err := JSONMarshalIndent(read_data, true)
		if err != nil {
			fmt.Println(err)
			return
		}
		gw_json = string(cisco_json)
             	//fmt.Println(gw_json)
             	//time.Sleep(5000 * time.Millisecond)
        }
}

func Index(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	w.Header().Set("Content-Type", "application/json")
    	fmt.Fprint(w, gw_json)
}

func main() {
	// defining structs / maps for GW Data



	//fmt.Println(all_data.Interface[0])
	//fmt.Println(all_data.Interface[1])

	//fmt.Println(all_data)

	go version()
	go gps()
	go cellular0()
	go cellular1()
	go act_int()
	go wifi()
	go interfaces()
	go json_proc()

	router := httprouter.New()
    	router.GET("/", Index)

	log.Fatal(http.ListenAndServe(":8080", router))

}
