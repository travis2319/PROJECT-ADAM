package routes

import (
	"github.com/travis2319/PROJECT-ADAM/routes/display"
	"github.com/travis2319/PROJECT-ADAM/routes/health"
	"github.com/travis2319/PROJECT-ADAM/routes/home"
	"github.com/travis2319/PROJECT-ADAM/routes/upload"

	"github.com/gofiber/fiber/v2"
)

// RegisterRoutes sets up all the routes for the app
func RegisterRoutes(app *fiber.App) {
	//Get routes
	app.Get("/", home.HomeHandler)
	app.Get("/health", health.HealthHandler)
	app.Get("/data", display.FetchHandler)

	//Post routes
	app.Post("/upload", upload.StoreHandler)

	//expo routes
	// app.Post("/auth/login", login.LoginHandler)
}
