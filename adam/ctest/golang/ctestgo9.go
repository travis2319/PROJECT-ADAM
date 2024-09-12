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

  // Function to send a command and wait for a response
  sendCommand := func(cmd string) (string, error) {
    _, err := port.Write([]byte(cmd + "\r"))
    if err != nil {
      return "", fmt.Errorf("failed to send command %s: %v", cmd, err)
    }
    time.Sleep(2 * time.Second)

    buf := make([]byte, 128)
    n, err := port.Read(buf)
    if err != nil {
      return "", fmt.Errorf("error reading from port: %v", err)
    }
    if n == 0 {
      return "", fmt.Errorf("no data read from port after sending command %s", cmd)
    }
    return string(buf[:n]), nil
  }

  // Initialize OBD communication
  fmt.Println("Sending ATZ command to initialize OBD communication...")
  response, err := sendCommand("ATZ")
  if err != nil {
    log.Fatalf("Failed to send ATZ command: %v", err)
  }
  fmt.Printf("Response to ATZ: %s\n", response)

  // Set protocol to auto
  fmt.Println("Setting protocol to auto (ATSP0)...")
  response, err = sendCommand("ATSP0")
  if err != nil {
    log.Fatalf("Failed to send ATSP0 command: %v", err)
  }
  fmt.Printf("Response to ATSP0: %s\n", response)

  // Send RPM request once
  fmt.Println("Sending RPM request (010C)...")
  response, err = sendCommand("010C")
  if err != nil {
    log.Fatalf("Failed to send RPM request: %v", err)
  }
  fmt.Printf("Response to 010C: %s\n", response)

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
    fmt.Printf("Received response: %s\n", response)

    // Filter the response
    filteredResponse := filterResponse(response)
    if filteredResponse == "" {
      log.Println("No relevant data in response, retrying...")
      continue
    }

    rpm, err := parseRPM(filteredResponse)
    if err != nil {
      log.Printf("Error parsing RPM: %v", err)
      continue
    }

    fmt.Printf("Current RPM: %d\n", rpm)
    time.Sleep(time.Second)
  }
}

func filterResponse(response string) string {
  lines := strings.Split(response, "\n")
  for _, line := range lines {
    line = strings.TrimSpace(line)
    if strings.HasPrefix(line, "41 0C") {
      return line
    }
  }
  return ""
}

func parseRPM(response string) (int, error) {
  // Example response: "41 0C 1A F8"
  // RPM = ((A * 256) + B) / 4
  parts := strings.Fields(response)
  if len(parts) < 4 {
    return 0, fmt.Errorf("invalid response length")
  }
  a, err := strconv.ParseInt(parts[2], 16, 64)
  if err != nil {
    return 0, err
  }
  b, err := strconv.ParseInt(parts[3], 16, 64)
  if err != nil {
    return 0, err
  }
  rpm := ((a * 256) + b) / 4
  fmt.Printf("Parsed RPM: %d\n", rpm)
  return int(rpm), nil
}
