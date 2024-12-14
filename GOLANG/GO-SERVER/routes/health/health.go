package health

import (
	"time"

	"github.com/travis2319/PROJECT-ADAM/utils"

	"github.com/gofiber/fiber/v2"
)

var startTime = time.Now()

func HealthHandler(c *fiber.Ctx) error {
	healthData := map[string]interface{}{
		"status":    "healthy",
		"uptime":    utils.GetUptime(startTime),
		"timestamp": time.Now().Format(time.RFC3339),
	}

	return c.Status(fiber.StatusOK).JSON(healthData)
}
