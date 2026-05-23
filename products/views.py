from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Product, Category
from .forms import ProductForm, ProductImageFormSet


def product_list(request):
    products   = Product.objects.filter(status='active').prefetch_related('images')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    context = {
        'products'   : products,
        'categories' : categories,
        'query'      : query,
    }
    return render(request, 'list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='active')
    images  = product.images.all()
    context = {
        'product' : product,
        'images'  : images,
    }
    return render(request, 'detail.html', context)


@staff_member_required(login_url='/accounts/login/')
def product_add(request):
    if request.method == 'POST':
        form     = ProductForm(request.POST, request.FILES)
        formset  = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product      = form.save(commit=False)
            product.slug = slugify(product.name)
            product.save()

            formset.instance = product
            formset.save()

            messages.success(request, f'"{product.name}" has been added successfully!')
            return redirect('products:detail', slug=product.slug)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form    = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'add.html', {
        'form'    : form,
        'formset' : formset,
    })


@staff_member_required(login_url='/accounts/login/')
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form    = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            product      = form.save(commit=False)
            product.slug = slugify(product.name)
            product.save()

            formset.instance = product
            formset.save()

            messages.success(request, f'"{product.name}" updated successfully!')
            return redirect('products:detail', slug=product.slug)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form    = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'edit.html', {
        'form'    : form,
        'formset' : formset,
        'product' : product,
    })


@staff_member_required(login_url='/accounts/login/')
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('products:list')
    return render(request, 'delete_confirm.html', {'product': product})