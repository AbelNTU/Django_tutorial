from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.home),
    url(r'^register/',views.register),
    url(r'^login/',views.User_login),
    url(r'^personal/',views.personal),
    url(r'^logout/',views.User_logout),
    url(r'^reset',views.reset_password),
    url(r'^(?P<product_id>[0-9]+)/$',views.product_detail),
    url(r'^car/',views.car),
] 