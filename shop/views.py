from django.shortcuts import render
from .form import RegisterForm, EditForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Product, ShoppingCar
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
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
        return HttpResponseRedirect('/')
    else:
        return render(request,'login.html',{'error_code':1,})

def User_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


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
    form = SetPasswordForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        #update_session_auth_hash(request, form.user)
        return HttpResponseRedirect('/logout/')
    return render(request, 'reset.html',{ 'form':form })

def home(request):
    if request.user.is_authenticated():
        mode = 1
    else:
        mode = 0
    product_list = Product.objects.all()
    return render(request,'home.html',{'product_list':product_list, 'mode':mode})

def product_detail(request, product_id):
    target = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        count = int(request.POST.get('book_count'))
        if count < 1:
            return render(request,'detail.html',{'product': target, 'remain_code':2})
        else:
            if target.update_remain(count):
                pass
            else:
                return render(request, 'detail.html',{'product': target, 'remain_code':1} )
        user = request.user
        booking = ShoppingCar.objects.create(client=user, product=target, count=count)
        booking.save()
    return render(request, 'detail.html',{'product': target} )

def car(request):
    if not request.user.is_authenticated():
        HttpResponseRedirect('/login/')
    user = request.user
    shopping_list = user.shoppingcar_set.all()
    if request.method == 'POST':
        #print("hello"+str(request.POST.get('booking_id')))
        booking = ShoppingCar.objects.get(pk=request.POST.get('booking_id'))
        booking.product.update_remain(-booking.count)
        booking.delete()
        HttpResponseRedirect('')
    total = user.get_user_total_pay

    ## For paypal from
    pay_check_description = ''
    for item in shopping_list:
        pay_check_description += item.product.product_name
        pay_check_description += '*' + str(item.count) + ', '
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": pay_check_description,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('done')),
        "cancel_return": request.build_absolute_uri(reverse('cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'car.html', {'list':shopping_list,'total':total,'form':form})

    