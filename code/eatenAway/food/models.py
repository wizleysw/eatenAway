from django.db import models


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