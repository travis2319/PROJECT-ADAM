package main

import (
	"flag"
	"fmt"
	"github.com/greenchapel-dev/elmobd"
)

func main() {
	serialPath := flag.String(
		"serial",
		"/dev/ttyACM0",
		"Path to the serial device to use",
	)

	flag.Parse()

	dev, err := elmobd.NewDevice(*serialPath,true)

	if err != nil {
		fmt.Println("Failed to create new device", err)
		return
	}

	version, err := dev.GetVersion()

	if err != nil {
		fmt.Println("Failed to get version", err)
		return
	}

	fmt.Println("Device has version", version)
}
