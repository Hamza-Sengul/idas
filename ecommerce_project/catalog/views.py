# catalog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product

class HomeView(ListView):
    """
    Anasayfa: Tüm aktif ürünleri (veya karışık  şekilde random çekebiliriz).
    Burada basitçe son eklenen ya da rastgele ürün listeleri gösterelim.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 12  # İsteğe bağlı sayfalama

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('?')  # rastgele sıralama


class CategoryDetailView(ListView):
    """
    Belirli bir kategori (ve varsa alt kategorileri) içinde ürünleri listeler.
    Eğer parent=None ise ana kategorinin alt kategorileri varsa onların ürünleri de listelenebilir.
    Alternatif olarak sadece alt kategori seçildiyse sadece onun ürünlerini listeleyebilirsiniz.
    """
    model = Product
    template_name = 'catalog/category_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        # Eğer ana kategori ise, hem ana kategori hem de alt kategorilerin ürünlerini al:
        if self.category.parent is None:
            sub_cats = self.category.children.filter(is_active=True)
            return Product.objects.filter(
                is_active=True,
                category__in=[self.category] + list(sub_cats)
            )
        else:
            # Alt kategori ise sadece bu alt kategorinin ürünleri:
            return Product.objects.filter(is_active=True, category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    """
    Ürün detay sayfası: Ürünün tüm varyantlarını, resimlerini ve favori/sepet butonlarını göstereceğiz.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Variantlar ve resimler zaten product modelinden erişilebilir.
        return context
