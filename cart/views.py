from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from products.models import Product

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartView(generics.RetrieveAPIView):
    """
    Представление для получения корзины пользователя.

    Поддерживает только GET-запросы.
    Доступно только для аутентифицированных пользователей.
    """

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Получает корзину текущего пользователя.
        Если корзина не существует, создает её.

        Возвращает:
        - Экземпляр корзины (Cart) для текущего пользователя.
        """
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    """
    Представление для добавления продуктов в корзину.

    Поддерживает только POST-запросы.
    Доступно только для аутентифицированных пользователей.
    """

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Добавляет продукт в корзину пользователя.

        Если продукт уже есть в корзине, увеличивает его количество.
        Если продукта нет в корзине, создает новый элемент корзины.

        Возвращает:
        - Сериализованные данные элемента корзины (CartItem)
        и статус HTTP 200 (если продукт уже был в корзине).
        - Сериализованные данные элемента корзины (CartItem)
        и статус HTTP 201 (если продукт добавлен впервые).
        """
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 0)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound('Продукт не найден')

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += int(quantity)
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=int(quantity))
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateCartItemView(generics.UpdateAPIView):
    """
    Представление для обновления количества продуктов в корзине.

    Поддерживает только PUT/PATCH-запросы.
    Доступно только для аутентифицированных пользователей.
    """

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_object(self):
        """
        Получает элемент корзины (CartItem) по его ID
        и корзине текущего пользователя.

        Возвращает:
        - Экземпляр элемента корзины (CartItem).

        Исключения:
        - NotFound: Если корзина или элемент корзины не найдены.
        """
        try:
            cart = Cart.objects.get(user=self.request.user)
            return CartItem.objects.get(pk=self.kwargs['pk'], cart=cart)
        except Cart.DoesNotExist:
            raise NotFound('Корзина не найдена для этого пользователя.')
        except CartItem.DoesNotExist:
            raise NotFound('Элемент корзины не найден в вашей корзине.')

    def update(self, request, *args, **kwargs):
        """
        Обновляет количество продуктов в элементе корзины.

        Аргументы:
        - quantity: Новое количество продуктов (обязательное поле).

        Возвращает:
        - Сериализованные данные обновленного элемента корзины (CartItem).

        Исключения:
        - HTTP 400: Если количество не указано, не является
        положительным целым числом или не является числом.
        """
        instance = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response(
                {"error": "Поле 'quantity' обязательно."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {"error": "Количество должно быть положительным числом."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"error": "Количество должно быть целым числом."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.quantity = quantity
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RemoveFromCartView(generics.DestroyAPIView):
    """
    Представление для удаления продукта из корзины.

    Поддерживает только DELETE-запросы.
    Доступно только для аутентифицированных пользователей.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_object(self):
        """
        Получает элемент корзины (CartItem) по его ID
        и корзине текущего пользователя.

        Возвращает:
        - Экземпляр элемента корзины (CartItem).

        Исключения:
        - NotFound: Если корзина или элемент корзины не найдены.
        """
        try:
            cart = Cart.objects.get(user=self.request.user)
            return CartItem.objects.get(pk=self.kwargs['pk'], cart=cart)
        except Cart.DoesNotExist:
            raise NotFound('Корзина не найдена для этого пользователя.')
        except CartItem.DoesNotExist:
            raise NotFound('Элемент корзины не найден в вашей корзине.')


class ClearCartView(generics.DestroyAPIView):
    """
    Представление для очистки корзины пользователя.

    Поддерживает только DELETE-запросы.
    Доступно только для аутентифицированных пользователей.
    """

    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет все элементы корзины текущего пользователя.

        Возвращает:
        - Статус HTTP 204 (No Content) при успешной очистке корзины.

        Исключения:
        - NotFound: Если корзина не найдена.
        """
        try:
            cart = Cart.objects.get(user=self.request.user)
            CartItem.objects.filter(cart=cart).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            raise NotFound('Корзина не найдена для этого пользователя.')
