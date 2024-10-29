package main

import (
    "fmt"
    "github.com/adrianmo/go-nmea"
    "io/ioutil"
    "log"
    "os"
    "strings"
    "time"
)

func getPortName() string {
    contents, err := ioutil.ReadFile("/boot/config.txt")
    if err != nil {
        log.Fatalf("Could not read config.txt: %v", err)
    }

    if strings.Contains(string(contents), "enable_uart=1") {
        return "/dev/ttyS0"
    } else {
        return "/dev/ttyAMA0"
    }
}

func main() {
    portName := getPortName()

    sentenceChan := make(chan nmea.Sentence)
    done := make(chan struct{})

    go func() {
        reader := nmea.NewReader(os.Stdin)
        for {
            select {
            case <-done:
                return
            default:
                s, err := reader.Read()
                if err != nil {
                    log.Println("Error reading:", err)
                    continue
                }
                sentenceChan <- s
            }
        }
    }()

    for {
        select {
        case s := <-sentenceChan:
            if s.DataType() == nmea.TypeRMC {
                rmc := s.(nmea.RMC)
                fmt.Printf("Time: %s, Latitude: %f, Longitude: %f\n",
                    rmc.Timestamp, rmc.Latitude, rmc.Longitude)
            }
        case <-time.After(500 * time.Millisecond):
            // Timeout after waiting for half a second without receiving a sentence
            fmt.Println("No valid sentence received.")
        }
    }

    close(done)
    close(sentenceChan)
}
