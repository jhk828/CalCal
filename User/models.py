from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

GENDER_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),
)

class UserManager(BaseUserManager):
    def create_user(self, username,email,  age, weight, height, gender, password=None):
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=email,
            age=age,
            weight=weight,
            height=height,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, age, weight, height, gender, password):
        user = self.create_user(
            username,
            email=email,
            password=password,
            age=age,
            weight=weight,
            height=height,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=40,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=240,
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'age', 'gender', 'weight', 'height']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin