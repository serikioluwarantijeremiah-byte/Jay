from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Order, ShipmentTracking
from .forms import OrderStatusForm, ShipmentTrackingForm


@staff_member_required(login_url='/accounts/login/')
def order_list(request):
    orders = Order.objects.all().prefetch_related('items')

    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    # Filter by channel
    channel = request.GET.get('channel')
    if channel:
        orders = orders.filter(channel=channel)

    # Search by name or email
    query = request.GET.get('q')
    if query:
        orders = orders.filter(customer_name__icontains=query) | \
                 orders.filter(customer_email__icontains=query)

    context = {
        'orders'          : orders,
        'status_choices'  : Order.STATUS_CHOICES,
        'channel_choices' : Order.CHANNEL_CHOICES,
        'current_status'  : status,
        'current_channel' : channel,
        'query'           : query,
    }
    return render(request, 'list.html', context)


@staff_member_required(login_url='/accounts/login/')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    tracking = getattr(order, 'tracking', None)

    if request.method == 'POST':
        status_form = OrderStatusForm(request.POST, instance=order)
        tracking_form = ShipmentTrackingForm(
            request.POST,
            instance=tracking
        )

        if 'update_status' in request.POST:
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Order status updated.')
                return redirect('orders:detail', pk=pk)

        if 'update_tracking' in request.POST:
            if tracking_form.is_valid():
                t          = tracking_form.save(commit=False)
                t.order    = order
                t.save()
                # Update order status to shipped
                order.status = 'shipped'
                order.save()
                messages.success(request, 'Tracking info saved. Order marked as shipped.')
                return redirect('orders:detail', pk=pk)
    else:
        status_form   = OrderStatusForm(instance=order)
        tracking_form = ShipmentTrackingForm(instance=tracking)

    context = {
        'order'         : order,
        'tracking'      : tracking,
        'status_form'   : status_form,
        'tracking_form' : tracking_form,
    }
    return render(request, 'detail.html', context)