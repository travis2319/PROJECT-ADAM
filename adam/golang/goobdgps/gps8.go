package main

import (
	"bytes" // Add this import for handling byte buffers
	"encoding/binary"
	"encoding/csv"
	"fmt"
	"github.com/adrianmo/go-nmea"
	"github.com/tarm/serial"
	"log"
	"net"
	"os"
	"strings"
	"time"
)

// GPS serial port configuration
const (
	serialPort = "/dev/ttyAMA0"
	baudRate   = 9600
)

// CSV file configuration
const (
	csvFilename = "gps_data.csv"
)

// UDP socket configuration
const (
	udpHost = "192.168.0.106"
	udpPort = 3000
)

// Struct for CSV data
type GPSData struct {
	Timestamp float64
	Latitude  float64
	Longitude float64
	Altitude  float64
}

func main() {
	// Open serial port for GPS
	serialConfig := &serial.Config{Name: serialPort, Baud: baudRate}
	ser, err := serial.OpenPort(serialConfig)
	if err != nil {
		log.Fatalf("Error opening serial port: %v", err)
	}
	defer ser.Close()

	// Open CSV file for writing
	file, err := os.OpenFile(csvFilename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("Error opening CSV file: %v", err)
	}
	defer file.Close()

	csvWriter := csv.NewWriter(file)
	defer csvWriter.Flush()

	// Start UDP client for sending data
	udpAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", udpHost, udpPort))
	if err != nil {
		log.Fatalf("Error resolving UDP address: %v", err)
	}

	udpConn, err := net.DialUDP("udp", nil, udpAddr)
	if err != nil {
		log.Fatalf("Error opening UDP connection: %v", err)
	}
	defer udpConn.Close()

	// Channel to handle program exit
	exitChan := make(chan struct{})
	go func() {
		fmt.Println("Press Enter to exit the program...")
		fmt.Scanln()
		close(exitChan)
	}()

	// Main loop to read and process GPS data
	for {
		select {
		case <-exitChan:
			fmt.Println("Exiting program...")
			return
		default:
			// Read from serial port
			buf := make([]byte, 128)
			n, err := ser.Read(buf)
			if err != nil {
				log.Printf("Error reading from serial: %v", err)
				continue
			}

			line := string(buf[:n])
			if strings.HasPrefix(line, "$GPGGA") {
				data, err := parseNMEA(line)
				if err != nil {
					log.Printf("Error parsing NMEA sentence: %v", err)
					continue
				}

				// Write to CSV
				if err := writeToCSV(csvWriter, data); err != nil {
					log.Printf("Error writing to CSV: %v", err)
				}

				// Send to UDP
				if err := sendToUDP(udpConn, data); err != nil {
					log.Printf("Error sending to UDP: %v", err)
				}
			}

			time.Sleep(1 * time.Second)
		}
	}
}

// Function to parse NMEA sentence and extract GPS data
func parseNMEA(line string) (GPSData, error) {
	s, err := nmea.Parse(line)
	if err != nil {
		return GPSData{}, fmt.Errorf("error parsing NMEA sentence: %v", err)
	}

	if gga, ok := s.(nmea.GGA); ok {
		data := GPSData{
			Timestamp: float64(time.Now().Unix()),
			Latitude:  gga.Latitude,
			Longitude: gga.Longitude,
			Altitude:  gga.Altitude,
		}

		return data, nil
	}

	return GPSData{}, fmt.Errorf("unsupported NMEA sentence type")
}

// Function to write GPS data to CSV file
func writeToCSV(writer *csv.Writer, data GPSData) error {
	record := []string{
		fmt.Sprintf("%.0f", data.Timestamp),
		fmt.Sprintf("%.6f", data.Latitude),
		fmt.Sprintf("%.6f", data.Longitude),
		fmt.Sprintf("%.2f", data.Altitude),
	}

	if err := writer.Write(record); err != nil {
		return fmt.Errorf("error writing CSV record: %v", err)
	}

	return nil
}

// Function to send GPS data over UDP
func sendToUDP(conn *net.UDPConn, data GPSData) error {
	buf := new(bytes.Buffer)
	err := binary.Write(buf, binary.BigEndian, data.Timestamp)
	if err != nil {
		return fmt.Errorf("error writing timestamp to buffer: %v", err)
	}
	err = binary.Write(buf, binary.BigEndian, data.Latitude)
	if err != nil {
		return fmt.Errorf("error writing latitude to buffer: %v", err)
	}
	err = binary.Write(buf, binary.BigEndian, data.Longitude)
	if err != nil {
		return fmt.Errorf("error writing longitude to buffer: %v", err)
	}

	_, err = conn.Write(buf.Bytes())
	if err != nil {
		return fmt.Errorf("error sending UDP data: %v", err)
	}

	return nil
}

