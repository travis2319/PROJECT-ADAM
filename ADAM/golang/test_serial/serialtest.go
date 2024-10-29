package main

import (
    "log"
    "github.com/tarm/serial"
)

func main() {
    // Configure the serial port
    config := &serial.Config{
        Name: "/dev/ttyAMA0",  // or whatever your serial port is
        Baud: 9600,
    }
    port, err := serial.OpenPort(config)
    if err != nil {
        log.Fatalf("serial port opening error: %v", err)
    }
    defer port.Close()

    // Example: reading from the serial port
    buf := make([]byte, 128)
    for {
        n, err := port.Read(buf)
        if err != nil {
            log.Fatalf("serial port reading error: %v", err)
        }
        if n > 0 {
            log.Printf("Received: %s", buf[:n])
        }
    }
}

