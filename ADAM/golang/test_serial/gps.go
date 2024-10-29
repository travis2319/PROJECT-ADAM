package main

import (
	"bufio"
	"fmt"
	"github.com/tarm/serial"
	"log"
	"strings"
	"time"
)

func main() {
	c := &serial.Config{Name: "/dev/ttyAMA0", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}
	defer s.Close()
	start := time.Now()
	scanner := bufio.NewScanner(s)
	for scanner.Scan() {
		line := scanner.Text()
		//fmt.Println("Received:", line)

		// Example parsing for GGA sentence (assuming NMEA format)
		if strings.HasPrefix(line, "$GPGGA") {
			parts := strings.Split(line, ",")
			if len(parts) >= 10 {
				latitude := parseCoordinate(parts[2], parts[3])
				longitude := parseCoordinate(parts[4], parts[5])
				altitude := parts[9]
				elapsed := time.Since(start)
                                log.Printf("Binomial took %s", elapsed)
				fmt.Printf("Latitude: %s, Longitude: %s, Altitude: %s\n", latitude, longitude, altitude)
			}
		}
	}
}

// Helper function to parse coordinates from NMEA format
func parseCoordinate(value string, direction string) string {
	if len(value) == 0 {
		return ""
	}

	// Convert NMEA format to standard decimal degrees
	degrees := value[:2]
	minutes := value[2:]
	coordinate := degrees + "°" + minutes + "'"

	if direction == "S" || direction == "W" {
		coordinate = "-" + coordinate
	}

	return coordinate
}

