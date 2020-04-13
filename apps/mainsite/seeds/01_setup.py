from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.sites.models import Site

from badgeuser.models import TermsVersion, BadgeUser
from institution.models import Institution, Faculty
from issuer.models import Issuer, BadgeClass
from mainsite.models import BadgrApp
# BadgrApp
from mainsite.seeds.constants import EDU_BADGES_FACULTY_NAME, SURF_INSTITUTION_NAME

setattr(settings, 'SUPPRESS_EMAILS', 1)

main_badgr_app, _ = BadgrApp.objects.get_or_create(
    is_active=1,
    cors=settings.UI_URL,
    email_confirmation_redirect="{}/login/".format(settings.UI_URL),
    forgot_password_redirect="{}/change-password/".format(settings.UI_URL),
    signup_redirect="{}/signup/".format(settings.UI_URL),
    ui_login_redirect="{}/auth/login/".format(settings.UI_URL),
    ui_signup_success_redirect="{}/signup/success/".format(settings.UI_URL),
    ui_connect_success_redirect="{}/profile/".format(settings.UI_URL),
    public_pages_redirect="{}/public/".format(settings.UI_URL),
    oauth_authorization_redirect="{}/oauth/".format(settings.UI_URL),
    use_auth_code_exchange=0
)

# Site
site, _ = Site.objects.get_or_create(domain=settings.DOMAIN, name=settings.DOMAIN)

# SocialApp
edu_id_secret = settings.EDU_ID_SECRET
edu_id_app, _ = SocialApp.objects.get_or_create(
    provider="edu_id",
    name="edu_id",
    client_id=settings.EDU_ID_CLIENT,
    secret=edu_id_secret
)

surf_conext_secret = settings.SURF_CONEXT_SECRET
surf_conext_app, _ = SocialApp.objects.get_or_create(
    provider="surf_conext",
    name="surf_conext",
    client_id=settings.SURF_CONEXT_CLIENT,
    secret=surf_conext_secret
)

edu_id_app.sites.add(site)
surf_conext_app.sites.add(site)

# TermsVersion
TermsVersion.objects.get_or_create(version=1, is_active=1)

# Superuser
superuser, _ = BadgeUser.objects.get_or_create(
    is_superuser=1,
    username=settings.SUPERUSER_NAME,
    email=settings.SUPERUSER_EMAIL,
    is_staff=1
)
superuser.set_password(settings.SUPERUSER_PWD)
superuser.save()

# SURF / eduBadges static
surf_net_institution, _ = Institution.objects.get_or_create(name=SURF_INSTITUTION_NAME,
                                                            identifier=SURF_INSTITUTION_NAME,
                                                            description=SURF_INSTITUTION_NAME)

edu_badges_faculty, _ = Faculty.objects.get_or_create(name=EDU_BADGES_FACULTY_NAME, institution=surf_net_institution,
                                                      description=EDU_BADGES_FACULTY_NAME)

surf_issuer, _ = Issuer.objects.get_or_create(name="SURF", image="uploads/issuers/surf.png", faculty=edu_badges_faculty,
                                              description="SURF", email="info@surf.nl", url="https://surf.nl",
                                              source="local", original_json="{}", badgrapp=main_badgr_app)

BadgeClass.objects.get_or_create(name=settings.EDUID_BADGE_CLASS_NAME, issuer=surf_issuer,
                                 image="uploads/badges/eduid.png",
                                 description="This is an example badge, please provide proof that you are eligible to receive more badges",
                                 source="local", old_json="{}")
