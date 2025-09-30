from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User model including a computed full name field.
    Combines username and last_name to provide a full name in the API response.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id","email","fullname"]

    def get_fullname(self, obj:User)->str:
        """
        Returns the user's full name by combining username and last_name.
        Used as a read-only field in the serialized response.
        """
        fullname = obj.username + " " + obj.last_name
        return fullname

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration handling full name parsing and password validation.
    Ensures email uniqueness and matching passwords before creating a new user.
    """
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
        """
        Ensures that the provided email is not already in use.
        Raises a validation error if a duplicate is found.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """
        Parses full name into username and last_name, checks passwords, and creates the user.
        Raises an error if passwords do not match or other validation fails.
        """
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
            raise serializers.ValidationError({'error': 'Passwords dont match'})
        
        account.set_password(pw)
        account.save()
        return account
    
class LoginTokenSerializer(serializers.Serializer):
    """
    Serializer to validate user credentials and authenticate by email and password.
    Adds authenticated user to validated data or raises validation error on failure.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, payload):
        """
        Authenticates the user using email and password.
        Adds the authenticated user to the validated payload or raises an error on failure.
        """
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