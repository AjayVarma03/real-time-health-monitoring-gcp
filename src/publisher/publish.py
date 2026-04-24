import json
import time
from google.cloud import pubsub_v1
from src.publisher.data_generator import generate_patient_data

project_id = "southern-engine-493410-b9"
topic_id = "patient-data-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


while True:
    data = generate_patient_data()

    message = json.dumps(data).encode("utf-8")
    publisher.publish(topic_path, message)

    print("Published:", data)

    time.sleep(2)