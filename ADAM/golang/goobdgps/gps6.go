package main

import (
    "fmt"
    "github.com/adrianmo/go-nmea"
    "os"
    "time"
)

const PORT = "/dev/ttyAMA0"

func main() {
    ser, err := os.OpenFile(PORT, os.O_RDWR|os.O_CREATE, 0666)
    if err != nil {
        fmt.Println("Unable to open serial device:", err)
        return
    }
    defer ser.Close()

    reader := nmea.NewReader(ser)

    for {
        select {
        case msg, ok := <-reader.Messages():
            if !ok {
                fmt.Println("Reader closed")
                return
            }
            processMessage(msg)
        case <-time.After(500 * time.Millisecond):
            fmt.Println("Timed out while waiting for message")
        }
    }
}

func processMessage(msg nmea.Sentence) {
    if msg.Type() == "RMC" {
        m := msg.(nmea.RMC)
        fmt.Printf("Time: %s, Latitude: %f, Longitude: %f\n",
            m.Time, m.Position.Latitude(), m.Position.Longitude())
    }
}
