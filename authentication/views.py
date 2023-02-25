from hashlib import algorithms_available
from django.conf import settings
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import generics, status, permissions, views
from django.urls import reverse
from yaml import serialize

from .renderers import UserRenderer
from .models import User
from .serializers import EmailVerificationSerializer, PasswordResetSerializer, RegisterSerializer, LoginSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from .serializers import UserSerializer

class CustomRedirect(HttpResponsePermanentRedirect):
    
    allowed_schemes = ['http','https']

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user=user).access_token
        
        # current_site = get_current_site(request).domain
        current_site = "localhost:8000"
        relativeLink = reverse("email-verify")
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi ' + user.username+". User link below to verify your email.\n  "+absurl
        data = {"domain": absurl,'email_body': email_body, 'email_subject': "Verify your email", "to_email": user.email}
        Util.send_mail(data)

        return Response(user_data, status= status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    token_param_config = openapi.Parameter("token", 
        in_=openapi.IN_QUERY, description="Description", type = openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        print(settings.SECRET_KEY)
        token = request.GET.get("token")
        frontend_login_url = "http://localhost:3000/login/"
        try:
            payload =jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            # return Response({"email":"Successfully activated"}, status=status.HTTP_200_OK)
            return redirect(frontend_login_url)
        
        except jwt.ExpiredSignatureError as e:
            return Response({"error":"Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)

        # user = User.objects.get(email = serializer.data["email"])
        # tokens = user.tokens()
        # print(tokens)
        # serializer.data["access"] = tokens["access"]
        # serializer.data["refresh"] = tokens["refresh"]
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = User.objects.get(email = request.data.get('email'))
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request = request).domain
        relativeLink = reverse("password-reset-confirm", kwargs = {"uidb64": uidb64, "token": token})
        absurl = 'http://'+current_site+relativeLink
        redirect_url = request.data.get("redirect_url", "")
        email_body = 'Hi . Use link below to reset the password .\n  '+absurl+"?redirect_url="+redirect_url
        data = {"domain": absurl,'email_body': email_body, 'email_subject': "Reset your password", "to_email": user.email}
        Util.send_mail(data)
        return Response({"success":"We have sentyou alink to reset your password"}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def get(self, request, uidb64, token):
        redirect_url = request.get("redirect_url")
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):

                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+"?token_valid=False")

                else:
                    return CustomRedirect(os.environ.get("FRONTEND_URL")+"?token_valid=False")
                # return Response({"error": "Token is not valid, please request a new token"}, status=status.HTTP_401_UNAUTHORIZED)
            if len(redirect_url) > 3:
                return CustomRedirect(redirect_url+"?token_valid=True&?message=Credentials Valid&?uidb64="+uidb64+"&?token="+token)
            else:
                return CustomRedirect(os.environ.get("FRONTEND_URL")+"?token_valid=False")
            # return Response({"success":True, "message":"Credentials Valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            if not PasswordResetTokenGenerator().check_token(user):
                return CustomRedirect(redirect_url+"?token_valid=False")

class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response({"success": True, "message": "Password reset successful"}, status = status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    # permission_classes = (permissions.AllowAny,)
    # authentication_classes = ()
    serializer_class = LogoutSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = "id"

    def get_queryset(self):
        return self.queryset




