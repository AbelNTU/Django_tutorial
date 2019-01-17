from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.core.validators import RegexValidator
from django.utils.html import format_html
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

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    product_price = models.IntegerField(default=0)
    product_image = models.ImageField(null=True, blank=True, upload_to='photos')
    remain_product = models.IntegerField(default=0)
    def __str__(self):
        return self.product_name
    
