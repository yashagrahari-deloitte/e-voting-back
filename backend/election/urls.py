from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from election import views

router = DefaultRouter()
router.register('election', views.ElectionInfoViewSet, basename='ElectionInfo')
router.register('session', views.ElectionTimingViewSet, basename='ElectionTiming')
router.register('getDropdown',views.ElectionDropdownViewSet, basename='ElectionDropdown')
router.register('assignRole',views.AssignRolesViewSet,basename='AssignRoles')
router.register('LockUnlock',views.ElectionLockingUnlockingViewSet, basename='ElectionLockingUnlocking')
router.register('AddCandidates',views.AddCandidateViewSet,basename='AddCandidate')

urlpatterns = [
    path('', include(router.urls)),
]