package main

import (
    "flag"
    "fmt"
    "github.com/rzetterberg/elmobd"
    "log"
)

func main() {
    log.Println("Starting program")

    serialPath := flag.String(
        "serial",
	"serial:///dev/ttyACM0",
        "Path to the serial device to use",
    )

    flag.Parse()

    log.Printf("Using serial path: %s", *serialPath)

    dev, err := elmobd.NewDevice(*serialPath, false)

    if err!= nil {
        log.Printf("Failed to create new device: %v", err)
        fmt.Println("Failed to create new device", err)
        return
    }

    log.Println("Device created successfully")

    rpm, err := dev.RunOBDCommand(elmobd.NewEngineRPM())

    if err!= nil {
        log.Printf("Failed to get rpm: %v", err)
        fmt.Println("Failed to get rpm", err)
        return
    }

    log.Println("RPM command executed successfully")

    log.Printf("RPM value: %s", rpm.ValueAsLit())

    fmt.Printf("Engine spins at %s RPMs\n", rpm.ValueAsLit())

    log.Println("Program completed successfully")
}
