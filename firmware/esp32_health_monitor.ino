/*
 * Smart Health Monitoring System - ESP32 Firmware
 * 
 * Hardware Interfacing:
 * - MAX30102: Pulse Oximeter & Heart Rate (I2C: SDA=21, SCL=22)
 * - LM35 / Temp Sensor: Body Temperature (Analog: VP/GPIO36)
 * - AD8232: Electrocardiogram / ECG Sensor (Analog: GPIO34, LO+=GPIO18, LO-=GPIO19)
 * - MPU6050: Accelerometer & Gyroscope (I2C: SDA=21, SCL=22)
 * 
 * Data Transmission: Transmits readings to ThingSpeak Cloud over Wi-Fi
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "MAX30105.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "config.h" // Copy config.example.h to config.h and insert credentials

// Sensor Objects
MAX30105 particleSensor;
Adafruit_MPU6050 mpu;

// Pin Definitions
const int LM35_PIN = 36;   // VP pin (Analog Input)
const int ECG_PIN = 34;    // Analog pin for ECG signal

unsigned long lastPostTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);
  
  Serial.println("\n[INIT] Starting Health Monitoring System...");

  // Initialize Wire (I2C)
  Wire.begin(21, 22);

  // Initialize MAX30102 Sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("[ERROR] MAX30102 sensor was not found. Please check wiring!");
  } else {
    Serial.println("[OK] MAX30102 initialized successfully.");
    particleSensor.setup(); // Configure sensor with default settings
  }

  // Initialize MPU6050 Sensor
  if (!mpu.begin()) {
    Serial.println("[ERROR] MPU6050 sensor was not found. Please check wiring!");
  } else {
    Serial.println("[OK] MPU6050 initialized successfully.");
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }

  // Connect to Wi-Fi Network
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("[WIFI] Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[WIFI] Connected! IP Address: " + WiFi.localIP().toString());
}

void loop() {
  if (millis() - lastPostTime >= DATA_POST_INTERVAL_MS) {
    lastPostTime = millis();
    
    // 1. Read MAX30102 (Heart Rate & SpO2)
    long irValue = particleSensor.getIR();
    float avgBPM = 75.0 + random(-5, 5); // Simulated dynamic HR reading for demonstration
    float avgSpO2 = 97.0 + random(-2, 2); // Simulated dynamic SpO2 reading

    // 2. Read LM35 Temperature Sensor
    int lm35Raw = analogRead(LM35_PIN);
    float lm35Voltage = (lm35Raw / 4095.0) * 3.3;
    float lm35Temp = lm35Voltage * 100.0; // Conversion to Celsius

    // 3. Read AD8232 ECG Sensor
    int ecgValue = analogRead(ECG_PIN);

    // 4. Read MPU6050 Accelerometer & Gyroscope Data
    sensors_event_t a, g, tempMPU;
    mpu.getEvent(&a, &g, &tempMPU);
    float ax = a.acceleration.x;
    float ay = a.acceleration.y;
    float az = a.acceleration.z;
    float tempMPU_val = tempMPU.temperature;

    // Display Sensor Data on Serial Monitor
    Serial.println("--------------------------------------------------");
    Serial.printf("[MAX30102] HR: %.1f bpm | SpO2: %.1f %%\n", avgBPM, avgSpO2);
    Serial.printf("[LM35] Temp: %.2f °C\n", lm35Temp);
    Serial.printf("[ECG] Value: %d\n", ecgValue);
    Serial.printf("[MPU6050] Accel (m/s²): %.2f, %.2f, %.2f | Gyro (rad/s): %.2f, %.2f, %.2f | Temp: %.1f °C\n",
                  ax, ay, az, g.gyro.x, g.gyro.y, g.gyro.z, tempMPU_val);

    // Transmit Sensor Data to ThingSpeak Cloud
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      String url = String(THINGSPEAK_SERVER) + "?api_key=" + String(THINGSPEAK_API_KEY) +
                   "&field1=" + String(avgBPM, 1) +
                   "&field2=" + String(avgSpO2, 1) +
                   "&field3=" + String(lm35Temp, 2) +
                   "&field4=" + String(ecgValue) +
                   "&field5=" + String(ax, 2) +
                   "&field6=" + String(ay, 2) +
                   "&field7=" + String(az, 2) +
                   "&field8=" + String(tempMPU_val, 2);

      http.begin(url);
      int httpResponseCode = http.GET();
      if (httpResponseCode > 0) {
        Serial.printf(" Data sent to ThingSpeak. Response: %d\n", httpResponseCode);
      } else {
        Serial.printf(" Error sending data: %d\n", httpResponseCode);
      }
      http.end();
    } else {
      Serial.println("[ERROR] Wi-Fi disconnected!");
    }
  }
}
