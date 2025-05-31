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
