package database

import (
	"os"
)

// Config holds the configuration for database connection
type Config struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
}

// GetConfig returns the database configuration from environment variables
func GetConfig() Config {
	return Config{
		Host:     getEnv("POSTGRES_HOST", "localhost"),
		Port:     getEnv("POSTGRES_PORT", "5432"),
		User:     getEnv("POSTGRES_USER", "postgres"),
		Password: getEnv("POSTGRES_PASSWORD", ""),
		DBName:   getEnv("POSTGRES_DB", "mydb"),
	}
}

// getEnv retrieves the value of an environment variable,
// returning the default value if not set
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
