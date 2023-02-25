from lib2to3.pgen2.tokenize import TokenError
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, NotFound

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
import json


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError("The username should contain alphanumeric characters")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255, min_length = 3)
    password = serializers.CharField(max_length = 68, min_length = 3, write_only = True)
    username = serializers.CharField(max_length = 255, min_length = 3, read_only = True)
    # tokens = serializers.CharField(max_length = 68, min_length = 3, read_only = True)
    access = serializers.CharField(read_only = True)
    refresh = serializers.CharField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    is_admin = serializers.BooleanField(read_only= True)
    # Refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password", "username","access", "refresh"]

    def validate(self, attrs):
        email = attrs.get("email","")
        password = attrs.get("password","")

        user = auth.authenticate(email=email, password = password)
        
        if not user:
            raise AuthenticationFailed("Invalid credentials", "try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled", "contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        # return super().validate( attrs)
        tokens = user.tokens()
        print(tokens)
        return {
            "email": user.email,
            "username": user.username,
            "user_id": user.id,
            "is_admin": user.is_staff,
            "access": tokens["access"],
            "refresh": tokens["refresh"]
        }

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length = 2)
    redirect_url = serializers.CharField(max_length = 500, required = False)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get("email",'')
        if not User.objects.filter(email = email).exists():
            raise NotFound("No user found with given mail id", "please register")
        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length = 3, max_length = 68, write_only = True)
    token = serializers.CharField(min_length = 1, write_only = True)
    uidb64 = serializers.CharField(min_length = 1, write_only = True)

    class Meta:
        fields = ['password', 'token', 'uidb64']
    
    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user

        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': "token is expired or invalid"
    }

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        return super().validate(attrs)
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            self.fail("bad_token")

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "email", "is_staff"]