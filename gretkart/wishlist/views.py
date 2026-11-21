from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from store.models import product
from .models import Wishlist


# DISPLAY WISHLIST
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product', 'product__category')

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
    }

    return render(request, 'wishlist/wishlist.html', context)


# ADD OR REMOVE PRODUCT FROM WISHLIST
@login_required
def toggle_wishlist(request, product_id):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        }, status=405)

    product_item = get_object_or_404(
        product,
        id=product_id
    )

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product_item
    ).first()

    if wishlist_item:
        wishlist_item.delete()
        added = False
        message = 'Product removed from your wishlist.'
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product_item
        )
        added = True
        message = 'Product added to your wishlist!'

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    return JsonResponse({
        'success': True,
        'added': added,
        'message': message,
        'wishlist_count': wishlist_count
    })


# REMOVE PRODUCT FROM WISHLIST
@login_required
def remove_from_wishlist(request, product_id):

    if request.method == 'POST':
        Wishlist.objects.filter(
            user=request.user,
            product_id=product_id
        ).delete()

        messages.success(
            request,
            'Product removed from your wishlist.'
        )

    return redirect('wishlist')
