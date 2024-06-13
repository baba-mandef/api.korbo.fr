from django.db import models

from korbo.account.models import AccountMixin
from korbo.user.models import User


class Startup(AccountMixin, User):
    user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    industry = models.CharField(blank=True)
    description = models.TextField(blank=True)
    found_at = models.DateField(blank=True)



    role = "startup"


    class Meta:
        managed = True
