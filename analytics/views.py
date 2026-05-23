from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderItem
from products.models import Product
from .models import DailySales, ProductPerformance


@staff_member_required(login_url='/accounts/login/')
def overview(request):

    today     = timezone.now().date()
    last_7    = today - timedelta(days=7)
    last_30   = today - timedelta(days=30)

    # --- Summary cards ---
    total_revenue  = Order.objects.exclude(
        status__in=['cancelled', 'refunded']
    ).aggregate(t=Sum('total'))['t'] or 0

    revenue_today  = Order.objects.filter(
        created_at__date=today
    ).exclude(status__in=['cancelled','refunded']
    ).aggregate(t=Sum('total'))['t'] or 0

    revenue_7days  = Order.objects.filter(
        created_at__date__gte=last_7
    ).exclude(status__in=['cancelled','refunded']
    ).aggregate(t=Sum('total'))['t'] or 0

    total_orders   = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_products = Product.objects.filter(status='active').count()
    low_stock      = Product.objects.filter(status='active', stock__lte=5).count()

    # --- Orders by channel ---
    channel_stats = Order.objects.exclude(
        status__in=['cancelled', 'refunded']
    ).values('channel').annotate(
        revenue = Sum('total'),
        count   = Count('id'),
    ).order_by('-revenue')

    # --- Orders by status ---
    status_stats = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    # --- Recent orders ---
    recent_orders = Order.objects.select_related().prefetch_related(
        'items'
    ).order_by('-created_at')[:8]

    # --- Top products ---
    top_products = OrderItem.objects.values(
        'product__name',
        'product__slug',
    ).annotate(
        units_sold = Sum('quantity'),
        revenue    = Sum('price'),
    ).order_by('-units_sold')[:5]

    # --- Daily revenue last 30 days (for chart) ---
    daily_data = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        rev = Order.objects.filter(
            created_at__date=day
        ).exclude(
            status__in=['cancelled', 'refunded']
        ).aggregate(t=Sum('total'))['t'] or 0
        daily_data.append({
            'date'    : day.strftime('%d %b'),
            'revenue' : float(rev),
        })

    context = {
        'total_revenue'  : total_revenue,
        'revenue_today'  : revenue_today,
        'revenue_7days'  : revenue_7days,
        'total_orders'   : total_orders,
        'pending_orders' : pending_orders,
        'total_products' : total_products,
        'low_stock'      : low_stock,
        'channel_stats'  : channel_stats,
        'status_stats'   : status_stats,
        'recent_orders'  : recent_orders,
        'top_products'   : top_products,
        'daily_data'     : daily_data,
    }
    return render(request, 'overview.html', context)