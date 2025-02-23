import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from cart.models import Cart, CartItem
from products.models import Category, Product, Subcategory

User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Фикстура для автоматического предоставления доступа к БД во всех тестах.

    Особенности:
    - Автоматически активируется для всех тестов благодаря autouse=True
    - Позволяет избежать необходимости маркировать каждый тест декоратором
      @pytest.mark.django_db
    """
    pass


@pytest.fixture
def category(db):
    """Создание категории для тестов."""
    return Category.objects.create(
        name='Test Category',
        slug='test-category'
    )


@pytest.fixture
def subcategory(category, db):
    """Создание подкатегории для тестов."""
    return Subcategory.objects.create(
        parent_category=category,
        name='Test Subcategory',
        slug='test-subcategory'
    )


@pytest.fixture
def image():
    """Создание тестового изображения."""
    return SimpleUploadedFile(
        'test_image.jpg',
        b'file_content',
        content_type='image/jpeg'
    )


@pytest.fixture
def product(subcategory, image, db):
    """Создание продукта для тестов."""
    product_data = {
        'parent_subcategory': subcategory,
        'name': 'Test Product',
        'price': 10.00,
        'image_small': image,
        'image_medium': image,
        'image_large': image,
    }
    return Product.objects.create(**product_data)


@pytest.fixture
def user(db):
    """Создание пользователя для тестов."""
    user = User.objects.create_user(
        username='testuser',
        email='testuser@mail.ru',
        password='testpassword'
    )
    Token.objects.create(user=user)
    return user


@pytest.fixture
def other_user():
    """Создание фикстуры для другого пользователя."""
    User = get_user_model()
    other_user = User.objects.create_user(
        username='otheruser',
        email='otheruser@mail.ru',
        password='otherpass'
    )
    return other_user


@pytest.fixture
def api_client():
    """Фикстура для создания экземпляра APIClient."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Фикстура для создания аутентифицированного клиента."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def cart(user, db):
    """Создание корзины для тестов."""
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(cart, product, db):
    """Создание элемента корзины для тестов."""
    return CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2
    )


@pytest.fixture
def other_user_cart(other_user):
    """Создание фикстуры для корзины другого пользователя."""
    return Cart.objects.create(user=other_user)
