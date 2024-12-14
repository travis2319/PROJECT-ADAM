package utils

import "time"

func GetUptime(startTime time.Time) float64 {
	return time.Since(startTime).Seconds()
}
