from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer

class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['email','username','nickname','password','avatar']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','nickname','password','avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if len(data.get("password")) <= 6:
            raise serializers.ValidationError({'error':'Passwords must be larger than 6 letters !'})
        return data

    def create(self,validated_data):
        password =  validated_data.pop("password",None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
