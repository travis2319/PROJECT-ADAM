package main

import (
    "database/sql"
    "encoding/csv"
    "fmt"
    "io"
    "log"
    "net/http"
    // "os"

    _ "github.com/lib/pq"
)

func main() {
    // PostgreSQL connection setup
    db, err := sql.Open("postgres", "your_connection_string")
    if err != nil {
        log.Fatal("Error connecting to the database:", err)
    }
    defer db.Close()

    // Create the table if it doesn't exist (adjust as needed)
    _, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS your_table_name (
            id SERIAL PRIMARY KEY,
            column1 TEXT,
            column2 TEXT,
            -- Add more columns as needed
        )
    `)
    if err != nil {
        log.Fatal("Error creating table:", err)
    }

    http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodPost {
            http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
            return
        }

        // Parse the uploaded file
        file, _, err := r.FormFile("csvFile") // Adjust 'csvFile' if your form field has a different name
        if err != nil {
            http.Error(w, "Error parsing file", http.StatusBadRequest)
            return
        }
        defer file.Close()

        // Read the CSV data
        reader := csv.NewReader(file)
        // Skip the header row if needed
        _, err = reader.Read()
        if err != nil {
            http.Error(w, "Error reading CSV header", http.StatusBadRequest)
            return
        }

        // Process each row
        for {
            record, err := reader.Read()
            if err == io.EOF {
                break
            }
            if err != nil {
                http.Error(w, "Error reading CSV row", http.StatusBadRequest)
                return
            }

            // Insert into the database (adjust the column names and placeholders as needed)
            _, err = db.Exec(`
                INSERT INTO your_table_name (column1, column2)
                VALUES ($1, $2)
            `, record[0], record[1]) // Assuming two columns in your CSV
            if err != nil {
                http.Error(w, "Error inserting into database", http.StatusInternalServerError)
                return
            }
        }

        fmt.Fprintln(w, "CSV data uploaded and stored successfully!")
    })

    // Start the server
    log.Println("Server listening on :8080...")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
