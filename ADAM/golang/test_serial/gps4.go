package main

import (
	"bufio"
	"encoding/csv"
	"github.com/tarm/serial"
	"log"
	"os"
	"strings"
	"time"
)

func main() {
	// Open serial port
	log.Println("Opening serial port...")
	serialPort, err := openSerialPort("/dev/ttyAMA0", 9600)
	if err != nil {
		log.Fatalf("Failed to open serial port: %v", err)
	}
	defer serialPort.Close()
	log.Println("Serial port opened successfully.")

	// Open CSV file
	log.Println("Opening CSV file...")
	csvFile, err := openCSVFile("gps_data.csv", false)
	if err != nil {
		log.Fatalf("Failed to open CSV file: %v", err)
	}
	defer csvFile.Close()
	log.Println("CSV file opened successfully.")

	// Create a CSV writer
	csvWriter := csv.NewWriter(csvFile)

	// Write CSV header if the file is new
	_, err = os.Stat("gps_data.csv")
	if err != nil && os.IsNotExist(err) {
		log.Println("Writing CSV header...")
		err = csvWriter.Write([]string{"Latitude", "Longitude", "Altitude"})
		if err != nil {
			log.Fatalf("Error writing CSV header: %v", err)
		}
		log.Println("CSV header written successfully.")
	}

	// Wait for a short time to allow the serial port to stabilize
	log.Println("Waiting for 5 seconds to allow serial port to stabilize...")
	time.Sleep(5 * time.Second)

	// Start reading from serial port
	log.Println("Starting serial port reading...")
	dataChannel := make(chan string)
	go readSerialPort(serialPort, dataChannel)

	// Process data received from the channel
	log.Println("Processing data from serial port...")
	for line := range dataChannel {
		log.Printf("Received line: %s", line)

		if strings.HasPrefix(line, "$GPGGA") {
			latitude, longitude, altitude := processGPGGA(line)
			log.Printf("Latitude: %s, Longitude: %s, Altitude: %s", latitude, longitude, altitude)

			err = csvWriter.Write([]string{
				latitude,
				longitude,
				altitude,
			})
			if err != nil {
				log.Printf("Error writing to CSV file: %v", err)
			}
			csvWriter.Flush()
		}
	}
	log.Println("Program execution completed.")
}

func openSerialPort(device string, baud int) (*serial.Port, error) {
	log.Printf("Opening serial port: %s at %d baud", device, baud)
	config := &serial.Config{Name: device, Baud: baud}
	port, err := serial.OpenPort(config)
	if err != nil {
		log.Printf("Failed to open serial port: %v", err)
	}
	return port, err
}

func openCSVFile(filename string, createNew bool) (*os.File, error) {
	log.Printf("Opening CSV file: %s", filename)
	var flags int
	if createNew {
		flags = os.O_CREATE | os.O_WRONLY | os.O_TRUNC
	} else {
		flags = os.O_CREATE | os.O_APPEND | os.O_WRONLY
	}
	file, err := os.OpenFile(filename, flags, 0644)
	if err != nil {
		log.Printf("Failed to open CSV file: %v", err)
	}
	return file, err
}

func readSerialPort(s *serial.Port, dataChannel chan<- string) {
	log.Println("Starting serial port reader...")
	scanner := bufio.NewScanner(s)
	for scanner.Scan() {
		dataChannel <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		log.Fatalf("Error reading from serial port: %v", err)
	}
	close(dataChannel)
	log.Println("Serial port reader stopped.")
}

func processGPGGA(line string) (string, string, string) {
	log.Printf("Processing GPGGA sentence: %s", line)
	parts := strings.Split(line, ",")
	if len(parts) < 15 {
		log.Printf("Invalid GPGGA sentence: %s", line)
		return "", "", ""
	}

	latitude := parts[2]
	longitude := parts[4]
	altitude := parts[9]

	return latitude, longitude, altitude
}
