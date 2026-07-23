#ifndef CONFIG_H
#define CONFIG_H

// Wi-Fi Credentials
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ThingSpeak API Credentials
const char* THINGSPEAK_SERVER = "http://api.thingspeak.com/update";
const char* THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY";

// Sampling Parameters
const unsigned long DATA_POST_INTERVAL_MS = 1000; // 1 second interval

#endif // CONFIG_H
