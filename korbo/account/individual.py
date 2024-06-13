
from django.db import models
from django.contrib.postgres.fields import ArrayField


class IndividualAccountMixin(models.Model):
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    skills = ArrayField(models.IntegerField())
    experiences = ArrayField(models.IntegerField())
    

    
    @property
    def name(self)->str:
        return f'{self.first_name} {self.last_name}'


    class Meta:
        abstract = True
