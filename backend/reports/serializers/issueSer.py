from rest_framework import serializers
from ..models import Issue

class IssueSerializer(serializers.ModelSerializer):
    citizen_name = serializers.ReadOnlyField(source='citizen.full_name')

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'category', 'location_id', 
            'location_name', 'status', 'comment', 'photo', 
            'citizen_name', 'created_at'
        ]
        read_only_fields = ['status', 'comment', 'citizen']