"""Serializers for JSON/XML conversation and validation"""
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """Get the is_owner field"""
        request = self.context['request']  # from context in views.py functions
        return request.user == obj.owner

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Profile
        # fields = '__all__'
        fields = ['id', 'owner', 'created_at',
                  'updated_at', 'name', 'content',
                  'image', 'is_owner']
