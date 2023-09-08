"""Serializers for JSON/XML conversation and validation"""
from rest_framework import serializers
from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Profile
        # fields = '__all__'
        fields = ['id', 'owner', 'created_at',
                  'updated_at', 'name', 'content', 'image']
