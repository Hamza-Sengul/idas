# ecommerce_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog import views as catalog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Kullanıcı girişi, çıkışı, kayıt
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password_reset vs.

    # users app (örn: profil)
    path('users/', include('users.urls')),              # users/urls.py içinde tanımlanacak

    # catalog app (kategori, ürün, ana sayfa)
    path('', include('catalog.urls')),                  # Anasayfa ve kategori/ürün sayfaları

    # cart app (sepet işlemleri)
    path('cart/', include('cart.urls')),

    # favorites app (favori işlemleri)
    path('favorites/', include('favorites.urls')),
]

# Geliştirme sırasında medya dosyalarını sunmak için:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
