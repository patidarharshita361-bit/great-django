import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from carts.models import Cart, CartItem
from carts.views import _cart_id
from .models import Order, OrderProduct


@login_required(login_url='login')
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    cart_items = CartItem.objects.filter(Cart=cart, is_active=True)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    # stock check
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f'Only {item.product.stock} unit(s) of {item.product.product_name} are available.'
            )
            return redirect('cart')

    # totals
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address_line_1=request.POST['address_line_1'],
            address_line_2=request.POST.get('address_line_2', ''),
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            country=request.POST['country'],
            order_note=request.POST.get('order_note', ''),
            order_total=grand_total,
            tax=tax,
            ip=request.META.get('REMOTE_ADDR', ''),
            is_ordered=True,
        )

        # order number = date + order id
        today = datetime.date.today().strftime('%Y%m%d')
        order.order_number = today + str(order.id)
        order.save()

        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True,
            )
            order_product.variations.set(item.variations.all())

            # reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # empty the cart
        cart_items.delete()

    return redirect(f"{reverse('order_complete')}?order_number={order.order_number}")


@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, user=request.user, is_ordered=True)
    except Order.DoesNotExist:
        return redirect('home')

    ordered_products = OrderProduct.objects.filter(order=order)

    subtotal = 0
    for item in ordered_products:
        subtotal += item.product_price * item.quantity

    context = {
        
        'order': order,
        'ordered_products': ordered_products,
        'subtotal': subtotal,
        'show_thanks': True,
    }
    return render(request, 'orders/order_complete.html', context)
@login_required(login_url='login')
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user, is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order=order)

    subtotal = 0
    for item in ordered_products:
        subtotal += item.product_price * item.quantity

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'subtotal': subtotal,
        'show_thanks': False,
    }
    return render(request, 'orders/order_complete.html', context)