import os
import django
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eatenAway.settings')

django.setup()

from food.models import Food

f = open('FoodList.csv', 'r', encoding='utf-8')
info = []

rdr = csv.reader(f)

for row in rdr:
    menuname, category, country, ingredient, taste, stock, description, tmp = row
    if stock == 'TRUE':
        stock = True
    else:
        stock = False
    tuple = (menuname, category, country, ingredient, taste, stock, description)
    info.append(tuple)

f.close()

instances = []
for (menuname, category, country, ingredient, taste, stock, description) in info:
    instances.append(Food(menuname=menuname, category=category, country=country, ingredient=ingredient, taste=taste, stock=stock))

Food.objects.bulk_create(instances)