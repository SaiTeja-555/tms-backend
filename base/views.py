from asyncio import QueueEmpty
from django.shortcuts import render
from rest_framework import mixins, generics
from rest_framework.response import Response

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import Service, ServiceBooking, Temple, TempleService

from base.serializers import ServiceBookingSerializer, ServiceSerializer, TempleSerializer, TempleServiceSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings

import requests
from rest_framework.utils import json
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from base.models import TemplePic

from base.serializers import TemplePicSerializer
from rest_framework.decorators import  permission_classes, action

class TempleListView(generics.ListCreateAPIView):
    queryset = Temple.objects.all()
    serializer_class = TempleSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        else:
            return []
        
    def perform_create(self, serializer):
        # return serializer.save(admin = self.request.user)
        return serializer.save()

    def get_queryset(self):
        return self.queryset

class TempleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Temple.objects.all()
    serializer_class = TempleSerializer
    
    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def perform_create(self, serializer):
        return serializer.save(admin = self.request.user)

    def get_queryset(self):
        return self.queryset

class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    # lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset

# class ServiceListView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ServiceDetailView(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class TempleServiceListView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    serializer_class = TempleServiceSerializer
    queryset = TempleService.objects.all()

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = TempleService.objects.filter(temple_id = self.kwargs['temple_id'])
        print(self.kwargs)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(temple_id = Temple.objects.get(id = self.kwargs['temple_id']))
    

class TempleServiceDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = TempleService.objects.all()
    serializer_class = TempleServiceSerializer

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ServiceBookingListView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ServiceBookingDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TemplePicListView(generics.ListCreateAPIView):
    queryset = TemplePic.objects.all()
    serializer_class = TemplePicSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = TemplePic.objects.filter(temple_id = self.kwargs['temple_id'])
        return queryset


class TemplePicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemplePic.objects.all()
    serializer_class = TemplePicSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        else:
            return []

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        # queryset = TemplePic.objects.filter(temple_id = self.kwargs['temple_id'])
        return self.queryset
    

# class CustomUserCreate(APIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = ()
#     serializer_class = CustomUserSerializer

#     def post(self, request, format='json'):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 json = serializer.data
#                 return Response(json, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    # permission_classes = (permissions.AllowAny,)
    # authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status = status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status = status.HTTP_400_BAD_REQUEST)


# class GoogleLoginView(SocialLoginView):
#     authentication_classes = []
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = "http://localhost:3000"
#     client_class = OAuth2Client

# class GoogleSocialAuthView(generics.GenericAPIView):
#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, req):
#         serializer = self.serializer_class(data=req.data)
#         serializer.is_valid(raise_exception = True)
#         data = ((serializer.validated_data)["auth_token"])
#         return Response(data, status = status.HTTP_200_OK)

class GoogleView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)
        print(data)
        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            user = CustomUser()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
        
        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)

class HelloView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
