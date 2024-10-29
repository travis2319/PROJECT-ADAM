package obd

type OBDDevice struct {
    port     string
    baudRate int
}

func Connection(port string, baudRate int) *OBDDevice {
    return &OBDDevice{
        port:     port,
        baudRate: baudRate,
    }
}