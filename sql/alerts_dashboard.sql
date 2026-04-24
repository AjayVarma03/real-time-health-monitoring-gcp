
-- 1. Critical patients
SELECT 
  patient_id,
  heart_rate,
  oxygen_saturation,
  alerts,
  status
FROM patient_data.patient_stream
WHERE status = 'CRITICAL';


-- 2. Alert distribution
SELECT 
  alert,
  COUNT(*) AS total
FROM patient_data.patient_stream,
UNNEST(alerts) AS alert
GROUP BY alert;


-- 3. Critical cases over time
SELECT 
  TIMESTAMP_TRUNC(timestamp, MINUTE) AS minute,
  COUNTIF(status = 'CRITICAL') AS critical_cases
FROM patient_data.patient_stream
GROUP BY minute;