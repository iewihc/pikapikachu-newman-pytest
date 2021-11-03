#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

orderId = str(sys.argv[1])

# 向Queue發布訊息: roting_key是對列的名稱
channel.basic_publish(exchange='',
                      routing_key='[Order] Calculate Order Discount',
                      body=orderId)
                      
print(" ✔️ [Order] Calculate Order Discount")
connection.close()