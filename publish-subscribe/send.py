#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='exchange-1', exchange_type="fanout")

channel.basic_publish(exchange='exchange-1',
                      routing_key='',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
