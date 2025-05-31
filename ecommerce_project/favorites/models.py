# favorites/models.py

from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()

class Favorite(models.Model):
    """
    Bir kullanıcının favori (wishlist) ürünleri.
    """
    user        = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, related_name='favorited_by', on_delete=models.CASCADE)
    added_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favori Ürün"
        verbose_name_plural = "Favori Ürünler"
        unique_together = ('user', 'product')  # Aynı ürünü bir kullanıcı iki kez favori yapmasın

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
