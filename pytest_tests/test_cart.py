from django.urls import reverse
from rest_framework import status

from cart.models import CartItem


def test_get_cart(authenticated_client, cart_item):
    """Тест для получения корзины авторизованным пользователем.

    Этот тест отправляет GET-запрос к API для получения
    корзины и проверяет, что статус ответа 200 (OK)
    и что возвращаются ключи "items", "total_items_cart" и
    "total_price_cart" с корректными значениями.
    """
    url = reverse('cart-detail')
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK, (
        'Не удалось получить корзину')
    assert 'items' in response.data, (
        'Ключ "items" отсутствует в ответе')
    assert 'total_items_cart' in response.data, (
        'Ключ "total_items_cart" отсутствует в ответе')
    assert 'total_price_cart' in response.data, (
        'Ключ "total_price_cart" отсутствует в ответе')

    assert len(response.data['items']
               ) == 1, 'Количество товаров в корзине не совпадает'
    assert response.data['total_items_cart'] == 2, (
        'Общее количество товаров в корзине не совпадает')
    assert float(response.data['total_price_cart']
                 ) == 20.00, 'Общая стоимость корзины не совпадает'


def test_add_to_cart(authenticated_client, cart, product):
    """Тест для добавления товара в корзину авторизованным пользователем.

    Этот тест отправляет POST-запрос к API для добавления
    товара в корзину и проверяет, что статус ответа 201 (Created)
    и что количество товара обновлено в корзине.
    """
    url = reverse('cart-add')
    data = {'product_id': product.id, 'quantity': 3}
    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED, (
        'Не удалось добавить товар в корзину')

    cart_item = CartItem.objects.get(cart=cart, product=product)
    assert cart_item.quantity == 3, (
        'Количество товара в корзине не совпадает')

    cart.refresh_from_db()
    assert cart.total_price == 30.00, 'Общая стоимость корзины не совпадает'


def test_update_cart_item(authenticated_client, cart_item):
    """Тест для обновления элемента корзины авторизованным пользователем.

    Этот тест отправляет PATCH-запрос к API для обновления
    количества товара в корзине и проверяет, что статус
    ответа 200 (OK) и что количество товара обновлено.
    """
    url = reverse('cart-update', kwargs={'pk': cart_item.id})
    data = {'quantity': 4}
    response = authenticated_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK, (
        'Не удалось обновить элемент корзины')

    cart_item.refresh_from_db()
    assert cart_item.quantity == 4, 'Количество товара не обновилось'

    cart_item.cart.refresh_from_db()
    assert cart_item.cart.total_price == 40.00, (
        'Общая стоимость корзины не обновилась')


def test_remove_from_cart(authenticated_client, cart_item):
    """Тест для удаления элемента из корзины авторизованным пользователем.

    Этот тест отправляет DELETE-запрос к API для удаления
    товара из корзины и проверяет, что статус ответа 204
    (No Content) и что элемент был удален.
    """
    url = reverse('cart-remove', kwargs={'pk': cart_item.id})
    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT, (
        'Не удалось удалить элемент из корзины')

    # Проверяем, что элемент был удален
    assert not CartItem.objects.filter(
        id=cart_item.id).exists(), 'Элемент все еще существует в корзине'


def test_get_cart_unauthenticated(api_client):
    """Тест для проверки доступа к корзине неаутентифицированного пользователя.

    Этот тест отправляет GET-запрос к API для получения
    корзины и проверяет, что статус ответа 401 (Unauthorized)
    для неаутентифицированного пользователя.
    """
    url = reverse('cart-detail')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
        'Неаутентифицированный пользователь должен получить 401 статус')
