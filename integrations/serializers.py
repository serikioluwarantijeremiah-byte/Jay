def build_amazon_payload(product, store):
    """Format product data for Amazon SP-API"""
    markup  = float(store.markup_percent or 0)
    price   = float(product.price) * (1 + markup / 100)

    return {
        'sku'          : product.sku,
        'product_type' : 'PRODUCT',
        'attributes'   : {
            'item_name'       : [{'value': product.name, 'language_tag': 'en_GB'}],
            'product_description': [{'value': product.description, 'language_tag': 'en_GB'}],
            'list_price'      : [{'value': round(price, 2), 'currency': 'GBP'}],
            'fulfillment_availability': [{
                'fulfillment_channel_code': 'DEFAULT',
                'quantity': product.stock,
            }],
        }
    }


def build_ebay_payload(product, store):
    """Format product data for eBay Inventory API"""
    markup = float(store.markup_percent or 0)
    price  = float(product.price) * (1 + markup / 100)

    return {
        'sku'      : product.sku,
        'locale'   : 'en_GB',
        'product'  : {
            'title'      : product.name,
            'description': product.description,
            'imageUrls'  : [product.image.url] if product.image else [],
        },
        'condition'       : 'NEW',
        'availability'    : {
            'shipToLocationAvailability': {'quantity': product.stock}
        },
        'price'           : {
            'value'   : str(round(price, 2)),
            'currency': 'GBP',
        },
    }


def build_etsy_payload(product, store):
    """Format product data for Etsy Open API"""
    markup = float(store.markup_percent or 0)
    price  = float(product.price) * (1 + markup / 100)

    return {
        'title'        : product.name,
        'description'  : product.description,
        'price'        : round(price, 2),
        'quantity'     : product.stock,
        'who_made'     : 'i_did',
        'when_made'    : 'made_to_order',
        'is_supply'    : False,
        'currency_code': 'GBP',
    }