from rest_framework import serializers
from home.models import User, UserProfile, OfficialsDetails, LeftPanel, Roles

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_active','user_type']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['uniq_id', 'first_name', 'last_name',
                  'dob', 'gender', 'aadhar']


class OfficialsDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = OfficialsDetails
        fields = "__all__"

class LeftPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeftPanel
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"