package main

import (
    "log"
    "time"
    "github.com/tarm/serial"
)

func main() {
    port := "/dev/ttyAMA0" // Adjust this to your Raspberry Pi's serial port
    baudRates := []int{38400, 9600, 230400, 115200, 57600, 19200} // Baud rates to test

    var serialPort *serial.Port
    var err error

    // Function to send probe signal and detect response
    detectBaudRate := func(baud int) bool {
        // Close the serial port if it's already open
        if serialPort != nil {
            serialPort.Close()
        }

        // Configure and open the serial port with the current baud rate
        config := &serial.Config{
            Name: port,
            Baud: baud,
        }

        serialPort, err = serial.OpenPort(config)
        if err != nil {
            log.Printf("Error opening port at baud rate %d: %v", baud, err)
            return false
        }

        // Send sync bytes or probe signal
        _, err = serialPort.Write([]byte("SYNC"))
        if err != nil {
            log.Printf("Error writing to port at baud rate %d: %v", baud, err)
            return false
        }

        // Wait and read response
        buf := make([]byte, 100)
        n, err := serialPort.Read(buf)
        if err != nil {
            log.Printf("Error reading from port at baud rate %d: %v", baud, err)
            return false
        }

        // Check response and return true if detection is successful
        return n > 0 && string(buf[:n]) == "ACK"
    }

    // Try different baud rates and detect
    for _, baud := range baudRates {
        log.Printf("Trying baud rate: %d", baud)
        if detectBaudRate(baud) {
            log.Printf("Detected baud rate: %d", baud)
            // Use this baud rate for further communication
            break
        }
        time.Sleep(1 * time.Second) // Adjust delay as necessary
    }

    // Further communication using the detected baud rate
    // Example: serialPort.Write([]byte("Hello"))

    if serialPort != nil {
        serialPort.Close()
    }
}

