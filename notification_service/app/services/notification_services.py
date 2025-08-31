from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from typing import Dict
import resend
import pika
import os

from app.schemas.schemas import AuditEvent

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

resend.api_key = RESEND_API_KEY


def consume():
    rabbitmq_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    connection_params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        print(f"[x] Received {body.decode()}")
        send_mail(AuditEvent.parse_raw(body))

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=True
    )
    channel.start_consuming()


def send_mail(event: AuditEvent) -> Dict:
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template('activity_notification.html')

    html_content = template.render(
        user=event.user,
        action=event.action,
        model=event.model,
        record_id=event.record_id,
        changes=event.changes or {},
        timestamp=event.timestamp
    )

    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": ["sebastian.faure.l@gmail.com"],
        "subject": f"[Audit] {event.action.upper()} on {event.model} record {event.record_id}",
        "html": html_content,
    }

    email: resend.Email = resend.Emails.send(params)

    return email
