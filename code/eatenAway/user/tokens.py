from eatenAway.settings import JWT_AUTH
import requests
import jwt


class Token:
    def __init__(self, token):
        self.token = token

    def has_token(self):
        if self.token is not None:
            return True
        else:
            return False

    def get_account_token(self, username, password):
        url = "http://localhost:8000/api/token/"
        r = requests.post(url, data={'username': username, 'password': password})
        if r.status_code == 200:
            res = r.json()['token']
        else:
            res = None
        return res

    def verify(self):
        if self.has_token():
            url = "http://localhost:8000/api/token/verify/"
            r = requests.post(url, data={'token': self.token})
            if r.status_code == 200 and r.json()['token']:
                return True
            else:
                return False
        return False

    def decode_jwt(self):
        if self.has_token() and self.verify():
            return jwt.decode(self.token, JWT_AUTH['JWT_SECRET_KEY'])
        return None
