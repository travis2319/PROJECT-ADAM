#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// Pin assignments and baud rate for GPS
static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

// GPS and software serial objects
TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

// Millis tracking for GPS detection
unsigned long lastCheckMillis = 0;
const unsigned long gpsCheckInterval = 5000; // 5 seconds interval for checking GPS

void setup() {
  Serial.begin(115200); // Increase baud rate for faster data display on Serial Monitor
  ss.begin(GPSBaud);
  Serial.println(F("GPS Module Test"));

  // Ensure SoftwareSerial is initialized correctly
  if (!ss) {
    Serial.println(F("SoftwareSerial failed to initialize. Check pin assignments."));
  }
}

void loop() {
  // Buffer GPS data more efficiently
  while (ss.available() > 0) {
    char c = ss.read();
    if (gps.encode(c)) {
      displayInfo();
    }
  }

  // Check if GPS is detected every 5 seconds
  if (millis() - lastCheckMillis > gpsCheckInterval) {
    lastCheckMillis = millis(); // Reset the timer
    if (gps.charsProcessed() < 10) {
      Serial.println(F("No GPS detected: check wiring."));
    }
  }
}

// Function to display GPS information
void displayInfo() {
  // Store values locally to avoid repeated function calls
  bool locationValid = gps.location.isValid();

  // Print location
  Serial.print(F("Location: ")); 
  if (locationValid) {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
  } else {
    Serial.print(F("INVALID"));
  }

  Serial.println();
}
