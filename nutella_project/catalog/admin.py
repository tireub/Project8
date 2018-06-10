from django.contrib import admin

from .models import Product, Research, Contact, Category


# Register your models here.



class CategoryProductInline(admin.TabularInline):
    model = Category.products.through
    extra = 1
    verbose_name = "Catégorie"
    verbose_name_plural = "Catégories"

class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1
    verbose_name = "Produit"
    verbose_name_plural = "Produits"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name", "id"]
    inlines = [CategoryProductInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name", "id"]
    inlines = [ProductCategoryInline]

