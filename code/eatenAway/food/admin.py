from django.contrib import admin
from .models import Food, DailyUserFood, FoodComment

admin.site.register(Food)
admin.site.register(DailyUserFood)
admin.site.register(FoodComment)

