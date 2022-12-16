from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from django.views.decorators.csrf import ensure_csrf_cookie
from home.serializers import UserSerializer, UserProfileSerializer, OfficialsDetailsSerializer, LeftPanelSerializer
from home.utils import generate_access_token, generate_refresh_token
from home.authentication import SafeJWTAuthentication
from home.models import UserProfile, OfficialsDetails, Roles, LeftPanel
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response


class UserProfileViewSet(viewsets.ModelViewSet):
    """View for Manage Session Api"""
    serializer_class = UserProfileSerializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = UserProfile.objects.filter(aadhar=user)
        return queryset



class OfficialsDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = OfficialsDetailsSerializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = OfficialsDetails.objects.exclude(official=user)
        return queryset

class LeftPanelViewSet(viewsets.ModelViewSet):
    serializer_class = LeftPanelSerializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, url_path=r'get-roles',)
    def get_roles(self,request):
        user = self.request.user
        official = OfficialsDetails.objects.get(official=user)
        item_list = Roles.objects.filter(official=official.id).values_list('item_id')
        left_panel = LeftPanel.objects.filter(sno__in=item_list).values()
        data = dict()
        for heading in left_panel:
            head_route = heading['name']
            sub_route = LeftPanel.objects.filter(pid=heading['sno']).values().order_by('priority')
            data[head_route]=sub_route
        return Response(data)