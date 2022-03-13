import yaml
import shopify as shopify

def start_session():
    with open("config.yaml", "r") as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    conf_shop_url = conf['shop_url']
    conf_api_version = conf['api_version']
    conf_api_key = conf['api_key']
    conf_secret =conf['secret']
    shopify.Session.setup(api_key=conf_api_key, secret=conf_secret)
    session = shopify.Session(conf_shop_url, conf_api_version, conf_secret)
    shopify.ShopifyResource.activate_session(session)
    return(session , conf)