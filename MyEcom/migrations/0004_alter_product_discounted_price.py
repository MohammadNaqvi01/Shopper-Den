# Generated by Django 3.2.5 on 2021-07-24 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyEcom', '0003_auto_20210724_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.FloatField(),
        ),
    ]
