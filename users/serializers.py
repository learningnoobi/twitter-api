from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if len(data.get("password")) <= 6:
            raise serializers.ValidationError("Password must be greater than 6 characters !")
        return data

    def create(self,validated_data):
        password =  validated_data.pop("password",None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
