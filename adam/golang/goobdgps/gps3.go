package main

import (
    "fmt"
    "log"
    "time"

    "github.com/tarm/serial"
    "github.com/keegancsmith/nmea"
)

func main() {
    // Open the serial port
    port, err := serial.Open("/dev/ttyAMA0", &serial.Config{BaudRate: 9600})
    if err != nil {
        log.Fatal(err)
    }
    defer port.Close()

    // Set timeout duration
    port.Flush() // Clear buffer before starting
    port.SetTimeout(time.Second * 5)

    // Continuously read NMEA sentences from the GPS module
    for {
        sentenceBytes, err := port.Read(1024)
        if err != nil {
            log.Println("Error reading:", err)
            continue
        }

        sentenceStr := string(sentenceBytes)
        sentences := nmea.Split(sentenceStr)

        // Process each sentence
        for _, s := range sentences {
            if len(s) == 0 || !nmea.IsValidSentence(s) {
                continue
            }

            decodedSentence, err := nmea.Parse(s)
            if err != nil {
                log.Printf("Failed to parse %q: %v\n", s, err)
                continue
            }

            switch decodedSentence.Type {
            case "RMC":
                rmc := decodedSentence.(nmea.Rmc)
                fmt.Printf("Time: %s, Latitude: %f, Longitude: %f\n",
                    rmc.Timestamp, rmc.Latitude, rmc.Longitude)
            default:
                fmt.Printf("%s: %+v\n", decodedSentence.Type, decodedSentence)
            }
        }
    }
}
