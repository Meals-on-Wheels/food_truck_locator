from django.urls import path
# Import all classes from the .views file
from .views import blogListView, blogDetailView, blogCreateView, blogUpdateView, blogDeleteView


urlpatterns = [
    path('', blogListView.as_view(), name='blog_read_list'),
    path('new/', blogCreateView.as_view(), name="blog_create"),
    path('<int:pk>/', blogDetailView.as_view(), name='blog_read_detail'),
    path('<int:pk>/edit', blogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete', blogDeleteView.as_view(), name='blog_delete'),
]
