# Generated by Django 3.1.4 on 2020-12-16 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_rate', '0014_auto_20201216_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='book_rate.book'),
        ),
        migrations.AddField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='book_rate.user'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
