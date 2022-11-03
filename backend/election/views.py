from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from election.models import ElectionInfo
from election import serializers
from helpers.ElectionTiming_helper import ElectionTimingHelper
from home.authentication import SafeJWTAuthentication

# Create your views here.
class ElectionInfoViewSet(viewsets.ModelViewSet):
    """View For Manage Election Api"""

    serializer_class = serializers.ElectionInfoSerializer
    session_id = ElectionTimingHelper.get_current_session_id()
    queryset = ElectionInfo.objects.filter(session = session_id)
    authentication_classes =[SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter()