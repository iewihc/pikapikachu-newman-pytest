import json
import re
import subprocess
from rich.console import Console
from rich.table import Table
import requests
import requests.packages.urllib3
from lib.queue_client import QueueClient

requests.packages.urllib3.disable_warnings()


class PromotionFlow():
    def __init__(self, *args):
        # json collection 原始文件
        self.postman_collection_original_path = './src/EC.postman_collection.json'
        # 修改json文件後保存的路徑
        self.postman_collection_fixed_path = './src/EC.postman_collection1.json'
        # 修改json暫存
        self.dict = {}
        # ec userName
        self.userName = 'wei'
        self.token = ''

    def mq_empty_carts(self):
        response = QueueClient.call(self=QueueClient(), body=self.userName,
                                    queueName='[ShoppingCart] Empty Shopping Cart',
                                    executeAlias='清空購物車')

    def get_json_data(self, tmpl):
        with open(self.postman_collection_original_path, 'rb') as f:
            params = json.load(f)
            params['item'][1]['event'][0]['script']['exec'] = [tmpl]
            # 將修改後的內容保存在dict中
            dict = params
        f.close()
        return dict

    def write_json_data(self, dict):
        with open(self.postman_collection_fixed_path, 'w') as r:
            json.dump(dict, r)
        r.close()

    def execute_newman(self):
        completed = subprocess.Popen(
            ["powershell", "-Command", f' newman run {self.postman_collection_fixed_path} --insecure '],
            shell=True, stdout=subprocess.PIPE)
        stdout, _ = completed.communicate(timeout=30)
        consoleResult = stdout.decode(encoding="utf8")
        regex = r"(?<='訂單編號:', ')\w+"
        matches = re.finditer(regex, consoleResult, re.MULTILINE)

        orderId = ''
        for _, match in enumerate(matches, start=1):
            orderId = match.group()

        return orderId

    def modify_postman_collection(self, data):
        data = f'var arrangedData={data}'
        template = '''

            arrangedData.forEach(function(item, i) {
            var data = { data : item};
            data = JSON.stringify(data);
            pm.sendRequest({
                    url : "https://localhost:5001/Carts",
                    method : "POST",
                    header: {
                        'Authorization': 'bearer ' + pm.globals.get("token"),
                        "Content-Type": "application/json"
                    },
                    body : data
                }, function (err, response) {

                });
            });
        '''
        template = data + template
        # 調用兩個函數，更新JSON內容
        the_revised_dict = self.get_json_data(template)
        self.write_json_data(the_revised_dict)

    def beautiful_after_order_output(self, obj):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("GoodsId", style="dim")
        table.add_column("Qty")
        table.add_column("Amount")
        table.add_column("PromotionId")
        table.add_column("PromotionName")
        for item in obj['goods']:
            # print(item)
            table.add_row(
                f"{item['goodsId']}", f"{item['quantity']}", f"{item['amount']}", f"{item['promotionId']}",
                f"{item['promotionName']}"
            )

        console.print(table)

    def beautiful_before_order_output(self, data):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("GoodsId", style="dim")
        table.add_column("Qty")
        for item in data:
            # print(item)
            table.add_row(item['goodsId'], str(item['quantity']))

        console.print(table)

    def request_api_order_details(self, orderId):
        url = f"https://localhost:5001/Order/{orderId}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        return response.json()

    def request_api_token(self):
        url = f"https://localhost:5001/Auth/sales/login"

        payload = {"data": {"id": "wei", "password": "12345678"}}
        headers = {'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        self.token = response.json()['data']['userToken']

    def do_work(self, data, index=0):
        print('案例', index)
        print('==================Before')
        self.beautiful_before_order_output(data)

        self.request_api_token()
        # 清除購物車
        self.mq_empty_carts()

        self.modify_postman_collection(data)

        # 執行newMan
        orderId = self.execute_newman()

        if orderId != '':
            response = QueueClient.call(self=QueueClient(), body=orderId, queueName='[Order] Calculate Order Discount',
                                        executeAlias='計算販促')

            # 打API呼叫訂單資訊並格式化成好看的結果
            a = self.request_api_order_details(orderId)
            param = a['data']['goodsInfo']['goods']
            for item in param:
                promotionId = "" if item['promotions'][0]['promotionId'] is None else item['promotions'][0][
                    'promotionId']
                promotionName = "" if item['promotions'][0]['promotionName'] is None else item['promotions'][0][
                    'promotionName']
                item['promotionId'] = promotionId
                item['promotionName'] = promotionName
                param = item

            print('==================After')
            self.beautiful_after_order_output(a['data']['goodsInfo'])
            return a['data']['goodsInfo']


class GetCase(PromotionFlow):
    def __init__(self):
        super(GetCase, self).__init__()
        print('滿足Case1,Case2的第N件測試資料')

    @staticmethod
    def get_case1():
        return [
            {"goodsId": "2823563800061 ", "quantity": 5},
            {"goodsId": "2824480000311 ", "quantity": 1},
        ]

    @staticmethod
    def get_case2():
        return [
            {"goodsId": "2823563800061 ", "quantity": 1},
            {"goodsId": "2824480000311 ", "quantity": 1},
        ]

    @staticmethod
    def get_case3():
        return [
            {"goodsId": "2823563800061 ", "quantity": 5},
            {"goodsId": "2824480000311 ", "quantity": 24},
        ]

    @staticmethod
    def get_case4():
        return [
            {"goodsId": "2823563800061 ", "quantity": 6},
            {"goodsId": "2824480000311 ", "quantity": 24},
        ]

    @staticmethod
    def get_case5():
        return [
            {"goodsId": "2823563800061 ", "quantity": 6},
            {"goodsId": "2824480000311 ", "quantity": 23},
        ]

    @staticmethod
    def get_case6():
        return [
            {"goodsId": "2823563800061 ", "quantity": 5},
            {"goodsId": "2824480000311 ", "quantity": 24},
            {"goodsId": "2111108183101 ", "quantity": 1},
        ]


if __name__ == '__main__':
    p = PromotionFlow()
    p.do_work(GetCase.get_case1(), 1)
    p.do_work(GetCase.get_case2(), 2)
    p.do_work(GetCase.get_case3(), 3)
    p.do_work(GetCase.get_case4(), 4)
    p.do_work(GetCase.get_case5(), 5)
    p.do_work(GetCase.get_case6(), 6)
