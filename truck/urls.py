from django.urls import path
# Import all classes from the .views file
from .views import test_map_view


urlpatterns = [
    path('', test_map_view, name='test_map_view'),
]
