from flask import request
import yaml
import requests
import sys
import json

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

print("looking for existing orders webhooks...")
result = requests.get(url=f'https://{conf_shop_url}/admin/api/2022-01/webhooks.json',headers=headers)
resp = json.loads(result._content)
for i in resp["webhooks"]:
    print(f"webhook with ID {i['id']} found, type 'y' to confirm delete")
    x = input()
    if x.lower() == "y":
        print(f"Deleting webhook {i['id']}")
        result = requests.delete(url=f'https://{conf_shop_url}/admin/api/2022-01/webhooks/{i["id"]}.json',headers=headers)
    else:
        print("skipping deletion")

#Register webhook for orders/create
endpoint = f'https://{sys.argv[1]}/orders_webhook'
body = {
  "webhook": {
    "topic": "orders/create",
    "address": endpoint,
    "format": "json",
    "private_metafield_namespaces": ['uma_bundles']
  }
}
print(f"Registering new orders/create webhook from https://{conf_shop_url}/admin/api/2022-01/webhooks.json to https://{sys.argv[1]}/orders_webhook")

result = requests.post(url=f'https://{conf_shop_url}/admin/api/2022-01/webhooks.json',headers=headers, json=body)
if result.status_code == 201:
    print("webhook creation successful!")
else:
    print(f"error creating webhook. {result.status_code}:{result.reason}")

#Register webhook for orders/edit (Purely to simulate what DOMS would see)
endpoint = f'https://{sys.argv[1]}/orders_edited_webhook'
body = {
  "webhook": {
    "topic": "orders/edited",
    "address": endpoint,
    "format": "json",
    "private_metafield_namespaces": ['uma_bundles']
  }
}
print(f"Registering new orders/edited webhook from https://{conf_shop_url}/admin/api/2022-01/webhooks.json to https://{sys.argv[1]}/orders_edited_webhook")

result = requests.post(url=f'https://{conf_shop_url}/admin/api/2022-01/webhooks.json',headers=headers, json=body)
if result.status_code == 201:
    print("webhook creation successful!")
else:
    print(f"error creating webhook. {result.status_code}:{result.reason}")