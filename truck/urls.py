from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path('activate_account_sent/', views.activate_account_sent, name='activate_account_sent'),
    path('activate_account_invalid/', views.activate_account_invalid, name='activate_account_invalid'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
