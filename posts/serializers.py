"""Serializers for JSON/XML conversation and validation"""
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        """Get the is_owner field"""
        request = self.context['request']  # from context in views.py functions
        return request.user == obj.owner

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Post
        # fields = '__all__'
        fields = ['id', 'owner', 'profile_id', 'created_at',
                  'profile_image', 'updated_at', 'name', 'content',
                  'image', 'is_owner']
