"""Serializers for JSON/XML conversation and validation"""
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):  # get_(fieldname)
        """Get the is_owner field"""
        request = self.context['request']  # from context in views.py functions
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Comment
        # fields = '__all__'
        fields = ['id', 'owner', 'is_owner', 'profile_id',
                  'post', 'content', 'created_at', 'updated_at',
                  'profile_image']


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in Comment Detail view
    Post is read only, so we don't have to set it for each update
    """
    post = serializers.ReadOnlyField(source='post.id')