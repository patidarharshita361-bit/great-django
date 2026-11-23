import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from carts.models import Cart, CartItem
from carts.views import _cart_id
from .models import Order, OrderProduct

def get_tracking_steps(order):
    statuses = Order.STATUS

    if order.status == 'Cancelled':
        return []

    current_index = [status[0] for status in statuses].index(order.status)

    return [
        {
            'name': label,
            'completed': index < current_index,
            'current': index == current_index,
        }
        for index, (value, label) in enumerate(statuses)
    ]
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
        'tracking_steps': get_tracking_steps(order),
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
        'tracking_steps': get_tracking_steps(order),
    }
    return render(request, 'orders/order_complete.html', context)
@login_required(login_url='login')
def cancel_order(request, order_number):

    if request.method != 'POST':
        return redirect('my_orders')

    with transaction.atomic():

        order = get_object_or_404(
            Order.objects.select_for_update(),
            order_number=order_number,
            user=request.user,
            is_ordered=True
        )

        allowed_statuses = ['New', 'Accepted', 'Processing']

        if order.status not in allowed_statuses:
            messages.error(
                request,
                'Sorry! This order cannot be cancelled at its current stage.'
            )

        else:
            ordered_products = OrderProduct.objects.select_for_update().filter(order=order)

            for item in ordered_products:
                product = item.product
                product.stock += item.quantity
                product.save(update_fields=['stock'])

            order.status = 'Cancelled'
            order.save(update_fields=['status', 'updated_at'])

            messages.success(request, 'Your order has been cancelled successfully.')

    return redirect('order_detail', order_number=order_number)