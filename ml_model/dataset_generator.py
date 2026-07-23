"""
Dataset Generator for Random Forest ML Model
Generates extended synthetic health monitoring dataset (extended_heart_data.csv)
based on project parameters: HR, SpO2, ECG_mean, ECG_std, HRV, Pulse_amp, Accel_mag, Temp, label.
Supports both pandas/numpy and standard Python library fallbacks.
"""

import csv
import math
import random
import os

def generate_dataset(num_samples=1000, random_seed=42):
    random.seed(random_seed)
    
    # Try using pandas/numpy if available and permitted by system policy
    try:
        import pandas as pd
        import numpy as np
        
        np.random.seed(random_seed)
        
        hr = np.clip(np.random.normal(75, 10, num_samples), 50, 120)
        spo2 = np.clip(np.random.normal(95, 3, num_samples), 85, 100)
        ecg_mean = np.clip(np.random.normal(2000, 500, num_samples), 300, 4095)
        ecg_std = np.clip(np.random.normal(100, 50, num_samples), 10, 200)
        hrv = np.clip(np.random.normal(50, 15, num_samples), 20, 120)
        pulse_amp = np.clip(np.random.normal(500, 200, num_samples), 100, 1000)
        
        ax = np.random.normal(0, 0.5, num_samples)
        ay = np.random.normal(0, 0.5, num_samples)
        az = np.random.normal(1, 0.5, num_samples)
        accel_mag = np.sqrt(ax**2 + ay**2 + az**2)
        
        temp = np.clip(np.random.normal(36.5, 0.5, num_samples), 35, 38)
        
        df = pd.DataFrame({
            'HR': hr,
            'SpO2': spo2,
            'ECG_mean': ecg_mean,
            'ECG_std': ecg_std,
            'HRV': hrv,
            'Pulse_amp': pulse_amp,
            'Accel_mag': accel_mag,
            'Temp': temp
        })
        
        def generate_label(row):
            if row['HR'] < 60 or row['HR'] > 100 or row['SpO2'] < 90 or row['ECG_mean'] < 300 or row['ECG_mean'] > 4095 or row['HRV'] < 30 or row['HRV'] > 100:
                return 1
            return 0
            
        df['label'] = df.apply(generate_label, axis=1)
        df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)
        
        os.makedirs("ml_model", exist_ok=True)
        output_filename = "ml_model/extended_heart_data.csv"
        df.to_csv(output_filename, index=False)
        print(f"[OK] Generated {num_samples} samples saved to '{output_filename}' (via Pandas/Numpy)")
        return

    except Exception as e:
        print(f"[INFO] Pandas/Numpy unavailable or blocked by system policy ({e}). Using standard Python generator...")

    # Standard Python Fallback
    rows = []
    header = ['HR', 'SpO2', 'ECG_mean', 'ECG_std', 'HRV', 'Pulse_amp', 'Accel_mag', 'Temp', 'label']
    
    for _ in range(num_samples):
        hr = max(50.0, min(120.0, random.gauss(75.0, 10.0)))
        spo2 = max(85.0, min(100.0, random.gauss(95.0, 3.0)))
        ecg_mean = max(300.0, min(4095.0, random.gauss(2000.0, 500.0)))
        ecg_std = max(10.0, min(200.0, random.gauss(100.0, 50.0)))
        hrv = max(20.0, min(120.0, random.gauss(50.0, 15.0)))
        pulse_amp = max(100.0, min(1000.0, random.gauss(500.0, 200.0)))
        
        ax = random.gauss(0.0, 0.5)
        ay = random.gauss(0.0, 0.5)
        az = random.gauss(1.0, 0.5)
        accel_mag = math.sqrt(ax**2 + ay**2 + az**2)
        
        temp = max(35.0, min(38.0, random.gauss(36.5, 0.5)))
        
        # Label generation
        if hr < 60 or hr > 100 or spo2 < 90 or ecg_mean < 300 or ecg_mean > 4095 or hrv < 30 or hrv > 100:
            label = 1 # Abnormal / Heart Disease Risk
        else:
            label = 0 # Healthy
            
        rows.append([round(hr, 2), round(spo2, 2), round(ecg_mean, 2), round(ecg_std, 2),
                     round(hrv, 2), round(pulse_amp, 2), round(accel_mag, 2), round(temp, 2), label])
                     
    random.shuffle(rows)
    
    os.makedirs("ml_model", exist_ok=True)
    output_filename = "ml_model/extended_heart_data.csv"
    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        
    print(f"[OK] Generated {num_samples} samples saved to '{output_filename}' (via Standard Python)")

if __name__ == "__main__":
    generate_dataset()
