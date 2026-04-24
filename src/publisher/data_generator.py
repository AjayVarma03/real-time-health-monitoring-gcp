import random
from datetime import datetime

def generate_patient_data():
    return {
        "patient_id":               f"P{random.randint(1, 5)}",
        "timestamp":                datetime.utcnow().isoformat() + "Z",

        "heart_rate":               random.randint(60, 105),   # normal: 60-100
        "blood_pressure_systolic":  random.randint(100, 145),  # normal: 90-120
        "blood_pressure_diastolic": random.randint(60, 90),    # normal: 60-80
        "oxygen_saturation":        random.randint(93, 100),   # normal: 95-100
        "respiratory_rate":         random.randint(12, 22),    # normal: 12-20
        "body_temperature":         round(random.uniform(36.1, 38.2), 1),  # normal: 36.1-37.2

        "device_id":    f"D{random.randint(1, 3)}",
        "hospital_id":  f"H{random.randint(1, 2)}",
        "room_number":  f"R{random.randint(1, 20)}",
        "bed_number":   f"B{random.randint(1, 5)}",
    }