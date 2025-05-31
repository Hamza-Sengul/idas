# catalog/context_processors.py

from .models import Category

def menu_categories(request):
    """
    Tüm aktif ana kategorileri (parent=None) ve alt kategorilerini getirir.
    Navbar içinde kullanmak için.
    """
    main_categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by('name')
    # İlgili ana kategorinin children özelliği üzerinden alt kategoriye erişilebilir.
    # Örnek: main_categories[0].children.all()
    return {
        'menu_categories': main_categories
    }

# catalog/context_processors.py

from django.contrib.auth.models import AnonymousUser
from cart.models import Cart, CartItem
from favorites.models import Favorite

def cart_and_favorite_counts(request):
    """
    Eğer kullanıcı girişli ise:
      - cart_count: Sepetteki toplam ürün adedi (CartItem.quantity toplamı)
      - favorite_count: Favori listesinde kaç ürün var
    Aksi halde her iki değer 0 döner.
    """
    user = request.user
    cart_count = 0
    favorite_count = 0

    # AnonymousUser değilse (yani girişli bir kullanıcıysa) sorgulayalım
    if user is not None and not isinstance(user, AnonymousUser):
        # Sepet nesnesini çek, varsa CartItem.quantity toplamı, yoksa 0
        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            cart_count = 0

        # Favoriler tablosundan kayıt sayısını al
        favorite_count = Favorite.objects.filter(user=user).count()

    return {
        'cart_count': cart_count,
        'favorite_count': favorite_count,
    }

