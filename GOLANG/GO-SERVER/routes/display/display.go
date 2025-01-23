package display

import (
	"context"
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/travis2319/PROJECT-ADAM/database"
)

// FetchHandler retrieves all records from the obdSensor table.
func FetchHandler(c *fiber.Ctx) error {
	pool := database.GetPool()
	conn, err := pool.Acquire(context.Background())
	if err != nil {
		log.Printf("Failed to acquire database connection: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Database connection error"})
	}
	defer conn.Release()

	query := `SELECT * FROM obdtest`
	rows, err := conn.Query(context.Background(), query)
	if err != nil {
		log.Printf("Failed to query data: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to query data"})
	}
	defer rows.Close()

	fieldDescriptions := rows.FieldDescriptions()
	columns := make([]string, len(fieldDescriptions))
	for i, fd := range fieldDescriptions {
		columns[i] = string(fd.Name)
	}

	var result []map[string]interface{}
	for rows.Next() {
		row := make([]interface{}, len(columns))
		rowPtrs := make([]interface{}, len(columns))
		for i := range row {
			rowPtrs[i] = &row[i]
		}

		if err := rows.Scan(rowPtrs...); err != nil {
			log.Printf("Failed to scan row: %v", err)
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to scan row"})
		}

		rowMap := make(map[string]interface{})
		for i, col := range columns {
			if v, ok := row[i].([]uint8); ok {
				rowMap[col] = string(v)
			} else {
				rowMap[col] = row[i]
			}
		}
		result = append(result, rowMap)
	}

	if err := rows.Err(); err != nil {
		log.Printf("Row iteration error: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Error reading data"})
	}

	return c.JSON(fiber.Map{
		"data":    result,
		"count":   len(result),
		"columns": columns,
	})
}
