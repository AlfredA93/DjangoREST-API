"""Serializers for JSON/XML conversation and validation"""
from rest_framework import serializers
from .models import Profile
from follower.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """Get the is_owner field"""
        request = self.context['request']  # from context in views.py functions
        return request.user == obj.owner

    def get_following_id(self, obj):
        """Get Follower id"""
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Profile
        fields = '__all__'
        fields = ['id', 'owner', 'created_at',
                  'updated_at', 'name', 'content',
                  'image', 'is_owner', 'following_id']
