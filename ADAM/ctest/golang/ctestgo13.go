package main

import (
  "encoding/json"
  "log"
  "time"

  "github.com/tarm/serial"
  "github.com/trestletech/gobd"
)

// SensorData represents the car's sensor data
type SensorData struct {
  Time      int64    json:"time"
  Load      *float64 json:"load"
  Temp      *int     json:"temp"
  RPM       *float64 json:"rpm"
  Speed     *int     json:"speed"
  Throttle  *float64 json:"throttle"
  FuelLevel *float64 json:"fuel_level"
}

// fetchData retrieves data from the OBD device and populates the SensorData struct
func fetchData(obd *gobd.OBD, data *SensorData) {
  load, err := obd.GetEngineLoad()
  if err == nil {
    data.Load = &load
  }

  temp, err := obd.GetCoolantTemp()
  if err == nil {
    data.Temp = &temp
  }

  rpm, err := obd.GetRPM()
  if err == nil {
    data.RPM = &rpm
  }

  speed, err := obd.GetSpeed()
  if err == nil {
    data.Speed = &speed
  }

  throttle, err := obd.GetThrottlePosition()
  if err == nil {
    data.Throttle = &throttle
  }

  fuel, err := obd.GetFuelLevel()
  if err == nil {
    data.FuelLevel = &fuel
  }
}

func main() {
  c := &serial.Config{Name: "/dev/ttyACM0", Baud: 38400, ReadTimeout: time.Second * 5}
  var s *serial.Port
  var err error

  for i := 0; i < 3; i++ { // Retry opening the port 3 times
    s, err = serial.OpenPort(c)
    if err == nil {
      break
    }
    log.Printf("Error opening serial port: %v. Retrying...", err)
    time.Sleep(2 * time.Second)
  }

  if err != nil {
    log.Fatalf("Failed to open serial port: %v", err)
  }

  obd, err := gobd.NewDebugOBD(s, log.Printf)
  if err != nil {
    log.Fatal(err)
  }

  tick := time.Tick(3 * time.Second)
  for range tick {
    data := SensorData{Time: time.Now().Unix()}
    fetchData(obd, &data)

    jsonData, err := json.Marshal(data)
    if err != nil {
      log.Printf("Error marshalling data to JSON: %v", err)
      continue
    }

    log.Println(string(jsonData))
  }
}
