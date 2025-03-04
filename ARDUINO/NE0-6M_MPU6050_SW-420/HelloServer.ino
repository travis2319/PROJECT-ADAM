#include <Wire.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <ESP8266WiFi.h>

// Constants
const unsigned long GPS_READ_INTERVAL = 500;    // GPS reading interval (1 second)
const unsigned long IMU_READ_INTERVAL = 100;     // IMU reading interval (100ms)
const unsigned long VIB_READ_INTERVAL = 50;      // Vibration reading interval (50ms)
const int SERIAL_BAUD = 115200;
const int GPS_BAUD = 9600;

// Pin Definitions
struct Pins {
    static const int GPS_RX = 12;    // D6
    static const int GPS_TX = 13;    // D7
    static const int VIB_PIN = 14;   // D5
};

// Sensor objects
TinyGPSPlus gps;
SoftwareSerial gpsSerial(Pins::GPS_RX, Pins::GPS_TX);
Adafruit_MPU6050 mpu;

// Timing variables
unsigned long lastGpsRead = 0;
unsigned long lastImuRead = 0;
unsigned long lastVibRead = 0;
unsigned long lastPrintTime = 0;  // Track when to print data

// Sensor data structure
struct SensorData {
    // GPS data
    double latitude = 0;
    double longitude = 0;
    bool gpsValid = false;
    
    // IMU data
    struct {
        float x, y, z;
    } accel, gyro;
    
    // Vibration data
    bool vibrationDetected = false;
} sensorData;

void setupMPU() {
    if (!mpu.begin()) {
        Serial.println(F("MPU6050 not found!"));
        while (1) delay(10);
    }
    
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void readGPS() {
    while (gpsSerial.available() > 0) {
        if (gps.encode(gpsSerial.read())) {
            sensorData.gpsValid = gps.location.isValid();
            if (sensorData.gpsValid) {
                sensorData.latitude = gps.location.lat();
                sensorData.longitude = gps.location.lng();
            }
        }
    }
}

void readIMU() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    // Store acceleration data
    sensorData.accel.x = a.acceleration.x;
    sensorData.accel.y = a.acceleration.y;
    sensorData.accel.z = a.acceleration.z;
    
    // Store gyroscope data
    sensorData.gyro.x = g.gyro.x;
    sensorData.gyro.y = g.gyro.y;
    sensorData.gyro.z = g.gyro.z;
}

void readVibration() {
    sensorData.vibrationDetected = digitalRead(Pins::VIB_PIN) == HIGH;
}

void printData() {
    Serial.print(F("[GPS] "));
    if (sensorData.gpsValid) {
        Serial.print(F("Lat: "));
        Serial.print(sensorData.latitude, 6);
        Serial.print(F(", Lon: "));
        Serial.print(sensorData.longitude, 6);
    } else {
        Serial.print(F("No GPS Signal"));
    }

    // IMU Data
    Serial.print(F(" | ACC (m/s²) X: "));
    Serial.print(sensorData.accel.x);
    Serial.print(F(" Y: "));
    Serial.print(sensorData.accel.y);
    Serial.print(F(" Z: "));
    Serial.print(sensorData.accel.z);
    
    Serial.print(F(" | GYRO (°/s) X: "));
    Serial.print(sensorData.gyro.x);
    Serial.print(F(" Y: "));
    Serial.print(sensorData.gyro.y);
    Serial.print(F(" Z: "));
    Serial.print(sensorData.gyro.z);
    
    // Vibration Data
    Serial.print(F(" | VIBRATION: "));
    Serial.println(sensorData.vibrationDetected ? F("DETECTED") : F("NO"));

    lastPrintTime = millis();
}

void setup() {
    Serial.begin(SERIAL_BAUD);
    gpsSerial.begin(GPS_BAUD);
    Wire.begin();
    
    setupMPU();
    pinMode(Pins::VIB_PIN, INPUT);
    
    Serial.println(F("System initialized"));
}

void loop() {
    unsigned long currentMillis = millis();
    
    // Read GPS continuously whenever data is available
    readGPS();
    
    // Read IMU at specified interval
    if (currentMillis - lastImuRead >= IMU_READ_INTERVAL) {
        readIMU();
        lastImuRead = currentMillis;
    }
    
    // Read vibration sensor at specified interval
    if (currentMillis - lastVibRead >= VIB_READ_INTERVAL) {
        readVibration();
        lastVibRead = currentMillis;
    }
    
    // Print all data once per second
    if (currentMillis - lastPrintTime >= GPS_READ_INTERVAL) {
        printData();
    }
}


// #include <Wire.h>
// #include <TinyGPS++.h>
// #include <SoftwareSerial.h>
// #include <Adafruit_MPU6050.h>
// #include <Adafruit_Sensor.h>

// // GPS Module
// static const int RXPin = 12, TXPin = 13;  // D6 = RX, D7 = TX
// static const uint32_t GPSBaud = 9600;
// TinyGPSPlus gps;
// SoftwareSerial gpsSerial(RXPin, TXPin);

// // MPU6050
// Adafruit_MPU6050 mpu;

// // SW-420 Vibration Sensor
// const int vibrationPin = 14;  // D5 = GPIO14

// void setup() {
//     Serial.begin(115200);
//     gpsSerial.begin(GPSBaud);
//     Wire.begin();

//     // Initialize MPU6050
//     if (!mpu.begin()) {
//         Serial.println("MPU6050 not found!");
//         while (1);
//     }
//     mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
//     mpu.setGyroRange(MPU6050_RANGE_500_DEG);
//     mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

//     // Vibration sensor pin setup
//     pinMode(vibrationPin, INPUT);
// }

// void loop() {
//     // Read GPS data
//     while (gpsSerial.available() > 0) {
//         gps.encode(gpsSerial.read());
//     }
    
//     // Read MPU6050 sensor data
//     sensors_event_t a, g, temp;
//     mpu.getEvent(&a, &g, &temp);

//     // Read SW-420 vibration sensor
//     int vibrationState = digitalRead(vibrationPin);

//     // Print GPS data if available
//     if (gps.location.isValid()) {
//         Serial.print("Latitude: ");
//         Serial.print(gps.location.lat(), 6);
//         Serial.print(", Longitude: ");
//         Serial.print(gps.location.lng(), 6);
//     } else {
//         Serial.print("Waiting for GPS...");
//     }

//     // Print IMU data
//     Serial.print(" | Accel (m/s²): X=");
//     Serial.print(a.acceleration.x);
//     Serial.print(" Y=");
//     Serial.print(a.acceleration.y);
//     Serial.print(" Z=");
//     Serial.print(a.acceleration.z);

//     Serial.print(" | Gyro (°/s): X=");
//     Serial.print(g.gyro.x);
//     Serial.print(" Y=");
//     Serial.print(g.gyro.y);
//     Serial.print(" Z=");
//     Serial.print(g.gyro.z);

//     // Print vibration status
//     Serial.print(" | Vibration: ");
//     Serial.println(vibrationState == HIGH ? "Detected" : "No Vibration");

//     delay(1000);  // Delay for readability
// }
