import json
import random
import string
import time

from rich.console import Console
from rich.table import Table

from lib.queue_client import QueueClient


class Flow(object):
    def __init__(self):
        self.orderId = ''
        self.userId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4)) + '_bot'
        self.isDebug = False
        self.result = {}

    def generate_seed(self):
        qc = QueueClient()
        return qc.call(body=self.userId,
                       queueName='[Promotion] Generate Seed With Promotion',
                       execute_alias='產生隨機資料',
                       isDebug=self.isDebug)

    def __empty_shopping_cart(self):
        qc = QueueClient()
        qc.call(body=self.userId,
                queueName='[ShoppingCart] Empty Shopping Cart',
                execute_alias='清空購物車',
                isDebug=self.isDebug)

    def __add_shopping_cart(self, data):
        qc = QueueClient()
        for i in data:
            i['userId'] = self.userId
            qc.call(body=json.dumps(i),
                    queueName='[ShoppingCart] Add to Shopping Cart',
                    execute_alias='加入購物車',
                    isDebug=self.isDebug)

    def __checkout_order(self):
        qc = QueueClient()
        order_id = qc.call(
            body=self.userId,
            queueName='[Order] Generate Order Id',
            execute_alias='結帳訂單',
            isDebug=self.isDebug)
        self.orderId = str(order_id.decode())

    def __calc_prom(self):
        qc = QueueClient()
        qc.call(body=self.orderId,
                queueName='[Order] Calculate Order Discount',
                execute_alias='計算販促',
                isDebug=self.isDebug)

    def get_order_details(self):
        qc = QueueClient()
        order = qc.call(body=self.orderId,
                        queueName='[Order] Get Order Details By Id',
                        execute_alias='獲取訂單資料',
                        isDebug=self.isDebug)
        order = order.decode()
        order = json.loads(order)
        # 攤平訂單裡面的販促結構
        param = order['goodsInfo']['goods']
        for item in param:
            promotionId = "" if item['promotions'][0]['promotionId'] is None else item['promotions'][0][
                'promotionId']
            promotionName = "" if item['promotions'][0]['promotionName'] is None else item['promotions'][0][
                'promotionName']
            item['promotionId'] = promotionId
            item['promotionName'] = promotionName

        self.result = order['goodsInfo']
        self.__beautiful_after_order_output(self.result)
        return order['goodsInfo']['goods']

    def __beautiful_before_order_output(self, data):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("GoodsId", style="dim")
        table.add_column("Qty")
        for item in data:
            table.add_row(item['goodsId'], str(item['quantity']))
        print('==================Before')
        console.print(table)

    def __beautiful_after_order_output(self, obj):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("GoodsId", style="dim")
        table.add_column("Qty")
        table.add_column("Amount")
        table.add_column("PromotionId")
        table.add_column("PromotionName")
        for item in obj['goods']:
            table.add_row(
                f"{item['goodsId']}", f"{item['quantity']}", f"{item['amount']}", f"{item['promotionId']}",
                f"{item['promotionName']}"
            )
        print('==================After')
        console.print(table)

    def __empty_all_trash(self, order_id):
        qc = QueueClient()
        qc.call(body=order_id,
                queueName='[Order] Empty Order Related by OrderId',
                execute_alias='清空訂單資料',
                isDebug=self.isDebug)
        self.__empty_shopping_cart()

    def do_work(self, data):
        self.__beautiful_before_order_output(data)
        self.__empty_shopping_cart()
        self.__add_shopping_cart(data)
        self.__checkout_order()
        self.__calc_prom()
        order_data = self.get_order_details()
        self.__empty_all_trash(self.orderId)
        return order_data, self.orderId, self.userId


if __name__ == '__main__':
    # f = Flow()
    # f.do_work([])
    # data = f.generate_seed()
    # print(data.decode())
    pass
