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
    url(r'^profile/(?P<user_id>\d+)/$', views.public_profile_inspect, name='profile_detail'),
    url(r'^users/$', views.show_users, name='users'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^add_closet_item/$', views.add_closet_item, name='add_closet_item'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^delete_from_wishlist/$', views.delete_from_wishlist, name='delete_from_wishlist'),
    url(r'^item_details/$', views.item_details, name='view_item_details'),
    url(r'^item_details/(?P<item_id>\d+)/$', views.item_details, name='view_item_details'),
    url(r'^transaction/cash_only/(?P<item_id>\d+)/$', views.cash_transaction, name='view_item_details'),
    url(r'^transaction/items_only/(?P<item_id>\d+)/$', views.trade_transaction, name='view_item_details'),
    url(r'^transaction/free/(?P<item_id>\d+)/$', views.free_transaction, name='view_item_details'),
    url(r'^edit_closet_item/$', views.edit_closet_item, name='edit_closet_item'),
    url(r'^delete_closet_item/$', views.delete_closet_item, name='delete_closet_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
