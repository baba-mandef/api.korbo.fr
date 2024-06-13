import binascii
import os
from django.db import models

from korbo.extra.tools import generate_uid


class Token(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=generate_uid)
    key = models.CharField(max_length=40)
    refresh = models.CharField(max_length=40, null=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.refresh = self.generate_key()
        return super().save(*args, **kwargs)
        
    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    def regenerate(self, force_refresh=False):
        
        self.key = self.generate_key()

        if force_refresh:
            self.refresh = self.generate_key()
        self.save()

    def __str__(self):
        return self.key
    
    class Meta:
        abstract = True