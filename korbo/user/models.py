from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from korbo.abstract.models import KorboObject
from django.contrib.auth.models import PermissionsMixin
from korbo.extra.enum import GenderEnum
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if email is not None:

            email = self.normalize_email(email)
        
        is_consultant = extra_fields.get('is_consultant')
        if is_consultant:
            extra_fields['freelance'] = False
            extra_fields['is_active'] = True

        is_startup = extra_fields.get('is_startup')
        if is_startup:
            extra_fields['freelance'] = False
            extra_fields['is_active'] = True

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        else:
            user.set_unusable_password(password)

        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must have is_superuser=True.')

        extra_fields['email'] = email

        return self.create_user(password, **extra_fields)


class User(KorboObject, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique=True, db_index=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_consultant = models.BooleanField(default=False)
    is_freelance = models.BooleanField(default=True)
    is_startup = models.BooleanField(default=False)

    joined = models.DateField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def has_role(self, perm) -> bool:

        if self.is_active and self.is_superuser:
            return True

        perm = perm
        role = getattr(self, f"is_{perm}", False)

        return bool(role) and self.is_active

    def __str__(self) -> str:
        return f'{self.email}'

    """  @property
    def name(self) -> str:
        return f'{self.last_name.title()} {self.first_name.split(" ")[-1].title()}'
    """