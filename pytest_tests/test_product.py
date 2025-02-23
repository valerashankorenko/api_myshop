from django.urls import reverse
from rest_framework import status


def test_product_list_api(api_client, product):
    """
    Тест для проверки получения списка продуктов через API.

    Этот тест отправляет GET-запрос к API для получения
    списка продуктов и проверяет, что статус ответа 200 (OK)
    и что возвращается один продукт.
    """
    url = reverse('product-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK, (
        f'Ожидался статус код 200, но получен {response.status_code}'
    )

    assert len(response.data['results']) == 1, (
        f'Ожидался один продукт, но получено {len(response.data["results"])}'
    )

    product_data = response.data['results'][0]
    assert product_data['name'] == product.name, 'Имя продукта не совпадает'
    assert float(product_data['price']
                 ) == product.price, 'Цена продукта не совпадает'
    assert product_data['category'] == (
        product.parent_subcategory.parent_category.name), (
            'Категория продукта не совпадает')
    assert product_data['subcategory'] == (
        product.parent_subcategory.name), (
            'Подкатегория продукта не совпадает')


def test_category_list_api(api_client):
    """
    Тест для проверки получения списка категорий через API.

    Этот тест отправляет GET-запрос к API для получения
    списка категорий и проверяет, что статус ответа 200 (OK).
    """
    url = reverse('category-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK, (
        f'Ожидался статус код 200, но получен {response.status_code}'
    )
