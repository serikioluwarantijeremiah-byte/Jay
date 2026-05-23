from django.db import models
from products.models import Product


class DailySales(models.Model):
    """Snapshot of sales per day per channel"""

    CHANNEL_CHOICES = [
        ('website', 'Website'),
        ('amazon',  'Amazon'),
        ('ebay',    'eBay'),
        ('etsy',    'Etsy'),
    ]

    date     = models.DateField()
    channel  = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    revenue  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    orders   = models.PositiveIntegerField(default=0)
    units    = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'channel')
        ordering        = ['-date']

    def __str__(self):
        return f'{self.date} — {self.channel} — £{self.revenue}'


class ProductPerformance(models.Model):
    """How each product is performing"""
    product      = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='performance')
    total_sold   = models.PositiveIntegerField(default=0)
    total_revenue= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    view_count   = models.PositiveIntegerField(default=0)
    last_sold_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} — {self.total_sold} sold'