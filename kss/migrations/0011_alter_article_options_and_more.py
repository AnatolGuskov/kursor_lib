# Generated by Django 5.0.3 on 2024-06-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kss', '0010_book_image_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['data', 'pagina']},
        ),
        migrations.RenameField(
            model_name='bookbook',
            old_name='pagina_nome',
            new_name='status',
        ),
        migrations.AddField(
            model_name='genre',
            name='thema',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
