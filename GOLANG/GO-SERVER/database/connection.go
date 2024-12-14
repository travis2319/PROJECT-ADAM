package database

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

var (
	dbPool *pgxpool.Pool
	once   sync.Once
)

// Connect establishes a connection pool to the PostgreSQL database
func Connect() error {
	// Retrieve database configuration
	cfg := GetConfig()

	// Construct the connection URL
	connURL := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		cfg.User,
		cfg.Password,
		cfg.Host,
		cfg.Port,
		cfg.DBName,
	)

	// Configure the connection pool
	poolConfig, err := pgxpool.ParseConfig(connURL)
	if err != nil {
		return fmt.Errorf("unable to parse database config: %v", err)
	}

	// Set pool configuration
	poolConfig.MaxConns = 50                      // Maximum number of connections in the pool
	poolConfig.MinConns = 5                       // Minimum number of connections to keep open
	poolConfig.MaxConnLifetime = 30 * time.Minute // Maximum lifetime of a connection
	poolConfig.MaxConnIdleTime = 5 * time.Minute  // Maximum idle time for a connection

	// Create the connection pool with retry logic
	var pool *pgxpool.Pool
	maxRetries := 10
	for attempts := 0; attempts < maxRetries; attempts++ {
		pool, err = pgxpool.NewWithConfig(context.Background(), poolConfig)
		if err == nil {
			// Verify the connection
			if pingErr := pool.Ping(context.Background()); pingErr == nil {
				break
			}
		}

		log.Printf("Database connection attempt %d failed: %v", attempts+1, err)
		if attempts < maxRetries-1 {
			// Wait before retrying
			time.Sleep(5 * time.Second)
		}
	}

	if err != nil {
		return fmt.Errorf("failed to connect to database after %d attempts: %v", maxRetries, err)
	}

	// Store the pool using sync.Once to ensure thread-safety
	once.Do(func() {
		dbPool = pool
	})

	log.Println("Successfully connected to the database")
	return nil
}

// GetPool returns the database connection pool
func GetPool() *pgxpool.Pool {
	return dbPool
}

// Close closes the database connection pool
func Close() {
	if dbPool != nil {
		dbPool.Close()
	}
}
