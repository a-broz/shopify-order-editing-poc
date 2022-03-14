# shopify-order-editing-poc
POC flask based middleware to break out bundle components post order placement via the Shopify order editing API.  

Before installing, make sure that:
- You have `pip3` and `python3` PATH setup
- Have the ngrok executable handy (https://ngrok.com/download)
- Have installed a private/custom Shopify app and have the keys ready to go!

<h2>Installation steps:</h2>

1. clone the project 
2. run `./bundlesapp.sh setup`
3. configure the `example_config.yaml` file with the bundle and API setup  and rename to `config.yaml`
4. run `./bundlesapp.sh configure_bundle` . NOTE: If you make a mistake here with the bundle configuration, run `./bundlesapp.sh delete_bundle` to delete the metafields so you can start again.
5. start ngrok server pointing to 8080 via `ngrok http 8080` and retrieve the ngrok endpoint url, e.g. <i>'bfd4-151-231-84-15.ngrok.io'</i> NOTE: the exposed endpoint only processes verified shopify webhooks by calculating a digital signature.
6. run `./bundlesapp.sh create_webhook <ngrok>` using the ngrok endpoint created in previous step
7. run `./bundlesapp.sh start_server` to begin listening for incoming orders.
8. Place an order with the product configured in the config.yaml file and watch it split!

NOTE: If lost, run `./bundlesapp.sh help` for options
```
- 'setup' - install virtual python environment
- 'configure_bundle' - configure bundle metafield to parent product based on config.py
- 'delete_bundle' - delete metafields from the parent product.
- 'create_webhook <endpoint>' - create orders webhook to point at given endpoint.
- 'start_server' - starts the server to listen for webhooks. (make sure ngrok is running first)
```