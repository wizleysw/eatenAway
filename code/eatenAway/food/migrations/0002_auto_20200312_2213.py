# Generated by Django 3.0.3 on 2020-03-12 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='menuname',
            field=models.SlugField(max_length=30, unique=True, verbose_name='메뉴이름'),
        ),
    ]