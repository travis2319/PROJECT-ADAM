package models

import "time"

type gps struct {
	UserId       int
	TimestampGps time.Time
	Latitude     float64
	Longitude    float64
}
