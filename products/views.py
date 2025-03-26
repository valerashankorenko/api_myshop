from rest_framework import permissions, viewsets

from products.paginations import CustomPagination

from .models import Category, Product, Subcategory
from .serializers import (CategorySerializer, ProductSerializer,
                          SubcategorySerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для модели Category.

    Поддерживает только чтение (GET-запросы).
    Позволяет получать список всех категорий или одну категорию по её ID.
    """

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.AllowAny,)


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для модели Subcategory.

    Поддерживает только чтение (GET-запросы).
    Позволяет получать список всех подкатегорий или одну подкатегорию по её ID.
    """

    queryset = Subcategory.objects.all().order_by('id')
    serializer_class = SubcategorySerializer
    pagination_class = CustomPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для получения списка продуктов.

    Поддерживает только чтение (GET-запросы).
    Позволяет получать список всех продуктов или один продукт по его ID.
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
