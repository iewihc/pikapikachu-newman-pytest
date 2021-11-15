import time
import uuid

import pika
from rich.console import Console
from rich.table import Table


class QueueClient(object):
    def __init__(self):
        # Queue 連線設定檔
        self.host = 'localhost'

        # Queue Remote 遠程設定
        if self.host != 'localhost':
            self.credit = pika.PlainCredentials(username='', password='')
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='', credentials=self.credit))
        else:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host))

        self._queueName = '[Order] Calculate Order Discount'
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def beautiful_mq_output(self, outputStr):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("QueueName Name", style="dim")
        table.add_column("Test Name")
        table.add_column("Test Result")
        table.add_row(f"{outputStr[0]}", f"{outputStr[1]}", f"{outputStr[2]}")
        console.print(table)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body, queueName='', executeAlias='', isDebug=False):
        if queueName != '':
            self._queueName = queueName
        self.response = None
        self.corr_id = str(uuid.uuid4())
        if isDebug:
            self.beautiful_mq_output([self._queueName, executeAlias, body])
        self.channel.basic_publish(
            exchange='',
            routing_key=self._queueName,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(body))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)

    # 心跳檢查
    def heartbeats(self):
        while True:
            connect_close = self.connection.is_closed
            connect_open = self.connection.is_open
            channel_close = self.channel.is_closed
            channel_open = self.channel.is_open

            print("connection is_closed ", connect_close)
            print("connection is_open ", connect_open)
            print("channel is_closed ", channel_close)
            print("channel is_open ", channel_open)
            print("")
            time.sleep(5)
