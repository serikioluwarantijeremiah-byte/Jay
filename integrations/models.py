from django.db import models
from products.models import Product
from stores.models import Store


class IntegrationEvent(models.Model):

    EVENT_CHOICES = [
        ('product_created', 'Product Created'),
        ('product_updated', 'Product Updated'),
        ('product_deleted', 'Product Deleted'),
        ('stock_changed',   'Stock Changed'),
        ('price_changed',   'Price Changed'),
        ('order_received',  'Order Received'),
    ]

    STATUS_CHOICES = [
        ('queued',     'Queued'),
        ('processing', 'Processing'),
        ('done',       'Done'),
        ('failed',     'Failed'),
        ('retrying',   'Retrying'),
    ]

    product    = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='events', null=True, blank=True)
    store      = models.ForeignKey(Store, on_delete=models.CASCADE,
                                   related_name='events')
    event      = models.CharField(max_length=30, choices=EVENT_CHOICES)
    status     = models.CharField(max_length=15, choices=STATUS_CHOICES,
                                  default='queued')
    payload    = models.JSONField(default=dict)   # data sent to API
    response   = models.JSONField(default=dict)   # response from API
    retries    = models.PositiveIntegerField(default=0)
    error      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.store.channel} — {self.event} — {self.status}'