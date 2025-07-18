# Generated by Django 5.2.3 on 2025-07-06 17:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0003_alter_quote_weight'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quote.quote', verbose_name='Цитата'),
        ),
        migrations.AlterField(
            model_name='opinion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='opinion',
            constraint=models.UniqueConstraint(fields=('user', 'quote'), name='unique_user_quote'),
        ),
        migrations.AddConstraint(
            model_name='quote',
            constraint=models.UniqueConstraint(fields=('text', 'source'), name='unique_text_source'),
        ),
        migrations.AddConstraint(
            model_name='source',
            constraint=models.UniqueConstraint(fields=('title', 'source_type'), name='unique_title_type'),
        ),
    ]
