# catalog/models.py

from django.db import models
from django.urls import reverse

class Category(models.Model):
    """
    Kategori modelimiz. Her kategorinin isteğe bağlı bir üst kategorisi (parent) olabilir.
    parent=None ise ana kategori, parent dolu ise alt kategoridir.
    """
    name        = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug        = models.SlugField(max_length=120, unique=True, verbose_name="Slug")
    parent      = models.ForeignKey(
        'self', 
        related_name='children', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    is_active   = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Kategori detay sayfası URL'si (isteğe bağlı, ileride kullanabiliriz)
        return reverse('category_detail', args=[self.slug])


class Product(models.Model):
    """
    Ürün modelimiz. Her ürün mutlaka bir ana kategoriye (veya alt kategoriye) ait olacak.
    """
    name            = models.CharField(max_length=200, verbose_name="Ürün Adı")
    slug            = models.SlugField(max_length=220, unique=True, verbose_name="Slug")
    description     = models.TextField(verbose_name="Ürün Açıklaması")
    category        = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_featured_image(self):
        """
        Önce is_featured=True olan resmi, eğer yoksa ilk resmi döndürür. 
        Yoksa None döner.
        """
        featured = self.images.filter(is_featured=True).first()
        if featured:
            return featured
        return self.images.first()

    def get_min_price(self):
        """
        İlgili ürünün fiyat varyantları arasından en düşük fiyatı döndürür.
        """
        variants = self.variants.all()
        if variants.exists():
            return variants.order_by('price').first().price
        return 0

    def get_absolute_url(self):
        """
        Ürün detay sayfası URL’si
        """
        return reverse('product_detail', args=[self.slug])


class ProductVariant(models.Model):
    """
    Her ürünün farklı boyut/özellik/sürüm (örneğin farklı beden, renk, vb.) varyantı olabilir.
    Örnek: Küçük (S), Orta (M), Büyük (L) gibi ve her birinin farklı fiyatı olabilir.
    """
    product         = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_name    = models.CharField(max_length=50, verbose_name="Varyant (Örn: Küçük, Orta, Büyük)")
    price           = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")

    class Meta:
        verbose_name = "Ürün Varyantı"
        verbose_name_plural = "Ürün Varyantları"
        ordering = ['variant_name']

    def __str__(self):
        return f"{self.product.name} - {self.variant_name} ({self.price}₺)"


class ProductImage(models.Model):
    """
    Ürüne ait birden fazla resim yükleyebilmek için ayrı tablo.
    """
    product     = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='product_images/', verbose_name="Ürün Resmi")
    alt_text    = models.CharField(max_length=150, blank=True, verbose_name="Alternatif Metin")
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan Resim (Thumbnail)")

    class Meta:
        verbose_name = "Ürün Resmi"
        verbose_name_plural = "Ürün Resimleri"

    def __str__(self):
        return f"{self.product.name} resmi"

class SliderImage(models.Model):
    image      = models.ImageField(upload_to='slider_images/', verbose_name="Slider Görseli")
    title      = models.CharField(max_length=100, blank=True, verbose_name="Başlık (Opsiyonel)")
    caption    = models.TextField(blank=True, verbose_name="Açıklama (Opsiyonel)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active  = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Slider Görseli"
        verbose_name_plural = "Slider Görselleri"

    def __str__(self):
        # Başlık varsa onu, yoksa ID’yi göster
        return self.title if self.title else f"Slider Görseli #{self.id}"