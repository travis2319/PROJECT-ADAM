package main

import (
    "bufio"
    "fmt"
    "github.com/tarm/serial"
    "log"
    "time"
)

func main() {
    fmt.Println("Starting OBD-II communication")

    // Configure the serial port for communication with the OBD-II adapter
    c := &serial.Config{
        Name: "/dev/ttyACM0", // Adjust this based on your OBD-II adapter's port
        Baud: 38400,          // Typical baud rate for ELM327 adapters
    }
    s, err := serial.OpenPort(c)
    if err != nil {
        log.Fatal(err)
    }
    defer s.Close()

    fmt.Println("Serial port opened successfully")

    // Initialize a bufio reader for reading responses from the OBD-II adapter
    reader := bufio.NewReader(s)

    // Send commands to the OBD-II adapter and read responses
    commands := []string{"ATZ\r", "ATSP0\r", "010C\r"}
    for _, cmd := range commands {
        fmt.Printf("Sending command: %s", cmd)
        _, err := s.Write([]byte(cmd))
        if err != nil {
            log.Fatal(err)
        }

        // Read the response from the OBD-II adapter
        response, err := reader.ReadString('>')
        if err != nil {
            log.Fatal(err)
        }

        // Print the response
        fmt.Printf("Response for %s: %s\n", cmd, response)

        // Sleep for a moment before sending the next command
        time.Sleep(500 * time.Millisecond)
    }

    fmt.Println("Finished OBD-II communication")
}

