# Generated by Django 2.0.3 on 2018-06-10 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20180610_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='research',
            name='created_at',
        ),
    ]
