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
    "strconv"
    _ "github.com/lib/pq"
    "strings"
)

var stringColumns = map[string]bool{
    "TIMESTAMP":      true,
    "OBD_COMPLIANCE": true,
    "PIDS_B":         true,
    "PIDS_C":         true,
    "FUEL_TYPE":      true,
}

func main() {
    connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
        os.Getenv("POSTGRES_HOST"),
        os.Getenv("POSTGRES_PORT"),
        os.Getenv("POSTGRES_USER"),
        os.Getenv("POSTGRES_PASSWORD"),
        os.Getenv("POSTGRES_DB"),
    )

    db, err := sql.Open("postgres", connStr)
    if err != nil {
        log.Fatal("Error connecting to the database:", err)
    }
    defer db.Close()

    if err := db.Ping(); err != nil {
        log.Fatal("Database connection failed:", err)
    }
    
    http.HandleFunc("/status", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Server is live!")
	})

    http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != "POST" {
            http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
            return
        }

        file, _, err := r.FormFile("file")
        if err != nil {
            http.Error(w, "Failed to get the file", http.StatusBadRequest)
            return
        }
        defer file.Close()

        csvReader := csv.NewReader(file)
        header, err := csvReader.Read()
        if err != nil {
            http.Error(w, "Failed to read CSV header", http.StatusBadRequest)
            return
        }

        createTableQuery := fmt.Sprintf("CREATE TABLE IF NOT EXISTS your_table (%s)",
            createTableColumns(header))
        if _, err := db.Exec(createTableQuery); err != nil {
            http.Error(w, "Failed to create table", http.StatusInternalServerError)
            return
        }

        placeholders := make([]string, len(header))
        for i := range placeholders {
            placeholders[i] = fmt.Sprintf("$%d", i+1)
        }
        query := fmt.Sprintf("INSERT INTO your_table (%s) VALUES (%s)",
            strings.Join(header, ", "), strings.Join(placeholders, ", "))

        tx, err := db.Begin()
        if err != nil {
            http.Error(w, "Failed to start transaction", http.StatusInternalServerError)
            return
        }

        for {
            record, err := csvReader.Read()
            if err == io.EOF {
                break
            }
            if err != nil {
                tx.Rollback()
                http.Error(w, "Error reading CSV data", http.StatusInternalServerError)
                return
            }

            values := make([]interface{}, len(record))
            for i, v := range record {
                columnName := header[i]
                if v == "" {
                    values[i] = nil
                } else if stringColumns[columnName] {
                    values[i] = v
                } else {
                    floatValue, err := strconv.ParseFloat(v, 64)
                    if err != nil {
                        tx.Rollback()
                        http.Error(w, fmt.Sprintf("Invalid float data in column %s", columnName), http.StatusBadRequest)
                        return
                    }
                    values[i] = floatValue
                }
            }

            if _, err := tx.Exec(query, values...); err != nil {
                tx.Rollback()
                log.Printf("Error inserting record: %v\n", err)
                http.Error(w, "Error inserting data into database", http.StatusInternalServerError)
                return
            }
        }

        if err := tx.Commit(); err != nil {
            http.Error(w, "Failed to commit transaction", http.StatusInternalServerError)
            return
        }

        w.Write([]byte("CSV data successfully imported"))
    })

    // New route to retrieve data as JSON
    http.HandleFunc("/data", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != "GET" {
            http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
            return
        }

        rows, err := db.Query("SELECT * FROM your_table")
        if err != nil {
            http.Error(w, "Failed to query data", http.StatusInternalServerError)
            return
        }
        defer rows.Close()

        columns, err := rows.Columns()
        if err != nil {
            http.Error(w, "Failed to get columns", http.StatusInternalServerError)
            return
        }

        var result []map[string]interface{}

        for rows.Next() {
            row := make([]interface{}, len(columns))
            rowPtrs := make([]interface{}, len(columns))
            for i := range row {
                rowPtrs[i] = &row[i]
            }

            if err := rows.Scan(rowPtrs...); err != nil {
                http.Error(w, "Failed to scan row", http.StatusInternalServerError)
                return
            }

            rowMap := make(map[string]interface{})
            for i, col := range columns {
                rowMap[col] = row[i]
            }
            result = append(result, rowMap)
        }

        jsonData, err := json.Marshal(result)
        if err != nil {
            http.Error(w, "Failed to convert data to JSON", http.StatusInternalServerError)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        w.Write(jsonData)
    })

    log.Println("Starting server on :8080...")
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func createTableColumns(header []string) string {
    columns := make([]string, len(header))
    for i, col := range header {
        columnName := strings.TrimSpace(col)
        if stringColumns[columnName] {
            columns[i] = fmt.Sprintf("%s TEXT", columnName)
        } else {
            columns[i] = fmt.Sprintf("%s DOUBLE PRECISION", columnName)
        }
    }
    return strings.Join(columns, ", ")
}
