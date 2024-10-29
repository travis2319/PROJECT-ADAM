// package main

// import(
// 	PROJECT_ADAM/obd
// )


// type OBD struct {
// 	port *serial.Port
// }

// // NewOBD initializes a new OBD connection
// func NewOBD(portName string, baudRate int) (*OBD, error) {
// 	config := &serial.Config{
// 		Name: portName,
// 		Baud: baudRate,
// 	}
// 	port, err := serial.OpenPort(config)
// 	if err != nil {
// 		return nil, err
// 	}
// 	return &OBD{port: port}, nil
// }

// // Close closes the OBD connection
// func (o *OBD) Close() error {
// 	return o.port.Close()
// }

// // SendCommand sends a command to the OBD device
// func (o *OBD) SendCommand(cmd string) (string, error) {
// 	_, err := o.port.Write([]byte(cmd + "\r"))
// 	if err != nil {
// 		return "", err
// 	}
// 	time.Sleep(time.Second)

// 	buf := make([]byte, 128)
// 	n, err := o.port.Read(buf)
// 	if err != nil {
// 		return "", err
// 	}

// 	return string(buf[:n]), nil
// }

// // // ParseRPM parses the RPM from the OBD response
// // func (o *OBD) ParseRPM(response string) (int, error) {
// // 	// Example response: "41 0C 1A F8"
// // 	// RPM = ((A * 256) + B) / 4
// // 	if len(response) < 11 {
// // 		return 0, fmt.Errorf("invalid response length")
// // 	}
// // 	data := response[6:11] // Extract "1A F8"
// // 	a, err := strconv.ParseInt(data[:2], 16, 64)
// // 	if err != nil {
// // 		return 0, err
// // 	}
// // 	b, err := strconv.ParseInt(data[3:], 16, 64)
// // 	if err != nil {
// // 		return 0, err
// // 	}
// // 	rpm := ((a * 256) + b) / 4
// // 	return int(rpm), nil
// // }

// func(o*OBD)ParseRPM(response string)(int,error){
// 	response=strings.ReplaceAll(response," ","")
// 	if len(response)<8{
// 	return 0,fmt.Errorf("invalid response length")
// 	}
// 	data:=response[4:8]
// 	a,err:=strconv.ParseInt(data[:2],16,64)
// 	if err!=nil{
// 	return 0,err
// 	}
// 	b,err:=strconv.ParseInt(data[2:],16,64)
// 	if err!=nil{
// 	return 0,err
// 	}
// 	rpm:=((a*256)+b)/4
// 	return int(rpm),nil
// 	}

// func main(){
	
// 	log.Println("Starting the OBD and GPS data logger...")

//     // config := &serial.Config{
// 	// 	Name: "/dev/ttyACM0",
// 	// 	Baud: 38400,
// 	//   }
	
// 	//   port, err := serial.OpenPort(config)
// 	//   if err != nil {
// 	// 	log.Fatalf("Failed to open port: %v", err)
// 	//   }
// 	//   defer port.Close()

// 	// OBD represents the OBD connection

// 	obd, err := NewOBD("/dev/ttyACM0", 38400)
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	defer obd.Close()

// 	// Initialize OBD communication
// 	fmt.Println("Sending ATZ command to initialize OBD communication...")
// 	_, err = obd.SendCommand("ATZ")
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	// Set protocol to auto
// 	fmt.Println("Setting protocol to auto (ATSP0)...")
// 	_, err = obd.SendCommand("ATSP0")
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	iterationCount := 0
// 	for iterationCount < 10 {
// 		// Send RPM request
// 		fmt.Println("Sending RPM request (010C)...")
// 		response, err := obd.SendCommand("010C")
// 		if err != nil {
// 			log.Println(err)
// 			continue
// 		}

// 		// Parse RPM data
// 		fmt.Printf("Received response: %s\n", response)
// 		rpm, err := obd.ParseRPM(response)
// 		if err != nil {
// 			log.Println(err)
// 			continue
// 		}

// 		fmt.Printf("Current RPM: %d\n", rpm)
// 		iterationCount++
// 		time.Sleep(time.Second)
// 	}

// 	fmt.Println("Completed 10 iterations of RPM retrieval.")

// }

// package main

// import (
//     "flag"
//     "fmt"
//     "github.com/rzetterberg/elmobd"
// )

// func main() {
//     serialPath := flag.String(
//         "serial",
//         "/dev/ttyACM0",
//         "Path to the serial device to use",
//     )

//     flag.Parse()

//     dev, err := elmobd.NewDevice(*serialPath, false)

//     if err != nil {
//         fmt.Println("Failed to create new device", err)
//         return
//     }else if(dev == null){
// 		fmt.Println(dev)
// 	}
// }

package main

import (
	"fmt"
	"strconv"
    "strings"
)

func main() {
	response := "41 00 BE 3F A8 13"
	supportedPIDs := parseSupportedPIDs(response)
	fmt.Printf("Supported PIDs: %v\n", supportedPIDs)
}

func parseSupportedPIDs(response string) []int {
	parts := strings.Fields(response)
	if len(parts) < 6 {
		fmt.Println("Invalid response length")
		return nil
	}

	var supportedPIDs []int
	for i, part := range parts[2:] {
		byteVal, err := strconv.ParseUint(part, 16, 8)
		if err != nil {
			fmt.Printf("Error parsing part %s: %v\n", part, err)
			continue
		}

		for bit := 0; bit < 8; bit++ {
			if (byteVal & (1 << uint(7-bit))) != 0 {
				supportedPIDs = append(supportedPIDs, i*8+bit+1)
			}
		}
	}

	return supportedPIDs
}


//!!!! imp code??

// package main

// import (
// 	"fmt"
// 	"log"
// 	"strings"
// 	"sync"
// 	"time"

// 	"github.com/tarm/serial"
// )

// // OBDCommand holds the PID, its latest response, and associated callbacks
// type OBDCommand struct {
// 	PID       string
// 	Response  string
// 	Callbacks []func(string) // List of callback functions
// }

// // AsyncOBD manages the asynchronous OBD-II operations
// type AsyncOBD struct {
// 	commands  map[string]*OBDCommand
// 	port      *serial.Port
// 	running   bool
// 	mutex     sync.Mutex
// 	delayCmds time.Duration
// }

// // NewAsyncOBD creates a new instance of AsyncOBD
// func NewAsyncOBD(port *serial.Port, delayCmds time.Duration) *AsyncOBD {
// 	return &AsyncOBD{
// 		commands:  make(map[string]*OBDCommand),
// 		port:      port,
// 		delayCmds: delayCmds,
// 	}
// }

// // Watch adds a PID to the watch list and registers a callback
// func (a *AsyncOBD) Watch(pid string, callback func(string)) {
// 	a.mutex.Lock()
// 	defer a.mutex.Unlock()

// 	if _, exists := a.commands[pid]; !exists {
// 		a.commands[pid] = &OBDCommand{PID: pid}
// 	}

// 	if callback != nil {
// 		a.commands[pid].Callbacks = append(a.commands[pid].Callbacks, callback)
// 	}
// }

// // Unwatch removes a PID from the watch list, and optionally removes a specific callback
// func (a *AsyncOBD) Unwatch(pid string, callback func(string)) {
// 	a.mutex.Lock()
// 	defer a.mutex.Unlock()

// 	if cmd, exists := a.commands[pid]; exists {
// 		if callback != nil {
// 			// Remove specific callback
// 			newCallbacks := []func(string){}
// 			for _, cb := range cmd.Callbacks {
// 				if fmt.Sprintf("%p", cb) != fmt.Sprintf("%p", callback) {
// 					newCallbacks = append(newCallbacks, cb)
// 				}
// 			}
// 			cmd.Callbacks = newCallbacks
// 		} else {
// 			// Remove the command completely
// 			delete(a.commands, pid)
// 		}
// 	}
// }

// // UnwatchAll removes all PIDs and their callbacks from the watch list
// func (a *AsyncOBD) UnwatchAll() {
// 	a.mutex.Lock()
// 	defer a.mutex.Unlock()
// 	a.commands = make(map[string]*OBDCommand)
// }

// // Start begins the asynchronous PID polling loop
// func (a *AsyncOBD) Start() {
// 	if a.running {
// 		return
// 	}
// 	a.running = true

// 	go func() {
// 		for a.running {
// 			a.mutex.Lock()
// 			for pid, cmd := range a.commands {
// 				response := a.query(pid)
// 				cmd.Response = response

// 				// Call the callbacks
// 				for _, callback := range cmd.Callbacks {
// 					callback(response)
// 				}
// 				time.Sleep(a.delayCmds)
// 			}
// 			a.mutex.Unlock()
// 			time.Sleep(250 * time.Millisecond)
// 		}
// 	}()
// }

// // Stop stops the asynchronous PID polling loop
// func (a *AsyncOBD) Stop() {
// 	a.running = false
// }

// // query sends a request for the given PID and returns the response
// func (a *AsyncOBD) query(pid string) string {
// 	_, err := a.port.Write([]byte(pid + "\r"))
// 	if err != nil {
// 		log.Printf("Failed to send request for PID %s: %v", pid, err)
// 		return ""
// 	}

// 	buf := make([]byte, 128)
// 	n, err := a.port.Read(buf)
// 	if err != nil {
// 		log.Printf("Error reading from port: %v", err)
// 		return ""
// 	}

// 	if n == 0 {
// 		log.Println("No data read from port")
// 		return ""
// 	}

// 	return strings.TrimSpace(string(buf[:n]))
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

// 	// Initialize the Async OBD
// 	asyncOBD := NewAsyncOBD(port, 1*time.Second)

// 	// Watch some PIDs with callbacks
// 	asyncOBD.Watch("010C", func(response string) {
// 		fmt.Printf("RPM: %s\n", response)
// 	})
// 	asyncOBD.Watch("010D", func(response string) {
// 		fmt.Printf("Speed: %s\n", response)
// 	})

// 	// Start the async loop
// 	asyncOBD.Start()

// 	// Let it run for a while
// 	time.Sleep(10 * time.Second)

// 	// Stop and clean up
// 	asyncOBD.Stop()
// 	asyncOBD.UnwatchAll()
// }
