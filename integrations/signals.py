from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from .handlers import sync_product_to_all_channels


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    """
    Fires every time a product is saved.
    Only syncs if product is active.
    """
    if instance.status == 'active':
        sync_product_to_all_channels(instance)