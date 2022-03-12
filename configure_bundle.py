import shopify as shopify
import json 
from helper.session import start_session

session , conf = start_session()
bundles = conf['bundle_products']

#get shopify parent product resource
product = shopify.Product.find(id_=bundles['id'])

#setup bundle json for children
bundle_components = {"children":[]}
for i in bundles["children"]:
    bundle_components["children"].append({"sku":i["sku"] , "price":i["price"]})

bundle_components = {
        'namespace': 'uma_bundles',
        'key': 'bundle_components',
        'value': json.dumps(bundle_components),
        'type': 'json'
}

product.add_metafield(shopify.Metafield(bundle_components))

print(product.metafields()[0].attributes["id"] , product.metafields()[0].attributes["value"])

