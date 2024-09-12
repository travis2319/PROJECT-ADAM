package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
	"time"

	"github.com/tarm/serial"
)

func main() {
	config := &serial.Config{
		Name: "/dev/ttyACM0",
		Baud: 38400,
	}

	port, err := serial.OpenPort(config)
	if err != nil {
		log.Fatalf("Failed to open port: %v", err)
	}
	defer port.Close()

	// Initialize OBD communication
	fmt.Println("Sending ATZ command to initialize OBD communication...")
	_, err = port.Write([]byte("ATZ\r"))
	if err != nil {
		log.Fatalf("Failed to send ATZ command: %v", err)
	}
	time.Sleep(2 * time.Second)

	// Set protocol to auto
	fmt.Println("Setting protocol to auto (ATSP0)...")
	_, err = port.Write([]byte("ATSP0\r"))
	if err != nil {
		log.Fatalf("Failed to send ATSP0 command: %v", err)
	}
	time.Sleep(2 * time.Second)

	// Send RPM request once
	fmt.Println("Sending RPM request (010C)...")
	_, err = port.Write([]byte("010C\r"))
	if err != nil {
		log.Fatalf("Failed to send RPM request: %v", err)
	}

	// Enter a loop to read and parse the response
	for {
		// Read response
		buf := make([]byte, 128)
		n, err := port.Read(buf)
		if err != nil {
			log.Printf("Error reading from port: %v", err)
			continue
		}

		if n == 0 {
			log.Println("No data read from port, retrying...")
			continue
		}

		// Parse RPM data
		response := string(buf[:n])
		response = strings.TrimSpace(response) // Trim any extra spaces or newlines
		fmt.Printf("Received response: %s\n", response)
		rpm, err := parseRPM(response)
		if err != nil {
			log.Printf("Error parsing RPM: %v", err)
			continue
		}

		fmt.Printf("Current RPM: %d\n", rpm)
		time.Sleep(time.Second)
	}
}

// parseRPM takes a response string and extracts the RPM value.
func parseRPM(response string) (int, error) {
	// Example response: "41 0C 1A F8"
	// RPM = ((A * 256) + B) / 4
	if len(response) < 11 {
		return 0, fmt.Errorf("invalid response length")
	}

	// Split the response string by spaces
	parts := strings.Fields(response)

	// Ensure we have at least 4 parts
	if len(parts) < 4 {
		return 0, fmt.Errorf("invalid response format")
	}

	// Extract the two bytes A and B
	aStr := parts[2]
	bStr := parts[3]

	// Convert A and B from hex strings to integers
	a, err := strconv.ParseInt(aStr, 16, 64)
	if err != nil {
		return 0, fmt.Errorf("invalid hex value for A: %v", err)
	}

	b, err := strconv.ParseInt(bStr, 16, 64)
	if err != nil {
		return 0, fmt.Errorf("invalid hex value for B: %v", err)
	}

	// Calculate RPM
	rpm := ((a * 256) + b) / 4
	fmt.Printf("Parsed RPM: %d\n", rpm)
	return int(rpm), nil
}
