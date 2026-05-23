from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import IntegrationEvent
from products.models import Product
from stores.models import Store
from .handlers import sync_product_to_all_channels
from django.contrib import messages
from django.shortcuts import redirect


@staff_member_required(login_url='/accounts/login/')
def event_list(request):
    events = IntegrationEvent.objects.select_related(
        'product', 'store'
    ).order_by('-created_at')[:50]

    # Filter by status
    status = request.GET.get('status')
    if status:
        events = events.filter(status=status)

    context = {
        'events'         : events,
        'status_choices' : IntegrationEvent.STATUS_CHOICES,
        'current_status' : status,
    }
    return render(request, 'integrations/events.html', context)


@staff_member_required(login_url='/accounts/login/')
def manual_sync(request, product_id):
    """Manually trigger sync for a product"""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        sync_product_to_all_channels(product)
        messages.success(request, f'"{product.name}" sync triggered for all active channels.')
        return redirect('integrations:events')

    return render(request, 'integrations/manual_sync.html', {'product': product})