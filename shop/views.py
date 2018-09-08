from django.shortcuts import render
from .form import RegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
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
    if request.method == 'POST':
        print(request.user.username)
        user = User.objects.get(username=request.user.username)
        user.name = request.POST.get('name')
        user.sex = request.POST.get('sex')
        user.phone = request.POST.get('phone')
        user.save()
        return HttpResponseRedirect('/personal/')
    else:
        return render(request, 'personal.html',{'account':request.user.username, 'password':request.user.password,
                                                'name':request.user.name, 'sex':request.user.sex,
                                                'phone':request.user.phone})
    return HttpResponseRedirect('/login/')

def home(request):
    return render(request,'home.html')