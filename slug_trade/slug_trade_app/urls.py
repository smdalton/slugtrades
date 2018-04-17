from django.conf.urls import url
from . import views

#template tagging
app_name = 'slug_trade_app'

urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^products/$', views.products, name='products'),
    url(r'^profile/$', views.profile, name='profile')
]
