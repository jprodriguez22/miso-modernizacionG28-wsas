import json
import os
import pika


class AlertasOrdenes:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv("RABBIT_HOST"),
                port=5672,
                virtual_host="/",
                credentials=pika.PlainCredentials(
                    username=os.getenv("RABBIT_USER"), password=os.getenv("RABBIT_PWD")
                ),
            )
        )
        self.queue = os.getenv("RABBIT_QUEUE")
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def send_message(self, message):
        msg = json.dumps(message)
        self.channel.basic_publish(exchange="", routing_key=self.queue, body=msg)
        self.connection.close()
        return {"message": f"Se ha enviado lo siguiente: {msg}"}, 200
