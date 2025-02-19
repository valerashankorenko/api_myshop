import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from products.models import Category, Product, Subcategory

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загрузка пользователей, категорий, подкатегорий и продуктов в базу'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Загрузка пользователей, категорий, подкатегорий '
            'и продуктов в базу начата'))

        self.load_users()
        self.load_categories()
        self.load_subcategories()
        self.load_products()

        self.stdout.write(self.style.SUCCESS('Данные загружены'))

    def load_users(self):
        """
        Загружает пользователей из файла users.json в базу данных.
        """
        try:
            with open('data/users.json', encoding='utf-8') as data_file_users:
                user_data = json.load(data_file_users)
                for user in user_data:
                    user_password = make_password(
                        user['password'])  # Хэшируем пароль
                    try:
                        User.objects.get_or_create(
                            username=user['username'],
                            defaults={
                                'email': user['email'],
                                'password': user_password,
                                'first_name': user.get('first_name', ''),
                                'last_name': user.get('last_name', '')
                            }
                        )
                    except IntegrityError:
                        logger.error(
                            f"Пользователь {user['username']} уже существует.")
        except FileNotFoundError:
            logger.error('Файл users.json не найден.')
        except json.JSONDecodeError:
            logger.error('Ошибка при чтении JSON. Проверьте формат файла.')
        except Exception as e:
            logger.error(
                f'Произошла ошибка при загрузке пользователей: {str(e)}')

    def load_categories(self):
        """
        Загружает категории из файла categories.json в базу данных.
        """
        try:
            with open(
                'data/categories.json',
                ncoding='utf-8'
            ) as data_file_categories:
                categories_data = json.load(data_file_categories)
                for category in categories_data:
                    Category.objects.get_or_create(**category)
        except FileNotFoundError:
            logger.error('Файл categories.json не найден.')
        except json.JSONDecodeError:
            logger.error('Ошибка при чтении JSON. Проверьте формат файла.')
        except Exception as e:
            logger.error(f'Произошла ошибка при загрузке категорий: {str(e)}')

    def load_subcategories(self):
        """
        Загружает подкатегории из файла subcategories.json в базу данных.
        """
        try:
            with open(
                'data/subcategories.json',
                encoding='utf-8'
            ) as data_file_subcategories:
                subcategories_data = json.load(data_file_subcategories)
                for subcategory in subcategories_data:
                    category_id = subcategory.pop('parent_category', None)
                    if category_id is not None:
                        try:
                            category = Category.objects.get(id=category_id)
                            subcategory['parent_category'] = category
                            Subcategory.objects.get_or_create(**subcategory)
                        except Category.DoesNotExist:
                            logger.error(
                                f'Категория с ID {category_id} не найдена '
                                f'для подкатегории {subcategory["name"]}.'
                            )
                    else:
                        logger.warning(
                            f'Не указана категория для подкатегории '
                            f'{subcategory["name"]}.'
                        )
        except FileNotFoundError:
            logger.error('Файл subcategories.json не найден.')
        except json.JSONDecodeError:
            logger.error('Ошибка при чтении JSON. Проверьте формат файла.')
        except Exception as e:
            logger.error(
                f'Произошла ошибка при загрузке подкатегорий: {str(e)}')

    def load_products(self):
        """
        Загружает продукты из файла products.json в базу данных.
        """
        try:
            with open(
                'data/products.json',
                encoding='utf-8'
            ) as data_file_products:
                products_data = json.load(data_file_products)
                for product in products_data:
                    subcategory_id = product.pop('parent_subcategory', None)
                    if subcategory_id is not None:
                        try:
                            subcategory = Subcategory.objects.get(
                                id=subcategory_id)
                            product['parent_subcategory'] = subcategory
                            Product.objects.get_or_create(**product)
                        except Subcategory.DoesNotExist:
                            logger.error(
                                f'Подкатегория с ID {subcategory_id} не '
                                f'найдена для продукта {product["name"]}.')
                    else:
                        logger.warning(
                            f'Не указана подкатегория для продукта '
                            f'{product["name"]}.'
                        )
        except FileNotFoundError:
            logger.error('Файл products.json не найден.')
        except json.JSONDecodeError:
            logger.error('Ошибка при чтении JSON. Проверьте формат файла.')
        except Exception as e:
            logger.error(f'Произошла ошибка при загрузке продуктов: {str(e)}')
