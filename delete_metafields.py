import shopify as shopify
import json 
from helper.session import start_session
session , conf = start_session()
bundles = conf['bundle_products']

#get shopify parent product resource
product = shopify.Product.find(id_=bundles['id'])
for i in product.metafields():
    print(f"deleting {i.id}")
    i.destroy()
