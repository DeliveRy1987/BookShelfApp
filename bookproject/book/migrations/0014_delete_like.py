# Generated by Django 4.2.13 on 2024-10-14 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_like'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]
