from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.view_that_asks_for_money),
    url(r'^done/$', views.payment_done
        , name='done'),
    url(r'^cancel/$', views.payment_cancel
        , name='cancel'),
] 