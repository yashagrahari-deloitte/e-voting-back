from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from election.models import ElectionInfo, Electiontiming, ElectionDropdown, ElectionPhaseWiseState_2022, ElectionStateWiseConsituency_2022, ElectionRolesAssigned_2022, ElectionLockingUnlocking_2022, EligibleVoters_2022, ElectionCandidates_2022
from home.models import OfficialsDetails, UserProfile
from election import serializers
from helpers.ElectionTiming_helper import ElectionTimingHelper
from home.authentication import SafeJWTAuthentication
import operator
import itertools
from datetime import datetime



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
        queryset = ElectionInfo.objects.filter(session_id=session_id,status='INSERT').order_by('-id')
        return queryset 
    
    @action(detail=False, url_path=r'get-phase-state',)
    def get_phase_state(self,request):
        if self.request.user.is_authenticated:
            election_id = self.request.query_params.get('election_id')
            data = list(ElectionPhaseWiseState_2022.objects.filter(election_id=election_id).values())
            response_data = {}
            for i,g in itertools.groupby(data, key=operator.itemgetter("phase")):
                response_data[i]=list(g)
            return Response(response_data)
        return Response({"msg":"You are unauthorized for this request"},status=403)

    @action(detail=False, url_path=r'get-state-constituency',)
    def get_constituency(self,request):
        if self.request.user.is_authenticated:
            state_id = self.request.query_params.get('state_id')
            data = list(ElectionStateWiseConsituency_2022.objects.filter(phase_stateid=state_id).values())
            return Response(data)
        return Response({"msg":"You are unauthorized for this request"},status=403)


    @action(detail=False, methods=['post'], url_path=r'add-election')
    def add_election(self,request):
        data = request.data 
        phase_data = data.get("phases_list")
        session_id = data['session_id']
        official = OfficialsDetails.objects.get(official_id = self.request.user)
        if self.request.user.is_authenticated:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                instance = serializer.save(added_by=official,status='INSERT',current_status='DRAFTED',session_id=session_id)
                for phases in phase_data:
                    states = phase_data.get(phases)
                    for state in states: 
                        qry = ElectionPhaseWiseState_2022.objects.create(election_id=instance, phase=phases, state=state,session_id=session_id)
                        constituencies = states.get(state)
                        for constituency in constituencies:
                            ElectionStateWiseConsituency_2022.objects.create(phase_stateid=qry,constituency=constituency.get("Constituency"),session_id=session_id)  
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
            election_type_ids = self.queryset.filter(field='ELECTION TYPE',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=election_type_ids)
        elif request_type == 'roles': 
            roles_ids =  self.queryset.filter(field='ROLES',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=roles_ids)
        elif request_type == 'lock_type': 
            locktype_ids =  self.queryset.filter(field='LOCK TYPE',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=locktype_ids)
        elif request_type == 'party': 
            party_ids =  self.queryset.filter(field='PARTY',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=party_ids)
        elif request_type == 'religion': 
            religion_ids =  self.queryset.filter(field='RELIGION',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=religion_ids)
        elif request_type == 'degree': 
            degree_ids =  self.queryset.filter(field='DEGREE',value__isnull=True).values_list('sno')
            self.queryset = self.queryset.filter(pid__in=degree_ids)
        elif request_type == 'get_category':
            self.queryset = self.queryset.filter(value__isnull=True)
        elif request_type == 'get_subcategory':
            s_no = self.request.query_params.get('s_no')
            self.queryset = self.queryset.filter(pid=s_no)
        return self.queryset
    

class AssignRolesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ElectionRolesAssigned_2022
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        official_id = self.request.query_params.get('official_id')
        queryset = ElectionRolesAssigned_2022.objects.filter(assigned_to=official_id).values()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

    @action(detail=False, url_path=r'get-assigned-election',)
    def get_assigned_election(self,request):
        if self.request.user.is_authenticated:
            user = request.user
            official = OfficialsDetails.objects.get(official=user)
            qry = ElectionRolesAssigned_2022.objects.filter(assigned_to=official.id).select_related('election_id')
            data = []
            for q in qry:
                obj = {
                    'title':q.election_id.title,
                    'id':q.election_id.id
                }
                data.append(obj)
        return Response(data)

    @action(detail=False, url_path=r'get-assigned-details',)
    def get_assigned_details(self,request):
        if self.request.user.is_authenticated:
            user = request.user
            election_id = self.request.query_params.get('election_id')
            official = OfficialsDetails.objects.get(official=user)
            qry = ElectionRolesAssigned_2022.objects.filter(assigned_to=official.id,election_id=election_id).select_related('phase_stateid','constituency_id')
            data = []
            for q in qry:
                phase_data = {'id':q.phase_stateid.uid,'phase':q.phase_stateid.phase,'state':q.phase_stateid.state}
                constituency_data = {'id':q.constituency_id.uid,'constituency':q.constituency_id.constituency}
                obj = {
                    'phase':phase_data,
                    'constituency':constituency_data
                }
                data.append(obj)
        return Response(data)

            
    


class ElectionLockingUnlockingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ElectionLockingUnlocking_2022Serializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ElectionLockingUnlocking_2022.objects.all().order_by('-id')

    def get_queryset(self):
        return self.queryset


class AddCandidateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ElectionCandidates_2022Serializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        aadhar = data['aadhar_no']
        candidate = UserProfile.objects.get(aadhar=aadhar)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(candidate_id=candidate)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAndGetElectionsDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EligibleVoters_2022Serializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset

    @action(detail=False, url_path=r'get-electionwise-candidates',)
    def get_electionwise_candidates(self,request):
        user = self.request.query_params.get('aadhar_no')
        if 'session_id' in self.request.query_params: 
            session_id = self.request.query_params.get('session_id')
        else:
            session = ElectionTimingHelper.get_current_session()
            session_id = session.uid
        user_profile = UserProfile.objects.get(aadhar=user)
        eligible_voter = EligibleVoters_2022.objects.filter(uniq_id=user_profile.uniq_id).values()
        if(len(eligible_voter)>0 and eligible_voter[0]['is_voted'] == False):
            phase_ids = ElectionStateWiseConsituency_2022.objects.filter(constituency=eligible_voter[0]['constituency'],session=session).values_list('phase_stateid')
            elections = ElectionPhaseWiseState_2022.objects.filter(uid__in=phase_ids).values()
            obj = {}
            for election in elections:
                election_details = ElectionInfo.objects.filter(id=election['election_id_id']).values()
                # check_lock = ElectionLockingUnlocking_2022.objects.filter(starttime__gte=datetime.now(), endtime__lte=datetime.now(), phase=election['phase'],election_id=election['election_id_id']).exists()
                if(True):
                    constiuency_id = ElectionStateWiseConsituency_2022.objects.filter(phase_stateid=election['uid'],constituency = eligible_voter[0]['constituency']).values('uid')
                    candidates = list(ElectionCandidates_2022.objects.filter(constituency=constiuency_id[0]['uid']).values('candidate_id__first_name','candidate_id__last_name','constituency_id','party_id','candidate_id','constituency_id__phase_stateid__election_id'))
                    election_title=election_details[0]['title']
                    obj[election_title] = candidates
                    print(obj)
            return Response(obj)
        else:
            return Response({"msg":"You are not allowed to vote"},status=204)