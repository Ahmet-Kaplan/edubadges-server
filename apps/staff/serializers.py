from rest_framework import serializers
from badgeuser.serializers import UserSlugRelatedField
from institution.serializers import InstitutionSlugRelatedField, FacultySlugRelatedField
from issuer.serializers import IssuerSlugRelatedField, BadgeClassSlugRelatedField
from mainsite.utils import EmailMessageMaker
from staff.models import InstitutionStaff, FacultyStaff, IssuerStaff, BadgeClassStaff


class BaseStaffSerializer(serializers.Serializer):

    may_create = serializers.CharField(allow_blank=False, required=True)
    may_read = serializers.CharField(allow_blank=False, required=True)
    may_update = serializers.CharField(allow_blank=False, required=True)
    may_delete = serializers.CharField(allow_blank=False, required=True)
    may_sign = serializers.CharField(allow_blank=False, required=True)
    may_award = serializers.CharField(allow_blank=False, required=True)
    may_administrate_users = serializers.CharField(allow_blank=False, required=True)


class StaffUpdateSerializer(BaseStaffSerializer):

    def update(self, instance, validated_data):
        original_perms = instance.permissions
        for permission in original_perms.keys():
            new_value = bool(int(validated_data[permission]))
            original_value = original_perms[permission]
            if original_value != new_value:  # this permission is changed
                setattr(instance, permission, new_value)  # update the permission
        instance.save()
        return instance


class BaseStaffCreateSerializer(BaseStaffSerializer):
    user = UserSlugRelatedField(slug_field='entity_id', required=True)

    def _base_create(self, validated_data, object_name, object_class):
        created_by = validated_data.pop('created_by')
        if created_by.is_user_within_scope(validated_data['user']):
            perms_allowed_to_assign = validated_data[object_name].get_permissions(created_by)
            for perm in perms_allowed_to_assign:
                if not perms_allowed_to_assign[perm] and int(validated_data[perm]):
                    raise serializers.ValidationError("May not assign permissions that you don't have yourself")
            new_staff_membership = object_class.objects.create(**validated_data)
            message = EmailMessageMaker.create_staff_member_addition_email(new_staff_membership)
            entity_name = new_staff_membership.object.__class__.__name__
            determiner = 'an' if entity_name[0] in 'aeiouAEIOU' else 'a'
            new_staff_membership.user.email_user(subject='You have been added to {} {}'.format(determiner, entity_name),
                                                 message=message)
            return new_staff_membership
        else:
            raise serializers.ValidationError("You may not administrate this user.")


class InstitutionStaffSerializer(BaseStaffCreateSerializer):
    institution = InstitutionSlugRelatedField(slug_field='entity_id', required=True)

    def create(self, validated_data):
        return self._base_create(validated_data, 'institution', InstitutionStaff)


class FacultyStaffSerializer(BaseStaffCreateSerializer):
    faculty = FacultySlugRelatedField(slug_field='entity_id', required=True)

    def create(self, validated_data):
        return self._base_create(validated_data, 'faculty', FacultyStaff)


class IssuerStaffSerializer(BaseStaffCreateSerializer):
    issuer = IssuerSlugRelatedField(slug_field='entity_id', required=True)

    def create(self, validated_data):
        return self._base_create(validated_data, 'issuer', IssuerStaff)


class BadgeClassStaffSerializer(BaseStaffCreateSerializer):
    badgeclass = BadgeClassSlugRelatedField(slug_field='entity_id', required=True)

    def create(self, validated_data):
        return self._base_create(validated_data, 'badgeclass', BadgeClassStaff)

