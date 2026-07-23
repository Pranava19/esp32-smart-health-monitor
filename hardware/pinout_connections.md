# Hardware Pinout & Circuit Connection Guide

## Microcontroller: ESP32 Development Board (38-pin / 30-pin WROOM)

| Sensor Module | Sensor Pin | ESP32 Pin | Communication Type / Notes |
| :--- | :--- | :--- | :--- |
| **MAX30102** (Pulse Oximeter & HR) | VIN | 3.3V | Power (3.3V Supply) |
| | GND | GND | Ground |
| | SDA | GPIO 21 | I2C Data Line |
| | SCL | GPIO 22 | I2C Clock Line |
| **LM35** (Analog Temperature Sensor) | VCC | 5V / 3.3V | Power Supply |
| | GND | GND | Ground |
| | OUT | GPIO 36 (VP) | Analog Input (ADC1_0) |
| **AD8232** (ECG Sensor) | 3.3V | 3.3V | Power Supply |
| | GND | GND | Ground |
| | OUTPUT | GPIO 34 | Analog Input (ADC1_6) |
| | LO+ | GPIO 18 | Digital Lead-Off Output (+) |
| | LO- | GPIO 19 | Digital Lead-Off Output (-) |
| **MPU6050** (Accel + Gyro) | VCC | 3.3V / 5V | Power Supply |
| | GND | GND | Ground |
| | SDA | GPIO 21 | I2C Shared Data Line |
| | SCL | GPIO 22 | I2C Shared Clock Line |

## Circuit Diagram Notes:
- **I2C Bus Shared**: Both **MAX30102** and **MPU6050** share the standard ESP32 I2C pins (`SDA` -> `GPIO 21`, `SCL` -> `GPIO 22`).
- **Analog Readings**: Ensure analog pins used (`GPIO 36`, `GPIO 34`) belong to ADC1 so Wi-Fi does not interfere with ADC conversion.
