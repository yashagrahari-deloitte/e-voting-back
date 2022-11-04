from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from election.models import ElectionInfo, Electiontiming, ElectionDropdown
from election import serializers
from helpers.ElectionTiming_helper import ElectionTimingHelper
from home.authentication import SafeJWTAuthentication

# Create your views here.
class ElectionInfoViewSet(viewsets.ModelViewSet):
    """View For Manage Election Api"""

    serializer_class = serializers.ElectionInfoSerializer
    authentication_classes =[SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'session_id' in self.request.query_params: 
            session_id = self.request.query_params.get('session_id')
        else:
            session = ElectionTimingHelper.get_current_session()
            session_id = session.uid
        print(session_id)
        queryset = ElectionInfo.objects.filter(session_id=session_id,status='INSERT')
        return queryset 


class ElectionTimingViewSet(viewsets.ModelViewSet):
    """View for Manage Session Api"""
    serializer_class = serializers.ElectionTimingSerializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Electiontiming.objects.all().order_by('-uid')

    def get_queryset(self):
        return self.queryset


class ElectionDropdownViewSet(viewsets.ModelViewSet):
    """View for Manage Session Api"""
    serializer_class = serializers.ElectionDropDownsSerializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ElectionDropdown.objects.all()

    def get_queryset(self):
        request_type = self.request.query_params.get('request_type')
        if request_type == 'election_type':
            elction_type_ids = self.queryset.filter(field='ELECTION TYPE',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=elction_type_ids)            

        return self.queryset
    