from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='posts-detail',
        lookup_field='pk'
    )
    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 
                  'body', 'created_date',
                  'published_date',
                  'is_published', 'author']


class PostProSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='posts-pro-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Post
        fields = '__all__'
    
    def create(self, validated_data):
        is_published = validated_data.get('is_published')
        instance = self.Meta.model(**validated_data)
        if is_published:
            instance.publish()
        else:
            instance.private()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if validated_data.get('is_published'):
            instance.publish()
        else:
            instance.private()
        instance.save()
        return instance 
