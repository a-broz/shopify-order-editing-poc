from flask import Flask, request, Response
from threading import Thread
from helper.session import start_session
import shopify
import json

app = Flask(__name__)

@app.route('/orders_webhook', methods=['POST'])
def display():
    def process_order(order):
        new_lines = []
        print("starting Thread")
        start_session()
        for i in order["line_items"]:
            product = shopify.Product.find(id_=i["product_id"])
            metafields = product.metafields()
            for x in metafields:
                metafield = x.attributes
                if metafield["key"] == 'bundle_components':
                    print("Identified bundled product order, adding lines")
                    metafield = json.loads(metafield['value'])
                    for z in metafield["children"]:
                        new_lines.append(z)
            print(f"new lines to be added to order: {new_lines}")

        #TODO add order editing code here based off of ID of products to be added stored in new_lines
        #NOTE: this needs to be done by graphql
        """
        mutation beginEdit{
            orderEditBegin(id: "gid://shopify/Order/1234"){
                calculatedOrder{
                id
                }
            }
        }
        """

    thread = Thread(target=process_order, kwargs={'order': request.get_json()})
    thread.start()
    status_code = Response(status=201) 
    print("Incoming order detected, server returning 201 status code")
    return status_code 

app.run('0.0.0.0','8080')
