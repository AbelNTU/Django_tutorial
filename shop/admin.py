from django.contrib import admin

# Register your models here.
from .models import User, Product
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

@admin.register(User)
class newUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'sex','email','phone','is_active','is_staff')
    list_filter = ('username','sex',)

@admin.register(Product)
class newProduct(admin.ModelAdmin):
    list_display = ('product_name','product_price','product_description','image_view')
    readonly_fields = ('image_view',)
    def image_view(self,obj):
        return u'<img src="%s" height="150"/>' % obj.product_image.url
    image_view.allow_tags = True
