import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue="queue-1")

def callback(ch, method, properties, body):
    response = f"Response: {body.decode()}"
    print(f"Received: {body.decode()}; Sending {response}")
    ch.basic_publish(exchange="", routing_key=properties.reply_to, properties=pika.BasicProperties(correlation_id=properties.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

print(' [*] Waiting for queue-1. To exit press CTRL+C')

channel.basic_consume(queue="queue-1", on_message_callback=callback, auto_ack=False)

channel.start_consuming()
