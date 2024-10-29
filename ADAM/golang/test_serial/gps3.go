package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"github.com/tarm/serial"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	// Open serial port
	serialPort, err := openSerialPort("/dev/ttyAMA0", 9600)
	if err != nil {
		log.Fatalf("Failed to open serial port: %v", err)
	}
	defer serialPort.Close()

	// Open CSV file
	csvFile, err := openCSVFile("gps_data.csv", !isFileExists("gps_data.csv"))
	if err != nil {
		log.Fatalf("Failed to open CSV file: %v", err)
	}
	defer csvFile.Close()

	// Create a CSV writer
	csvWriter := csv.NewWriter(csvFile)

	// Start reading from serial port
	dataChannel := make(chan string)
	go readSerialPort(serialPort, dataChannel)

	// Process data received from the channel
	startTime := time.Now()
	for line := range dataChannel {
		log.Printf("Received line: %s", line)

		if strings.HasPrefix(line, "$GPGGA") {
			processGPGGA(line, csvWriter, &startTime)
		} else if strings.HasPrefix(line, "$GPGLL") {
			processGPGLL(line, csvWriter, &startTime)
		} else {
			log.Printf("Unsupported NMEA sentence: %s", line)
		}
	}
}

func openSerialPort(device string, baud int) (*serial.Port, error) {
	config := &serial.Config{Name: device, Baud: baud}
	return serial.OpenPort(config)
}

func openCSVFile(filename string, createNew bool) (*os.File, error) {
	flags := os.O_APPEND | os.O_CREATE | os.O_WRONLY
	if createNew {
		flags |= os.O_TRUNC
	}
	return os.OpenFile(filename, flags, 0644)
}

func isFileExists(filename string) bool {
	_, err := os.Stat(filename)
	return !os.IsNotExist(err)
}

func readSerialPort(s *serial.Port, dataChannel chan<- string) {
	scanner := bufio.NewScanner(s)
	for scanner.Scan() {
		dataChannel <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		log.Fatalf("Error reading from serial port: %v", err)
	}
	close(dataChannel)
}

func processGPGGA(line string, csvWriter *csv.Writer, startTime *time.Time) {
	parts := strings.Split(line, ",")
	if len(parts) < 15 {
		log.Printf("Invalid GPGGA sentence: %s", line)
		return
	}

	latitude, err := parseNmeaCoordinate(parts[2], parts[3])
	if err != nil {
		log.Printf("Error parsing latitude: %v", err)
		return
	}
	longitude, err := parseNmeaCoordinate(parts[4], parts[5])
	if err != nil {
		log.Printf("Error parsing longitude: %v", err)
		return
	}
	altitude := parts[9]
	fixQuality := parts[6]
	satellites := parts[7]
	hdop := parts[8]
	height := parts[11]

	elapsed := time.Since(*startTime)
	log.Printf("Latitude: %f, Longitude: %f, Altitude: %s, Fix Quality: %s, Satellites: %s, HDOP: %s, Height: %s", latitude, longitude, altitude, fixQuality, satellites, hdop, height)
	log.Printf("Time elapsed since start: %s", elapsed)

	err = csvWriter.Write([]string{
		fmt.Sprintf("%.6f", latitude),
		fmt.Sprintf("%.6f", longitude),
		altitude,
		fixQuality,
		satellites,
		hdop,
		height,
		elapsed.String(),
	})
	if err != nil {
		log.Printf("Error writing to CSV file: %v", err)
	}
	csvWriter.Flush()

	*startTime = time.Now()
}

func processGPGLL(line string, csvWriter *csv.Writer, startTime *time.Time) {
	parts := strings.Split(line, ",")
	if len(parts) < 7 {
		log.Printf("Invalid GPGLL sentence: %s", line)
		return
	}

	latitude, err := parseNmeaCoordinate(parts[1], parts[2])
	if err != nil {
		log.Printf("Error parsing latitude: %v", err)
		return
	}
	longitude, err := parseNmeaCoordinate(parts[3], parts[4])
	if err != nil {
		log.Printf("Error parsing longitude: %v", err)
		return
	}
	timeUTC := parts[5]

	elapsed := time.Since(*startTime)
	log.Printf("Latitude: %f, Longitude: %f, UTC Time: %s", latitude, longitude, timeUTC)
	log.Printf("Time elapsed since start: %s", elapsed)

	err = csvWriter.Write([]string{
		fmt.Sprintf("%.6f", latitude),
		fmt.Sprintf("%.6f", longitude),
		"",
		"",
		"",
		"",
		"",
		elapsed.String(),
	})
	if err != nil {
		log.Printf("Error writing to CSV file: %v", err)
	}
	csvWriter.Flush()

	*startTime = time.Now()
}

func parseNmeaCoordinate(value, direction string) (float64, error) {
	if len(value) == 0 {
		return 0, fmt.Errorf("empty coordinate value")
	}

	degrees, err := strconv.ParseFloat(value[:2], 64)
	if err != nil {
		return 0, fmt.Errorf("error parsing degrees: %w", err)
	}

	minutes, err := strconv.ParseFloat(value[2:], 64)
	if err != nil {
		return 0, fmt.Errorf("error parsing minutes: %w", err)
	}

	decimalDegrees := degrees + minutes/60.0
	if direction == "S" || direction == "W" {
		decimalDegrees = -decimalDegrees
	}

	return decimalDegrees, nil
}
