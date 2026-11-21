from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import product, Variation
from category.models import category


def _apply_filters(request, products):
    sizes = [s.lower() for s in request.GET.getlist('size')]
    colors = [c.lower() for c in request.GET.getlist('color')]
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')

    if sizes:
        size_q = Q()
        for s in sizes:
            size_q |= Q(variation__variation_value__iexact=s)
        products = products.filter(
            size_q,
            variation__variation_category='size',
            variation__is_active=True,
        )

    if colors:
        color_q = Q()
        for c in colors:
            color_q |= Q(variation__variation_value__iexact=c)
        products = products.filter(
            color_q,
            variation__variation_category='color',
            variation__is_active=True,
        )

    if min_price.isdigit():
        products = products.filter(price__gte=int(min_price))
    if max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_date')
    else:
        products = products.order_by('id')

    return products.distinct()


def _filter_context(request):
    variations = Variation.objects.filter(is_active=True)
    sizes = sorted({v.strip().lower() for v in
                    variations.filter(variation_category='size').values_list('variation_value', flat=True)})
    colors = sorted({v.strip().lower() for v in
                     variations.filter(variation_category='color').values_list('variation_value', flat=True)})

    params = request.GET.copy()
    params.pop('page', None)

    return {
        'size_options': sizes,
        'color_options': colors,
        'selected_sizes': [s.lower() for s in request.GET.getlist('size')],
        'selected_colors': [c.lower() for c in request.GET.getlist('color')],
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'sort': request.GET.get('sort', ''),
        'keyword': request.GET.get('keyword', ''),
        'query_string': params.urlencode(),
    }


def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(category, slug=category_slug)
        products = product.objects.filter(category=categories, is_available=True)
    else:
        products = product.objects.filter(is_available=True)

    products = _apply_filters(request, products)
    paged_product = Paginator(products, 6).get_page(request.GET.get('page'))

    context = {
        'products': paged_product,
        'product_count': products.count(),
    }
    context.update(_filter_context(request))
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(product, category__slug=category_slug, slug=product_slug)
    context = {
        'single_product': single_product,
        'in_cart': False,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = product.objects.none()
    keyword = request.GET.get('keyword')

    if keyword:
        products = product.objects.filter(
            Q(description__icontains=keyword) | Q(product_name__icontains=keyword),
            is_available=True,
        )
        products = _apply_filters(request, products)

    paged_product = Paginator(products, 6).get_page(request.GET.get('page'))

    context = {
        'products': paged_product,
        'product_count': products.count(),
    }
    context.update(_filter_context(request))
    return render(request, 'store/store.html', context)