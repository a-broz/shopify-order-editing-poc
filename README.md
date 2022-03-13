# shopify-order-editing-poc
POC Python based Middleware to break out bundle components post order placement via the Shopify order editing API.

The webserver uses multi-threading for asynchronicity 

Before installing, make sure that you have `pip3` and `python3` PATH vars setup, and have the ngrok executable handy

<h2>Installation steps:</h2>

1. clone the project 
2. run `./bundlesapp.sh setup`
3. configure the `example_config.yaml` file with the bundle and API setup  and rename to `config.yaml`
4. run `./bundlesapp.sh configure_bundle`
5. start ngrok server pointing to 8080 via `ngrok http 8080` and retrieve the ngrok endpoint url, e.g. <i>'bfd4-151-231-84-15.ngrok.io'</i>
6. run `./bundlesapp.sh create_webhook <ngrok>` using the ngrok endpoint created in previous step
7. run `./bundlesapp.sh start_server` to begin listening for incoming orders.
8. Place an order with the product configured in the config.yaml file and watch it split!

NOTE: If lost, run `./bundlesapp.sh help` for options

```-------COMMAND MENU-------

- 'setup' - install virtual python environment
- 'configure_bundle' - configure bundle metafield to parent product based on config.py
- 'delete_bundle' - delete metafields from the parent product.
- 'create_webhook <endpoint>' - create orders webhook to point at given endpoint.
- 'start_server' - starts the server to listen for webhooks.
```