from rest_framework import serializers, status
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)
    conf_pass = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number', 'password', 'conf_pass']


    def validate(self, data):
        password = data.get('password')
        conf_pass = data.get('conf_pass')

        if password and conf_pass and password != conf_pass:
            raise ValidationError({"msg": "Parollar mos emas"})
        return data


    def  validate_username(self, username):
        if username[0].isdigit():
            raise ValidationError({"msg": 'Username raqam bilna boshlanmasin'})


        
        return username

    def create(self, validated_data):
        validated_data.pop('conf_pass', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        user = super().to_representation(instance)

        return{
            "msg" : "signup",
            "user" : user
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError("Noto'g'ri login yoki paril.")

        data['user'] = user

        return data

    def to_representation(self, instance):
        
        user = instance.get('user')

        token, _ = Token.objects.get_or_create(user=user)

        return {
            'username' : user.username,
            'token' : token.key
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number']



class ProfileUpdateSerializer(ProfileSerializer):
    id = serializers.CharField(read_only = True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    conf_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        conf_password = attrs.get('conf_password')

        if conf_password and new_password and conf_password != new_password:
            raise ValidationError(detail='Yangi oarollar mos emas')

        if old_password:
            if not user.check_password(old_password):
                raise ValidationError(detail="Eski parol xato")
            if new_password and new_password == old_password:
                raise ValidationError(detail='Yangi parol eskisiga teng bolmasin')

        return attrs


    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user