import yaml
import shopify as shopify
import hmac
import base64
import hashlib

def start_session():
    conf=read_config("config.yaml")
    conf_shop_url = conf['shop_url']
    conf_api_version = conf['api_version']
    conf_api_key = conf['api_key']
    conf_secret = conf['secret']
    shopify.Session.setup(api_key=conf_api_key, secret=conf_secret)
    session = shopify.Session(conf_shop_url, conf_api_version, conf_secret)
    shopify.ShopifyResource.activate_session(session)
    return(session , conf)

def read_config(conf_file):
    with open(conf_file, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf

def verify_webhook(data, hmac_header, secret_key):
    digest = hmac.new(secret_key.encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)

    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))