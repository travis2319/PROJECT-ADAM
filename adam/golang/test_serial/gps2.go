package main

import (
    "bufio"
    "fmt"
    "github.com/tarm/serial"
    "log"
    "strconv"
    "strings"
    "time"
)

func main() {
    c := &serial.Config{Name: "/dev/ttyAMA0", Baud: 9600}
    s, err := serial.OpenPort(c)
    if err != nil {
        log.Fatalf("Failed to open serial port: %v", err)
    }
    defer s.Close()

    // Create a channel to send lines from the serial port to the processing function
    dataChannel := make(chan string)

    // Start a goroutine for reading from the serial port
    go readSerialPort(s, dataChannel)

    // Process data received from the channel
    start := time.Now()
    for line := range dataChannel {
        //log.Printf("Received line: %s", line)
        if strings.HasPrefix(line, "$GPGGA") {
            parts := strings.Split(line, ",")
            if len(parts) >= 10 {
                latitude := parseCoordinate(parts[2], parts[3])
                longitude := parseCoordinate(parts[4], parts[5])
                altitude := parts[9]

                // Calculate elapsed time
                elapsed := time.Since(start)
                fmt.Printf("Latitude: %s, Longitude: %s, Altitude: %s\n", latitude, longitude, altitude)
                fmt.Printf("Time elapsed since start: %s\n", elapsed)

                // Reset start time for next measurement
                start = time.Now()
            } else {
                log.Printf("Invalid GPGGA sentence: %s", line)
            }
        } else if strings.HasPrefix(line, "$GPGLL") {
            parts := strings.Split(line, ",")
            if len(parts) >= 7 {
                latitude := parseCoordinate(parts[1], parts[2])
                longitude := parseCoordinate(parts[3], parts[4])
                timeUTC := parts[5]

                // Calculate elapsed time
                elapsed := time.Since(start)
                fmt.Printf("Latitude: %s, Longitude: %s, UTC Time: %s\n", latitude, longitude, timeUTC)
                fmt.Printf("Time elapsed since start: %s\n", elapsed)

                // Reset start time for next measurement
                start = time.Now()
            } else {
                log.Printf("Invalid GPGLL sentence: %s", line)
            }
        }
    }
}

// Function to read from the serial port and send data to a channel
func readSerialPort(s *serial.Port, dataChannel chan<- string) {
    scanner := bufio.NewScanner(s)
    for scanner.Scan() {
        line := scanner.Text()
        //log.Printf("Read line from serial port: %s", line)
        dataChannel <- line
    }
    if err := scanner.Err(); err != nil {
        log.Fatalf("Error reading from serial port: %v", err)
    }
    close(dataChannel)
}

// Helper function to parse coordinates from NMEA format
func parseCoordinate(value string, direction string) string {
    if len(value) == 0 {
        return ""
    }

    // Convert NMEA format to standard decimal degrees
    degrees, err := strconv.ParseFloat(value[:2], 64)
    if err != nil {
        log.Printf("Error parsing degrees: %v", err)
        return ""
    }

    minutes, err := strconv.ParseFloat(value[2:], 64)
    if err != nil {
        log.Printf("Error parsing minutes: %v", err)
        return ""
    }

    decimalDegrees := degrees + minutes/60
    if direction == "S" || direction == "W" {
        decimalDegrees = -decimalDegrees
    }

    return fmt.Sprintf("%.6f", decimalDegrees)
}

