# favorites/views.py

from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product
from .models import Favorite

class FavoriteListView(LoginRequiredMixin, View):
    """
    Kullanıcının favori ürünlerini listeleyen view.
    """
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related('product')
        return render(request, 'favorites/favorite_list.html', {'favorites': favorites})


class AddToFavoriteView(LoginRequiredMixin, View):
    """
    Belirli bir ürünü favoriye ekler.
    """
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        Favorite.objects.get_or_create(user=request.user, product=product)
        return redirect('favorite_list')


class RemoveFromFavoriteView(LoginRequiredMixin, View):
    """
    Favori listesinden kaldırma işlemi.
    """
    def get(self, request, favorite_id):
        fav = get_object_or_404(Favorite, id=favorite_id, user=request.user)
        fav.delete()
        return redirect('favorite_list')
