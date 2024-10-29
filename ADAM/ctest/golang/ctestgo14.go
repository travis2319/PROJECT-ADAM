package main

import (
  "fmt"
  "log"
  "time"

  "go.bug.st/serial"
)

func GetRPMs() {
   mode := &serial.Mode{BaudRate: 38400}
   port, err := serial.Open("/dev/ttyACM0", mode)
  //c := &serial.Config{Name: "/dev/ttyACM0", Baud: 38400, ReadTimeout: time.Second * 5}
  //port, err := serial.OpenPort(c)
  if err != nil {
    log.Fatal(err)
  }
  defer port.Close()

  err = port.SetReadTimeout(10 * time.Second)
  if err != nil {
    log.Fatal(err)
  }

  if _, err = port.Write([]byte("ATZ\r")); err != nil {
    log.Fatal(err)
  }
  ReadAndLog(port)

  // Create a channel to signal the end of the 30-second period
  stop := time.After(30 * time.Second)

  for {
    select {
    case <-stop:
      fmt.Println("Completed 30 seconds of data collection.")
      return // Exit the function, which will close the port due to defer
    default:
      // Send the "01 0C" command to request the engine RPM
      if _, err = port.Write([]byte("01 0C\r")); err != nil {
        log.Fatal(err)
      }

      // Read and log the response from the device
      response := ReadAndLog(port)
      if len(response) < 8 { // Expecting at least 8 bytes for RPM response
        log.Fatal("Invalid response length")
      }

      // Calculate the engine RPM from the response
      rpm := ((int(response[6]) * 256) + int(response[7])) / 4
      // Print the engine RPM
      fmt.Printf("Engine RPM: %d\n", rpm)

      // Delay before sending the next request (e.g., 2 seconds)
      time.Sleep(2 * time.Second)
    }
  }
}

