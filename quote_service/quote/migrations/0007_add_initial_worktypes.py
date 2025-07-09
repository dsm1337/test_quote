from django.db import migrations


def add_work_types(apps, schema_editor):
    WorkType = apps.get_model('quote', 'WorkType')
    WorkType.objects.get_or_create(name='Фильм')
    WorkType.objects.get_or_create(name='Книга')


class Migration(migrations.Migration):

    dependencies = [
        ("quote", "0006_alter_source_source_type"),
    ]

    operations = [migrations.RunPython(add_work_types),]