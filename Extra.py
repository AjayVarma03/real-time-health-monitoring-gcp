#removed import section and this from pipeline.py
class ApplyAlerts(beam.DoFn):
    def process(self, record):
        alerts = check_alerts(record)
        record["alerts"] = alerts
        yield record


#old Publish.py






#alerting.py -removed completely
def generate_alerts(row):
    alerts = []

    if row["heart_rate"] > 120:
        alerts.append("HIGH_HEART_RATE")

    if row["oxygen_saturation"] < 90:
        alerts.append("LOW_OXYGEN")

    return alerts



#pipeline.py above check_alerts
def parse_message(message):
    try:
        return json.loads(message.decode("utf-8"))
    except:
        return None
    


pipeline.py
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from src.monitoring.alerting import check_alerts


with open("data/schema.json") as f:
    schema = json.load(f)


def parse_message(message):
    try:
        return json.loads(message.decode("utf-8"))
    except Exception as e:
        print("Parse error:", e)
        return None
    
def process_row(row):
    alerts = check_alerts(row)
    row["alerts"] = alerts
    row["status"] = "NORMAL" if not alerts else "CRITICAL"
    return row



def run():
    project_id = "southern-engine-493410-b9"
    subscription = f"projects/{project_id}/subscriptions/patient-sub"

    options = PipelineOptions(
        streaming=True,
        project=project_id,
        region="us-central1"
    )

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read from PubSub" >> beam.io.ReadFromPubSub(subscription=subscription)
            | "Parse JSON" >> beam.Map(parse_message)
            | "Filter None" >> beam.Filter(lambda x: x is not None)
            | "Process Data" >> beam.Map(process_row)
            | "Debug Print" >> beam.Map(print)
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table="southern-engine-493410-b9:patient_data.patient_stream",
                schema=schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )


if __name__ == "__main__":
    run()






venv\Scripts\activate






with open("data/schema.json") as f:
    schema = json.load(f)