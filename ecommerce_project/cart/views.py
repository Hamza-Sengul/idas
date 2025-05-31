# cart/views.py

from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import ProductVariant, Product
from .models import Cart, CartItem

class CartView(LoginRequiredMixin, View):
    """
    Kullanıcının sepetini görüntüleyen view. LoginRequiredMixin, giriş yapılmamışsa login sayfasına yönlendirir.
    """
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related('product', 'variant').all()
        total_price = cart.get_total_price()
        return render(request, 'cart/cart.html', {'cart': cart, 'items': items, 'total_price': total_price})


class AddToCartView(LoginRequiredMixin, View):
    """
    Ürün varyantını sepete ekleyen view.
    POST yerine GET de kullanılabilir; örnek URL: /cart/add/5/?qty=2
    """
    def get(self, request, variant_id):
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Aynı varyanttan varsa miktarı güncelle, yoksa yeni satır ekle
        cart_item, created_item = CartItem.objects.get_or_create(
            cart=cart,
            product=variant.product,
            variant=variant
        )
        if not created_item:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('view_cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Sepetten ürün/satırı kaldıran view.
    """
    def get(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('view_cart')


class UpdateCartItemView(LoginRequiredMixin, View):
    """
    Sepetteki ürün miktarını güncelleyen view. 
    POST ile gönderilmesi tavsiye edilir; örn: qty=3
    """
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        return redirect('view_cart')
