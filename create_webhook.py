from flask import request
import yaml
import requests
import sys

if len(sys.argv) < 2:
    sys.exit("NGROK address not supplied")

with open("config.yaml", "r") as stream:
    try:
        conf = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

conf_shop_url = conf['shop_url']
conf_api_version = conf['api_version']
conf_access_key = conf['secret']

headers={
    "X-Shopify-Access-Token" : conf_access_key,
    "Content-Type": "application/json"
}
   
endpoint = f'https://{sys.argv[1]}'

body = {
  "webhook": {
    "topic": "orders/create",
    "address": endpoint,
    "format": "json",
    "fields": [
      "id",
      "note"
    ]
  }
}
print(f"Registering webhook from https://{conf_shop_url}/admin/api/2022-01/webhooks.json to {sys.argv[0]}")
result = requests.post(url=f'https://{conf_shop_url}/admin/api/2022-01/webhooks.json',headers=headers, json=body)

print(result.reason)
print(result.request.headers)
print(result.request.body)
print(result.request.url)