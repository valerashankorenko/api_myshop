from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from products.models import Product

User = get_user_model()


class Cart(models.Model):
    """
    Модель для корзины, связанной с пользователем.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'

    def __str__(self):
        return f'Корзина пользователя: {self.user.username}'


class CartItem(models.Model):
    """
    Модель для корзины, которая содержит продукты и их количество.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        'Количество продуктов в корзине',
        default=0
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity < 0 or self.quantity > 1000:
            raise ValidationError('Количество должно быть от 0 до 1000.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
