from django.db import models
from User.models import User
from datetime import datetime

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
    authuser = models.ForeignKey(User,on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField('음식 이름', max_length=30)
    serving_wt = models.FloatField('제공량')
    kcal = models.FloatField('칼로리')
    carbo = models.FloatField('탄수화물')
    protein = models.FloatField('단백질')
    fat = models.FloatField('지방')
    company = models.TextField('회사명', max_length=30)
    amount = models.FloatField('섭취량', default=1)
    # date = models.DateTimeField('날짜', default=datetime.now, blank=True)
    date = models.DateField('날짜', default=datetime.now().strftime('%Y-%m-%d'), blank=True)
    def __str__(self):
        return self.name