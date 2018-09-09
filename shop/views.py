from django.shortcuts import render
from .form import RegisterForm, EditForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.forms import SetPasswordForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form,})

def User_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    print(username)
    print(password)
    print(user)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/personal/')
    else:
        return render(request,'login.html')

def User_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def personal(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = EditForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
    else:
        form = EditForm(instance=instance)
    return render(request, 'personal.html',
        {
            'account': request.user.username,
            'form':form
        })

def reset_password(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    form = SetPasswordForm(user=request.user)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/logout/')
    return render(request, 'reset.html',{ 'form':form })

def home(request):
    return render(request,'home.html')