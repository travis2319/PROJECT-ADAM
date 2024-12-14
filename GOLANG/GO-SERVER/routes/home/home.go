package home

import "github.com/gofiber/fiber/v2"

// HomeHandler handles the root endpoint
func HomeHandler(c *fiber.Ctx) error {
	return c.SendString("Welcome to PROJECT-ADAM!!")
}
