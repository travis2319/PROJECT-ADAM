package main

import (
    "encoding/binary"
    "fmt"
    "log"
    "net"
    "os"
    "time"

    "github.com/adrianmo/go-nmea"
    "github.com/tarm/serial"
)

const (
    csvFilename = "gps_data.csv"
    csvHeaders  = "timestamp,latitude,longitude,altitude"
    udpHost     = "192.168.0.106"
    udpPort     = 3000
)

var (
    running = true
)

func writeToCSV(data map[string]interface{}) {
    file, err := os.OpenFile(csvFilename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err!= nil {
        log.Fatal(err)
    }
    defer file.Close()

    if _, err := file.WriteString(fmt.Sprintf("%s\n", csvHeaders)); err!= nil {
        log.Fatal(err)
    }

    if _, err := file.WriteString(fmt.Sprintf("%v,%v,%v,%v\n", data["timestamp"], data["latitude"], data["longitude"], data["altitude"])); err!= nil {
        log.Fatal(err)
    }
}

func sendToUDP(data map[string]interface{}) {
    udpAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", udpHost, udpPort))
    if err!= nil {
        log.Fatal(err)
    }

    conn, err := net.DialUDP("udp", nil, udpAddr)
    if err!= nil {
        log.Fatal(err)
    }
    defer conn.Close()

    binaryData := make([]byte, 24)
    binary.LittleEndian.PutUint64(binaryData[:8], uint64(data["timestamp"].(float64)))
    binary.LittleEndian.PutUint64(binaryData[8:16], uint64(data["latitude"].(float64)))
    binary.LittleEndian.PutUint64(binaryData[16:24], uint64(data["longitude"].(float64)))

    if _, err := conn.Write(binaryData); err!= nil {
        log.Fatal(err)
    }
}

func exitProgram() {
    fmt.Println("Press Enter to exit the program...")
    var input string
    fmt.Scanln(&input)
    running = false
}

func main() {
    // Open serial port
    serialPort, err := serial.Open(&serial.Config{Name: "/dev/ttyAMA0", Baud: 9600, Timeout: time.Second})
    if err!= nil {
        log.Fatal(err)
    }
    defer serialPort.Close()

    // Start exit thread
    go exitProgram()

    for running {
        // Read from serial port
        line, err := serialPort.ReadString('\n')
        if err!= nil {
            log.Fatal(err)
        }

        // Parse NMEA sentence
        msg, err := nmea.Parse(line)
        if err!= nil {
            log.Fatal(err)
        }

        // Extract data
        data := map[string]interface{}{
            "timestamp": time.Now().UnixNano() / 1e6,
            "latitude":  msg.Latitude,
            "longitude": msg.Longitude,
            "altitude":  msg.Altitude,
        }

        // Write to CSV
        writeToCSV(data)

        // Send to UDP
        sendToUDP(data)

        time.Sleep(time.Second)
    }

    log.Println("Program terminated.")
}
