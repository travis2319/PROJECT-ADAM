package main

import (
    "fmt"
    "github.com/tarm/serial"
    "log"
)

func main() {
    c := &serial.Config{Name: "/dev/ttyAMA0", Baud: 9600}
    s, err := serial.OpenPort(c)
    if err != nil {
        log.Fatal(err)
    }

    buf := make([]byte, 128)
    for {
        n, err := s.Read(buf)
        if err != nil {
            log.Fatal(err)
        }
        fmt.Printf("%s", buf[:n])
    }
}

