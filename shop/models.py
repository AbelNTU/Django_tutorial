from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.core.validators import RegexValidator
from django.utils.html import format_html
from django.core.validators import MinValueValidator, MaxValueValidator
class User(AbstractUser):
    gender = (
        ("male", '男'),
        ("female", '女')
    )
    phone_reg = RegexValidator(r'^09\d{2}-?\d{3}-?\d{3}$',"Please enter valid Taiwanese phone number.")
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    sex = models.CharField(max_length=10,choices=gender)
    phone = models.CharField(max_length=20, validators=[phone_reg])

    def __str__(self):
        return self.name

    def get_user_total_pay(self):
        total_price = 0
        for item in self.shoppingcar_set.all():
            total_price += item.price()
        return total_price
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    product_price = models.IntegerField(default=0)
    product_image = models.ImageField(null=True, blank=True, upload_to='photos')
    remain_product = models.IntegerField(default=0)
    def __str__(self):
        return self.product_name
    def update_remain(self, number):
        if number > int(self.remain_product):
            return False
        else:
            self.remain_product-=number
            self.save()
            return True
class ShoppingCar(models.Model):
    client = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    count = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    def __str__(self):
        return self.client.name + self.count + "products"
    def price(self):
        return self.product.product_price * self.count        
    
            