def check_alerts(record):
    alerts = []

    # Heart Rate
    if record["heart_rate"] < 50:
        alerts.append("LOW_HEART_RATE")
    elif record["heart_rate"] > 120:
        alerts.append("HIGH_HEART_RATE")

    # Blood Pressure
    if record["blood_pressure_systolic"] < 90:
        alerts.append("LOW_BP")
    elif record["blood_pressure_systolic"] > 140:
        alerts.append("HIGH_BP")

    # Oxygen
    if record["oxygen_saturation"] < 92:
        alerts.append("LOW_OXYGEN")

    # Temperature
    if record["body_temperature"] < 35:
        alerts.append("LOW_TEMP")
    elif record["body_temperature"] > 38:
        alerts.append("HIGH_TEMP")

    # Respiratory
    if record["respiratory_rate"] < 12:
        alerts.append("LOW_RESP_RATE")
    elif record["respiratory_rate"] > 25:
        alerts.append("HIGH_RESP_RATE")

    return alerts




if __name__ == "__main__":
    sample = {
        "heart_rate": 130,
        "blood_pressure_systolic": 150,
        "oxygen_saturation": 90,
        "respiratory_rate": 30,
        "body_temperature": 39
    }

    print(check_alerts(sample))
