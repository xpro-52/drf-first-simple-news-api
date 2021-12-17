from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Post


USER = get_user_model()

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=USER.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = '__all__'
    
    def _is_publish(self, instance, validated_data):
        is_published = validated_data.get('is_published')
        if is_published is None:
            pass
        elif is_published:
            instance.publish()
        else:
            instance.private()
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        self._is_publish(instance, validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        self._is_publish(instance, validated_data)
        instance.save()
        return instance
