from django.forms import ModelForm
#from django.contrib.auth.models import User
from django.db import models
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "密碼"
        self.fields['password2'].label = "密碼確認"
    class Meta:
        model = User
        fields = ('username','password1','password2','name','sex','phone')
        labels = {
            "username": "帳號",
            "name":"姓名",
            "sex":"性別",
            "phone":"手機",
        }

'''
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username','password1')

class EditForm(ModelForm):
    class Meta:
        model = User
        fields = 
'''