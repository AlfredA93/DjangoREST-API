"""Serializers for JSON/XML conversation and validation"""
from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Follower
        # fields = '__all__'
        fields = ['id', 'owner', 'followed', 'followed_name', 'created_at']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Possible Duplicate'
            })
