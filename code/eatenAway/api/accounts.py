from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from user.models import Account


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
        except:
            return False

    def is_password_correct(self):
        if self.is_account_available() and check_password(self.password, self.account.password):
            return True
        else:
            return False

    def already_have_username(self):
        try:
            res = Account.objects.get(username=self.username)
            return True
        except:
            return False

    def already_have_email(self, email):
        try:
            res = Account.objects.get(email=email)
            return True
        except:
            return False

    def get_account_by_pk(self, uidb64):
        uid = force_text(urlsafe_base64_decode(uidb64))
        res = Account.objects.get(pk=uid)
        self.account = res
        return res

    def get_account(self):
        res = Account.objects.get(username=self.username)
        return res

    def check_account_activation(self, token):
        if self.account is None:
            return False
        elif account_activation_token.check_token(self.account, token):
            self.account.status = 'O'
            self.account.active = True
            self.account.is_active = True
            self.account.save()
            return True
        return False

    def get_email_link(self):
        user = self.get_account()
        message = render_to_string('activate.html', {
            'domain': 'localhost:8000',
            'username': self.username,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        return message

    def send_email(self, email):
        mail_subject = 'eaten-Away 이메일 인증'
        to_email = email
        message = self.get_email_link()
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()