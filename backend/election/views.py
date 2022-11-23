from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from election.models import ElectionInfo, Electiontiming, ElectionDropdown, ElectionPhaseWiseState_2022, ElectionStateWiseConsituency_2022
from home.models import OfficialsDetails
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
        queryset = ElectionInfo.objects.filter(session_id=session_id,status='INSERT').order_by('-id')
        return queryset 
    
    # def perform_create(self, serializer):
    #     official = OfficialsDetails.objects.get(official_id = self.request.user)
    #     if self.request.user.is_authenticated:
    #         instance = serializer.save(added_by=official,status='INSERT',current_status='DRAFTED')


    @action(detail=False, methods=['post'], url_path=r'add-election')
    def add_election(self,request):
        data = request.data 
        phase_data = data.get("phases_list")
        print(data)
        print(phase_data)
        official = OfficialsDetails.objects.get(official_id = self.request.user)
        if self.request.user.is_authenticated:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                instance = serializer.save(added_by=official,status='INSERT',current_status='DRAFTED')
                for phase in phase_data:
                    phase_value = phase_data.get(phase)
                    state = phase_value.get('state')
                    constituencies = phase_value.get('constituency')
                    qry = ElectionPhaseWiseState_2022.objects.create(election_id=instance, phase=phase, state=state)
                    for constituency in constituencies:
                        ElectionStateWiseConsituency_2022.objects.create(phase_stateid=qry,constituency=constituency)   
            else:
                return Response(serializer.errors)
        return Response(data)

    @action(detail=False, url_path=r'poll-info',)
    def post_info(self,request):
        if 'session_id' in self.request.query_params: 
            session_id = self.request.query_params.get('session_id')
        else:
            session = ElectionTimingHelper.get_current_session()
            session_id = session.uid
        queryset = ElectionInfo.objects.filter(session_id=session_id,status='INSERT')
        polls_info = {
            'active':0,
            'completed':0,
            'drafted':0
        }
        for query in queryset:
            current_status = query.current_status
            if 'ACTIVE' in current_status:
                polls_info['active']+=1
            elif 'COMPLETED' in current_status:
                polls_info['completed']+=1
            elif 'DRAFTED' in current_status:
                polls_info['drafted']+=1
        return Response(polls_info)


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
    