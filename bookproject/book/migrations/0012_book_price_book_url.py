# Generated by Django 4.2.13 on 2024-10-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_alter_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
