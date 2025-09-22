from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']
        
    def get_fullname(self, obj:User):
        return f'{obj.username} {obj.last_name}'.strip()

class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        fullname = self.validated_data['fullname']
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        name_parts = fullname.strip().split()

        username = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        account = User(
            email=self.validated_data['email'], 
            username=username, 
            last_name=last_name
        )

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'passwords dont match'})
        
        account.set_password(pw)
        account.save()
        return account
    
class LoginTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, payload):
        payload_email = payload.get('email')
        payload_password = payload.get('password')

        try:
            user = User.objects.get(email=payload_email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email or password is not match")

        user = authenticate(username=user.username, password=payload_password)
        if not user:
            raise serializers.ValidationError("Email or password is not match")

        payload['user'] = user
        return payload