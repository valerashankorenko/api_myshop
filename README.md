# api_myshop

## О проекте
API магазина продуктов.

Реализовано:
- Административная панель на русском языке для управления контентом.
- Возможность создания, редактирования, удаления категорий и подкатегорий товаров в админке.
- Эндпоинт для просмотра всех категорий с подкатегориями и предусмотрена пагинация.
- Возможность добавления, изменения, удаления продуктов в админке.
- Эндпоинт вывода продуктов с пагинацией.
- Эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
- Эндпоинт вывода состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
- Возможность полной очистки корзины.
- Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь.
- Операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной.
- Авторизация по токену.
- Фикстуры приложения.
- Подключена документация в формате swagger и redoc.


## Автор проекта:
Валерий Шанкоренко<br/>
Github: 👉 [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram: 📱 [@valeron007](https://t.me/valeron007)<br/>
E-mail: 📧 valerashankorenko@yandex.by<br/>

## Стек технологий
![Python 3.12.4](https://img.shields.io/badge/Python-3.12.4-3776AB?style=flat-square&logo=python&logoColor=white)
![Django 5.1.6](https://img.shields.io/badge/Django-5.1.6-092E20?style=flat-square&logo=django&logoColor=white)
![Django REST framework 3.15.2](https://img.shields.io/badge/Django%20REST%20framework-3.15.2-3C873A?style=flat-square&logo=django&logoColor=white)
![Pillow 11.1.0](https://img.shields.io/badge/Pillow-11.1.0-EBEEEF?style=flat-square&logo=pillow&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Pytest 8.3.4](https://img.shields.io/badge/Pytest-8.3.4-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Pytest-django 4.10.0](https://img.shields.io/badge/Pytest--django-4.10.0-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![drf-spectacular 0.28.0](https://img.shields.io/badge/drf--spectacular-0.28.0-3C873A?style=flat-square&logo=django&logoColor=white)

## Как запустить проект локально:
1. Клонировать репозиторий и перейти в его директорию в командной строке:
```shell
git clone git@github.com:valerashankorenko/api_myshop.git
```
2. Переход в директорию api_myshop
```shell
cd api_myshop
```
3. Cоздать и активировать виртуальное окружение:
 - для Linux/MacOS
```shell
python3 -m venv venv
source venv/bin/activate
```
- для Windows
```shell
python -m venv venv
source venv/Scripts/activate
```
4. Обновить пакетный менеджер pip
```shell
python3 -m pip install --upgrade pip
```
5. Установить зависимости из файла requirements.txt:
```shell
pip install -r requirements.txt
```
6. Применение миграций
```shell
python manage.py migrate
```
7. В корневой директории создать файл .env и заполнить своими данными:
```
DJANGO_DEBUG=True # для разработки
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=секретный ключ Django
Данные для суперпользователя
DJANGO_SUPERUSER_USERNAME=your_first_username
DJANGO_SUPERUSER_EMAIL=email
DJANGO_SUPERUSER_PASSWORD=password
DJANGO_SUPERUSER_FIRST_NAME=your_first_name
DJANGO_SUPERUSER_LAST_NAME=your_last_name
```
8. Создать суперпользователя
```shell
python manage.py create_superuser
```
9. Наполнение БД тестовыми данными
```shell
python manage.py load_database
```
10. Запуск тестов Unittest
```shell
python manage.py test
```
Запуск тестов Pytest
```shell
pytest
```
11. Запуск проекта
```shell
python manage.py runserver
```
12. Документация по API в формате swagger:<br/>
http://localhost:8000/api/schema/swagger-ui/

13. Документация по API в формате redoc:<br/>
http://localhost:8000/api/schema/redoc/

13. Получение токена:<br/>
http://localhost:8000/api/token-auth/<br/>
Для авторизации 'Token <ваш_токен>'

### Примеры запросов к API

#### Получение списка продуктов

```http
GET /api/products/
```

#### Добавление продукта в корзину

```http
POST /api/cart/add/
Content-Type: application/json

{
  "product": {
    "name": "string",
    "slug": "slug-name",
    "price": "string"
  },
  "product_id": "string",
  "quantity": 0
}
```