import json
import re
import subprocess

import pika

json_path = './src/EC.postman_collection.json'
# json原文件
json_path1 = './src/EC.postman_collection1.json'
# 修改json文件後保存的路徑

dict = {}


# 用來存儲數據

def empty_carts(name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key='[ShoppingCart] Empty Shopping Cart',
                          body=name)
    print("🥺 Sent [ShoppingCart] Empty Shopping Cart")
    connection.close()


def get_json_data(json_path, tmpl):
    # 獲取json里面數據

    with open(json_path, 'rb') as f:
        # 定義為只讀模型，並定義名稱為f
        params = json.load(f)
        # 加載json文件中的內容給params
        params['item'][1]['event'][0]['script']['exec'] = [tmpl]
        # 修改內容
        # print("params",params)
        # 打印
        dict = params
    # 將修改後的內容保存在dict中

    f.close()
    # 關閉json讀模式
    print('')

    return dict


# 返回dict字典內容
def write_json_data(dict):
    # 寫入json文件

    with open(json_path1, 'w') as r:
        # 定義為寫模式，名稱定義為r

        json.dump(dict, r)
    # 將dict寫入名稱為r的文件中

    r.close()


# 關閉json寫模式

def execute_newman():
    completed = subprocess.Popen(["powershell", "-Command", f' newman run {json_path1} --insecure '],
                                 shell=True, stdout=subprocess.PIPE)
    stdout, _ = completed.communicate(timeout=20)
    consoleResult = stdout.decode(encoding="utf8")
    regex = r"(?<='訂單編號:', ')\w+"
    matches = re.finditer(regex, consoleResult, re.MULTILINE)

    orderId = ''
    for _, match in enumerate(matches, start=1):
        orderId = match.group()

    print(consoleResult)
    return orderId

def execute_prom(orderId):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 向Queue發布訊息: roting_key是對列的名稱
    channel.basic_publish(exchange='',
                        routing_key='[Order] Calculate Order Discount',
                        body=orderId)
                        
    print(f"🥺 [Order] Calculate Order Discount : {orderId}")
    connection.close()



def doWork(data):
    # 清除購物車
    empty_carts('wei')

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

    # 調用兩個函數，更新內容
    the_revised_dict = get_json_data(json_path, template)
    write_json_data(the_revised_dict)

    # 執行newMan
    orderId = execute_newman()
    if orderId!='':
        execute_prom(orderId)


if __name__ == '__main__':
    doWork([
        {"goodsId": "2839796000161", "quantity": 1},
        {"goodsId": "2839796000211", "quantity": 1},
        {"goodsId": "2839796000041", "quantity": 1},
    ])
