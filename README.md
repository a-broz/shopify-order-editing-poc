# shopify-order-editing-poc
POC Middleware type application to break out bundle components post order placement

run `./bundlesapp.sh help` for options

-------COMMAND MENU-------

- 'setup' - install virtual python environment
- 'configure_bundle' - configure bundle metafield to parent product based on config.py
- 'delete_bundle' - delete metafields from the parent product.
- 'create_webhook <endpoint>' - create orders webhook to point at given endpoint.
- 'start_server' - starts the server to listen for webhooks.