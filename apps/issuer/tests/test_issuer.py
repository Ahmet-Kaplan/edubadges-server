# encoding: utf-8
from __future__ import unicode_literals

import os
import os.path
import json
import unittest
from django.core.files.images import get_image_dimensions
from oauth2_provider.models import Application

from badgeuser.models import CachedEmailAddress
from issuer.models import Issuer, BadgeClass
from mainsite.models import ApplicationInfo
from mainsite.tests.base import BadgrTestCase, SetupIssuerHelper, SetupInstitutionHelper, SetupPermissionHelper


class IssuerTests(SetupIssuerHelper, SetupInstitutionHelper, SetupPermissionHelper, BadgrTestCase):
    example_issuer_props = {
        'name': 'Awesome Issuer',
        'description': 'An issuer of awe-inspiring credentials',
        'url': 'http://example.com',
        'email': 'contact@example.org'
    }

    def __init__(self, *args, **kwargs):
        super(IssuerTests, self).__init__(*args, **kwargs)
        self.second_eduid = "urn:mace:eduid.nl:1.0:d57b4355-c7c6-4924-a944-6172e31e9bbc:27871c14-b952-4d7e-85fd-6329ac5c6f19"

    @unittest.skip('For debug speedup')
    def test_cant_create_issuer_if_unauthenticated(self):
        response = self.client.post('/v1/issuer/issuers', self.example_issuer_props)
        self.assertIn(response.status_code, (401, 403))

    @unittest.skip('For debug speedup')
    def test_create_issuer_if_authenticated(self):
        test_faculty = self.setup_faculty()
        test_group = self.setup_faculty_admin_group()
        test_user = self.setup_user(authenticate=True, faculty=test_faculty, groups=[test_group], teacher=True)
        issuer_email = CachedEmailAddress.objects.create(
            user=test_user, email=self.example_issuer_props['email'], verified=True)
        example_issuer = self.example_issuer_props.copy()
        example_issuer["faculty"] = {"id": test_faculty.id, "name": test_faculty.name}
        example_issuer['extensions'] = [{'InstitutionIdentifierExtension': {"institutionIdentifier": "sgs"}}]
        response = self.client.post('/v1/issuer/issuers', json.dumps(example_issuer), content_type='application/json')

        self.assertEqual(response.status_code, 201)

        # assert that name, description, url, etc are set properly in response badge object
        badge_object = response.data.get('json')
        self.assertEqual(badge_object['url'], example_issuer['url'])
        self.assertEqual(badge_object['name'], example_issuer['name'])
        self.assertEqual(badge_object['description'], example_issuer['description'])
        self.assertEqual(badge_object['email'], example_issuer['email'])
        self.assertIsNotNone(badge_object.get('id'))
        self.assertIsNotNone(badge_object.get('@context'))

        # assert that the issuer was published to and fetched from the cache
        # with self.assertNumQueries(0):
        #     slug = response.data.get('slug')
        #     response = self.client.get('/v1/issuer/issuers/{}'.format(slug))
        #     self.assertEqual(response.status_code, 200)

    @unittest.skip('For debug speedup')
    def test_cant_create_issuer_if_authenticated_with_unconfirmed_email(self):
        self.setup_user(authenticate=True, verified=False)

        response = self.client.post('/v1/issuer/issuers', self.example_issuer_props)
        self.assertEqual(response.status_code, 403)

    def _create_issuer_with_image_and_test_resizing(self, image_path, desired_width=400, desired_height=400):
        test_faculty = self.setup_faculty()
        test_group = self.setup_faculty_admin_group()
        test_user = self.setup_user(authenticate=True, faculty=test_faculty, groups=[test_group], teacher=True)
        issuer_email = CachedEmailAddress.objects.create(
            user=test_user, email=self.example_issuer_props['email'], verified=True)

        with open(image_path, 'r') as badge_image:
            issuer_fields_with_image = self.example_issuer_props.copy()
            issuer_fields_with_image['image'] = badge_image
            # issuer_fields_with_image['faculty'] = {'id': test_faculty.id, 'name': test_faculty.name}

            response = self.client.post('/v1/issuer/issuers', issuer_fields_with_image, format='multipart') #content_type='*/*')
            self.assertEqual(response.status_code, 201)

            self.assertIn('slug', response.data)
            issuer_slug = response.data.get('slug')
            new_issuer = Issuer.objects.get(entity_id=issuer_slug)

            image_width, image_height = get_image_dimensions(new_issuer.image.file)
            self.assertEqual(image_width, desired_width)
            self.assertEqual(image_height, desired_height)

    @unittest.skip('For debug speedup')
    def test_create_issuer_image_500x300_resizes_to_400x400(self):
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', '500x300.png')
        self._create_issuer_with_image_and_test_resizing(image_path)

    @unittest.skip('For debug speedup')
    def test_create_issuer_image_450x450_resizes_to_400x400(self):
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', '450x450.png')
        self._create_issuer_with_image_and_test_resizing(image_path)

    @unittest.skip('For debug speedup')
    def test_create_issuer_image_300x300_stays_300x300(self):
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfiles', '300x300.png')
        self._create_issuer_with_image_and_test_resizing(image_path, 300, 300)

    @unittest.skip('For debug speedup')
    def test_can_update_issuer_if_authenticated(self):
        test_faculty = self.setup_faculty()
        test_group = self.setup_faculty_admin_group()
        test_user = self.setup_user(authenticate=True, teacher=True, faculty=test_faculty, groups=[test_group])

        original_issuer_props = {
            'name': 'Test Issuer Name',
            'description': 'Test issuer description',
            'url': 'http://example.com/1',
            'email': 'example1@example.org',
            'faculty': {'id': test_faculty.id,
                        'name': test_faculty.name}

        }


        issuer_email_1 = CachedEmailAddress.objects.create(
            user=test_user, email=original_issuer_props['email'], verified=True)

        response = self.client.post('/v1/issuer/issuers', json.dumps(original_issuer_props), content_type='application/json')
        response_slug = response.data.get('slug')

        updated_issuer_props = {
            'name': 'Test Issuer Name 2',
            'description': 'Test issuer description 2',
            'url': 'http://example.com/2',
            'email': 'example2@example.org',
            'faculty': {'id': test_faculty.id,
                        'name': test_faculty.name}
        }

        issuer_email_2 = CachedEmailAddress.objects.create(
            user=test_user, email=updated_issuer_props['email'], verified=True)

        response = self.client.put('/v1/issuer/issuers/{}'.format(response_slug), json.dumps(updated_issuer_props), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['url'], updated_issuer_props['url'])
        self.assertEqual(response.data['name'], updated_issuer_props['name'])
        self.assertEqual(response.data['description'], updated_issuer_props['description'])
        self.assertEqual(response.data['email'], updated_issuer_props['email'])

    @unittest.skip('For debug speedup')
    def test_get_empty_issuer_editors_set(self):
        test_user = self.setup_user(authenticate=True, teacher=True)
        issuer = self.setup_issuer(owner=test_user)

        response = self.client.get('/v1/issuer/issuers/{slug}/staff'.format(slug=issuer.entity_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assert that there is just a single owner

    @unittest.skip('For debug speedup')
    def test_add_user_to_issuer_editors_set_by_email(self):
        test_user = self.setup_user(authenticate=True, teacher=True)
        issuer = self.setup_issuer(owner=test_user)

        other_user = self.setup_user(authenticate=False, teacher=True, surfconext_id="44e494b6ca74a10417d9d6dec1bec8f88c04e446")

        response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=issuer.entity_id), {
            'action': 'add',
            'email': other_user.primary_email,
            'role': 'editor'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Assert that there is now one editor

    @unittest.skip('For debug speedup')
    def test_cannot_add_user_by_unverified_email(self):
        test_user = self.setup_user(authenticate=True, teacher=True)
        self.client.force_authenticate(user=test_user)

        user_to_update = self.setup_user(teacher=True, surfconext_id='somelongstring')
        new_email = CachedEmailAddress.objects.create(
            user=user_to_update, verified=False, email='newemailsonew@example.com')

        post_response = self.client.post(
            '/v1/issuer/issuers/test-issuer/staff',
            {'action': 'add', 'email': new_email.email, 'role': 'editor'}
        )

        self.assertEqual(post_response.status_code, 404)

    @unittest.skip('For debug speedup')
    def test_add_user_to_issuer_editors_set_too_many_methods(self):
        """
        Enter a username or email. Both are not allowed.
        """
        test_user = self.setup_user(authenticate=True)
        issuer = self.setup_issuer(owner=test_user)

        response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=issuer.entity_id), {
            'action': 'add',
            'email': 'test3@example.com',
            'username': 'test3',
            'role': 'editor'
        })
        self.assertEqual(response.status_code, 400)

    @unittest.skip('For debug speedup')
    def test_add_user_to_issuer_editors_set_missing_identifier(self):
        test_user = self.setup_user(authenticate=True)
        issuer = self.setup_issuer(owner=test_user)

        response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=issuer.entity_id), {
            'action': 'add',
            'role': 'editor'
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'User not found. Neither email address or username was provided.')

    @unittest.skip('For debug speedup')
    def test_bad_action_issuer_editors_set(self):
        test_user = self.setup_user(authenticate=True)
        issuer = self.setup_issuer(owner=test_user)

        response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=issuer.entity_id), {
            'action': 'DO THE HOKEY POKEY',
            'username': 'test2',
            'role': 'editor'
        })
        self.assertEqual(response.status_code, 400)

    @unittest.skip('For debug speedup')
    def test_add_nonexistent_user_to_issuer_editors_set(self):
        test_user = self.setup_user(authenticate=True)
        issuer = self.setup_issuer(owner=test_user)

        erroneous_username = 'wronguser'
        response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=issuer.entity_id), {
            'action': 'add',
            'username': erroneous_username,
            'role': 'editor'
        })
        self.assertContains(response, "User not found.".format(erroneous_username), status_code=404)

    @unittest.skip('For debug speedup')
    def test_add_user_to_nonexistent_issuer_editors_set(self):
        test_user = self.setup_user(authenticate=True)
        erroneous_issuer_slug = 'wrongissuer'
        response = self.client.post(
            '/v1/issuer/issuers/{slug}/staff'.format(slug=erroneous_issuer_slug),
            {'action': 'add', 'username': 'test2', 'role': 'editor'}
        )
        self.assertEqual(response.status_code, 404)

    @unittest.skip('For debug speedup')
    def test_add_remove_user_with_issuer_staff_set(self):
        test_user = self.setup_user(authenticate=True, teacher=True)
        test_issuer = self.setup_issuer(owner=test_user)

        other_user = self.setup_user(authenticate=False, teacher=True, surfconext_id="7980e81d94c0c5a201bf6809c51e5edc8c7d2601")

        self.assertEqual(len(test_issuer.staff.all()), 1)

        first_response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=test_issuer.entity_id), {
            'action': 'add',
            'email': other_user.primary_email
        })
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(len(test_issuer.staff.all()), 2)

        second_response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=test_issuer.entity_id), {
            'action': 'remove',
            'email': other_user.primary_email
        })
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(len(test_issuer.staff.all()), 1)

    def test_modify_staff_user_role(self):
        test_user = self.setup_user(authenticate=True)
        test_issuer = self.setup_issuer(owner=test_user)
        self.assertEqual(test_issuer.staff.count(), 1)

        other_user = self.setup_user(authenticate=False, eduid=self.second_eduid)

        first_response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=test_issuer.entity_id), {
            'action': 'add',
            'email': other_user.primary_email
        })
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(len(test_issuer.staff.all()), 2)
        self.assertEqual(test_issuer.editors.count(), 1)
        self.assertEqual(test_issuer.staff.count(), 2)

        second_response = self.client.post('/v1/issuer/issuers/{slug}/staff'.format(slug=test_issuer.entity_id), {
            'action': 'modify',
            'email': other_user.primary_email,
            'role': 'editor'
        })
        self.assertEqual(second_response.status_code, 200)
        staff = test_issuer.staff.all()
        self.assertEqual(test_issuer.editors.count(), 2)

    @unittest.skip('For debug speedup')
    def test_cannot_modify_or_remove_self(self):
        """
        The authenticated issuer owner cannot modify their own role or remove themself from the list.
        """
        test_user = self.setup_user(authenticate=True, teacher=True)
        test_issuer = self.setup_issuer(owner=test_user)
        self.client.force_authenticate(user=test_user)
        post_response = self.client.post(
            '/v1/issuer/issuers/{}/staff'.format(test_issuer.entity_id),
            {'action': 'remove', 'email': test_user.email}
        )

        self.assertEqual(post_response.status_code, 400)

        post_response = self.client.post(
            '/v1/issuer/issuers/{}/staff'.format(test_issuer.entity_id),
            {'action': 'modify', 'email': test_user.email, 'role': 'staff'}
        )

        self.assertEqual(post_response.status_code, 400)

    @unittest.skip('For debug speedup')
    def test_delete_issuer_successfully(self):
        test_user = self.setup_user(authenticate=True, teacher=True)
        test_issuer = self.setup_issuer(owner=test_user)

        response = self.client.delete('/v1/issuer/issuers/{slug}'.format(slug=test_issuer.entity_id), {})
        self.assertEqual(response.status_code, 204)

    @unittest.skip('For debug speedup')
    def test_delete_issuer_with_unissued_badgeclass_successfully(self):
        test_user = self.setup_user(authenticate=True, teacher=True)
        test_issuer = self.setup_issuer(owner=test_user)

        test_badgeclass = BadgeClass(name="Deletable Badge", issuer=test_issuer)
        test_badgeclass.save()

        response = self.client.delete('/v1/issuer/issuers/{slug}'.format(slug=test_issuer.entity_id), {})
        self.assertEqual(response.status_code, 204)

    @unittest.skip('For debug speedup')
    def test_cant_delete_issuer_with_issued_badge(self):
        test_faculty = self.setup_faculty()
        test_group = self.setup_faculty_admin_group()
        test_user = self.setup_user(authenticate=True, faculty=test_faculty, groups=[test_group], teacher=True)
        test_issuer = self.setup_issuer(owner=test_user)

        test_badgeclass = self.setup_badgeclass(issuer=test_issuer)
        test_badgeclass.issue(recipient_id='new-bage-recipient@email.test')

        response = self.client.delete('/v1/issuer/issuers/{slug}'.format(slug=test_issuer.entity_id), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            'Issuer can not be deleted because it has previously issued badges.')

    @unittest.skip('For debug speedup')
    def test_cant_create_issuer_without_permission_v1(self):
        test_faculty = self.setup_faculty()
        test_user = self.setup_user(authenticate=True, teacher=True, faculty=test_faculty)
        new_issuer_props = json.dumps({
            'name': 'Test Issuer Name',
            'description': 'Test issuer description',
            'url': 'http://example.com/1',
            'email': 'example1@example.org',
            'faculty': {'id': test_faculty.id,
                        'name': test_faculty.name}
        })

        response = self.client.post('/v1/issuer/issuers', new_issuer_props, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.')

    # def test_cant_create_issuer_with_unverified_email_v2(self):
    #     test_faculty = self.setup_faculty()
    #     test_group = self.setup_faculty_admin_group()
    #     test_user = self.setup_user(authenticate=True, teacher=True, faculty=test_faculty, groups=[test_group])
    #     new_issuer_props = {
    #         'name': 'Test Issuer Name',
    #         'description': 'Test issuer description',
    #         'url': 'http://example.com/1',
    #         'email': 'example1@example.org'
    #     }
    #
    #     response = self.client.post('/v2/issuers', new_issuer_props)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(
    #         response.data['validationErrors'][0],
    #         'Issuer email must be one of your verified addresses. Add this email to your profile and try again.')

    def test_trusted_user_can_create_issuer_with_unverified_email(self):
        test_faculty = self.setup_faculty()
        test_user = self.setup_user(authenticate=True)
        application = Application.objects.create(user=test_user, faculty=test_faculty)
        app_info = ApplicationInfo.objects.create(application=application, trust_email_verification=True)

        new_issuer_props = {
            'name': 'Test Issuer Name',
            'description': 'Test issuer description',
            'url': 'http://example.com/1',
            'email': 'an+unknown+email@badgr.test',
            'faculty': {'id': test_faculty.id,
                        'name': test_faculty.name}
        }

        response = self.client.post('/v2/issuers', new_issuer_props)
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/v1/issuer/issuers', new_issuer_props)
        self.assertEqual(response.status_code, 201)
