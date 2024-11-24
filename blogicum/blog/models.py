from django.db import models
from django.contrib.auth import get_user_model
from core.models import PublishedModel
from blog.constants import MAX_LEN

User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(max_length=MAX_LEN, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        # По другому тесты не проходит
        help_text=(
            'Идентификатор страницы для URL; разрешены символы'
            + ' латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(max_length=MAX_LEN, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(max_length=MAX_LEN, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            + 'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации',
        related_name='authors'
    )
    location = models.ForeignKey(
        Location,
        unique=False,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        related_name='locations'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',
        related_name='categories'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
