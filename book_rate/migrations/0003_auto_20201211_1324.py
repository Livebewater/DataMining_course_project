# Generated by Django 3.1.4 on 2020-12-11 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_rate', '0002_auto_20201211_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='year_of_publication',
            field=models.DateField(),
        ),
    ]
