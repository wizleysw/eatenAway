from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser

class Account(AbstractBaseUser):
    account_no = models.AutoField(primary_key=True)

    name = models.CharField(max_length=20, verbose_name='이름', default='Chihiro')
    birth = models.DateField(null=True)
    area = models.CharField(max_length=10, verbose_name='지역', default='Seoul')
    sex_selection = (
        ('M', '남성'),
        ('W', '여성'),
    )
    sex = models.CharField(max_length=1, choices=sex_selection, default='W')

    username = models.CharField(max_length=10, verbose_name='아이디')
    password = models.CharField(max_length=16, verbose_name='패스워드')
    email = models.EmailField(max_length=32, verbose_name='이메일')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="가입날짜")
    comment = models.CharField(max_length=20, verbose_name="코멘트", blank=True)
    profile = models.ImageField(upload_to="user_profile/profile_picture", blank=True)

    account_status_selection = (
        ('O', '정상'),
        ('X', '삭제'),
        ('B', '정지'),
        ('W', '검증'),
    )
    status = models.CharField(max_length=1, choices=account_status_selection, default="W")

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username