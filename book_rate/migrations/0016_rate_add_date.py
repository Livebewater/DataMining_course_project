# Generated by Django 3.1.4 on 2020-12-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_rate', '0015_auto_20201216_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='add_date',
            field=models.DateField(default='2020-12-16'),
        ),
    ]
