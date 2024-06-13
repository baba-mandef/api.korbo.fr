from django.db import models
from django.utils.timezone import now
from korbo.account.models import AccountMixin
from korbo.user.models import User
from korbo.account.individual import IndividualAccountMixin



class Consultant(AccountMixin, IndividualAccountMixin, User):
    user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)


    role = "consultant"
        

    class Meta:
        managed = True
