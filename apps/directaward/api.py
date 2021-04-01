from rest_framework.response import Response
from rest_framework import status

from entity.api import BaseEntityListView, BaseEntityDetailView, VersionedObjectMixin
from directaward.serializer import DirectAwardSerializer, DirectAwardBundleSerializer
from directaward.models import DirectAward
from directaward.permissions import IsDirectAwardOwner
from mainsite.exceptions import BadgrValidationError, BadgrValidationFieldError
from mainsite.permissions import AuthenticatedWithVerifiedEmail
from staff.permissions import HasObjectPermission


class DirectAwardBundleList(VersionedObjectMixin, BaseEntityListView):
    permission_classes = (AuthenticatedWithVerifiedEmail,)  # permissioned in serializer
    v1_serializer_class = DirectAwardBundleSerializer
    http_method_names = ['post']
    permission_map = {'POST': 'may_award'}


class DirectAwardDetail(BaseEntityDetailView):
    model = DirectAward
    permission_classes = (AuthenticatedWithVerifiedEmail, HasObjectPermission)
    v1_serializer_class = DirectAwardSerializer
    http_method_names = ['put', 'delete']
    permission_map = {'PUT': 'may_award', 'DELETE': 'may_award'}

    def delete(self, request, **kwargs):
        """
        DELETE a single DirectAward by identifier
        """
        obj = self.get_object(request, **kwargs)
        if not self.has_object_permissions(request, obj):
            return Response(status=status.HTTP_404_NOT_FOUND)

        revocation_reason = request.data.get('revocation_reason', None)
        if not revocation_reason:
            raise BadgrValidationFieldError('revocation_reason', "This field is required", 999)

        obj.revoke(revocation_reason)
        return Response(status=status.HTTP_200_OK)


class DirectAwardAccept(BaseEntityDetailView):
    model = DirectAward  # used by .get_object()
    permission_classes = (AuthenticatedWithVerifiedEmail, IsDirectAwardOwner)
    http_method_names = ['post']

    def post(self, request, **kwargs):
        directaward = self.get_object(request, **kwargs)
        if not self.has_object_permissions(request, directaward):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.data.get('accept', False):  # has accepted it
            if not directaward.badgeclass.terms_accepted(request.user):
                raise BadgrValidationError("Cannot accept direct award, must accept badgeclass terms first", 999)
            assertion = directaward.award(recipient=request.user)
            directaward.delete()
            return Response({'entity_id': assertion.entity_id}, status=status.HTTP_201_CREATED)
        elif not request.data.get('accept', True):  # has rejected it
            directaward.status = DirectAward.STATUS_REJECTED  # reject it
            directaward.save()
            return Response({'rejected': True}, status=status.HTTP_200_OK)
        raise BadgrValidationError('Neither accepted or rejected the direct award', 999)
