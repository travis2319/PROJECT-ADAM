//1
// package main

// import (
// 	"fmt"
// 	"log"
// 	"strconv"
// 	"strings"
// 	"time"

// 	"github.com/tarm/serial"
// )

// // rpm(010C),speed(010D),engineload(0104),coolanttemp(0105),intakeairtemp(010F),
// // massairflow(0110),fueltrim1(0107),fueltrim2(0108),throttlepos(0111),supportedpids(0100 )

// func main() {
// 	config := &serial.Config{
// 		Name: "/dev/ttyACM0",
// 		Baud: 38400,
// 	}

// 	port, err := serial.OpenPort(config)
// 	if err != nil {
// 		log.Fatalf("Failed to open port: %v", err)
// 	}
// 	defer port.Close()

// 	// Initialize OBD communication
// 	fmt.Println("Sending ATZ command to initialize OBD communication...")
// 	_, err = port.Write([]byte("ATZ\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send ATZ command: %v", err)
// 	}
// 	time.Sleep(2 * time.Second)

// 	// Set protocol to auto
// 	fmt.Println("Setting protocol to auto (ATSP0)...")
// 	_, err = port.Write([]byte("ATSP0\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send ATSP0 command: %v", err)
// 	}
// 	time.Sleep(2 * time.Second)

// 	// Send RPM request once
// 	fmt.Println("Sending RPM request (010C)...")
// 	_, err = port.Write([]byte("010C\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send RPM request: %v", err)
// 	}

// 	// Enter a loop to read and parse the response
// 	for {
// 		// Read response
// 		buf := make([]byte, 128)
// 		n, err := port.Read(buf)
// 		if err != nil {
// 			log.Printf("Error reading from port: %v", err)
// 			continue
// 		}

// 		if n == 0 {
// 			log.Println("No data read from port, retrying...")
// 			continue
// 		}

// 		// Parse RPM data
// 		response := string(buf[:n])
// 		response = strings.TrimSpace(response) // Trim any extra spaces or newlines
// 		fmt.Printf("Received response: %s\n", response)
// 		rpm, err := parseRPM(response)
// 		if err != nil {
// 			log.Printf("Error parsing RPM: %v", err)
// 			continue
// 		}

// 		fmt.Printf("Current RPM: %d\n", rpm)
// 		time.Sleep(time.Second)
// 	}
// }

// // parseRPM takes a response string and extracts the RPM value.
// func parseRPM(response string) (int, error) {
// 	// Example response: "41 0C 1A F8"
// 	// RPM = ((A * 256) + B) / 4
// 	if len(response) < 11 {
// 		return 0, fmt.Errorf("invalid response length")
// 	}

// 	// Split the response string by spaces
// 	parts := strings.Fields(response)

// 	// Ensure we have at least 4 parts
// 	if len(parts) < 4 {
// 		return 0, fmt.Errorf("invalid response format")
// 	}

// 	// Extract the two bytes A and B
// 	aStr := parts[2]
// 	bStr := parts[3]

// 	// Convert A and B from hex strings to integers
// 	a, err := strconv.ParseInt(aStr, 16, 64)
// 	if err != nil {
// 		return 0, fmt.Errorf("invalid hex value for A: %v", err)
// 	}

// 	b, err := strconv.ParseInt(bStr, 16, 64)
// 	if err != nil {
// 		return 0, fmt.Errorf("invalid hex value for B: %v", err)
// 	}

// 	// Calculate RPM
// 	rpm := ((a * 256) + b) / 4
// 	fmt.Printf("Parsed RPM: %d\n", rpm)
// 	return int(rpm), nil
// }


//3 ✔️

// package main

// import (
//         "encoding/csv"
//         "fmt"
//         "log"
//         "os"
//         "strings"
//         "time"

//         "github.com/tarm/serial"
// )

// const (
// 	baudRate = 38400 // Adjust as needed based on device support
// 	bufferSize = 128
// 	delayBetweenPids = 500 * time.Millisecond // Adjust based on observed response times
// )

// var pids = []string{
//         "010C", // RPM
//         "010D", // Speed
//         "0104", // Engine Load
//         "0105", // Coolant Temperature
//         "010F", // Intake Air Temperature
//         "0110", // Mass Airflow
//         "0107", // Fuel Trim 1
//         "0108", // Fuel Trim 2
//         "0111", // Throttle Position
//         "0100", // Supported PIDs
// }

// func main() {
//         config := &serial.Config{
//                 Name: "/dev/ttyACM0",
//                 Baud: baudRate,
//         }

//         port, err := serial.OpenPort(config)
//         if err != nil {
//                 log.Fatalf("Failed to open port: %v", err)
//         }
//         defer port.Close()

//         // Initialize OBD communication
//         fmt.Println("Sending ATZ command to initialize OBD communication...")
//         _, err = port.Write([]byte("ATZ\r"))
//         if err != nil {
//                 log.Fatalf("Failed to send ATZ command: %v", err)
//         }
//         time.Sleep(2 * time.Second)

//         // Set protocol to auto
//         fmt.Println("Setting protocol to auto (ATSP0)...")
//         _, err = port.Write([]byte("ATSP0\r"))
//         if err != nil {
//                 log.Fatalf("Failed to send ATSP0 command: %v", err)
//         }
//         time.Sleep(2 * time.Second)

//         // Prepare the CSV file
//         fileName := "obd_data.csv"
//         fileExists := false

//         // Check if file exists
//         if _, err := os.Stat(fileName); err == nil {
//                 fileExists = true
//         }

//         // Open the file for appending or create it if it doesn't exist
//         file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
//         if err != nil {
//                 log.Fatalf("Failed to open file: %v", err)
//         }
//         defer file.Close()

//         writer := csv.NewWriter(file)
//         defer writer.Flush()

//         // Write the header if the file was just created
//         if !fileExists {
//                 header := append([]string{"Timestamp"}, pids...)
//                 if err := writer.Write(header); err != nil {
//                         log.Fatalf("Failed to write header to CSV: %v", err)
//                 }
//         }

//         // Loop 10 times to collect data
//         for i := 0; i < 10; i++ {
//                 fmt.Printf("Iteration %d of 10\n", i+1)

//                 var results []string
//                 for _, pid := range pids {
//                         fmt.Printf("Sending request for PID: %s\n", pid)
//                         _, err = port.Write([]byte(pid + "\r"))
//                         if err != nil {
//                                 log.Fatalf("Failed to send request for PID %s: %v", pid, err)
//                         }

//                         // Read response
//                         buf := make([]byte, bufferSize)
//                         n, err := port.Read(buf)
//                         if err != nil {
//                                 log.Printf("Error reading from port: %v", err)
//                                 continue
//                         }

//                         if n == 0 {
//                                 log.Println("No data read from port, retrying...")
//                                 continue
//                         }

//                         // Process and store response
//                         response := string(buf[:n])
//                         fmt.Printf("Raw response (length %d): %s\n", n, response) // Print buffer length
//                         response = strings.TrimSpace(response)
//                         fmt.Printf("Received response for PID %s: %s\n", pid, response)
//                         results = append(results, response)

//                         time.Sleep(delayBetweenPids) // Delay before sending next PID
//                 }

//                 // Write the results to the CSV file
//                 record := append([]string{time.Now().Format(time.RFC3339)}, results...)
//                 if err := writer.Write(record); err != nil {
//                         log.Fatalf("Failed to write record to CSV: %v", err)
//                 }

//                 // Wait before the next iteration
//                 //fmt.Println("Waiting for 10 seconds before the next iteration...")
//                 //time.Sleep(10 * time.Second)
//         }

//         fmt.Println("Data collection completed.")
// }

//4

// package main

// import (
// 	"encoding/csv"
// 	"fmt"
// 	"log"
// 	"os"
// 	"strings"
// 	"time"

// 	"github.com/tarm/serial"
// )

// const (
// 	baudRate        = 38400
// 	bufferSize      = 128
// 	delayBetweenPids = 200 * time.Millisecond // Reduced delay for faster data collection
// )

// var pids = []string{
// 	"010C", // RPM
// 	"010D", // Speed
// 	"0104", // Engine Load
// 	"0105", // Coolant Temperature
// 	"010F", // Intake Air Temperature
// 	"0110", // Mass Airflow
// 	"0107", // Fuel Trim 1
// 	"0108", // Fuel Trim 2
// 	"0111", // Throttle Position
// 	"0100", // Supported PIDs
// }

// func main() {
// 	config := &serial.Config{
// 		Name: "/dev/ttyACM0",
// 		Baud: baudRate,
// 	}

// 	port, err := serial.OpenPort(config)
// 	if err != nil {
// 		log.Fatalf("Failed to open port: %v", err)
// 	}
// 	defer port.Close()

// 	// Initialize OBD communication with minimal delay
// 	fmt.Println("Sending ATZ command to initialize OBD communication...")
// 	_, err = port.Write([]byte("ATZ\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send ATZ command: %v", err)
// 	}
// 	time.Sleep(1 * time.Second) // Reduced sleep time

// 	// Set protocol to auto
// 	fmt.Println("Setting protocol to auto (ATSP0)...")
// 	_, err = port.Write([]byte("ATSP0\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send ATSP0 command: %v", err)
// 	}
// 	time.Sleep(1 * time.Second) // Reduced sleep time

// 	// Prepare the CSV file
// 	fileName := "obd_data.csv"
// 	fileExists := false

// 	// Check if file exists
// 	if _, err := os.Stat(fileName); err == nil {
// 		fileExists = true
// 	}

// 	// Open the file for appending or create it if it doesn't exist
// 	file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
// 	if err != nil {
// 		log.Fatalf("Failed to open file: %v", err)
// 	}
// 	defer file.Close()

// 	writer := csv.NewWriter(file)
// 	defer writer.Flush()

// 	// Write the header if the file was just created
// 	if !fileExists {
// 		header := append([]string{"Timestamp"}, pids...)
// 		if err := writer.Write(header); err != nil {
// 			log.Fatalf("Failed to write header to CSV: %v", err)
// 		}
// 	}

// 	// Loop 10 times to collect data
// 	for i := 0; i < 10; i++ {
// 		fmt.Printf("Iteration %d of 10\n", i+1)

// 		var results []string
// 		for _, pid := range pids {
// 			fmt.Printf("Sending request for PID: %s\n", pid)
// 			_, err = port.Write([]byte(pid + "\r"))
// 			if err != nil {
// 				log.Fatalf("Failed to send request for PID %s: %v", pid, err)
// 			}

// 			// Read response
// 			buf := make([]byte, bufferSize)
// 			n, err := port.Read(buf)
// 			if err != nil {
// 				log.Printf("Error reading from port: %v", err)
// 				continue
// 			}

// 			if n == 0 {
// 				log.Println("No data read from port, retrying...")
// 				continue
// 			}

// 			// Process and store response
// 			response := strings.TrimSpace(string(buf[:n]))
// 			fmt.Printf("Received response for PID %s: %s\n", pid, response)
// 			results = append(results, response)

// 			time.Sleep(delayBetweenPids) // Reduced delay before sending next PID
// 		}

// 		// Write the results to the CSV file
// 		record := append([]string{time.Now().Format(time.RFC3339)}, results...)
// 		if err := writer.Write(record); err != nil {
// 			log.Fatalf("Failed to write record to CSV: %v", err)
// 		}
// 	}

// 	fmt.Println("Data collection completed.")
// }

package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/tarm/serial"
)

const (
	baudRate        = 38400
	bufferSize      = 128
	delayBetweenPids = 100 * time.Millisecond // Adjust based on observed response times
)

var pids = []string{
	"010C", // RPM
	"010D", // Speed
	"0104", // Engine Load
	"0105", // Coolant Temperature
	"010F", // Intake Air Temperature
	"0110", // Mass Airflow
	"0107", // Fuel Trim 1
	"0108", // Fuel Trim 2
	"0111", // Throttle Position
	"0100", // Supported PIDs
}

func main() {
	config := &serial.Config{
		Name: "/dev/ttyACM0",
		Baud: baudRate,
	}

	port, err := serial.OpenPort(config)
	if err != nil {
		log.Fatalf("Failed to open port: %v", err)
	}
	defer port.Close()

	// Initialize OBD communication with minimal delay
	fmt.Println("Sending ATZ command to initialize OBD communication...")
	_, err = port.Write([]byte("ATZ\r"))
	if err != nil {
		log.Fatalf("Failed to send ATZ command: %v", err)
	}
	time.Sleep(1 * time.Second)

	// Set protocol to auto
	fmt.Println("Setting protocol to auto (ATSP0)...")
	_, err = port.Write([]byte("ATSP0\r"))
	if err != nil {
		log.Fatalf("Failed to send ATSP0 command: %v", err)
	}
	time.Sleep(1 * time.Second)

	// Prepare the CSV file
	fileName := "obd_data.csv"
	fileExists := false

	// Check if file exists
	if _, err := os.Stat(fileName); err == nil {
		fileExists = true
	}

	// Open the file for appending or create it if it doesn't exist
	file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("Failed to open file: %v", err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write the header if the file was just created
	if !fileExists {
		header := append([]string{"Timestamp"}, pids...)
		if err := writer.Write(header); err != nil {
			log.Fatalf("Failed to write header to CSV: %v", err)
		}
	}

	// Loop 10 times to collect data
	for i := 0; i < 10; i++ {
		fmt.Printf("Iteration %d of 10\n", i+1)

		var wg sync.WaitGroup
		results := make([]string, len(pids))
		errors := make([]error, len(pids))

		// Collect data concurrently
		for j, pid := range pids {
			wg.Add(1)
			go func(index int, pid string) {
				defer wg.Done()
				fmt.Printf("Sending request for PID: %s\n", pid)
				_, err := port.Write([]byte(pid + "\r"))
				if err != nil {
					errors[index] = fmt.Errorf("Failed to send request for PID %s: %v", pid, err)
					return
				}

				// Read response
				buf := make([]byte, bufferSize)
				n, err := port.Read(buf)
				if err != nil {
					errors[index] = fmt.Errorf("Error reading from port for PID %s: %v", pid, err)
					return
				}

				if n == 0 {
					errors[index] = fmt.Errorf("No data read from port for PID %s, retrying...", pid)
					return
				}

				// Process and store response
				response := strings.TrimSpace(string(buf[:n]))
				fmt.Printf("Received response for PID %s: %s\n", pid, response)
				results[index] = response

			}(j, pid)
		}

		// Wait for all goroutines to finish
		wg.Wait()

		// Handle errors (optional)
		for _, err := range errors {
			if err != nil {
				log.Println(err)
			}
		}

		// Write the results to the CSV file
		record := append([]string{time.Now().Format(time.RFC3339)}, results...)
		if err := writer.Write(record); err != nil {
			log.Fatalf("Failed to write record to CSV: %v", err)
		}

		// Short delay between iterations (optional)
		time.Sleep(delayBetweenPids)
	}

	fmt.Println("Data collection completed.")
}



//2
// package main

// import (
// 	"fmt"
// 	"log"
// 	"strings"
// 	"time"

// 	"github.com/tarm/serial"
// )

// var pids = []string{
// 	"010C", // RPM
// 	"010D", // Speed
// 	"0104", // Engine Load
// 	"0105", // Coolant Temperature
// 	"010F", // Intake Air Temperature
// 	"0110", // Mass Airflow
// 	"0107", // Fuel Trim 1
// 	"0108", // Fuel Trim 2
// 	"0111", // Throttle Position
// 	"0100", // Supported PIDs
// }

// func main() {
// 	config := &serial.Config{
// 		Name: "/dev/ttyACM0",
// 		Baud: 38400,
// 	}

// 	port, err := serial.OpenPort(config)
// 	if err != nil {
// 		log.Fatalf("Failed to open port: %v", err)
// 	}
// 	defer port.Close()

// 	// Initialize OBD communication
// 	fmt.Println("Sending ATZ command to initialize OBD communication...")
// 	_, err = port.Write([]byte("ATZ\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send ATZ command: %v", err)
// 	}
// 	time.Sleep(2 * time.Second)

// 	// Set protocol to auto
// 	fmt.Println("Setting protocol to auto (ATSP0)...")
// 	_, err = port.Write([]byte("ATSP0\r"))
// 	if err != nil {
// 		log.Fatalf("Failed to send ATSP0 command: %v", err)
// 	}
// 	time.Sleep(2 * time.Second)

// 	// Loop through PIDs, send each request, and read the response
// 	for _, pid := range pids {
// 		fmt.Printf("Sending request for PID: %s\n", pid)
// 		_, err = port.Write([]byte(pid + "\r"))
// 		if err != nil {
// 			log.Fatalf("Failed to send request for PID %s: %v", pid, err)
// 		}

// 		// Read response
// 		buf := make([]byte, 128)
// 		n, err := port.Read(buf)
// 		if err != nil {
// 			log.Printf("Error reading from port: %v", err)
// 			continue
// 		}

// 		if n == 0 {
// 			log.Println("No data read from port, retrying...")
// 			continue
// 		}

// 		// Print response
// 		response := string(buf[:n])
// 		response = strings.TrimSpace(response) // Trim any extra spaces or newlines
// 		fmt.Printf("Received response for PID %s: %s\n", pid, response)

// 		time.Sleep(1 * time.Second) // Delay before sending next PID
// 	}
// }
