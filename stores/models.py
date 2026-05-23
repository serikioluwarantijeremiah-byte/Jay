from django.db import models


class Store(models.Model):

    CHANNEL_CHOICES = [
        ('website', 'Website'),
        ('amazon',  'Amazon'),
        ('ebay',    'eBay'),
        ('etsy',    'Etsy'),
        ('google',  'Google Shopping'),
    ]

    STATUS_CHOICES = [
        ('active',      'Active'),
        ('inactive',    'Inactive'),
        ('error',       'Error'),
        ('pending',     'Pending Setup'),
    ]

    # Core info
    name        = models.CharField(max_length=255)
    channel     = models.CharField(max_length=20, choices=CHANNEL_CHOICES, unique=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)

    # API Credentials (stored securely)
    api_key      = models.CharField(max_length=500, blank=True)
    api_secret   = models.CharField(max_length=500, blank=True)
    access_token = models.CharField(max_length=500, blank=True)
    refresh_token= models.CharField(max_length=500, blank=True)
    store_id     = models.CharField(max_length=255, blank=True)  # seller ID / store ID

    # Settings
    auto_sync      = models.BooleanField(default=False)  # auto push products
    sync_inventory = models.BooleanField(default=True)   # sync stock levels
    sync_prices    = models.BooleanField(default=True)   # sync prices
    markup_percent = models.DecimalField(                # price markup for this channel
        max_digits=5, decimal_places=2, default=0
    )

    # Stats
    total_listings = models.PositiveIntegerField(default=0)
    total_orders   = models.PositiveIntegerField(default=0)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.channel})'


class SyncLog(models.Model):

    ACTION_CHOICES = [
        ('product_push',   'Product Push'),
        ('stock_update',   'Stock Update'),
        ('price_update',   'Price Update'),
        ('order_pull',     'Order Pull'),
        ('full_sync',      'Full Sync'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed',  'Failed'),
        ('partial', 'Partial'),
    ]

    store      = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='logs')
    action     = models.CharField(max_length=30, choices=ACTION_CHOICES)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message    = models.TextField(blank=True)
    items      = models.PositiveIntegerField(default=0)  # how many items synced
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.store.channel} — {self.action} — {self.status}'