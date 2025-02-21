from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product, Subcategory


class ProductTests(APITestCase):
    """
    Тесты для модели Product и API.

    Этот класс содержит тесты для проверки функциональности API продуктов.
    Он включает в себя создание категорий и подкатегорий, а также тестирование
    получения списка продуктов через API.
    """

    def setUp(self):
        """Настройка тестовых данных для тестов."""
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

    def tearDown(self):
        """Очистка данных после тестов."""
        self.product.image_small.delete(save=False)
        self.product.image_medium.delete(save=False)
        self.product.image_large.delete(save=False)
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_product_list_api(self):
        """
        Тест для проверки получения списка продуктов через API.

        Этот тест отправляет GET-запрос к API для получения
        списка продуктов и проверяет, что статус ответа 200 (OK)
        и что возвращается один продукт.
        """
        url = reverse(
            'product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Ожидался статус код 200, но получен {}'
                         .format(response.status_code))

        self.assertEqual(len(response.data['results']), 1,
                         'Ожидался один продукт, но получено {}'
                         .format(len(response.data['results'])))

        product_data = response.data['results'][0]
        self.assertEqual(product_data['name'], self.product.name,
                         'Имя продукта не совпадает')
        self.assertEqual(float(product_data['price']), self.product.price,
                         'Цена продукта не совпадает')
        self.assertEqual(
            product_data['category'],
            self.product.parent_subcategory.parent_category.name,
            'Категория продукта не совпадает'
        )
        self.assertEqual(product_data['subcategory'],
                         self.product.parent_subcategory.name,
                         'Подкатегория продукта не совпадает'
                         )
