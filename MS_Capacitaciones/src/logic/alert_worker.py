import json
import pika

from os import getenv

class EventLogger:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=getenv("RABBIT_HOST"),
                port=5672,
                virtual_host="/",
                credentials=pika.PlainCredentials(
                    username=getenv("RABBIT_USER"), password=getenv("RABBIT_PWD")
                ),
            )
        )
        self.queue = getenv("RABBIT_QUEUE")
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def send_message(self, message):
        msg = json.dumps(message)
        self.channel.basic_publish(exchange="", routing_key=self.queue, body=msg)
        self.connection.close()
        return {"message": f"Se ha enviado el siguiente mensaje: {msg}"}, 200
