from django.db import models
from datetime import datetime

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):
        return self.username

class Table(models.Model):
    name = models.CharField('음식 이름', max_length=30)
    serving_wt = models.FloatField('제공량')
    kcal = models.FloatField('칼로리')
    carbo = models.FloatField('탄수화물')
    protein = models.FloatField('단백질')
    fat = models.FloatField('지방')
    company = models.TextField('회사명', max_length=30)

    def __str__(self):
        return self.name


class UserTable(models.Model):
    authuser = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField('음식 이름', max_length=30)
    serving_wt = models.FloatField('제공량')
    kcal = models.FloatField('칼로리')
    carbo = models.FloatField('탄수화물')
    protein = models.FloatField('단백질')
    fat = models.FloatField('지방')
    company = models.TextField('회사명', max_length=30)
    amount = models.FloatField('섭취량', default=1)
    date = models.DateTimeField('날짜', default=datetime.now, blank=True)
    date_1 = models.DateField('날짜2', default=datetime.now().strftime('%Y-%m-%d'), blank=True)
    def __str__(self):
        return self.name