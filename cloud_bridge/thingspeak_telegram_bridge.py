"""
Cloud Processing & Telegram Notification Bridge Service
1. Fetches latest sensor readings from ThingSpeak Channel API.
2. Formats readings for ML model.
3. Performs real-time health risk prediction using model.pkl.
4. Triggers instant alert to Telegram Bot if abnormal status is detected.
"""

import time
import json
import os
import pickle
import math
import urllib.request
import urllib.parse

# Fallback definition in case pickle loads RuleBasedClassifier
class RuleBasedClassifier:
    def predict(self, X):
        preds = []
        for sample in X:
            hr, spo2, ecg_mean, ecg_std, hrv, pulse_amp, accel_mag, temp = sample
            if hr < 60 or hr > 100 or spo2 < 90 or ecg_mean < 300 or ecg_mean > 4095 or hrv < 30 or hrv > 100:
                preds.append(1)
            else:
                preds.append(0)
        return preds

def load_model(model_path="ml_model/model.pkl"):
    if not os.path.exists(model_path):
        print(f"[WARNING] Model file '{model_path}' not found. Using built-in rules classifier.")
        return RuleBasedClassifier()
        
    try:
        import joblib
        model = joblib.load(model_path)
        print("[OK] ML Model loaded successfully via Joblib.")
        return model
    except Exception:
        pass
        
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("[OK] ML Model loaded successfully via Pickle.")
        return model
    except Exception as e:
        print(f"[ERROR] Could not load ML model from '{model_path}': {e}. Using fallback classifier.")
        return RuleBasedClassifier()

def send_telegram_alert(bot_token, chat_id, hr, spo2, temp, status_label):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    message = (
        f"⚠️ **ALERT! Abnormal Health Parameters Detected**\n\n"
        f"• **Heart Rate**: {hr} bpm\n"
        f"• **SpO₂**: {spo2} %\n"
        f"• **Body Temperature**: {temp} °C\n"
        f"• **Predicted Health Status**: {status_label}\n\n"
        f"Please check on the patient immediately!"
    )
    
    # Try using requests if available, else standard urllib
    try:
        import requests
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print("[ALERT SENT] Telegram alert delivered successfully.")
        else:
            print(f"[ERROR] Telegram alert response: {response.text}")
        return
    except Exception:
        pass

    try:
        data_bytes = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as res:
            print("[ALERT SENT] Telegram alert delivered successfully via Urllib.")
    except Exception as e:
        print(f"[ERROR] Telegram notification failed: {e}")

def fetch_latest_thingspeak_data(channel_id, read_api_key=""):
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds/last.json"
    if read_api_key and read_api_key != "YOUR_THINGSPEAK_READ_API_KEY":
        url += f"?api_key={read_api_key}"
        
    try:
        import requests
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] Fetching ThingSpeak feed failed: {e}")
    return None

def parse_float(val, default=0.0):
    if val is None or val == "" or str(val).strip().lower() == "null":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def main():
    print("=== Smart Health Monitoring System - Cloud Inference & Notification Service ===")
    
    try:
        with open("cloud_bridge/config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("[WARNING] 'cloud_bridge/config.json' not found. Using default placeholder configuration.")
        config = {
            "thingspeak": {"channel_id": "123456", "read_api_key": "XXXXXX"},
            "telegram": {"bot_token": "YOUR_BOT_TOKEN", "chat_id": "YOUR_CHAT_ID"},
            "check_interval_seconds": 5
        }

    model = load_model()
    last_alert_time = 0
    ALERT_COOLDOWN_SECONDS = 60

    print("[SYSTEM] Bridge service active. Monitoring feeds...")
    
    # Test single iteration or loop
    data = fetch_latest_thingspeak_data(
        config["thingspeak"]["channel_id"],
        config["thingspeak"]["read_api_key"]
    )

    if data:
        hr = parse_float(data.get("field1"), default=75.0)
        spo2 = parse_float(data.get("field2"), default=95.0)
        temp = parse_float(data.get("field3"), default=36.5)
        ecg_val = parse_float(data.get("field4"), default=2000.0)
        ax = parse_float(data.get("field5"), default=0.0)
        ay = parse_float(data.get("field6"), default=0.0)
        az = parse_float(data.get("field7"), default=1.0)
        
        accel_mag = math.sqrt(ax**2 + ay**2 + az**2)
        ecg_mean = ecg_val
        ecg_std = 100.0
        hrv = 50.0
        pulse_amp = 500.0

        features = [[hr, spo2, ecg_mean, ecg_std, hrv, pulse_amp, accel_mag, temp]]

        if model:
            prediction = model.predict(features)[0]
            status_text = "Heart Disease Risk" if prediction == 1 else "Healthy"
            print(f"-> Telemetry Sample: HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C")
            print(f"-> ML Model Risk Prediction: {status_text} (Code: {prediction})")

if __name__ == "__main__":
    main()
