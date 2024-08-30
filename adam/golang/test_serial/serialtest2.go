package main

import (
    "log"
    "time"
    "github.com/tarm/serial"
)

var tryBauds = []int{38400, 9600, 230400, 115200, 57600, 19200}

func autoBaudrate(portName string, timeout time.Duration) (int, bool) {
    for _, baud := range tryBauds {
        config := &serial.Config{
            Name:        portName,
            Baud:        baud,
            ReadTimeout: timeout,
        }
        port, err := serial.OpenPort(config)
        if err != nil {
            log.Printf("Error opening port at baud %d: %v", baud, err)
            continue
        }

        port.Flush() // Clear input and output buffers

        _, err = port.Write([]byte("\x7F\x7F\r"))
        if err != nil {
            log.Printf("Error writing to port at baud %d: %v", baud, err)
            port.Close()
            continue
        }

        buf := make([]byte, 1024)
        n, err := port.Read(buf)
        if err != nil {
            log.Printf("Error reading from port at baud %d: %v", baud, err)
            port.Close()
            continue
        }

        response := buf[:n]
        log.Printf("Response from baud %d: %s", baud, string(response))

        if len(response) > 0 && response[len(response)-1] == '>' {
            log.Printf("Choosing baud %d", baud)
            port.Close()
            return baud, true
        }

        port.Close()
    }

    log.Println("Failed to choose baud")
    return 0, false
}

func main() {
    portName := "/dev/ttyAMA0"
    timeout := 2 * time.Second

    baud, success := autoBaudrate(portName, timeout)
    if success {
        log.Printf("Successfully detected baud rate: %d", baud)
    } else {
        log.Println("Failed to detect baud rate")
    }
}

