import json
import uuid

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

from badgeuser.models import BadgeUser, TermsAgreement
from institution.models import Institution
from mainsite.seeds.constants import ENROLLED_STUDENT_EMAIL, REVOKED_STUDENT_EMAIL, INSTITUTION_UNIVERSITY_EXAMPLE_ORG, \
    AWARDED_STUDENT_EMAIL
from staff.models import InstitutionStaff

# Institution
[
    Institution.objects.get_or_create(identifier=ins['name'],
                                      name=ins['name'],
                                      description=ins['description'],
                                      image="uploads/institution/surf.png",
                                      grading_table="https://url.to.gradingtable/gradingtable.html",
                                      brin="000-7777-11111") for ins in
    [
        {'name': INSTITUTION_UNIVERSITY_EXAMPLE_ORG, 'description': 'The university example is always a good place to hang out'},
        {'name': 'diy.surfconext.nl', 'description': 'The university diy is also a good place to hang out'},
        {'name': 'university1', 'description': 'University1 description'},
        {'name': 'university2', 'description': 'University2 description'},
    ]
]


def accept_terms(user):
    TermsAgreement.objects.get_or_create(user=user, terms_version=1, agreed=True, valid=True)


# Users - Teachers
all_perms = {
    'may_create': True,
    'may_read': True,
    'may_update': True,
    'may_delete': True,
    'may_award': True,
    'may_sign': True,
    'may_administrate_users': True
}

no_perms = {
    'may_create': False,
    'may_read': False,
    'may_update': False,
    'may_delete': False,
    'may_award': False,
    'may_sign': False,
    'may_administrate_users': False
}


def create_admin(username, email, first_name, last_name, institution_name, uid, perms=all_perms):
    user, _ = BadgeUser.objects.get_or_create(username=username, email=email, last_name=last_name,
                                              first_name=first_name, is_teacher=True)
    accept_terms(user)

    EmailAddress.objects.get_or_create(verified=1, primary=1, email=email, user=user)
    SocialAccount.objects.get_or_create(provider='surf_conext', uid=uid, user=user)

    institution = Institution.objects.get(name=institution_name)
    user.institution = institution
    user.save()
    InstitutionStaff.objects.get_or_create(user=user, institution=institution, **perms)


def create_teacher(username, email, first_name, last_name, institution_name, uid, perms=no_perms):
    user, _ = BadgeUser.objects.get_or_create(username=username, email=email, last_name=last_name,
                                              first_name=first_name, is_teacher=True)
    accept_terms(user)

    EmailAddress.objects.get_or_create(verified=1, primary=1, email=email, user=user)
    SocialAccount.objects.get_or_create(provider='surf_conext', uid=uid, user=user)

    institution = Institution.objects.get(name=institution_name)
    user.institution = institution
    user.save()


institution_admins = [
    {
        "username": "joseph+weeler",
        "email": "Joseph+Weeler@university-example.org",
        "first_name": "Joseph",
        "last_name": "Wheeler",
        "institution_name": "university-example.org",
        "uid": "4b8c7b23bb0c99c85b5a0cbe63a826f45e147787",
    },
    {
        "username": "test12345",
        "email": "thisisa@valid.email",
        "first_name": "Firster",
        "last_name": "LastNamer",
        "institution_name": "university-example.org",
        "uid": "5d0584e3bf178ab4f6d6c9e02ebbd195afd10853",
    },
    {
        "username": "p1u1",
        "email": "professor1@university1.org",
        "first_name": "professor1",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "a20ccd72975606f20a05772182482b0eeb88dc09",
    },
    {
        "username": "p2u1",
        "email": "professor2@university1.org",
        "first_name": "professor2",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "b40d3e0abe239e22c84605231de16a9ddea9698b",
    },
    {
        "username": "p1u2",
        "email": "professor1@university2.org",
        "first_name": "professor1",
        "last_name": "university2",
        "institution_name": "university2",
        "uid": "00020001",
    },
]

teachers = [
    {
        "username": "test123456",
        "email": "test123456@university-example.org",
        "first_name": "Seconder",
        "last_name": "LastNamer2",
        "institution_name": "university-example.org",
        "uid": "847292f4f83cfc3835d9f367c4ec659a4c844a0a",
    },
    {
        "username": "p3u1",
        "email": "professor3@university1.org",
        "first_name": "professor3",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "e1d42cb2da86d8763053ea7c9e29ad87fcbc73aa",
    },
    {
        "username": "p4u1",
        "email": "professor4@university1.org",
        "first_name": "professor4",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "52622709ca4e5590a611d5f6f49f0712c7e513a8",
    },
    {
        "username": "p5u1",
        "email": "professor5@university1.org",
        "first_name": "professor5",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "aaf4dda63707f0b2a59fdfaee75df0ce7579bbe0",
    },
    {
        "username": "p6u1",
        "email": "professor6@university1.org",
        "first_name": "professor6",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "72ca9407474db806cfb457ac00a12dc601865591",
    },
    {
        "username": "p7u1",
        "email": "professor7@university1.org",
        "first_name": "professor7",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "02ffce96ae4a9c318ae074054429a8fed7784442",
    },
    {
        "username": "p8u1",
        "email": "professor8@university1.org",
        "first_name": "professor8",
        "last_name": "university1",
        "institution_name": "university1",
        "uid": "9a988eab38ad87ee4398e0af6f5807d63255cf6a",
    },
    {
        "username": "p2u2",
        "email": "professor2@university2.org",
        "first_name": "professor2",
        "last_name": "university2",
        "institution_name": "university2",
        "uid": "00020002",
    },
]

[create_admin(**a) for a in institution_admins]

[create_teacher(**t) for t in teachers]

# Users - Students
extra_data = json.dumps({"eduid": uuid.uuid4()})


def create_student(username, first_name, last_name, email, uid):
    user, _ = BadgeUser.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
    accept_terms(user)

    EmailAddress.objects.get_or_create(verified=1, primary=1, email=email, user=user)
    SocialAccount.objects.get_or_create(provider='edu_id', uid=uid, user=user, extra_data=extra_data)


students = [
    {
        "username": "user",
        "first_name": "John",
        "last_name": "Doe",
        "email": "edubadges.surf@gmail.com",
        "uid": "5acb63239f298a0a7de0081cd4a603d807178846"
    },
    {
        "username": "mary",
        "first_name": "Mary",
        "last_name": "Doe",
        "email": ENROLLED_STUDENT_EMAIL,
        "uid": "7ec1acf9ce98835e29c337077491b4ba6d1ed21d"
    },
    {
        "username": "sarah",
        "first_name": "Sarah",
        "last_name": "Doe",
        "email": REVOKED_STUDENT_EMAIL,
        "uid": "7fc994786c9e7815da17f5e97f796f67e891509e"
    },
    {
        "username": "carl",
        "first_name": "Carl",
        "last_name": "Doolittle",
        "email": AWARDED_STUDENT_EMAIL,
        "uid": "78b9ec1bb8731ec04b42137faf6a3c7068c89212"
    }
]

[create_student(**s) for s in students]
