# Generated by Django 3.1.4 on 2020-12-13 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_rate', '0005_auto_20201211_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_rate.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_rate.user')),
            ],
        ),
    ]
