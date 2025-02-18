from django.contrib import admin

from .models import Category, Product, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug')
    ordering = ('id',)
    empty_value_display = '-пусто-'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category', 'slug', 'image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug', 'parent_category__name')
    ordering = ('parent_category', 'id')
    empty_value_display = '-пусто-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'parent_subcategory', 'image_small')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'parent_subcategory__name',
                     'parent_subcategory__parent_category__name')
    ordering = ('parent_subcategory', 'id')
    empty_value_display = '-пусто-'
