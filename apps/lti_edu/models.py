from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from issuer.models import BadgeClass, Issuer, BadgeInstance
from entity.models import BaseVersionedEntity

import random


def get_uuid():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(25))


class LtiPayload(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    data = models.TextField()


class LtiClient(BaseVersionedEntity, models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=400, default='', blank=True, null=True)

    is_active = models.BooleanField(default=True)

    issuer = models.ForeignKey(Issuer, related_name='lti_client', on_delete=models.CASCADE)

    consumer_key = models.CharField(max_length=50, default=get_uuid)
    shared_secret = models.CharField(max_length=50, default=get_uuid)

    def __str__(self):
        return self.name

    # class Meta:
    #     unique_together = ('name', 'issuer')

    def validate_unique(self, *args, **kwargs):
        super(LtiClient, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(issuer=self.issuer, name=self.name).exists():
            raise ValidationError(
                message='LtiClient with this name and Issuer already exists.',
                code='unique_together',
            )

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(LtiClient, self).save(*args, **kwargs)


class ResourceLinkBadge(models.Model):
    # resource link is unique per placement, for each placement a unique badgeClass is created
    date_created = models.DateTimeField(default=timezone.now)

    resource_link = models.CharField(unique=True, max_length=255)
    issuer = models.ForeignKey(Issuer, related_name='lti_resource_link', on_delete=models.CASCADE)
    badge_class = models.ForeignKey(BadgeClass, related_name='lti_resource_link', on_delete=models.CASCADE)


class StudentsEnrolled(models.Model):
    badge_class = models.ForeignKey(BadgeClass, related_name='lti_students', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    edu_id = models.CharField(max_length=400, default='', blank=True, null=True)

    date_consent_given = models.DateTimeField(default=None, blank=True, null=True)

    email = models.EmailField()
    first_name = models.CharField(max_length=400, default='', blank=True, null=True)
    last_name = models.CharField(max_length=400, default='', blank=True, null=True)

    assertion_slug = models.CharField(max_length=150, default='', blank=True, null=True)
    date_awarded = models.DateTimeField(default=None, blank=True, null=True)
    denied = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    @property
    def assertion(self):
        try:
            return BadgeInstance.objects.get(entity_id=self.assertion_slug)
        except BadgeInstance.DoesNotExist:
            return None
        
    def assertion_is_revoked(self):
        assertion = self.assertion
        if assertion:
            return assertion.revoked
        else:
            return False    
