# Generated by Django 3.1.4 on 2020-12-15 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_rate', '0012_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='add_date',
            field=models.DateField(default='2020-12-15'),
        ),
        migrations.AlterField(
            model_name='book',
            name='add_date',
            field=models.DateField(default='2020-12-15'),
        ),
    ]
