from django.shortcuts import render, redirect, get_object_or_404
from store.models import product as Product
from .models import Cart, CartItem, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        request.session.create()

    cart = request.session.session_key
    return cart


# ADD TO CART
def add_cart(request, product_id):
    product_item = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product_item,
                    variation_category__iexact=key.lower(),
                    variation_value__iexact=value,
                    is_active=True
                )
                product_variation.append(variation)

            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    cart.save()

    cart_items = CartItem.objects.filter(
        product=product_item,
        Cart=cart
    )

    cart_item = None

    selected_ids = set(
        item.id for item in product_variation
    )

    for item in cart_items:
        existing_ids = set(
            item.variations.values_list('id', flat=True)
        )

        if existing_ids == selected_ids:
            cart_item = item
            break

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()

    else:
        cart_item = CartItem.objects.create(
            product=product_item,
            quantity=1,
            Cart=cart
        )

        if product_variation:
            cart_item.variations.set(product_variation)

    # AJAX RESPONSE
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        cart_items = CartItem.objects.filter(
            Cart=cart,
            is_active=True
        )

        cart_count = sum(
            item.quantity for item in cart_items
        )

        return JsonResponse({
            'success': True,
            'cart_item_id': cart_item.id,
            'quantity': cart_item.quantity,
            'cart_count': cart_count
        })

    return redirect('cart')


# DECREASE QUANTITY
def remove_cart(request, cart_item_id):
    cart = Cart.objects.get(
        cart_id=_cart_id(request)
    )

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        Cart=cart
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        quantity = cart_item.quantity

    else:
        cart_item.delete()
        quantity = 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        cart_count = sum(
            item.quantity
            for item in CartItem.objects.filter(
                Cart=cart,
                is_active=True
            )
        )

        return JsonResponse({
            'success': True,
            'quantity': quantity,
            'cart_count': cart_count
        })

    return redirect('cart')


# INCREASE QUANTITY
def increment_cart(request, cart_item_id):
    cart = Cart.objects.get(
        cart_id=_cart_id(request)
    )

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        Cart=cart
    )

    cart_item.quantity += 1
    cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        cart_count = sum(
            item.quantity
            for item in CartItem.objects.filter(
                Cart=cart,
                is_active=True
            )
        )

        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'cart_count': cart_count
        })

    return redirect('cart')


# REMOVE COMPLETE PRODUCT
def remove_cart_item(request, cart_item_id):
    cart = Cart.objects.get(
        cart_id=_cart_id(request)
    )

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        Cart=cart
    )

    cart_item.delete()

    return redirect('cart')


# CART PAGE
def cart(request, total=0, quantity=0, cart_items=None):
    cart_items = []

    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )

        cart_items = CartItem.objects.filter(
            Cart=cart,
            is_active=True
        )

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(
        request,
        'store/cart.html',
        context
    )


# CHECKOUT
@login_required(login_url='login')
def checkout(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = []

    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )

        cart_items = CartItem.objects.filter(
            Cart=cart,
            is_active=True
        )

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    if not cart_items:
        messages.error(
            request,
            'Your cart is empty. Please add a product first.'
        )
        return redirect('cart')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(
        request,
        'store/checkout.html',
        context
    )