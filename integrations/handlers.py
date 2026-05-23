import requests
import logging
from django.utils import timezone
from stores.models import Store, SyncLog
from .models import IntegrationEvent
from .serializers import build_amazon_payload, build_ebay_payload, build_etsy_payload

logger = logging.getLogger(__name__)


def get_payload(product, store):
    """Return correct payload builder per channel"""
    builders = {
        'amazon' : build_amazon_payload,
        'ebay'   : build_ebay_payload,
        'etsy'   : build_etsy_payload,
    }
    builder = builders.get(store.channel)
    if builder:
        return builder(product, store)
    return {}


def push_to_amazon(product, store, event):
    """Push product to Amazon SP-API"""
    try:
        payload  = build_amazon_payload(product, store)
        headers  = {
            'Content-Type'  : 'application/json',
            'x-amz-access-token': store.access_token,
        }
        url      = f'https://sellingpartnerapi-eu.amazon.com/listings/2021-08-01/items/{store.store_id}/{product.sku}'
        response = requests.put(url, json=payload, headers=headers, timeout=15)

        event.payload  = payload
        event.response = response.json()

        if response.status_code in [200, 201]:
            event.status = 'done'
            _log_sync(store, 'product_push', 'success', f'Pushed {product.name}', 1)
        else:
            event.status = 'failed'
            event.error  = str(response.text)
            _log_sync(store, 'product_push', 'failed', response.text, 0)

    except Exception as e:
        event.status = 'failed'
        event.error  = str(e)
        _log_sync(store, 'product_push', 'failed', str(e), 0)
        logger.error(f'Amazon push failed: {e}')

    finally:
        event.save()


def push_to_ebay(product, store, event):
    """Push product to eBay Inventory API"""
    try:
        payload  = build_ebay_payload(product, store)
        headers  = {
            'Content-Type'  : 'application/json',
            'Authorization' : f'Bearer {store.access_token}',
        }
        url      = f'https://api.ebay.com/sell/inventory/v1/inventory_item/{product.sku}'
        response = requests.put(url, json=payload, headers=headers, timeout=15)

        event.payload  = payload
        event.response = response.json() if response.text else {}

        if response.status_code in [200, 204]:
            event.status = 'done'
            _log_sync(store, 'product_push', 'success', f'Pushed {product.name}', 1)
        else:
            event.status = 'failed'
            event.error  = str(response.text)
            _log_sync(store, 'product_push', 'failed', response.text, 0)

    except Exception as e:
        event.status = 'failed'
        event.error  = str(e)
        _log_sync(store, 'product_push', 'failed', str(e), 0)
        logger.error(f'eBay push failed: {e}')

    finally:
        event.save()


def push_to_etsy(product, store, event):
    """Push product to Etsy Open API"""
    try:
        payload  = build_etsy_payload(product, store)
        headers  = {
            'Content-Type'  : 'application/json',
            'x-api-key'     : store.api_key,
            'Authorization' : f'Bearer {store.access_token}',
        }
        shop_id  = store.store_id
        url      = f'https://openapi.etsy.com/v3/application/shops/{shop_id}/listings'
        response = requests.post(url, json=payload, headers=headers, timeout=15)

        event.payload  = payload
        event.response = response.json()

        if response.status_code in [200, 201]:
            event.status = 'done'
            _log_sync(store, 'product_push', 'success', f'Pushed {product.name}', 1)
        else:
            event.status = 'failed'
            event.error  = str(response.text)
            _log_sync(store, 'product_push', 'failed', response.text, 0)

    except Exception as e:
        event.status = 'failed'
        event.error  = str(e)
        _log_sync(store, 'product_push', 'failed', str(e), 0)
        logger.error(f'Etsy push failed: {e}')

    finally:
        event.save()


def sync_product_to_all_channels(product):
    """
    Main function — called when product is saved.
    Pushes to every active store that has auto_sync on.
    """
    stores = Store.objects.filter(status='active', auto_sync=True)

    for store in stores:
        # Check product has sync enabled for this channel
        sync_field = f'sync_{store.channel}'
        if not getattr(product, sync_field, False):
            continue

        # Create event record
        event = IntegrationEvent.objects.create(
            product = product,
            store   = store,
            event   = 'product_created',
            status  = 'processing',
        )

        # Push to correct channel
        if store.channel == 'amazon':
            push_to_amazon(product, store, event)
        elif store.channel == 'ebay':
            push_to_ebay(product, store, event)
        elif store.channel == 'etsy':
            push_to_etsy(product, store, event)

        # Update store last synced
        store.last_synced_at  = timezone.now()
        store.total_listings += 1
        store.save()


def _log_sync(store, action, status, message, items):
    """Helper to write to SyncLog"""
    SyncLog.objects.create(
        store   = store,
        action  = action,
        status  = status,
        message = message,
        items   = items,
    )