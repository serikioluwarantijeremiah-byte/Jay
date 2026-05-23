from django.db import models
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
        ('refunded',   'Refunded'),
    ]

    CHANNEL_CHOICES = [
        ('website', 'Website'),
        ('amazon',  'Amazon'),
        ('ebay',    'eBay'),
        ('etsy',    'Etsy'),
    ]

    # Customer info
    customer_name    = models.CharField(max_length=255)
    customer_email   = models.EmailField()
    customer_phone   = models.CharField(max_length=20, blank=True)

    # Shipping address
    address_line1    = models.CharField(max_length=255)
    address_line2    = models.CharField(max_length=255, blank=True)
    city             = models.CharField(max_length=100)
    postcode         = models.CharField(max_length=20)
    country          = models.CharField(max_length=100, default='United Kingdom')

    # Order info
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    channel          = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='website')
    channel_order_id = models.CharField(max_length=255, blank=True)  # Amazon/eBay order ID

    # Financials
    subtotal         = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total            = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Timestamps
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.customer_name} ({self.status})'

    def calculate_total(self):
        self.subtotal = sum(item.line_total() for item in self.items.all())
        self.total    = self.subtotal + self.shipping_cost
        self.save()


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class ShipmentTracking(models.Model):
    order           = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    carrier         = models.CharField(max_length=100)   # e.g. Royal Mail, DHL
    tracking_number = models.CharField(max_length=255)
    tracking_url    = models.URLField(blank=True)
    shipped_at      = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.carrier} — {self.tracking_number}'