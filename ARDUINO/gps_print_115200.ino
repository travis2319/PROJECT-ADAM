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
  bool dateValid = gps.date.isValid();
  bool timeValid = gps.time.isValid();

  // Print location
  Serial.print(F("Location: ")); 
  if (locationValid) {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
  } else {
    Serial.print(F("INVALID"));
  }

  // Print date and time
  Serial.print(F("  Date/Time: "));
  if (dateValid && timeValid) {
    char dateBuffer[11], timeBuffer[9];  // Buffer for date and time strings
    snprintf(dateBuffer, sizeof(dateBuffer), "%02d/%02d/%04d", gps.date.month(), gps.date.day(), gps.date.year());
    snprintf(timeBuffer, sizeof(timeBuffer), "%02d:%02d:%02d", gps.time.hour(), gps.time.minute(), gps.time.second());
    Serial.print(dateBuffer);
    Serial.print(F(" "));
    Serial.print(timeBuffer);
  } else {
    Serial.print(F("INVALID"));
  }
  Serial.println();
}


// #include <TinyGPS++.h>
// #include <SoftwareSerial.h>

// static const int RXPin = 4, TXPin = 3;
// static const uint32_t GPSBaud = 9600;

// TinyGPSPlus gps;
// SoftwareSerial ss(RXPin, TXPin);

// void setup() {
//   Serial.begin(9600);
//   ss.begin(GPSBaud);
//   Serial.println(F("GPS Module Test"));
// }

// void loop() {
//   while (ss.available() > 0) {
//     if (gps.encode(ss.read())) {
//       displayInfo();
//     }
//   }

//   if (millis() > 5000 && gps.charsProcessed() < 10) {
//     Serial.println(F("No GPS detected: check wiring."));
//     delay(5000);  // Wait 5 seconds before retrying
//   }
// }

// void displayInfo() {
//   Serial.print(F("Location: ")); 
//   if (gps.location.isValid()) {
//     Serial.print(gps.location.lat(), 6);
//     Serial.print(F(","));
//     Serial.print(gps.location.lng(), 6);
//   } else {
//     Serial.print(F("INVALID"));
//   }

//   Serial.print(F("  Date/Time: "));
//   if (gps.date.isValid() && gps.time.isValid()) {
//     Serial.print(gps.date.month());
//     Serial.print(F("/"));
//     Serial.print(gps.date.day());
//     Serial.print(F("/"));
//     Serial.print(gps.date.year());
//     Serial.print(F(" "));
//     if (gps.time.hour() < 10) Serial.print(F("0"));
//     Serial.print(gps.time.hour());
//     Serial.print(F(":"));
//     if (gps.time.minute() < 10) Serial.print(F("0"));
//     Serial.print(gps.time.minute());
//     Serial.print(F(":"));
//     if (gps.time.second() < 10) Serial.print(F("0"));
//     Serial.print(gps.time.second());
//   } else {
//     Serial.print(F("INVALID"));
//   }

//   Serial.println();
// }