package main

// import (
// 	"database/sql"
// 	"encoding/csv"
// 	"encoding/json"
// 	"fmt"
// 	_ "github.com/lib/pq"
// 	"io"
// 	"log"
// 	"net/http"
// 	"os"
// 	// "strconv"
// )

// func main() {
// 	// Build the connection string using environment variables
// 	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
// 		os.Getenv("POSTGRES_HOST"),
// 		os.Getenv("POSTGRES_PORT"),
// 		os.Getenv("POSTGRES_USER"),
// 		os.Getenv("POSTGRES_PASSWORD"),
// 		os.Getenv("POSTGRES_DB"),
// 	)

// 	// PostgreSQL connection setup
// 	db, err := sql.Open("postgres", connStr)
// 	if err != nil {
// 		log.Fatal("Error connecting to the database:", err)
// 	}
// 	defer db.Close()

// 	// Create the table if it doesn't exist
// 	// 	_, err = db.Exec(`
// 	// CREATE TABLE IF NOT EXISTS sensor (
// 	// 	id SERIAL PRIMARY KEY,
// 	// 	TIME TEXT,
// 	// 	SPEED TEXT,
// 	// 	SENSOR1 TEXT,
// 	// 	SENSOR2 TEXT,
// 	// 	SENSOR3 TEXT,
// 	// 	SENSOR4 TEXT,
// 	// 	SENSOR5 TEXT,
// 	// 	SENSOR6 TEXT,
// 	// 	SENSOR7 TEXT,
// 	// 	SENSOR8 TEXT,
// 	// 	SENSOR9 TEXT
// 	// );
// 	// `)
// 	// 	if err != nil {
// 	// 		log.Fatal("Error creating table:", err)
// 	// 	}

// 	// Create the OBD records table
// 	createTableSQL := `CREATE TABLE IF NOT EXISTS obd_records (
// 	timestamp DOUBLE PRECISION NULL,
// 	status TEXT NULL,
// 	fuel_status TEXT NULL,
// 	engine_load DOUBLE PRECISION NULL,
// 	coolant_temp DOUBLE PRECISION NULL,
// 	short_fuel_trim_1 DOUBLE PRECISION NULL,
// 	long_fuel_trim_1 DOUBLE PRECISION NULL,
// 	intake_pressure DOUBLE PRECISION NULL,
// 	rpm DOUBLE PRECISION NULL,
// 	speed DOUBLE PRECISION NULL,
// 	timing_advance DOUBLE PRECISION NULL,
// 	intake_temp DOUBLE PRECISION NULL,
// 	maf DOUBLE PRECISION NULL,
// 	throttle_pos DOUBLE PRECISION NULL,
// 	o2_sensors TEXT NULL,
// 	o2_b1s2 DOUBLE PRECISION NULL,
// 	obd_compliance TEXT NULL,
// 	run_time DOUBLE PRECISION NULL,
// 	pids_b TEXT NULL,
// 	distance_w_mil DOUBLE PRECISION NULL,
// 	o2_s1_wr_voltage DOUBLE PRECISION NULL,
// 	commanded_egr DOUBLE PRECISION NULL,
// 	evaporative_purge DOUBLE PRECISION NULL,
// 	warmups_since_dtc_clear DOUBLE PRECISION NULL,
// 	distance_since_dtc_clear DOUBLE PRECISION NULL,
// 	barometric_pressure DOUBLE PRECISION NULL,
// 	o2_s1_wr_current DOUBLE PRECISION NULL,
// 	catalyst_temp_b1s1 DOUBLE PRECISION NULL,
// 	catalyst_temp_b1s2 DOUBLE PRECISION NULL,
// 	pids_c TEXT NULL,
// 	control_module_voltage DOUBLE PRECISION NULL,
// 	absolute_load DOUBLE PRECISION NULL,
// 	commanded_equiv_ratio DOUBLE PRECISION NULL,
// 	relative_throttle_pos DOUBLE PRECISION NULL,
// 	throttle_pos_b DOUBLE PRECISION NULL,
// 	throttle_actuator DOUBLE PRECISION NULL,
// 	run_time_mil DOUBLE PRECISION NULL,
// 	time_since_dtc_cleared DOUBLE PRECISION NULL,
// 	fuel_type TEXT NULL,
// 	latitude DOUBLE PRECISION NULL,
// 	longitude DOUBLE PRECISION NULL
// )`
// 	_, err = db.Exec(createTableSQL)
// 	if err != nil {
// 		log.Fatal("Error creating table:", err)
// 	}
// 	fmt.Println("Connected to the database ")

// 	// Status route to check if server is live
// 	http.HandleFunc("/status", func(w http.ResponseWriter, r *http.Request) {
// 		w.WriteHeader(http.StatusOK)
// 		fmt.Fprintln(w, "Server is live!")
// 	})
// 	// http.HandleFunc("/csvupload", func(w http.ResponseWriter, r *http.Request) {
// 	// 	if r.Method != http.MethodPost {
// 	// 		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
// 	// 		return
// 	// 	}
// 	// 	// Get the file from the form
// 	// 	file, _, err := r.FormFile("file")
// 	// 	if err != nil {
// 	// 		fmt.Fprintln(w, "Error retrieving the file")
// 	// 		return
// 	// 	}
// 	// 	defer file.Close()

// 	// 	// Create a new CSV reader and read the file
// 	// 	reader := csv.NewReader(file)

// 	// 	// Read and discard the header
// 	// 	_, err = reader.Read()
// 	// 	if err != nil {
// 	// 		http.Error(w, "Error reading CSV header: "+err.Error(), http.StatusBadRequest)
// 	// 		return
// 	// 	}
// 	// 	insertSQL := `
// 	// 		INSERT INTO obd_records (
// 	// 			timestamp,status,fuel_status,engine_load,coolant_temp,short_fuel_trim_1,long_fuel_trim_1,intake_pressure,rpm,speed,timing_advance,intake_temp,maf,throttle_pos,o2_sensors,o2_b1s2,obd_compliance,run_time,pids_b,distance_w_mil,o2_s1_wr_voltage,commanded_egr,evaporative_purge,warmups_since_dtc_clear,distance_since_dtc_clear,barometric_pressure,o2_s1_wr_current,catalyst_temp_b1s1,catalyst_temp_b1s2,pids_c,control_module_voltage,absolute_load,commanded_equiv_ratio,relative_throttle_pos,throttle_pos_b,throttle_actuator,run_time_mil,time_since_dtc_cleared,fuel_type,timestamp,latitude,longitude
// 	// 		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,$21, $22, $23, $24, $25, $26, $27, $28, $29, $30,$31, $32, $33, $34, $35, $36, $37, $38, $39, $40,$41,$42)
// 	// 	`
// 	// 	Timestamp,STATUS,FUEL_STATUS,ENGINE_LOAD,COOLANT_TEMP,SHORT_FUEL_TRIM_1,LONG_FUEL_TRIM_1,INTAKE_PRESSURE,RPM,SPEED,TIMING_ADVANCE,INTAKE_TEMP,MAF,THROTTLE_POS,O2_SENSORS,O2_B1S2,OBD_COMPLIANCE,RUN_TIME,PIDS_B,DISTANCE_W_MIL,O2_S1_WR_VOLTAGE,COMMANDED_EGR,EVAPORATIVE_PURGE,WARMUPS_SINCE_DTC_CLEAR,DISTANCE_SINCE_DTC_CLEAR,BAROMETRIC_PRESSURE,O2_S1_WR_CURRENT,CATALYST_TEMP_B1S1,CATALYST_TEMP_B1S2,PIDS_C,CONTROL_MODULE_VOLTAGE,ABSOLUTE_LOAD,COMMANDED_EQUIV_RATIO,RELATIVE_THROTTLE_POS,THROTTLE_POS_B,THROTTLE_ACTUATOR,RUN_TIME_MIL,TIME_SINCE_DTC_CLEARED,FUEL_TYPE,Timestamp,Latitude,Longitude

// 	// 	// Process each row
// 	// 	for {
// 	// 		record, err := reader.Read()
// 	// 		if err == io.EOF {
// 	// 			break
// 	// 		}
// 	// 		if err != nil {
// 	// 			http.Error(w, "Error reading CSV row: "+err.Error(), http.StatusBadRequest)
// 	// 			return
// 	// 		}

// 	// 		// Ensure we have at least 11 fields
// 	// 		if len(record) < 43 {
// 	// 			http.Error(w, "CSV row does not have enough fields", http.StatusBadRequest)
// 	// 			return
// 	// 		}

// 	// 		// Extract values from the record
// 	// 		values := []interface{}{
// 	// 			record[1],
// 	// 			record[2],
// 	// 			record[3],
// 	// 			record[4],
// 	// 			record[5],
// 	// 			record[6],
// 	// 			record[7],
// 	// 			record[8],
// 	// 			record[9],
// 	// 			record[10],
// 	// 			record[11],
// 	// 			record[12],
// 	// 			record[13],
// 	// 			record[14],
// 	// 			record[15],
// 	// 			record[16],
// 	// 			record[17],
// 	// 			record[18],
// 	// 			record[19],
// 	// 			record[20],
// 	// 			record[21],
// 	// 			record[22],
// 	// 			record[23],
// 	// 			record[24],
// 	// 			record[25],
// 	// 			record[26],
// 	// 			record[27],
// 	// 			record[28],
// 	// 			record[29],
// 	// 			record[30],
// 	// 			record[31],
// 	// 			record[32],
// 	// 			record[33],
// 	// 			record[34],
// 	// 			record[35],
// 	// 			record[36],
// 	// 			record[37],
// 	// 			record[38],
// 	// 			record[39],
// 	// 			record[40],
// 	// 			record[41],
// 	// 			record[42]
// 	// 		}

// 	// 		// Insert into the database
// 	// 		_, err = db.Exec(insertSQL, values...)
// 	// 		if err != nil {
// 	// 			http.Error(w, "Error inserting into database: "+err.Error(), http.StatusInternalServerError)
// 	// 			return
// 	// 		}

// 	// 	}
// 	// 	// for {
// 	// 	//     record, err := reader.Read()
// 	// 	//     if err != nil {
// 	// 	//         break
// 	// 	//     }
// 	// 	//     // Log each row in the console
// 	// 	//     fmt.Println("CSV Record:", record)
// 	// 	// }
// 	// 	fmt.Fprintln(w, "File uploaded and logged successfully")
// 	// })

// 	http.HandleFunc("/csvupload", func(w http.ResponseWriter, r *http.Request) {
// 		// Limit upload size if needed
// 		r.Body = http.MaxBytesReader(w, r.Body, 10<<20) // 10 MB limit

// 		if r.Method != http.MethodPost {
// 			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
// 			return
// 		}

// 		// Get the file from the form
// 		file, header, err := r.FormFile("file")
// 		if err != nil {
// 			http.Error(w, "Error retrieving file", http.StatusBadRequest)
// 			return
// 		}
// 		defer file.Close()

// 		// Optional: Check file size
// 		if header.Size > 10<<20 { // 10 MB
// 			http.Error(w, "File too large", http.StatusBadRequest)
// 			return
// 		}

// 		// Start a transaction
// 		tx, err := db.Begin()
// 		if err != nil {
// 			http.Error(w, "Database error", http.StatusInternalServerError)
// 			return
// 		}
// 		defer tx.Rollback() // Rollback in case of error

// 		// Create a new CSV reader and read the file
// 		reader := csv.NewReader(file)
// 		reader.FieldsPerRecord = 42 // Enforce exact number of columns

// 		// Read and discard the header
// 		_, err = reader.Read()
// 		if err != nil {
// 			http.Error(w, "Invalid CSV header", http.StatusBadRequest)
// 			return
// 		}

// 		insertSQL := `
//     INSERT INTO obd_records (
//         timestamp, status, fuel_status, engine_load, coolant_temp,
//         short_fuel_trim_1, long_fuel_trim_1, intake_pressure, rpm, speed,
//         timing_advance, intake_temp, maf, throttle_pos, o2_sensors,
//         o2_b1s2, obd_compliance, run_time, pids_b, distance_w_mil,
//         o2_s1_wr_voltage, commanded_egr, evaporative_purge,
//         warmups_since_dtc_clear, distance_since_dtc_clear,
//         barometric_pressure, o2_s1_wr_current, catalyst_temp_b1s1,
//         catalyst_temp_b1s2, pids_c, control_module_voltage,
//         absolute_load, commanded_equiv_ratio, relative_throttle_pos,
//         throttle_pos_b, throttle_actuator, run_time_mil,
//         time_since_dtc_cleared, fuel_type, latitude, longitude
//     ) VALUES (
//         $1,
//         COALESCE(NULLIF($2, ''), 'default_status'),
//         COALESCE(NULLIF($3, ''), 0.0),
//         COALESCE(NULLIF($4, ''), 0.0),
//         COALESCE(NULLIF($5, ''), 0.0),
//         COALESCE(NULLIF($6, ''), 0.0),
//         COALESCE(NULLIF($7, ''), 0.0),
//         COALESCE(NULLIF($8, ''), 0.0),
//         COALESCE(NULLIF($9, ''), 0.0),
//         COALESCE(NULLIF($10, ''), 0.0),
//         COALESCE(NULLIF($11, ''), 0.0),
//         COALESCE(NULLIF($12, ''), 0.0),
//         COALESCE(NULLIF($13, ''), 0.0),
//         COALESCE(NULLIF($14, ''), 0.0),
//         COALESCE(NULLIF($15, ''), 0.0),
//         COALESCE(NULLIF($16, ''), 0.0),
//         COALESCE(NULLIF($17, ''), 0.0),
//         COALESCE(NULLIF($18, ''), 0.0),
//         COALESCE(NULLIF($19, ''), 0.0),
//         COALESCE(NULLIF($20, ''), 0.0),
//         COALESCE(NULLIF($21, ''), 0.0),
//         COALESCE(NULLIF($22, ''), 0.0),
//         COALESCE(NULLIF($23, ''), 0.0),
//         COALESCE(NULLIF($24, ''), 0.0),
//         COALESCE(NULLIF($25, ''), 0.0),
//         COALESCE(NULLIF($26, ''), 0.0),
//         COALESCE(NULLIF($27, ''), 0.0),
//         COALESCE(NULLIF($28, ''), 0.0),
//         COALESCE(NULLIF($29, ''), 0.0),
//         COALESCE(NULLIF($30, ''), 0.0),
//         COALESCE(NULLIF($31, ''), 0.0),
//         COALESCE(NULLIF($32, ''), 0.0),
//         COALESCE(NULLIF($33, ''), 0.0),
//         COALESCE(NULLIF($34, ''), 0.0),
//         COALESCE(NULLIF($35, ''), 0.0),
//         COALESCE(NULLIF($36, ''), 0.0),
//         COALESCE(NULLIF($37, ''), 0.0),
//         COALESCE(NULLIF($38, ''), 0.0),
//         COALESCE(NULLIF($39, ''), 0.0),
//         COALESCE(NULLIF($40, ''), 0.0),
//         COALESCE(NULLIF($41, ''), 0.0)
//     )
// `

// 		// insertSQL := `
// 		// 	INSERT INTO obd_records (
// 		// 		timestamp, status, fuel_status, engine_load, coolant_temp,
// 		// 		short_fuel_trim_1, long_fuel_trim_1, intake_pressure, rpm, speed,
// 		// 		timing_advance, intake_temp, maf, throttle_pos, o2_sensors,
// 		// 		o2_b1s2, obd_compliance, run_time, pids_b, distance_w_mil,
// 		// 		o2_s1_wr_voltage, commanded_egr, evaporative_purge,
// 		// 		warmups_since_dtc_clear, distance_since_dtc_clear,
// 		// 		barometric_pressure, o2_s1_wr_current, catalyst_temp_b1s1,
// 		// 		catalyst_temp_b1s2, pids_c, control_module_voltage,
// 		// 		absolute_load, commanded_equiv_ratio, relative_throttle_pos,
// 		// 		throttle_pos_b, throttle_actuator, run_time_mil,
// 		// 		time_since_dtc_cleared, fuel_type, latitude, longitude
// 		// 	) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
// 		// 			  $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24,
// 		// 			  $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35,
// 		// 			  $36, $37, $38, $39, $40, $41)
// 		// `

// 		// Prepare the statement once
// 		stmt, err := tx.Prepare(insertSQL)
// 		if err != nil {
// 			http.Error(w, "Prepare statement error", http.StatusInternalServerError)
// 			return
// 		}
// 		defer stmt.Close()

// 		// Process each row
// 		var recordsProcessed int
// 		for {
// 			record, err := reader.Read()
// 			if err == io.EOF {
// 				break
// 			}
// 			if err != nil {
// 				http.Error(w, "Invalid CSV data", http.StatusBadRequest)
// 				return
// 			}

// 			// Insert into the database
// 			_, err = stmt.Exec(
// 				record[1], record[2], record[3], record[4], record[5],
// 				record[6], record[7], record[8], record[9], record[10],
// 				record[11], record[12], record[13], record[14], record[15],
// 				record[16], record[17], record[18], record[19], record[20],
// 				record[21], record[22], record[23], record[24], record[25],
// 				record[26], record[27], record[28], record[29], record[30],
// 				record[31], record[32], record[33], record[34], record[35],
// 				record[36], record[37], record[38], record[39], record[40],
// 				record[41])
// 			if err != nil {
// 				http.Error(w, "Database insert error", http.StatusInternalServerError)
// 				return
// 			}
// 			recordsProcessed++
// 		}

// 		// Commit the transaction
// 		err = tx.Commit()
// 		if err != nil {
// 			http.Error(w, "Transaction commit error", http.StatusInternalServerError)
// 			return
// 		}

// 		fmt.Fprintf(w, "File uploaded successfully. %d records processed.", recordsProcessed)
// 	})

// 	http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
// 		if r.Method != http.MethodPost {
// 			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
// 			return
// 		}

// 		// Parse the uploaded file
// 		file, _, err := r.FormFile("csvFile")
// 		if err != nil {
// 			http.Error(w, "Error parsing file: "+err.Error(), http.StatusBadRequest)
// 			return
// 		}
// 		defer file.Close()

// 		// Read the CSV data
// 		reader := csv.NewReader(file)

// 		// Read and discard the header
// 		_, err = reader.Read()
// 		if err != nil {
// 			http.Error(w, "Error reading CSV header: "+err.Error(), http.StatusBadRequest)
// 			return
// 		}

// 		// Prepare the SQL statement
// 		insertSQL := `
// 			INSERT INTO sensor (
// 				TIME, SENSOR1, SENSOR2, SENSOR3, SENSOR4, SENSOR5,
// 				SENSOR6, SENSOR7, SENSOR8, SENSOR9, SENSOR10, SENSOR11, SENSOR12
// 			) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
// 		`

// 		// Process each row
// 		for {
// 			record, err := reader.Read()
// 			if err == io.EOF {
// 				break
// 			}
// 			if err != nil {
// 				http.Error(w, "Error reading CSV row: "+err.Error(), http.StatusBadRequest)
// 				return
// 			}

// 			// Ensure we have at least 11 fields
// 			if len(record) < 42 {
// 				http.Error(w, "CSV row does not have enough fields", http.StatusBadRequest)
// 				return
// 			}

// 			// Extract values from the record
// 			values := []interface{}{
// 				record[1],
// 				record[2],
// 				record[3],
// 				record[4],
// 				record[5],
// 				record[6],
// 				record[7],
// 				record[8],
// 				record[9],
// 				record[10],
// 				record[11],
// 				record[12],
// 				record[13],
// 				record[14],
// 				record[15],
// 				record[16],
// 				record[17],
// 				record[18],
// 				record[19],
// 				record[20],
// 				record[21],
// 				record[22],
// 				record[23],
// 				record[24],
// 				record[25],
// 				record[26],
// 				record[27],
// 				record[28],
// 				record[29],
// 				record[30],
// 				record[31],
// 				record[32],
// 				record[33],
// 				record[34],
// 				record[35],
// 				record[36],
// 				record[37],
// 				record[38],
// 				record[39],
// 				record[40],
// 				record[41],
// 				record[42],
// 				"",
// 				"",
// 				"",
// 			}

// 			// Insert into the database
// 			_, err = db.Exec(insertSQL, values...)
// 			if err != nil {
// 				http.Error(w, "Error inserting into database: "+err.Error(), http.StatusInternalServerError)
// 				return
// 			}
// 		}

// 		fmt.Fprintln(w, "CSV data uploaded and stored successfully!")
// 	})
// 	http.HandleFunc("/jsonupload", func(w http.ResponseWriter, r *http.Request) {
// 		// Check if method is POST
// 		if r.Method != http.MethodPost {
// 			http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
// 			return
// 		}
// 		// Read the body
// 		body, err := io.ReadAll(r.Body)
// 		if err != nil {
// 			http.Error(w, "Error reading request body", http.StatusInternalServerError)
// 			return
// 		}
// 		defer r.Body.Close()

// 		// Create a map to store the JSON data
// 		var data interface{}

// 		// Unmarshal JSON into the map
// 		err = json.Unmarshal(body, &data)
// 		if err != nil {
// 			http.Error(w, "Error parsing JSON", http.StatusBadRequest)
// 			return
// 		}

// 		// Pretty print the JSON
// 		prettyJSON, err := json.MarshalIndent(data, "", "    ")
// 		if err != nil {
// 			http.Error(w, "Error formatting JSON", http.StatusInternalServerError)
// 			return
// 		}

// 		// Print the received JSON
// 		fmt.Printf("Received JSON:\n%s\n", string(prettyJSON))

// 		// Send success response
// 		w.WriteHeader(http.StatusOK)
// 		w.Write([]byte("JSON received successfully"))
// 	})

// 	// View uploaded data
// 	http.HandleFunc("/view", func(w http.ResponseWriter, r *http.Request) {
// 		rows, err := db.Query("SELECT * FROM obd_records")
// 		if err != nil {
// 			http.Error(w, "Error querying database", http.StatusInternalServerError)
// 			return
// 		}
// 		defer rows.Close()

// 		var results []map[string]interface{}
// 		columns, _ := rows.Columns()
// 		for rows.Next() {
// 			columnsValues := make([]interface{}, len(columns))
// 			columnsPointers := make([]interface{}, len(columns))
// 			for i := range columnsValues {
// 				columnsPointers[i] = &columnsValues[i]
// 			}

// 			if err := rows.Scan(columnsPointers...); err != nil {
// 				http.Error(w, "Error scanning row", http.StatusInternalServerError)
// 				return
// 			}

// 			rowMap := make(map[string]interface{})
// 			for i, colName := range columns {
// 				rowMap[colName] = columnsValues[i]
// 			}
// 			results = append(results, rowMap)
// 		}

// 		w.Header().Set("Content-Type", "application/json")
// 		json.NewEncoder(w).Encode(results)
// 	})

// 	// Start the server
// 	log.Println("Server listening on :8080...")
// 	log.Fatal(http.ListenAndServe(":8080", nil))
// }
