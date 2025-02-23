# api_myshop

## О проекте
API магазина продуктов.

Реализовано:
- Реализована возможность создания, редактирования, удаления категорий и подкатегорий товаров в админке.
- Реализован эндпоинт для просмотра всех категорий с подкатегориями и предусмотрена пагинация.
- Реализована возможность добавления, изменения, удаления продуктов в админке.
- Реализован эндпоинт вывода продуктов с пагинацией.
- Реализован эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
- Реализован эндпоинт вывода состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
- Реализована возможность полной очистки корзины.
- Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь.
- Операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной.
- Реализована авторизация по токену.
- Реализованы фикстуры приложения.
- Подключена документация в формате swagger и redoc.


## Автор проекта:
Валерий Шанкоренко<br/>
Github: 👉 [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram: 📱 [@valeron007](https://t.me/valeron007)<br/>
E-mail: 📧 valerashankorenko@yandex.by<br/>

## Стек технологий
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html)
- [SQLite](https://www.sqlite.org/)

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
DJANGO_DEBUG=True #для разработки
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
10. Запуск тестов 
```shell
python manage.py test
```
11. Запуск проекта
```shell
python manage.py runserver
```
12. Документация по API в формате swagger:<br/>
http://localhost:8000/swagger/

13. Документация по API в формате redoc:<br/>
http://localhost:8000/redoc/
13. Получение токена:<br/>
http://localhost:8000/api/token-auth/

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