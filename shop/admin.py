from django.contrib import admin

# Register your models here.
from .models import User, Product
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class newUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'sex','email','phone','is_active','is_staff')
    list_filter = ('username','sex',)

@admin.register(Product)
class newProduct(admin.ModelAdmin):
    list_display = ('product_name', 'product_description', '')
