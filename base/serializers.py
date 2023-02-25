from multiprocessing import AuthenticationError
from rest_framework import serializers

from base.models import Service, ServiceBooking, Temple, TempleService
from base.models import TemplePic

class TempleSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)
    
    class Meta:
        model = Temple
        fields = "__all__"
        
        

class ServiceSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)
    class Meta:
        model = Service
        fields = "__all__"

class TempleServiceSerializer(serializers.ModelSerializer):
    temple_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()

    class Meta:
        model = TempleService
        fields = "__all__"

    def get_temple_name(self, obj):
        return obj.temple_id.name
    
    def get_service_name(self, obj):
        return obj.service_id.name

# class TempleServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TempleService
#         fields = "__all__"

class ServiceBookingSerializer(serializers.ModelSerializer):
    temple_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    slots = serializers.SerializerMethodField()
    class Meta:
        model = ServiceBooking
        fields = "__all__"
    
    def get_temple_name(self, obj):
        return obj.templeservice_id.temple_id.name
    
    def get_service_name(self, obj):
        return obj.templeservice_id.service_id.name
    
    def get_slots(self, obj):
        return obj.templeservice_id.slots

class TemplePicSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)
    class Meta:
        model = TemplePic
        fields = "__all__"

# class CustomUserSerializer(serializers.ModelSerializer):
#     # email = serializers.EmailField()
#     # username = serializers.CharField()
#     # password = serializers.CharField(write_only = True)

#     class Meta:
#         model = CustomUser
#         fields = "__all__"
        # extra_kwargs = {"password":{"write_only": True}}
    
    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #         validated_data["username"],
    #         validated_data["email"],
    #         validated_data["password"]
    #     )
    #     return user

# class GoogleSocialAuthSerializer(serializers.Serializer):
#     auth_token = serializers.CharField()

#     def validate_auth_token(self, auth_token):
#         user_data = google.Google.validate(auth_token)
#         try:
#             user_data["sub"]
#         except:
#             raise serializers.ValidationError(
#                 "The token is invalid or expired. Please login again"
#             )
#         if user_data['aud'] != process.env.GOOGLE_CLIENT_ID:
#             raise AuthenticationFailed("oops. Who are you?")
        
#         user_id = user_data['sub']
#         email = user_data['email']
#         name = user_data['name']
#         provider = 'google'

#         return register_social_user(
#             provider = provider, user_id = user_id, email = email, name = name
#         )

