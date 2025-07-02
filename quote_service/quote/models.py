from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Source(models.Model):
    '''Модель источников цитат'''
    title = models.CharField('Название', max_length=100)
    source_type = models.CharField(
        'Тип произведения', max_length=100, blank=True
    )

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'источники'

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
        ordering = ('weight','views', 'created_at')
        verbose_name = 'Цитата'
        verbose_name_plural = 'цитаты'

    def get_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.source} - {self.text[:50]}'


class Opinion(models.Model):
    '''Модель лайков и дизлайков'''
    OPINION_CHOICES = (
        (-1, 'Dislike'),
        (1, 'Like')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    value = models.SmallIntegerField('Мнение', choices=OPINION_CHOICES)
    created_at = models.DateTimeField('Время проставления', auto_now_add=True)

    class Meta:
        default_related_name = 'likes'
        ordering = ('created_at', )
        verbose_name = 'Мнение'
        verbose_name_plural = 'мнения'
    
    def __str__(self):
        return f'{self.author}: {self.quote} реакция: {self.value}'
