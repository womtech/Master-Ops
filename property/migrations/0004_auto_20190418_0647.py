# Generated by Django 2.1.7 on 2019-04-18 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_auto_20190418_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebook',
            name='fans',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='facebook',
            name='ptat',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='facebook',
            name='token',
            field=models.TextField(blank=True),
        ),
    ]
