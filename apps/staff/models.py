from django.db import models
from django.forms.models import model_to_dict
from entity.models import BaseVersionedEntity
from signing.models import SymmetricKey


class PermissionedRelationshipBase(BaseVersionedEntity):
    """
    Abstract base class used for inheritance in all the Staff Many2Many relationship models
    """
    user = models.ForeignKey('badgeuser.BadgeUser', on_delete=models.CASCADE)
    may_create = models.BooleanField(default=False)
    may_read = models.BooleanField(default=False)
    may_update = models.BooleanField(default=False)
    may_delete = models.BooleanField(default=False)
    may_award = models.BooleanField(default=False)
    may_sign = models.BooleanField(default=False)
    may_administrate_users = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def permissions(self):
        return model_to_dict(self, fields = ['may_create',
                                             'may_read',
                                             'may_update',
                                             'may_delete',
                                             'may_award',
                                             'may_sign',
                                             'may_administrate_users'])
    @property
    def has_a_permission(self):
        """check to see if at least one permission set to True"""
        return self.may_create or self.may_read or self.may_update or self.may_delete \
               or self.may_award or self.may_sign or self.may_administrate_users

    def has_permissions(self, permissions):
        """
        checks to see if all permissions are there
        :param permissions: list of permissions
        :return: Bool
        """
        has_perm_count = 0
        own_perms = self.permissions
        for perm in permissions:
            if own_perms[perm]:
                has_perm_count += 1
        return len(permissions) == has_perm_count

    def publish(self):
        super(PermissionedRelationshipBase, self).publish()
        self.object.publish()
        self.user.publish()

    def delete(self, *args, **kwargs):
        publish_object = kwargs.pop('publish_object', True)
        super(PermissionedRelationshipBase, self).delete()
        if publish_object:
            self.object.publish()  # update permissions instantly
        self.user.publish()  # update permissions instantly

    @property
    def cached_user(self):
        from badgeuser.models import BadgeUser
        return BadgeUser.cached.get(pk=self.user_id)


class InstitutionStaff(PermissionedRelationshipBase):
    """
    Many2Many realtionship between Institution and users, with permissions added to the relationship
    """
    institution = models.ForeignKey('institution.Institution', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'institution'], name='unique_institution_staff_membership')
        ]

    @property
    def object(self):
        return self.institution


class FacultyStaff(PermissionedRelationshipBase):
    """
    Many2Many realtionship between Faculty and users, with permissions added to the relationship
    """
    faculty = models.ForeignKey('institution.Faculty', on_delete=models.CASCADE)

    @property
    def object(self):
        return self.faculty


class IssuerStaff(PermissionedRelationshipBase):
    """
    Many2Many realtionship between Issuer and users, with permissions added to the relationship
    """
    issuer = models.ForeignKey('issuer.Issuer', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('issuer', 'user')

    @property
    def object(self):
        return self.issuer

    @property
    def may_become_signer(self):
        # return self.user.may_sign_assertions and SymmetricKey.objects.filter(user=self.user, current=True).exists()
        return SymmetricKey.objects.filter(user=self.user, current=True).exists()

    @property
    def is_signer(self):
        return self.may_sign


class BadgeClassStaff(PermissionedRelationshipBase):

    badgeclass = models.ForeignKey('issuer.BadgeClass', on_delete=models.CASCADE)

    @property
    def object(self):
        return self.badgeclass
