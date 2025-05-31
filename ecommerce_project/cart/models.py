# cart/models.py

from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product, ProductVariant

User = get_user_model()

class Cart(models.Model):
    """
    Bir kullanıcıya ait sepet. Sepetler, kullanıcıya bağlanır.
    """
    user        = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sepet"
        verbose_name_plural = "Sepetler"

    def __str__(self):
        return f"{self.user.username} - Sepet"

    def get_total_price(self):
        """
        Sepetteki tüm ürünlerin toplam fiyatını döndürür.
        """
        total = sum([item.get_item_price() for item in self.items.all()])
        return total


class CartItem(models.Model):
    """
    Sepetteki her bir ürün satırı. Her sepet birden çok CartItem içerir.
    """
    cart            = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant         = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity        = models.PositiveIntegerField(default=1)
    added_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sepet Ürün Kalemi"
        verbose_name_plural = "Sepet Ürün Kalemleri"

    def __str__(self):
        return f"{self.product.name} - {self.variant.variant_name} x {self.quantity}"

    def get_item_price(self):
        """
        Bu satırın toplam fiyatı = birim fiyat * miktar
        """
        return self.variant.price * self.quantity
