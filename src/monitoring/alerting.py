def check_alerts(row):
    alerts = []

    # Heart Rate
    if row["heart_rate"] < 50:
        alerts.append("LOW_HEART_RATE")
    elif row["heart_rate"] > 120:
        alerts.append("HIGH_HEART_RATE")

    # Blood Pressure
    if row["blood_pressure_systolic"] < 90:
        alerts.append("LOW_BP")
    elif row["blood_pressure_systolic"] > 140:
        alerts.append("HIGH_BP")

    # Oxygen
    if row["oxygen_saturation"] < 92:
        alerts.append("LOW_OXYGEN")

    # Temperature
    if row["body_temperature"] < 35:
        alerts.append("LOW_TEMP")
    elif row["body_temperature"] > 38:
        alerts.append("HIGH_TEMP")

    # Respiratory
    if row["respiratory_rate"] < 12:
        alerts.append("LOW_RESP_RATE")
    elif row["respiratory_rate"] > 25:
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
