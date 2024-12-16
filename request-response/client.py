import uuid
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

result = channel.queue_declare(queue="", exclusive=True)
callback_queue = result.method.queue

response = None
correlation_id = None

def callback(ch, method, properties, body):
    global response
    if correlation_id == properties.correlation_id:
        response = body

channel.basic_consume(queue=callback_queue, on_message_callback=callback, auto_ack=True)

correlation_id = str(uuid.uuid4())
channel.basic_publish(exchange="", routing_key="queue-1", properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=correlation_id), body="Hello World?")

while response is None:
    connection.process_data_events()

print(response)
