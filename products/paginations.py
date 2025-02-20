from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
    Пагинация для списков категорий, подкатегорий и продуктов.

    Атрибуты:
    - page_size: Количество элементов на одной странице по умолчанию.
    - page_size_query_param: Параметр запроса для изменения количества
      элементов на странице.
    - max_page_size: Максимальное количество элементов на одной странице.
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
