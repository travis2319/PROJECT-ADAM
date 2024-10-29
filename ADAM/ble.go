package main

import (
    "fmt"
    "github.com/paypal/gatt"
)

func main() {
    // Initialize default device
    d, err := gatt.NewDevice(option.DefaultServerOptions...)
    if err != nil {
        fmt.Printf("Failed to open device, err: %s\n", err)
        return
    }

    // Setup GAP and GATT services
    d.Init(onStateChanged)

    // Start the device
    select {}
}

func onStateChanged(d gatt.Device, s gatt.State) {
    switch s {
    case gatt.StatePoweredOn:
        // Create service
        svc := gatt.NewService(gatt.MustParseUUID("1234"))

        // Create a characteristic
        char := svc.AddCharacteristic(gatt.MustParseUUID("5678"))
        char.HandleReadFunc(
            func(rsp gatt.ResponseWriter, req *gatt.ReadRequest) {
                rsp.Write([]byte("Hello from Raspberry Pi!"))
            },
        )

        // Add service
        d.AddService(svc)

        // Advertise as a peripheral device
        d.AdvertiseNameAndServices("PiBluetooth", []gatt.UUID{svc.UUID()})
    default:
    }
}
