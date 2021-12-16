from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer


USER = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = USER
        fields = ['id', 'username', 'email', 'password']
        extra_fields = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
