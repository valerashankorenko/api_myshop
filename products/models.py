from django.db import models
from django.utils.text import slugify


class CategoryBase(models.Model):
    """
    Абстрактная модель для категорий, подкатегорий и продуктов.
    """
    name = models.CharField(
        'Название',
        max_length=255
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(CategoryBase):
    """
    Модель для категорий.
    """
    image = models.ImageField(
        'Изображение категории',
        upload_to='categories/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(CategoryBase):
    """
    Модель для подкатегорий.
    """
    parent_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Изображение подкатегории',
        upload_to='subcategories/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(CategoryBase):
    """
    Модель для продуктов.
    """
    parent_subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )
    image_small = models.ImageField(
        'Маленькое изображение продукта',
        upload_to='products/small/',
        blank=True,
        null=True
    )
    image_medium = models.ImageField(
        'Среднее изображение продукта',
        upload_to='products/medium/',
        blank=True,
        null=True
    )
    image_large = models.ImageField(
        'Большое изображение продукта',
        upload_to='products/large/',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        'Стоимость продукта',
        max_digits=10,
        decimal_places=2
    )

    @property
    def category(self):
        return (self.parent_subcategory.category
                if self.parent_subcategory else None)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
