import requests
import operator
import json


class APIAboutUser:
    def __init__(self, username):
        self.username = username

    def get_user_token(self, password, recaptcha):
        url = "http://localhost:8000/api/accounts/login/"
        r = requests.post(url, data={'username': self.username, 'password': password, 'g-recaptcha-response': recaptcha})
        if r.status_code == 200:
            res = r.json()['token']
        else:
            res = None
        return res

    def get_user_profile(self):
        url = "http://localhost:8000/api/accounts/profile/"
        r = requests.get(url + self.username)
        if r.status_code == 200:
            res = json.loads(r.json())
        else:
            res = None
        return res

    def get_user_preference(self):
        url = "http://localhost:8000/api/food/preference/"
        r = requests.get(url + self.username)
        if r.status_code == 200:
            res = r.json()
        else:
            res = None
        return res

    def get_user_foodcount(self):
        url = "http://localhost:8000/api/food/user/"
        r = requests.get(url + self.username)
        if r.status_code == 200:
            res = json.loads(r.json())
            if res is not None:
                res2 = res['dateinfo']
                res3 = sorted(res['foodcount'].items(), key=operator.itemgetter(1), reverse=True)
        else:
            res2 = res3 = None
        return res2, res3
