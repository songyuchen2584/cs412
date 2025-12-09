from django.contrib import admin

# Register your models here.
from .models import Account, Product, Favorite, Bid, Order, ProductImage

admin.site.register(Product)
admin.site.register(Account)
admin.site.register(Favorite)
admin.site.register(Bid)
admin.site.register(Order)
admin.site.register(ProductImage)
