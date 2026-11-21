from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = ('user', 'product', 'added_date')
    search_fields = ('user__email', 'product__product_name')
    list_filter = ('added_date',)