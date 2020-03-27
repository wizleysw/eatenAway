import requests
import json


class APIAboutFood:
    def __init__(self, username, foodname):
        self.username = username
        self.foodname = foodname

    def get_food_detail(self):
        url = "http://localhost:8000/api/food/"
        r = requests.get(url + self.foodname)
        if r.status_code == 200:
            res = r.json()
        else:
            res = None
        return res

    def get_user_food(self):
        url = "http://localhost:8000/api/food/user/"
        r = requests.post(url + self.username, data={'foodname': self.foodname})
        if r.status_code == 200:
            res = json.loads(r.json())
        else:
            res = {'nope': 1}
        return res

    def get_user_food_by_date(self, date):
        url = "http://localhost:8000/api/food/date/"
        r = requests.get(url + self.username + '/' + date)
        if r.status_code == 200:
            res = r.json()
        else:
            res = dict()
            res['B'] = res['L'] = res['D'] = '-'
        return res

    def update_user_food_by_date(self, requested_data):
        url = "http://localhost:8000/api/food/date/"
        r = requests.post(url + self.username, data=requested_data)
        if r.status_code == 200:
            res = '요청이 정상적으로 반영되었습니다.'
        else:
            res = '정보를 다시 확인해주세요.'
        return res

    def delete_user_food_by_date(self, date, mealkind):
        url = "http://localhost:8000/api/food/date/"
        r = requests.delete(url + self.username + '/' + date + '/' + mealkind)
        if r.status_code == 200:
            res = '요청이 정상적으로 반영되었습니다.'
        else:
            res = '정보를 다시 확인해주세요.'
        return res
