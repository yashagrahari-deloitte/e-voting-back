from rest_framework import serializers

from election.models import ElectionInfo

class ElectionInfoSerializer(serializers.ModelSerializer):
    """Serializer for Election"""

    class Meta:
        model = ElectionInfo
        fields = ['id','title','election_type','phases','session']
        read_only_fields = ['id']