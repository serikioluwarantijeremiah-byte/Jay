from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Store, SyncLog
from .forms import StoreForm


@staff_member_required(login_url='/accounts/login/')
def store_list(request):
    stores = Store.objects.all().order_by('channel')
    logs   = SyncLog.objects.select_related('store').order_by('-created_at')[:10]

    context = {
        'stores' : stores,
        'logs'   : logs,
    }
    return render(request, 'list.html', context)


@staff_member_required(login_url='/accounts/login/')
def store_add(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store connected successfully!')
            return redirect('stores:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = StoreForm()

    return render(request, 'form.html', {
        'form'  : form,
        'title' : 'Connect New Channel',
    })


@staff_member_required(login_url='/accounts/login/')
def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, f'{store.name} updated successfully!')
            return redirect('stores:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = StoreForm(instance=store)

    return render(request, 'form.html', {
        'form'  : form,
        'title' : f'Edit — {store.name}',
        'store' : store,
    })


@staff_member_required(login_url='/accounts/login/')
def store_delete(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        store.delete()
        messages.success(request, f'{store.name} removed.')
        return redirect('stores:list')
    return render(request, 'delete_confirm.html', {'store': store})


@staff_member_required(login_url='/accounts/login/')
def store_logs(request, pk):
    store = get_object_or_404(Store, pk=pk)
    logs  = store.logs.all()[:50]
    return render(request, 'logs.html', {
        'store' : store,
        'logs'  : logs,
    })