import requests
import json
import ssl


url = "https//192.168.1.90:8000/client/init"
url2 = "http://192.168.1.90:8000/client/test"
payload = {"aid":"001","gaid":"abc123","operator":"china mobile","is_wifi":True}

payload2 = {"aid": "001"}

API_KEY = '4e6909a09b907d202d46ee1f300bab42'

headers = {
'Content-Type': 'application/json',
'token': API_KEY
}

r = requests.post(url2,data=json.dumps(payload2),headers=headers)
print(r.status_code)
print(r.json())
#
r1 = requests.get(url=url2,params=payload2,headers=headers,verify=False)
print(r1.status_code)
print(r1.json())

# ssl._create_default_https_context = ssl._create_unverified_context
# r2 = requests.post(url=url,data=json.dumps(payload),verify=False)
# print(r2.status_code)
# print(r2.json())