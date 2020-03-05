from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    name = forms.CharField(label="name", max_length=20, min_length=3, required=True)
    birth = forms.DateField(label="birth", required=True)
    area = forms.CharField(label="area", max_length=10, required=True)
    sex = forms.CharField(label="sex", max_length=1, required=True)
    username = forms.CharField(label="username", max_length=10, min_length=4, required=True)
    password = forms.CharField(max_length=16, min_length=8, required=True)
    email = forms.EmailField(label="email", max_length=32, required=True)

    class Meta:
        model = Account
        exclude = ('comment', 'created_date', 'status', 'profile')

