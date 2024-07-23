from django.contrib import admin

from .models import Supplier, Category, Product, Order, OrderItem, Cart, CartItem, Contact

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Contact)