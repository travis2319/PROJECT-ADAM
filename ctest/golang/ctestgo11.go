package main

import (
  "fmt"
  "log"
  "strconv"
  "strings"
  "time"

  "github.com/tarm/serial"
)

// OBD represents the OBD connection
type OBD struct {
  port *serial.Port
}

// NewOBD initializes a new OBD connection
func NewOBD(portName string, baudRate int) (*OBD, error) {
  config := &serial.Config{
    Name: portName,
    Baud: baudRate,
  }
  port, err := serial.OpenPort(config)
  if err != nil {
    return nil, err
  }
  return &OBD{port: port}, nil
}

// Close closes the OBD connection
func (o *OBD) Close() error {
  return o.port.Close()
}

// SendCommand sends a command to the OBD device
func (o *OBD) SendCommand(cmd string) (string, error) {
  _, err := o.port.Write([]byte(cmd + "\r"))
  if err != nil {
    return "", err
  }
  time.Sleep(time.Second)

  buf := make([]byte, 128)
  n, err := o.port.Read(buf)
  if err != nil {
    return "", err
  }

  return string(buf[:n]), nil
}

// ParseRPM parses the RPM from the OBD response
func (o *OBD) ParseRPM(response string) (int, error) {
  // Example response: "41 0C 1A F8"
  // RPM = ((A * 256) + B) / 4
  parts := strings.Fields(response)
  if len(parts) < 4 {
    return 0, fmt.Errorf("invalid response format")
  }
  a, err := strconv.ParseInt(parts[2], 16, 64)
  if err != nil {
    return 0, err
  }
  b, err := strconv.ParseInt(parts[3], 16, 64)
  if err != nil {
    return 0, err
  }
  rpm := ((a * 256) + b) / 4
  return int(rpm), nil
}

func main() {
  obd, err := NewOBD("/dev/ttyACM0", 38400)
  if err != nil {
    log.Fatal(err)
  }
  defer obd.Close()

  // Initialize OBD communication
  fmt.Println("Sending ATZ command to initialize OBD communication...")
  _, err = obd.SendCommand("ATZ")
  if err != nil {
    log.Fatal(err)
  }

  // Set protocol to auto
  fmt.Println("Setting protocol to auto (ATSP0)...")
  _, err = obd.SendCommand("ATSP0")
  if err != nil {
    log.Fatal(err)
  }

  iterationCount := 0
  for iterationCount < 10 {
    // Send RPM request
    fmt.Println("Sending RPM request (010C)...")
    response, err := obd.SendCommand("010C")
    if err != nil {
      log.Println(err)
      continue
    }

    // Parse RPM data
    fmt.Printf("Received response: %s\n", response)
    rpm, err := obd.ParseRPM(response)
    if err != nil {
      log.Println(err)
      continue
    }

    fmt.Printf("Current RPM: %d\n", rpm)
    iterationCount++
    time.Sleep(time.Second)
  }

  fmt.Println("Completed 10 iterations of RPM retrieval.")
}
