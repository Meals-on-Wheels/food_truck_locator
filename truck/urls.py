from django.conf.urls import url
from django.urls import path, re_path

# Import all classes from the .views file
from .views import test_map_view
from . import views


urlpatterns = [
    path('', test_map_view, name='test_map_view'),
    path('signup/', views.SignUp, name='signup'),
    path('activate_account_sent/', views.activate_account_sent, name='activate_account_sent'),
    path('activate_account_invalid/', views.activate_account_invalid, name='activate_account_invalid'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
    #re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #views.activate, name='activate'),
]
