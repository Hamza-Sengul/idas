# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),                            # Anasayfa
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
