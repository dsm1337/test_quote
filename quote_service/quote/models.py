from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


User = get_user_model()


class WorkType(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тип произведения'
        verbose_name_plural = 'типы произведений'

    def __str__(self):
        return self.name


class Source(models.Model):
    '''Модель источников цитат'''
    title = models.CharField('Название', max_length=100)
    source_type = models.ForeignKey(
        WorkType, on_delete=models.SET_NULL, null=True,
        related_name='sources'
    )

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'источники'
        constraints = (models.constraints.UniqueConstraint(
            fields=('title', 'source_type'),
            name='unique_title_type'
        ),)

    def __str__(self):
        return self.title


class Quote(models.Model):
    '''Модель цитат'''
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField('Текст')
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, verbose_name='Источник'
    )
    views = models.IntegerField('Количество просмотров', default=0)
    weight = models.IntegerField(
        'Вес публикации',
        default=0,
        validators=(
            MaxValueValidator(100),
            MinValueValidator(1)
        )
    )
    created_at = models.DateTimeField('Время публикации', auto_now_add=True)

    class Meta:
        default_related_name = 'quotes'
        ordering = ('weight', 'views', 'created_at')
        verbose_name = 'Цитата'
        verbose_name_plural = 'цитаты'
        constraints = (models.constraints.UniqueConstraint(
            fields=('text', 'source'),
            name='unique_text_source'
        ),)

    def get_absolute_url(self):
        return reverse('quote:quote_detail', kwargs={'quote_id': self.pk})

    def __str__(self):
        return f'{self.source} - {self.text[:50]}'


class Opinion(models.Model):
    '''Модель лайков и дизлайков'''
    OPINION_CHOICES = (
        (-1, 'Dislike'),
        (1, 'Like')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, verbose_name='Цитата'
    )
    value = models.SmallIntegerField('Мнение', choices=OPINION_CHOICES)
    created_at = models.DateTimeField('Время проставления', auto_now_add=True)

    class Meta:
        default_related_name = 'likes'
        ordering = ('created_at', )
        verbose_name = 'Мнение'
        verbose_name_plural = 'мнения'
        constraints = (models.constraints.UniqueConstraint(
            fields=('user', 'quote'),
            name='unique_user_quote'
        ),)

    def __str__(self):
        return f'{self.user}: {self.quote} реакция: {self.value}'
