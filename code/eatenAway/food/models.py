from django.db import models
from user.models import Account


class Food(models.Model):
    menuname = models.CharField(verbose_name='메뉴이름', max_length=30, unique=True)
    category = models.CharField(verbose_name='카테고리', max_length=30,)
    country = models.CharField(verbose_name='나라', max_length=30,)
    ingredient = models.CharField(verbose_name='재료', max_length=30, null=True)
    taste = models.CharField(verbose_name='맛', max_length=30,)
    stock = models.BooleanField(verbose_name='국물여부', default=False)
    description = models.CharField(verbose_name='설명', max_length=50)
    profile = models.ImageField(upload_to="eatenAway/static/images/food_profile/", verbose_name='음식사진', blank=True)

    is_active = models.BooleanField(verbose_name='활성화 여부', default=True)

    def __str__(self):
        return self.menuname


class DailyUserFood(models.Model):
    username = models.CharField(max_length=10, verbose_name='유저')
    food = models.CharField(max_length=30, verbose_name='메뉴')
    meal_selection = (
        ('B', '아침'),
        ('L', '점심'),
        ('D', '저녁'),
    )
    mealkind = models.CharField(max_length=1, verbose_name='식사종류', choices=meal_selection, default='L')

    date = models.DateField(verbose_name='날짜')

    # location = models.CharField(max_length=64, verbose_name='장소')

    def __str__(self):
        return self.username + ':' + str(self.date) + ':' + self.mealkind


class FoodComment(models.Model):
    username = models.ForeignKey(Account, verbose_name='유저', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, verbose_name='메뉴', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    body = models.CharField(max_length=30)
    star = models.IntegerField(default=5)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food.menuname + ':' + self.username.username

