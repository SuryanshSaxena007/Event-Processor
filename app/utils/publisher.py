import pika, json
from app.core.config import RABBITMQ_URL

QUEUE = "vendor_orders"

def publish_event(event: dict):
    params = pika.URLParameters(RABBITMQ_URL)
    with pika.BlockingConnection(params) as conn:
        ch = conn.channel()
        ch.queue_declare(queue=QUEUE, durable=True)
        ch.basic_publish(
            exchange="",
            routing_key=QUEUE,
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2),
        )