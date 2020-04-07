from django.conf.urls import url
from institution.api import FacultyList, FacultyDetail, InstitutionDetail

urlpatterns = [
    url(r'^edit/(?P<slug>[^/]+)$', InstitutionDetail.as_view(), name='api_institution_detail'),
    url(r'^faculties/create$', FacultyList.as_view(), name='api_faculty_list'),
    url(r'^faculties/edit/(?P<slug>[^/]+)$', FacultyDetail.as_view(), name='api_faculty_detail'),
    ]

