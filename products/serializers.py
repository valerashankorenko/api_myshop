from rest_framework import serializers

from .models import Category, Product, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Поля:
    - id: Уникальный идентификатор категории.
    - name: Название категории.
    - slug: Уникальный слаг для URL.
    - image: Изображение категории.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subcategory.

    Поля:
    - id: Уникальный идентификатор подкатегории.
    - category: Связанная категория (внешний ключ).
    - name: Название подкатегории.
    - slug: Уникальный слаг для URL.
    - image: Изображение подкатегории.
    """

    class Meta:
        model = Subcategory
        fields = ['id', 'category', 'name', 'slug', 'image']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Поля:
    - id: Уникальный идентификатор продукта.
    - name: Название продукта.
    - slug: Уникальный слаг для URL.
    - category: Название категории продукта (только для чтения).
    - subcategory: Название подкатегории продукта (только для чтения).
    - price: Цена продукта.
    - images: Словарь с URL изображений продукта разных размеров.
    """

    category = serializers.CharField(
        source='category.name', read_only=True)
    subcategory = serializers.CharField(
        source='subcategory.name', read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category',
                  'subcategory', 'price', 'images']

    def get_images(self, obj):
        """
        Метод для получения URL изображений продукта разных размеров.

        Аргументы:
        - obj: Экземпляр модели Product.

        Возвращает:
        - Словарь с URL изображений продукта:
            - small: URL маленького изображения.
            - medium: URL среднего изображения.
            - large: URL большого изображения.
        """
        return {
            'small': obj.image_small.url if obj.image_small else None,
            'medium': obj.image_medium.url if obj.image_medium else None,
            'large': obj.image_large.url if obj.image_large else None,
        }
