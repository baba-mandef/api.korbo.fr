from importlib import import_module

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.timezone import now

from korbo.extra.tools import generate_token


class AccountMixin(models.Model):
    avatar = models.ImageField(null=True, upload_to="avatars/")
    avg_rating = models.DecimalField(max_digits=5, decimal_places=2)
    activated = models.DateTimeField(null=True)
    deactivated = models.DateTimeField(null=True)
    last_refresh = models.DateTimeField(null=True)
    location = models.CharField()
    number_of_reviews = models.PositiveIntegerField()
    deactivate_reason = models.CharField(max_length=300, null=True, blank=True)
    website = models.CharField(blank=True)
    
    #Todo: rewrite this method
    @property
    def rates(self):
        return None

    def activate(self):
        assert not self.activated, _("This account is already activated.")
        self.is_active = True
        self.activated = now()
        self.deactivated = None
        self.deactivate_reason = None
        self.save()

    def deactivate(self, reason=None):
        assert not self.deactivated, _("This account is already deactivated.")
        self.activated = None
        self.is_active = False
        self.deactivated = now()
        self.deactivate_reason = reason
        self.save()

    def get_login_token(self):
        assert self.object_name in ("consultant", "freelance", "startup", )

        token = getattr(import_module(f"korbo.auth.models"), f"{self.object_name.title()}Token").objects.create(
            user=self
        )

        return generate_token(
            token.key, token.refresh, token.public_id.hex, self.public_id.hex, token_type=self.object_name, lifetime=5
        )[0]

    class Meta:
        abstract = True
