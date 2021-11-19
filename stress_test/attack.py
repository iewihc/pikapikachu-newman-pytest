import json
import logging
import time

import requests

requests.packages.urllib3.disable_warnings()


class Attack(object):
    def __init__(self, index):
        # self.host = 'https://testecorder.everrich.com.tw/api/'
        self.host = 'https://localhost:5001'
        self.token = ''
        self.index = index

    def go_token(self):
        url = f"{self.host}/Auth/sales/login"
        start = time.process_time()
        payload = {"data": {"id": "wei", "password": "12345678"}}
        # payload = {"data": {"id": "98140rock", "password": "12345678"}}
        headers = {'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        self.token = response.json()['data']['userToken']
        end = time.process_time()
        logging.info("login: 執行時間：%f 秒" % (end - start) + "_" + str(self.index))

    def go_prom(self, orderId):
        url = f"{self.host}{orderId}/discount"
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response.content)

    def go_search_goods(self):
        start = time.process_time()
        url = f"{self.host}/Goods?PageIndex=1&PageSize=50"
        payload = {}
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=json.dumps(payload), verify=False)
        print(response.json())
        end = time.process_time()
        logging.info("search_goods: 執行時間：%f 秒" % (end - start) + "_" + str(self.index))

    def go_auto_complete(self):
        start = time.process_time()
        url = f"https://testecorder.everrich.com.tw/api/Search/autoComplete?keyword=%E9%A6%99"
        payload = {}
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=json.dumps(payload), verify=False)
        print(response.json())
        end = time.process_time()
        logging.info("auto_complete: 執行時間：%f 秒" % (end - start) + "_" + str(self.index))


if __name__ == '__main__':
    logging.basicConfig(filename='example.txt', encoding='utf-8', level=logging.INFO)

    i = 0
    while True:
        a = Attack(i)
        a.go_token()
        a.search_goods()
        a.go_auto_complete()
        print(f"執行第 {i} 次")
        i += 1
