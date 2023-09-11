"""Serializers for JSON/XML conversation and validation"""
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer"""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_image(self, value)   # Validate_(fieldname)
        if value.size > 1024 * 1024 * 2:  # if file size is more than 2MB
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px'
            )
        return value

    def get_is_owner(self, obj):  # get_(fieldname)
        """Get the is_owner field"""
        request = self.context['request']  # from context in views.py functions
        return request.user == obj.owner

    class Meta:
        """Which model data is the serializer accessing?"""
        model = Post
        # fields = '__all__'
        fields = ['id', 'owner', 'profile_id', 'created_at',
                  'profile_image', 'updated_at', 'name', 'content',
                  'image', 'is_owner', 'image_filter']
