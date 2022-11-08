from rest_framework import serializers

from election.models import ElectionInfo, Electiontiming, ElectionDropdown

class ElectionInfoSerializer(serializers.ModelSerializer):
    """Serializer for Election"""
    election_category = serializers.CharField(source='election_type.value', read_only=True)

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
