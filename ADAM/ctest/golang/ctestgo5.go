package main

import (
	"fmt"
	"log"
	"strconv"
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
		log.Fatal(err)
	}
	defer port.Close()

	// Initialize OBD communication
	fmt.Println("Sending ATZ command to initialize OBD communication...")
	_, err = port.Write([]byte("ATZ\r"))
	if err != nil {
		log.Fatal(err)
	}
	time.Sleep(time.Second)

	// Set protocol to auto
	fmt.Println("Setting protocol to auto (ATSP0)...")
	_, err = port.Write([]byte("ATSP0\r"))
	if err != nil {
		log.Fatal(err)
	}
	time.Sleep(time.Second)

	for {
		// Send RPM request
		fmt.Println("Sending RPM request (010C)...")
		_, err = port.Write([]byte("010C\r"))
		if err != nil {
			log.Println(err)
			continue
		}

		// Read response
		buf := make([]byte, 128)
		n, err := port.Read(buf)
		if err != nil {
			log.Println(err)
			continue
		}

		// Parse RPM data
		response := string(buf[:n])
		fmt.Printf("Received response: %s\n", response)
		rpm, err := parseRPM(response)
		if err != nil {
			log.Println(err)
			continue
		}

		fmt.Printf("Current RPM: %d\n", rpm)
		time.Sleep(time.Second)
	}
}

func parseRPM(response string) (int, error) {
	// Example response: "41 0C 1A F8"
	// RPM = ((A * 256) + B) / 4
	if len(response) < 11 {
		return 0, fmt.Errorf("invalid response length")
	}
	data := response[6:11] // Extract "1A F8"
	fmt.Printf("Parsing RPM data: %s\n", data)
	a, err := strconv.ParseInt(data[:2], 16, 64)
	if err != nil {
		return 0, err
	}
	b, err := strconv.ParseInt(data[3:], 16, 64)
	if err != nil {
		return 0, err
	}
	rpm := ((a * 256) + b) / 4
	fmt.Printf("Parsed RPM: %d\n", rpm)
	return int(rpm), nil
}
