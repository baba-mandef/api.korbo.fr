from django.db import models
from korbo.extra.tools import generate_uid 
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class KorboObjectManager(models.Manager):
    
    def get_by_public(self, public_id, **kwargs):
        error = "{self.model.__name__} does not exist"
        if public_id == "undefined":
            raise ObjectDoesNotExist(error)
        
        qs = self.filter(**kwargs)

        try:
            instance = qs.get(public_id=public_id)
        
        except (ObjectDoesNotExist, ValidationError, ValueError) as e:
            raise ObjectDoesNotExist(error)
        
        return instance
            


class KorboObject(models.Model):
    public_id = models.UUIDField(default=generate_uid, db_index=True, unique=True)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    objects = KorboObjectManager()

    class Meta():
        abstract = True
