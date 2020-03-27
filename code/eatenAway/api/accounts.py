from django.contrib.auth.hashers import check_password
from user.models import Account
import requests


class UserAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.account = None

    def is_account_status_ok(self):
        if self.account.status == 'O':
            return True
        else:
            return False

    def is_account_available(self):
        try:
            self.account = Account.objects.get(username=self.username)
            if self.is_account_status_ok():
                return True
            else:
                return False
        except Account.DoesNotExist:
            return False

    def is_password_correct(self):
        if self.is_account_available() and check_password(self.password, self.account.password):
            return True
        else:
            return False


