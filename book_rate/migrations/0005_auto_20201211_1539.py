# Generated by Django 3.1.4 on 2020-12-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_rate', '0004_auto_20201211_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=70)),
                ('author', models.CharField(max_length=30)),
                ('year_of_publication', models.CharField(max_length=4)),
                ('publisher', models.CharField(max_length=60)),
                ('add_date', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='Books',
        ),
    ]
