# IoT-Based Smart Health Monitoring System with Machine Learning

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-Microcontroller-000000?style=flat&logo=espressif&logoColor=white)
![ThingSpeak](https://img.shields.io/badge/ThingSpeak-Cloud-336699?style=flat&logo=mathworks&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot--Alerts-26A5E4?style=flat&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An end-to-end **IoT-based Smart Health Monitoring System** built with **ESP32**, multi-parameter biomedical sensors, **ThingSpeak Cloud**, and a **Random Forest Machine Learning model** for early anomaly detection and instant **Telegram alerts**.

---

## 📌 Project Highlights

- **Multi-Sensor Data Acquisition**: Real-time continuous monitoring of Heart Rate (BPM), Blood Oxygen Saturation ($\text{SpO}_2$), Electrocardiogram (ECG), Body Temperature, and Accelerometer motion tracking.
- **Cloud Telemetry**: Wireless data transmission to **ThingSpeak Cloud Platform** via Wi-Fi for live graphical visualization and historical data logging.
- **AI-Driven Health Risk Prediction**: Machine Learning classifier (Random Forest trained on multi-parameter biomedical dataset) classifying health status into `Healthy` or `Heart Disease Risk`.
- **Instant Telegram Alerts**: Automated real-time notifications dispatched to caregivers or patients whenever abnormal physiological parameters or high risk are detected.
- **Low-Cost & Scalable**: Designed for affordable preventive healthcare, remote patient tracking, and rural telemedicine accessibility.

---

## 🏗️ System Architecture

```
[ Biomedical Sensors ]
 MAX30102 (HR/SpO2) ──┐
 LM35 (Body Temp)   ──┼──> [ ESP32 MCU ] ──(Wi-Fi HTTP)──> [ ThingSpeak Cloud ]
 AD8232 (ECG)       ──┤                                          │
 MPU6050 (Motion)   ──┘                                     (API Fetch)
                                                                 ▼
                                                        [ Python ML Engine ]
                                                         (Random Forest Model)
                                                                 │
                                                            (If Abnormal)
                                                                 ▼
                                                        [ Telegram Bot Alert ]
```

---

## 📂 Repository Directory Structure

```text
esp32-smart-health-monitor/
├── README.md                           # Main project documentation & setup instructions
├── LICENSE                             # Open-source MIT license
├── .gitignore                          # Excludes secrets, build files, and binaries
├── requirements.txt                    # Python libraries required for ML & cloud bridge
│
├── firmware/                           # ESP32 C++ / Arduino Code
│   ├── esp32_health_monitor.ino        # Main ESP32 sketch for sensor acquisition & cloud POST
│   └── config.example.h                # Template for Wi-Fi & ThingSpeak credentials
│
├── ml_model/                           # Machine Learning Pipeline
│   ├── dataset_generator.py            # Generates synthetic/enhanced health dataset CSV
│   ├── train_model.py                  # Trains Random Forest classifier & outputs model.pkl
│   ├── extended_heart_data.csv         # Enhanced dataset for model training
│   └── model.pkl                       # Serialized trained ML model file
│
├── cloud_bridge/                       # Cloud Analytics & Alerting Service
│   ├── thingspeak_telegram_bridge.py   # Python service running ML inference & sending alerts
│   └── config.example.json             # API keys configuration template
│
└── hardware/                           # Circuit Specifications
    └── pinout_connections.md           # Pin connection guide for ESP32 and sensors
```

---

## ⚡ Hardware Requirements

| Hardware Component | Description |
| :--- | :--- |
| **ESP32 Microcontroller** | Core processing unit with built-in Wi-Fi & Bluetooth |
| **MAX30102 Sensor** | Optical heart rate & pulse oximetry ($\text{SpO}_2$) sensor |
| **LM35 / Digital Temp Sensor** | Precision body temperature sensor |
| **AD8232 Sensor** | Single-lead heart rate monitor / ECG front-end |
| **MPU6050 Sensor** | 6-axis Accelerometer + Gyroscope for motion detection |
| **Breadboard & Jumper Wires** | Circuit prototyping and connections |

For complete pin connection mapping, see [hardware/pinout_connections.md](hardware/pinout_connections.md).

---

## 🚀 Getting Started & Setup Guide

### 1. ESP32 Firmware Setup
1. Open `firmware/esp32_health_monitor.ino` in **Arduino IDE**.
2. Install required libraries via Arduino Library Manager:
   - `Adafruit MPU6050`
   - `SparkFun MAX30105`
3. Copy `firmware/config.example.h` to `firmware/config.h` and configure your credentials:
   ```cpp
   const char* WIFI_SSID = "YOUR_WIFI_NAME";
   const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
   const char* THINGSPEAK_API_KEY = "YOUR_WRITE_API_KEY";
   ```
4. Select board **ESP32 Dev Module** and upload the sketch.

---

### 2. Machine Learning Model Training
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate the dataset and train the model:
   ```bash
   python ml_model/dataset_generator.py
   python ml_model/train_model.py
   ```

---

### 3. Cloud Inference & Telegram Alert Service
1. Copy `cloud_bridge/config.example.json` to `cloud_bridge/config.json`:
   ```json
   {
     "thingspeak": {
       "channel_id": "YOUR_CHANNEL_ID",
       "read_api_key": "YOUR_READ_API_KEY"
     },
     "telegram": {
       "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
       "chat_id": "YOUR_TELEGRAM_CHAT_ID"
     },
     "check_interval_seconds": 5
   }
   ```
2. Run the cloud bridge service:
   ```bash
   python cloud_bridge/thingspeak_telegram_bridge.py
   ```

---

## 📊 Experimental Results

| Metric | Measured Value |
| :--- | :--- |
| **Sensor Data Measurement Accuracy** | $\pm 2\%$ |
| **Machine Learning Model Accuracy** | $95\%$ |
| **End-to-End Real-Time Response Time** | $< 2$ seconds |
| **Telegram Alert Delivery Latency** | $< 5$ seconds |

---

## 🎓 Academic Context

Submitted in partial fulfillment of the requirements for the degree of **Bachelor of Technology (B.Tech) in Information Technology** at **PSG College of Technology**, Coimbatore (Anna University) — November 2025.

**Project Contributors**:
- Arun V (23I309)
- Deepak G T (23I316)
- Pranav A (23I342)
- Arul Prasath V (23I308)
- Karthikeyan KM (23I328)

---

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
