# favorites/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.FavoriteListView.as_view(), name='favorite_list'),
    path('add/<int:product_id>/', views.AddToFavoriteView.as_view(), name='add_to_favorites'),
    path('remove/<int:favorite_id>/', views.RemoveFromFavoriteView.as_view(), name='remove_from_favorites'),
]
