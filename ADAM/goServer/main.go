package main

import (
	"database/sql"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	_ "github.com/lib/pq"
)

func main() {
	// Build the connection string using environment variables
	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		os.Getenv("POSTGRES_HOST"),
		os.Getenv("POSTGRES_PORT"),
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("POSTGRES_DB"),
	)

	// PostgreSQL connection setup
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Error connecting to the database:", err)
	}
	defer db.Close()

	// Create the table if it doesn't exist
	_, err = db.Exec(`
CREATE TABLE IF NOT EXISTS sensor (
	id SERIAL PRIMARY KEY,
	TIME TEXT,
	SPEED TEXT,
	SENSOR1 TEXT,
	SENSOR2 TEXT,
	SENSOR3 TEXT,
	SENSOR4 TEXT,
	SENSOR5 TEXT,
	SENSOR6 TEXT,
	SENSOR7 TEXT,
	SENSOR8 TEXT,
	SENSOR9 TEXT
);
`)
	if err != nil {
		log.Fatal("Error creating table:", err)
	}

	// Status route to check if server is live
	http.HandleFunc("/status", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Server is live!")
	})

	http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		// Parse the uploaded file
		file, _, err := r.FormFile("csvFile")
		if err != nil {
			http.Error(w, "Error parsing file: "+err.Error(), http.StatusBadRequest)
			return
		}
		defer file.Close()

		// Read the CSV data
		reader := csv.NewReader(file)

		// Read and discard the header
		_, err = reader.Read()
		if err != nil {
			http.Error(w, "Error reading CSV header: "+err.Error(), http.StatusBadRequest)
			return
		}

		// Prepare the SQL statement
		insertSQL := `
			INSERT INTO sensor (
				TIME, SENSOR1, SENSOR2, SENSOR3, SENSOR4, SENSOR5, 
				SENSOR6, SENSOR7, SENSOR8, SENSOR9, SENSOR10, SENSOR11, SENSOR12
			) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
		`

		// Process each row
		for {
			record, err := reader.Read()
			if err == io.EOF {
				break
			}
			if err != nil {
				http.Error(w, "Error reading CSV row: "+err.Error(), http.StatusBadRequest)
				return
			}

			// Ensure we have at least 11 fields
			if len(record) < 11 {
				http.Error(w, "CSV row does not have enough fields", http.StatusBadRequest)
				return
			}

			// Extract values from the record
			values := []interface{}{
				record[1],  // Start_Time (TIME)
				record[2],  // SPEED (SENSOR1)
				record[3],  // Coolant Temp (SENSOR2)
				record[4],  // Engine Load (SENSOR3)
				record[5],  // Timing Advance (SENSOR4)
				record[6],  // Short Trim B1 (SENSOR5)
				record[7],  // Long Trim B1 (SENSOR6)
				record[8],  // MAF (SENSOR7)
				record[9],  // Throttle_pos (SENSOR8)
				record[10], // End_Time (SENSOR9)
				"",         // Empty string for SENSOR10 (not present in CSV)
				"",         // Empty string for SENSOR11 (not present in CSV)
				"",         // Empty string for SENSOR12 (not present in CSV)
			}

			// Insert into the database
			_, err = db.Exec(insertSQL, values...)
			if err != nil {
				http.Error(w, "Error inserting into database: "+err.Error(), http.StatusInternalServerError)
				return
			}
		}

		fmt.Fprintln(w, "CSV data uploaded and stored successfully!")
	})

	// View uploaded data
	http.HandleFunc("/view", func(w http.ResponseWriter, r *http.Request) {
		rows, err := db.Query("SELECT * FROM sensor")
		if err != nil {
			http.Error(w, "Error querying database", http.StatusInternalServerError)
			return
		}
		defer rows.Close()

		var results []map[string]interface{}
		columns, _ := rows.Columns()
		for rows.Next() {
			columnsValues := make([]interface{}, len(columns))
			columnsPointers := make([]interface{}, len(columns))
			for i := range columnsValues {
				columnsPointers[i] = &columnsValues[i]
			}

			if err := rows.Scan(columnsPointers...); err != nil {
				http.Error(w, "Error scanning row", http.StatusInternalServerError)
				return
			}

			rowMap := make(map[string]interface{})
			for i, colName := range columns {
				rowMap[colName] = columnsValues[i]
			}
			results = append(results, rowMap)
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(results)
	})

	// Start the server
	log.Println("Server listening on :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
