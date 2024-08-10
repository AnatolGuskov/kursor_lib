# Generated by Django 5.0.3 on 2024-06-08 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kss', '0003_alter_book_options_rename_type_book_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'subtitle', 'data']},
        ),
        migrations.AddField(
            model_name='book',
            name='pseudonym',
            field=models.CharField(default='-', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='cognome',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='nome',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='padrenome',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='subtitle',
            field=models.CharField(max_length=100),
        ),
    ]
