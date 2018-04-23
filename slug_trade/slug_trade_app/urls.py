from django.conf.urls import url
from slug_trade_app import views
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

#template tagging
app_name = 'slug_trade_app'

urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^products/$', views.products, name='products'),
    url(r'^login/$', auth_views.login, {'template_name': 'slug_trade_app/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),

    # url(r'^items/$', views.show_items, name='items'),
    url(r'^users/$', views.show_users, name='users'),

    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),

]
