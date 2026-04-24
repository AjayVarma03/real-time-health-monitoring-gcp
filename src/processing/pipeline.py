"""
src/processing/pipeline.py

HOW TO RUN:
-----------
Local (DirectRunner):
    python -m src.processing.pipeline

Production (Dataflow):
    python -m src.processing.pipeline --runner=DataflowRunner \
        --temp_location=gs://southern-engine-493410-b9-dataflow/temp \
        --staging_location=gs://southern-engine-493410-b9-dataflow/staging \
        --region=us-central1 \
        --job_name=patient-health-pipeline \
        --project=southern-engine-493410-b9
"""

import json
import logging
import sys
from datetime import datetime

import apache_beam as beam
from apache_beam.options.pipeline_options import (
    PipelineOptions,
    StandardOptions,
    GoogleCloudOptions,
    SetupOptions,
)

from src.monitoring.alerting import check_alerts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)

# ── Constants ─────────────────────────────────────────────────────────────────
PROJECT_ID   = "southern-engine-493410-b9"
SUBSCRIPTION = f"projects/{PROJECT_ID}/subscriptions/patient-sub"
BQ_TABLE     = f"{PROJECT_ID}:patient_data.patient_stream"

BQ_SCHEMA = {
    "fields": [
        {"name": "patient_id",               "type": "STRING",    "mode": "NULLABLE"},
        {"name": "timestamp",                "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "heart_rate",               "type": "INTEGER",   "mode": "NULLABLE"},
        {"name": "blood_pressure_systolic",  "type": "INTEGER",   "mode": "NULLABLE"},
        {"name": "blood_pressure_diastolic", "type": "INTEGER",   "mode": "NULLABLE"},
        {"name": "oxygen_saturation",        "type": "INTEGER",   "mode": "NULLABLE"},
        {"name": "respiratory_rate",         "type": "INTEGER",   "mode": "NULLABLE"},
        {"name": "body_temperature",         "type": "FLOAT",     "mode": "NULLABLE"},
        {"name": "device_id",                "type": "STRING",    "mode": "NULLABLE"},
        {"name": "hospital_id",              "type": "STRING",    "mode": "NULLABLE"},
        {"name": "room_number",              "type": "STRING",    "mode": "NULLABLE"},
        {"name": "bed_number",               "type": "STRING",    "mode": "NULLABLE"},
        {"name": "alerts",                   "type": "STRING",    "mode": "NULLABLE"},
        {"name": "status",                   "type": "STRING",    "mode": "NULLABLE"},
    ]
}


# ── Transform functions ───────────────────────────────────────────────────────

def parse_message(message: bytes):
    try:
        return json.loads(message.decode("utf-8"))
    except Exception as e:
        logging.error(f"Parse error: {e}")
        return None


def process_row(row: dict) -> dict:
    alerts = check_alerts(row)
    row["alerts"] = ",".join(alerts)
    row["timestamp"] = (
        datetime.fromisoformat(row["timestamp"].replace("Z", ""))
        .isoformat() + "Z"
    )
    row["status"] = "CRITICAL" if alerts else "NORMAL"
    logging.info(
        f"patient={row['patient_id']}  "
        f"status={row['status']}  "
        f"alerts={row['alerts'] or 'none'}"
    )
    return row


# ── Pipeline ──────────────────────────────────────────────────────────────────

def run():
    # Read runner from command-line args (default = DirectRunner)
    options = PipelineOptions(sys.argv[1:])
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(StandardOptions).streaming = True

    runner = options.view_as(StandardOptions).runner or "DirectRunner"
    logging.info(f"Starting pipeline | runner={runner} | subscription={SUBSCRIPTION}")

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read PubSub"      >> beam.io.ReadFromPubSub(subscription=SUBSCRIPTION)
            | "Parse JSON"       >> beam.Map(parse_message)
            | "Filter None"      >> beam.Filter(lambda x: x is not None)
            | "Process Row"      >> beam.Map(process_row)
            | "Write BigQuery"   >> beam.io.WriteToBigQuery(
                                       table=BQ_TABLE,
                                       schema=BQ_SCHEMA,
                                       write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                                       create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                                   )
        )


if __name__ == "__main__":
    run()