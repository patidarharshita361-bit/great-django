
from django.shortcuts import render
from store.models import product
from carts.models import Cart, CartItem
from wishlist.models import Wishlist
from category.models import category as Category


def home(request):
    products = product.objects.filter(is_available=True)

    # Get all categories
    categories = Category.objects.all().order_by('category_name')

    cart = None
    session_key = request.session.session_key

    if session_key:
        cart = Cart.objects.filter(
            cart_id=session_key
        ).first()

    # Get logged-in user's wishlist product IDs
    wishlist_product_ids = set()

    if request.user.is_authenticated:
        wishlist_product_ids = set(
            Wishlist.objects.filter(
                user=request.user
            ).values_list('product_id', flat=True)
        )

    for item in products:

        item.has_variations = item.variation_set.filter(
            is_active=True
        ).exists()

        item.cart_item_id = None
        item.cart_quantity = 0

        item.is_wishlisted = item.id in wishlist_product_ids

        if cart and not item.has_variations:

            cart_item = CartItem.objects.filter(
                Cart=cart,
                product=item,
                is_active=True,
                variations__isnull=True
            ).first()

            if cart_item:
                item.cart_item_id = cart_item.id
                item.cart_quantity = cart_item.quantity

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'home.html', context)
