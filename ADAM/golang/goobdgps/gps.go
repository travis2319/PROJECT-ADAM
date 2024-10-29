package main

import (
	"encoding/binary"
	"encoding/csv"
	"fmt"
	"log"
	"math"
	"net"
	"os"
	"strings"
	"time"

	"github.com/adrianmo/go-nmea"
	"github.com/tarm/serial"
)

const (
	serialPort  = "/dev/ttyAMA0"
	baudRate    = 9600
	csvFilename = "gps_data.csv"
	udpHost     = "192.168.0.106"
	udpPort     = 3000
)

var csvHeaders = []string{"timestamp", "latitude", "longitude", "altitude"}

func main() {
	// Set up serial port
	c := &serial.Config{Name: serialPort, Baud: baudRate}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}
	defer s.Close()

	// Set up CSV file
	file, err := os.OpenFile(csvFilename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write CSV header if file is empty
	fi, err := file.Stat()
	if err != nil {
		log.Fatal(err)
	}
	if fi.Size() == 0 {
		if err := writer.Write(csvHeaders); err != nil {
			log.Fatal(err)
		}
	}

	// Set up UDP connection
	udpAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", udpHost, udpPort))
	if err != nil {
		log.Fatal(err)
	}
	conn, err := net.DialUDP("udp", nil, udpAddr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	// Main loop
	for {
		line, err := readLine(s)
		if err != nil {
			log.Printf("Error reading line: %v", err)
			continue
		}

		if strings.HasPrefix(line, "$GPGGA") {
			sentence, err := nmea.Parse(line)
			if err != nil {
				log.Printf("Error parsing NMEA sentence: %v", err)
				continue
			}

			if gga, ok := sentence.(nmea.GGA); ok {
				data := []string{
					fmt.Sprintf("%f", float64(time.Now().UnixNano()) / 1e9),
					fmt.Sprintf("%f", gga.Latitude),
					fmt.Sprintf("%f", gga.Longitude),
					fmt.Sprintf("%f", gga.Altitude),
				}

				// Write to CSV
				if err := writer.Write(data); err != nil {
					log.Printf("Error writing to CSV: %v", err)
				} else {
					fmt.Println("Data written to CSV")
				}

				// Send via UDP
				if err := sendToUDP(conn, gga); err != nil {
					log.Printf("Error sending to UDP: %v", err)
				} else {
					fmt.Println("Binary data sent to UDP socket")
				}
			}
		}

		time.Sleep(time.Second)
	}
}

func readLine(s *serial.Port) (string, error) {
	buf := make([]byte, 128)
	n, err := s.Read(buf)
	if err != nil {
		return "", err
	}
	return string(buf[:n]), nil
}

func sendToUDP(conn *net.UDPConn, gga nmea.GGA) error {
	buf := make([]byte, 24)
	binary.BigEndian.PutUint64(buf[0:8], math.Float64bits(float64(time.Now().UnixNano())/1e9))
	binary.BigEndian.PutUint64(buf[8:16], math.Float64bits(gga.Latitude))
	binary.BigEndian.PutUint64(buf[16:24], math.Float64bits(gga.Longitude))

	_, err := conn.Write(buf)
	return err
}
