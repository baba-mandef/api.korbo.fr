from django.db import models
from django.utils.timezone import now

from korbo.account.models import AccountMixin
from korbo.account.individual import IndividualAccountMixin
from korbo.user.models import User


class Freelance(AccountMixin, IndividualAccountMixin, User):
    user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE) 
    industry = models.CharField(max_length=100)
    portfolio = models.TextField() 
    



    role = "freelance"



    class Meta:
        managed = True
