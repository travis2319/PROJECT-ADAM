package upload

import (
	"context"
	"encoding/csv"
	"fmt"
	"log"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/travis2319/PROJECT-ADAM/database"
)

func StoreHandler(c *fiber.Ctx) error {

	fileHeader, err := c.FormFile("file")
	if err != nil {
		log.Printf("File upload error: %v", err)
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "No file uploaded",
		})
	}

	// Open the uploaded file
	file, err := fileHeader.Open()
	if err != nil {
		log.Printf("Could not open file: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Could not open file",
		})
	}
	defer file.Close()

	// Read the CSV file
	csvReader := csv.NewReader(file)

	// Get the headers (first row)
	header, err := csvReader.Read()
	if err != nil {
		log.Printf("Could not read CSV header: %v", err)
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Could not read CSV header",
		})
	}

	// Read the rest of the rows (data)
	records, err := csvReader.ReadAll()
	if err != nil {
		log.Printf("Could not read CSV data: %v", err)
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Could not read CSV data",
		})
	}

	// Validate data
	if len(records) == 0 {
		log.Println("CSV file is empty")
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "CSV file contains no data",
		})
	}

	// Build a dynamic SQL query to create a table
	tableName := "obdtest" // Use a dynamic name if needed
	columns := make([]string, len(header))
	for i, col := range header {
		columns[i] = fmt.Sprintf("%s TEXT", strings.ToLower(strings.ReplaceAll(col, " ", "_")))
	}
	createTableQuery := fmt.Sprintf("CREATE TABLE IF NOT EXISTS %s (%s);", tableName, strings.Join(columns, ", "))

	// Acquire a database connection
	pool := database.GetPool()
	conn, err := pool.Acquire(context.Background())
	if err != nil {
		log.Printf("Failed to acquire database connection: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Database connection error"})
	}
	defer conn.Release()

	// Execute the create table query
	_, err = conn.Exec(context.Background(), createTableQuery)
	if err != nil {
		log.Printf("Failed to create table: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to create table",
		})
	}

	// Prepare the insert query
	columnPlaceholders := make([]string, len(header))
	for i := range header {
		columnPlaceholders[i] = fmt.Sprintf("$%d", i+1)
	}
	insertQuery := fmt.Sprintf("INSERT INTO %s (%s) VALUES (%s)", tableName, strings.Join(header, ", "), strings.Join(columnPlaceholders, ", "))

	// Insert each record into the database
	for _, record := range records {
		if len(record) != len(header) {
			log.Printf("Record length (%d) does not match header length (%d). Skipping record.", len(record), len(header))
			continue
		}

		_, err := conn.Exec(context.Background(), insertQuery, toInterfaceSlice(record)...)
		if err != nil {
			log.Printf("Failed to insert record: %v", err)
			continue
		}
	}

	return c.SendStatus(fiber.StatusOK)
}

// Helper function to convert a slice of strings to a slice of empty interfaces
func toInterfaceSlice(slice []string) []interface{} {
	result := make([]interface{}, len(slice))
	for i, v := range slice {
		result[i] = v
	}
	return result
}
