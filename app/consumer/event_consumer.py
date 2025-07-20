import json, pika, asyncio
from datetime import datetime
from app.db.database import AsyncSessionLocal
from app.db.models import Order
from app.core.config import RABBITMQ_URL

QUEUE = "vendor_orders"
params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    ts = data.get("timestamp")
    if isinstance(ts, str):
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        data["timestamp"] = datetime.fromisoformat(ts)
    async def db_task():
        async with AsyncSessionLocal() as db:
            items = data["items"]
            total = sum(i["qty"] * i["unit_price"] for i in items)
            order = Order(**{
                "id": data["id"],
                "vendor_id": data["vendor_id"],
                "order_id": data["order_id"],
                "items": items,
                "total_amount": total,
                "high_value": total > 500,
                "timestamp": data["timestamp"]
            })
            db.add(order)
            await db.commit()
    asyncio.run(db_task())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)
print("▶️ Consumer up; waiting for messages.")
channel.start_consuming()
