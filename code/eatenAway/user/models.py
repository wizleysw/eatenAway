from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Account must have an username')
        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    account_no = models.AutoField(primary_key=True)

    name = models.CharField(max_length=20, verbose_name='이름', default='Chihiro')
    birth = models.DateField(null=True, verbose_name='생일')
    area = models.CharField(max_length=10, verbose_name='지역', default='Seoul')
    sex_selection = (
        ('M', '남성'),
        ('W', '여성'),
    )
    sex = models.CharField(max_length=1, verbose_name='성별', choices=sex_selection, default='W')

    username = models.CharField(max_length=10, verbose_name='아이디', unique=True)
    password = models.CharField(max_length=100, verbose_name='패스워드')
    email = models.EmailField(max_length=32, verbose_name='이메일')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="가입날짜")
    comment = models.CharField(max_length=20, verbose_name='코멘트', blank=True)
    profile = models.ImageField(upload_to="user_profile/profile_picture", verbose_name='프로필', blank=True)

    account_status_selection = (
        ('O', '정상'),
        ('X', '삭제'),
        ('B', '정지'),
        ('W', '검증'),
    )
    status = models.CharField(max_length=1, verbose_name='계정 상태', choices=account_status_selection, default="W")
    active = models.BooleanField(default=False, verbose_name="이메일 인증여부")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin