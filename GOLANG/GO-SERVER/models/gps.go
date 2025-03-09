package models

import "time"

type gps struct {
	UserId            int
	Timestamp         time.Time
	Gps_Status        string
	Latitude          float64
	Longitude         float64
	Acc_X             float64
	Acc_Y             float64
	Acc_Z             float64
	Gyro_X            float64
	Gyro_Y            float64
	Gyro_Z            float64
	Vibration_Status  string
	Timestamp_Esp8266 time.Time
}
