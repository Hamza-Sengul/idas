# cart/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='view_cart'),
    path('add/<int:variant_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
]
