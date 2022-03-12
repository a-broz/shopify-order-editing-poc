from flask import request
import yaml
import requests
import sys

if len(sys.argv) == 0:
    print("errore")
    sys.exit("NGROK address not supplied")

with open("config.yaml", "r") as stream:
    try:
        conf = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

conf_shop_url = conf['shop_url']
conf_api_version = conf['api_version']
conf_access_key = conf['access_key']

headers={
    "X-Shopify-Access-Token" : conf_access_key,
    "Content-Type": "application/json"
}
   
data = {
  "webhook": {
    "topic": "orders/create",
    "address": sys.argv[0],
    "format": "json",
    "fields": [
      "id",
      "note"
    ]
  }
}
print(f"Registering webhook to https://{conf_shop_url}/admin/api/2022-01/webhooks.json")

requests.request('POST',f'https://{conf_shop_url}/admin/api/2022-01/webhooks.json',headers=headers, data=data)