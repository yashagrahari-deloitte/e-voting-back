from rest_framework import serializers

from election.models import ElectionInfo, Electiontiming, ElectionDropdown, ElectionRolesAssigned_2022

class ElectionInfoSerializer(serializers.ModelSerializer):
    """Serializer for Election"""
    election_category = serializers.CharField(source='election_type.value', read_only=True)
    created_by_first_name = serializers.CharField(source='added_by.user.first_name',read_only=True)
    created_by_last_name = serializers.CharField(source='added_by.user.last_name',read_only=True)
    created_by_username = serializers.CharField(source='added_by.official',read_only=True)

    class Meta:
        model = ElectionInfo
        fields = '__all__'
        # fields = ['id','title','election_category','phases','session','current_status','description_language']
        read_only_fields = ['id']


class ElectionTimingSerializer(serializers.ModelSerializer):
    """Serializer for Election Timing"""

    class Meta:
        model = Electiontiming
        fields = '__all__'
        read_only_fields = ['id']

class ElectionDropDownsSerializer(serializers.ModelSerializer):
    """Serializer for Election Dropdowns"""

    class Meta:
        model = ElectionDropdown
        fields = ['sno','pid','field','value']
        read_only_fields = ['sno']


class ElectionRolesAssigned_2022(serializers.ModelSerializer):

    class Meta:
        model = ElectionRolesAssigned_2022
        fields = '__all__'