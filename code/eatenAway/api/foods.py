from food.models import Food, DailyUserFood
import operator
import datetime
import json


class DailyFood:
    def __init__(self, username):
        self.username = username
        self.taste = 0
        self.queryset = None
        self.mostpick = dict()
        self.ingredients = dict()
        self.categories = dict()
        self.countries = dict()
        self.foodcount = dict()
        self.dateinfo = dict()
        self.res = dict()

    def get_food_info(self, menuname):
        res = Food.objects.get(menuname=menuname)
        return res

    def get_average_of_taste(self, food):
        self.taste += int(food.taste)

    def add_food_to_dict(self, option, to):
        if not option in to:
            to[option] = 1
        else:
            to[option] += 1
        return to

    def add_food_to_dict_with_date(self, date, menuname, mealkind):
        if not str(date) in self.dateinfo:
            self.dateinfo[str(date)] = dict()
            self.dateinfo[str(date)][mealkind] = menuname
        else:
            self.dateinfo[str(date)][mealkind] = menuname

    def sort_dict(self, which):
        return sorted(which.items(), key=operator.itemgetter(1), reverse=True)

    def get_user_food_mealkind(self):
        for row in self.queryset:
            if not row.mealkind in self.res:
                self.res[row.mealkind] = 1
            else:
                self.res[row.mealkind] += 1
        return json.dumps(self.res)


    def get_user_food_preference(self):
        self.res['모스트 원픽'] = Food.objects.filter(menuname=self.mostpick[0][0]).order_by("?").first().menuname

        tmp = Food.objects.filter(taste=self.taste).order_by("?").first().menuname
        while tmp in self.res.values():
            tmp = Food.objects.filter(taste=self.taste).order_by("?").first().menuname
        self.res['평균적인 맛에 의거한 추천'] = tmp

        tmp = Food.objects.filter(ingredient=self.ingredients[0][0]).order_by("?").first().menuname
        while tmp in self.res.values():
            tmp = Food.objects.filter(ingredient=self.ingredients[0][0]).order_by("?").first().menuname
        self.res['재료에 의한 추천'] = tmp

        tmp = Food.objects.filter(category=self.categories[0][0]).order_by("?").first().menuname
        while tmp in self.res.values():
            tmp = Food.objects.filter(category=self.categories[0][0]).order_by("?").first().menuname
        self.res['음식의 종류에 따른 추천'] = tmp

        tmp = Food.objects.filter(country=self.countries[0][0]).order_by("?").first().menuname
        while tmp in self.res.values():
            tmp = Food.objects.filter(country=self.countries[0][0]).order_by("?").first().menuname
        self.res['특정 나라음식 추천'] = tmp

        tmp = Food.objects.order_by("?").first().menuname
        while tmp in self.res.values():
            tmp = Food.objects.order_by("?").first().menuname
        self.res['랜덤 추천'] = tmp

        tmp = Food.objects.order_by("?").first().menuname
        while tmp in self.res.values():
            tmp = Food.objects.order_by("?").first().menuname
        self.res['묻지마 추천'] = tmp

    def get_user_food_by_date(self, date):
        self.queryset = DailyUserFood.objects.filter(username=self.username, date=date)
        self.res = {}
        self.res['B'] = self.res['L'] = self.res['D'] = '-'
        if not self.queryset.exists():
            return self.res
        else:
            for row in self.queryset:
                self.res[row.mealkind] = row.food
            return self.res

    def get_user_food_by_date_and_mealkind(self, date, mealkind):
        res = DailyUserFood.objects.get(username=self.username, date=date, mealkind=mealkind)
        return res

    def get_user_food(self, foodname):
        self.queryset = DailyUserFood.objects.filter(username=self.username, food=foodname)
        return self.queryset

    def get_user_food_with_day(self, day):
        self.queryset = DailyUserFood.objects.filter(username=self.username, date__range=[datetime.date.today() - datetime.timedelta(days=day), datetime.date.today()])
        return self.queryset

    def get_preference(self):
        loop_count = 0
        for row in self.queryset:
            menuname = row.food
            food = self.get_food_info(menuname)
            self.get_average_of_taste(food)
            self.add_food_to_dict(food.menuname, self.mostpick)
            self.add_food_to_dict(food.ingredient, self.ingredients)
            self.add_food_to_dict(food.category, self.categories)
            self.add_food_to_dict(food.country, self.countries)
            loop_count += 1

        self.taste = int(self.taste/loop_count)
        self.mostpick = self.sort_dict(self.mostpick)
        self.ingredients = self.sort_dict(self.ingredients)
        self.categories = self.sort_dict(self.categories)
        self.countries = self.sort_dict(self.countries)

        self.get_user_food_preference()

        return self.res

    def get_foodcount_with_date(self):
        for row in self.queryset:
            menuname = row.food
            self.add_food_to_dict(menuname, self.foodcount)
            self.add_food_to_dict_with_date(row.date, menuname, row.mealkind)

        self.res['foodcount'] = self.foodcount
        self.res['dateinfo'] = self.dateinfo
        return json.dumps(self.res)

    def add_user_food(self, foodname, mealkind, date):
        res = DailyUserFood(username=self.username, food=foodname, date=date, mealkind=mealkind)
        res.save()

    def delete_user_food(self, date, mealkind):
        res = DailyUserFood.objects.get(username=self.username, date=date, mealkind=mealkind)
        res.delete()

