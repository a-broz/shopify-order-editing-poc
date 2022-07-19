from audioop import add
from flask import Flask, request, Response, abort
from threading import Thread
from helper.session import start_session , verify_webhook , read_config
import shopify
import json

app = Flask(__name__)

def process_order(order):
    new_lines = []
    print("starting Thread")
    session, conf = start_session()
    bundles = conf['bundle_products']
    bundle_parent_item_id = ""
    for i in order["line_items"]:
        product = shopify.Product.find(id_=i["product_id"])
        metafields = product.metafields()
        for x in metafields:
            metafield = x.attributes
            if metafield["key"] == 'bundle_components':
                print("Identified bundled product order, adding lines")
                bundle_parent_item_id = i["admin_graphql_api_id"]
                metafield = json.loads(metafield['value'])
                for z in metafield["children"]:
                    new_lines.append(z)
        print(f"new lines to be added to order: {new_lines}")

    #add order editing code here based off of ID of products to be added stored in new_lines
    #NOTE: this needs to be done by graphql
    order_gql_id = order['admin_graphql_api_id']

    #begin order edit
    calculated_order_result = shopify.GraphQL().execute(
        f'''
        mutation beginEdit{{
            orderEditBegin(id: "{order_gql_id}"){{
                calculatedOrder{{
                id
                }}
            }}
        }}
        '''
    )
    calculated_order_result = json.loads(calculated_order_result)
    calculated_order_id = calculated_order_result['data']['orderEditBegin']['calculatedOrder']['id']
    print(f"Opened order edit with ID {calculated_order_id}")
    total_cost = calculated_order_result["extensions"]["cost"]["actualQueryCost"]

    #add children variants to calculated order to GQL
    req = 'mutation batchUpdates ($id: ID!) {'
    for child in bundles['children']:
        req += f'''
            edit{child['id']}: orderEditAddVariant(id: $id, variantId: "gid://shopify/ProductVariant/{child['id']}", quantity: 1){{
                calculatedOrder {{
                    id
                    addedLineItems(first:5) {{
                        edges {{
                        node {{
                            id
                            quantity
                        }}
                        }}
                    }}
                }}
                userErrors {{
                    field
                    message
                }}
            }}
        '''
    
    print(f"Added Child products to open order edit GQL")
    bundle_parent_item_id = bundle_parent_item_id.replace("LineItem","CalculatedLineItem")

    #remove parent from calculated order to GQL
    req += f'''
        orderEditSetQuantity(id: $id, lineItemId: "{bundle_parent_item_id}", quantity: 0 )
        {{
            calculatedOrder {{
            id
            addedLineItems(first: 5) {{
                edges {{
                    node {{
                        id
                        quantity
                    }}
                }}
            }}
            }}
            userErrors {{
            field
            message
            }}
        }}
    '''
    print(f"Added parent product removal from order Edit: {bundle_parent_item_id} in GQL")

    #commit order edits
    req +=f'''
        orderEditCommit(id: $id, notifyCustomer: false, staffNote: "Order edited by Bundles API") {{
            order {{
            id
            }}
            userErrors {{
            field
            message
            }}
        }}
        '''
    
    variables = {'id': calculated_order_id}
    req += '\n}'
    resp = shopify.GraphQL().execute(req,variables=variables)
    total_cost += json.loads(resp)["extensions"]["cost"]["actualQueryCost"]

    print(f'~~~~~Committed order Edit! Completed.~~~~~~')
    print(f'Total Cost: {total_cost}')

def process_order_edit(order):
    print(f'Order Edit Webhook: {order}')

@app.route('/orders_webhook', methods=['POST'])
def process_webhook():
    #First verify that webhook came from Shopify by processing the HMAC
    conf=read_config("config.yaml")
    verified = verify_webhook(request.get_data(),request.headers.get('X-Shopify-Hmac-SHA256'),conf["access_key"])
    if not verified:
        print("bad request detected")
        abort(401)
    
    #If verified, we proceed asynchronously.
    thread = Thread(target=process_order, kwargs={'order': request.get_json()})
    thread.start()
    status_code = Response(status=201) 
    print("Incoming order detected, server returning 201 status code")
    return status_code


@app.route('/orders_edited_webhook', methods=['POST'])
def process_edit_webhook():
    #First verify that webhook came from Shopify by processing the HMAC
    conf=read_config("config.yaml")
    verified = verify_webhook(request.get_data(),request.headers.get('X-Shopify-Hmac-SHA256'),conf["access_key"])
    if not verified:
        print("bad request detected")
        abort(401)
    
    #If verified, we proceed asynchronously.
    thread = Thread(target=process_order_edit, kwargs={'order': request.get_json()})
    thread.start()
    status_code = Response(status=201) 
    print("Order edit detected, server returning 201 status code")
    return status_code


app.run('0.0.0.0','8080')