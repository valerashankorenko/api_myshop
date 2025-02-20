from django.db.models import Sum
from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CartItem.

    Поля:
    - id: Уникальный идентификатор элемента корзины.
    - product: Сериализованные данные о продукте (только для чтения).
    - product_id: ID продукта, который можно указать при создании/обновлении
    элемента корзины (только для записи).
    - quantity: Количество продукта в корзине.
    - total_price: Общая стоимость элемента корзины
    (количество * цена продукта, только для чтения).
    """

    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField(
        min_value=0,
        max_value=1000,
        default=0
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def validate_quantity(self, value):
        if value < 0 or value > 1000:
            raise serializers.ValidationError(
                "Количество должно быть от 0 до 1000.")
        return value


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Cart.

    Поля:
    - id: Уникальный идентификатор корзины.
    - items: Список элементов корзины
    (сериализованные данные CartItem, только для чтения).
    - total_items: Общее количество товаров в корзине
    (вычисляемое поле, только для чтения).
    - total_price: Общая стоимость всех товаров в корзине
    (вычисляемое поле, только для чтения).
    - user: Имя пользователя.
    """

    items = CartItemSerializer(many=True, read_only=True)
    total_items_cart = serializers.SerializerMethodField()
    total_price_cart = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items_cart', 'total_price_cart']
        read_only_fields = ['id', 'items']

    def get_total_items_cart(self, obj):
        """
        Метод для вычисления общего количества товаров в корзине.

        Аргументы:
        - obj: Экземпляр модели Cart.

        Возвращает:
        - Общее количество товаров в корзине
        (сумма quantity всех элементов корзины).
        """
        return obj.items.aggregate(total=Sum('quantity'))['total'] or 0

    def get_total_price_cart(self, obj):
        """
        Метод для вычисления общей стоимости всех товаров в корзине.

        Аргументы:
        - obj: Экземпляр модели Cart.

        Возвращает:
        - Общая стоимость всех товаров в корзине
        (сумма total_price всех элементов корзины).
        """
        total = sum(item.total_price for item in obj.items.all())
        return total
