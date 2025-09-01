from datetime import datetime, timezone
from dotenv import load_dotenv
import pika
import os
import json

from app.schemas.schemas import AuditEvent

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")


event = AuditEvent(
    user="admin@example.com",
    action="update",
    timestamp=datetime.now(timezone.utc),
    model="Product",
    record_id="8c3ab99e-df43-4c71-9adf-25bf84d03c8d",
    changes={
        "price": {"old": 10.5, "new": 12.0},
        "brand": {"old": "BrandA", "new": "BrandB"}
    }
)


def test_send_email():

    rabbitmq_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    connection_params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    message = event.model_dump_json()
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=message
    )
    connection.close()
