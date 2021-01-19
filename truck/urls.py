from django.conf.urls import url
from django.urls import path, re_path

# Import all classes from the .views file
# from .views import test_map_view
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('map/', views.test_map_view, name='test map'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('signed-in/', views.signIn, name="sign in"),
    path('activate_account_sent/', views.activate_account_sent, name='activate_account_sent'),
    path('activate_account_invalid/', views.activate_account_invalid, name='activate_account_invalid'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    #re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #views.activate, name='activate'),
    path('truck-list-view/', views.truck_list_view, name='truck list'),
    path('truck-list-view/truck-single-view/', views.truck_single_view, name="truck single view"),
    path('menu/', views.menu_page_view, name='menu'),
    path('menu/order-details/', views.order_detail_view, name="order details"),
    path('checkout/', views.checkout_view, name="checkout"),
    
]
