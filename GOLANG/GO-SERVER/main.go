package main

import (
	"log"

	"github.com/travis2319/PROJECT-ADAM/database"
	"github.com/travis2319/PROJECT-ADAM/routes"

	"github.com/gofiber/fiber/v2"
)

func main() {

	// Connect to the database
	if err := database.Connect(); err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer database.Close()

	// Initialize the Fiber app
	app := fiber.New()

	// Register routes
	routes.RegisterRoutes(app)

	// Start the server
	// log.Fatal(app.Listen(":3000"))
	log.Fatal(app.Listen("0.0.0.0:3000"))

}
