from django.db import IntegrityError
from mainsite.drf_fields import ValidImageField
from mainsite.serializers import StripTagsCharField
from rest_framework import serializers

from .models import Faculty, Institution


class InstitutionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = StripTagsCharField(max_length=16384, required=False)
    entity_id = StripTagsCharField(max_length=255, read_only=True)
    image = ValidImageField(required=False)
    grading_table = serializers.URLField(max_length=254, required=False)
    brin = serializers.CharField(max_length=254,  required=False)

    class Meta:
        model = Institution

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.image = validated_data.get('image')
        instance.grading_table = validated_data.get('grading_table')
        instance.brin = validated_data.get('brin')
        instance.save()
        return instance


class FacultySerializerV1(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=512)
    description = StripTagsCharField(max_length=16384, required=False)
    slug = StripTagsCharField(max_length=255, read_only=True, source='entity_id')


    class Meta:
        model = Faculty
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.save()
        return instance

    def create(self, validated_data, **kwargs):
        user_institution = self.context['request'].user.institution
        validated_data['institution'] = user_institution
        del validated_data['created_by']
        new_faculty = Faculty(**validated_data)
        try:
            new_faculty.save()
        except IntegrityError as e:
            raise serializers.ValidationError("Faculty name already exists")
        return new_faculty
