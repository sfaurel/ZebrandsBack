from dotenv import load_dotenv
import pika
import os

from app.schemas.schemas import AuditEvent

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")


def emit_crud_event(event: AuditEvent) -> None:
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
