# Generated by Django 3.0.3 on 2020-03-26 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food', '0006_dailyuserfood_mealkind'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=30)),
                ('star', models.IntegerField(default=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Food', verbose_name='메뉴')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='food.FoodComment')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
        ),
    ]
