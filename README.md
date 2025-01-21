# ADAM - Vehicle Diagnostic System

## Overview
A comprehensive vehicle diagnostic system that integrates OBD-II data collection, GPS tracking, and real-time analysis through multiple components including Go, Python, FastAPI, and React Native.

## Project Structure
```
.
├── ADAM/           # Core Go implementation
├── ARDUINO/        # GPS NodeMCU implementations
├── DATASET/        # Training and test datasets
├── DOCUMENTATION/  # Performance test data
├── FASTAPI/       # Backend API server
├── GOLANG/        # Additional Go servers
├── PYTHON/        # Python implementations
├── REACT-NATIVE/  # Mobile application
└── RUST/          # Rust implementations
```

## Setup Instructions

### 1. Go Implementation (ADAM)
```bash
cd ADAM
# Install dependencies
go mod download
# Run the main server
go run main.go
```

### 2. FastAPI Backend
```bash
cd FASTAPI
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

### 3. Python Modules
```bash
cd PYTHON/ADAM
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows

# Install necessary packages
pip install pandas numpy scikit-learn

# For GPS module
cd ../GPS
python -m venv venv
source venv/bin/activate
# Install GPS-specific requirements
```

### 4. React Native Mobile App
```bash
cd REACT-NATIVE/app
# Install dependencies
npm install

# Start the development server
npm start

# Run on Android
npm run android

# Run on iOS
npm run ios
```

### 5. Arduino Setup (Optional - for GPS)
1. Open Arduino IDE
2. Load `ARDUINO/gps-nodemcu.ino` or `gps_print_115200.ino`
3. Select appropriate board and port
4. Upload to device

### 6. Rust Components (Optional)
```bash
cd RUST/obd-rust
# Build the project
cargo build

# Run tests
cargo test

# Run the application
cargo run
```

## Development

### Prerequisites
- Go 1.19+
- Python 3.8+
- Node.js 14+
- Rust (latest stable)
- Arduino IDE (for GPS module)
- React Native CLI

### Dataset Usage
Training data is available in the DATASET directory:
- `kai1.csv`
- `obd_data.csv`
- `real_car.csv`
- `real_car_2.csv`

Performance test data is in the DOCUMENTATION directory, categorized by speed ranges.

## API Documentation
FastAPI automatically generates documentation at:
```
http://localhost:8000/docs
```

## Testing
```bash
# Go tests
cd ADAM
go test ./...

# Python tests
cd PYTHON/ADAM
python -m pytest

# React Native tests
cd REACT-NATIVE/app
npm test
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## Research References
Research papers are available in the RESEARCH PAPER directory, covering:
- Vehicle Black Box implementations
- OBD-II fleet management
- Traffic accident prediction
- Driving behavior analysis

## License
[Specify your license]

## Contact
[Your contact information]

---
**Note**: This project is under active development. Check for updates regularly.