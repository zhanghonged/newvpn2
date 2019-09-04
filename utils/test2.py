import requests
import json
import pymysql
from datetime import datetime
import asyncio

url = "http://192.168.1.90:8000/event/do"

def dateencoder(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')


@asyncio.coroutine
def work(i):
    conn = pymysql.connect(host = "127.0.0.1", user = "root",password = "root",database = "vpn0815",charset = "utf8mb4")
    cursor = conn.cursor()
    sql = "select * from event limit %d, 5000" %i
    print(sql)
    cursor.execute(sql)
    desc = cursor.description
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    data_list = [dict(zip([d[0] for d in desc],row)) for row in data]
    for d in data_list:
        d["parameters"] = {}
        d["parameters"]["country"] = d["country"]
        d["parameters"]["server"] = d["host"]
        d["create_time"] = dateencoder(d["create_time"])
        del d["country"]
        del d["host"]

        res = requests.post(url=url,data=json.dumps(d))
        print(res.status_code)
        print(res.json())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(0, 2580382, 5000):
        tasks.append(work(i))
    loop.run_until_complete(asyncio.wait(tasks))