from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from products.models import Category, Product, Subcategory

from .models import Cart, CartItem

User = get_user_model()


class CartTests(APITestCase):
    """
    Набор тестов для функциональности корзины
    в приложении электронной коммерции.
    Включает тесты на добавление, обновление,
    получение и удаление товаров из корзины.
    """

    def setUp(self):
        """
        Настройка тестовой среды: создание пользователя, токена,
        категории, подкатегории, товара и начального элемента корзины.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category = Category.objects.create(
            name='Test Category', slug='test-category')

        self.subcategory = Subcategory.objects.create(
            parent_category=self.category,
            name='Test Subcategory',
            slug='test-subcategory'
        )

        self.image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg")

        self.product_data = {
            'parent_subcategory': self.subcategory,
            'name': 'Test Product',
            'price': 10.00,
            'image_small': self.image,
            'image_medium': self.image,
            'image_large': self.image,
        }

        self.product = Product.objects.create(**self.product_data)

        self.cart = Cart.objects.create(user=self.user)

        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2)

    def tearDown(self):
        """Очистка данных после тестов."""
        self.product.image_small.delete(save=False)
        self.product.image_medium.delete(save=False)
        self.product.image_large.delete(save=False)
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()
        self.cart.delete()
        self.user.delete()
        self.token.delete()

    def test_get_cart(self):
        """
        Тестирование получения корзины.
        Убедитесь, что корзина возвращает правильное количество товаров
        и общую стоимость.
        """
        url = reverse('cart-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Не удалось получить корзину')

        # Проверка структуры ответа
        self.assertIn('items', response.data,
                      'Ключ "items" отсутствует в ответе')
        self.assertIn('total_items_cart', response.data,
                      'Ключ "total_items_cart" отсутствует в ответе')
        self.assertIn('total_price_cart', response.data,
                      'Ключ "total_price_cart" отсутствует в ответе')

        # Проверка данных
        self.assertEqual(len(response.data['items']), 1,
                         'Количество товаров в корзине не совпадает')
        self.assertEqual(response.data['total_items_cart'], 2,
                         'Общее количество товаров в корзине не совпадает')
        self.assertEqual(float(response.data['total_price_cart']), 20.00,
                         'Общая стоимость корзины не совпадает')

    def test_add_to_cart(self):
        """
        Тестирование добавления товара в корзину.
        Убедитесь, что товар добавляется правильно и количество обновляется.
        """
        self.cart_item.delete()

        url = reverse('cart-add')
        data = {'product_id': self.product.id, 'quantity': 3}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'Не удалось добавить товар в корзину')

        # Проверка, что товар добавлен в корзину
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 3,
                         'Количество товара в корзине не совпадает')

        # Проверка общей стоимости корзины
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_price, 30.00,
                         'Общая стоимость корзины не совпадает')

    def test_update_cart_item(self):
        """
        Тестирование обновления элемента корзины.
        Убедитесь, что количество товара обновляется правильно.
        """
        url = reverse('cart-update', kwargs={'pk': self.cart_item.id})
        data = {'quantity': 4}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Не удалось обновить элемент корзины')

        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 4,
                         'Количество товара не обновилось')

        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_price, 40.00,
                         'Общая стоимость корзины не обновилась')

    def test_remove_from_cart(self):
        """
        Тестирование удаления элемента из корзины.
        Убедитесь, что элемент успешно удаляется из корзины.
        """
        url = reverse('cart-remove', kwargs={'pk': self.cart_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         'Не удалось удалить элемент из корзины')

        # Проверка, что элемент удален
        with self.assertRaises(CartItem.DoesNotExist,
                               msg='Элемент корзины не был удален'):
            CartItem.objects.get(id=self.cart_item.id)

        # Проверка, что корзина пуста
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_items, 0,
                         'Корзина не пуста после удаления элемента')
        self.assertEqual(self.cart.total_price, 0.00,
                         'Общая стоимость корзины не обнулилась')
