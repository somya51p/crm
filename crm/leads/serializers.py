from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'category',
            'category_name',
            'agent',
            'agent_first_name',
            'age',
            'hotel_name',
            'hotel_address',
            'phone_number',
            'url',
            'country',
            'description',
            'created_at',
            'updated_at',
        ]

    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True,
    )

    agent_first_name = serializers.StringRelatedField(
        source='agent',
        read_only=True,
    )
