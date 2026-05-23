from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    # Core info
    name        = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    sku         = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Media
    image       = models.ImageField(upload_to='products/', blank=True, null=True)

    # Channel sync flags
    sync_amazon = models.BooleanField(default=False)
    sync_ebay   = models.BooleanField(default=False)
    sync_etsy   = models.BooleanField(default=False)

    # Timestamps
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Multiple images per product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='products/gallery/')
    alt     = models.CharField(max_length=150, blank=True)
    order   = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - image {self.order}"


class ChannelListing(models.Model):
    """Tracks where each product is listed and its status on each channel"""

    CHANNEL_CHOICES = [
        ('amazon', 'Amazon'),
        ('ebay', 'eBay'),
        ('etsy', 'Etsy'),
        ('google', 'Google Shopping'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]

    product        = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='listings')
    channel        = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    channel_id     = models.CharField(max_length=255, blank=True)  # ID given by Amazon/eBay etc
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    last_synced_at = models.DateTimeField(null=True, blank=True)
    error_message  = models.TextField(blank=True)

    class Meta:
        unique_together = ('product', 'channel')

    def __str__(self):
        return f"{self.product.name} → {self.channel} ({self.status})"
