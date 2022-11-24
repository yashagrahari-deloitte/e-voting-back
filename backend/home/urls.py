from django.urls import re_path as url, path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserProfileViewSet, basename='UserProfile')
router.register('officials',OfficialsDetailsViewSet,basename='OfficialsDetails')

urlpatterns = [
    url('login/',login_view),
    path('', include(router.urls)),
]