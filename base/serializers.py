from rest_framework import serializers

from base.models import Service, ServiceBooking, Temple, TempleService

class TempleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Temple
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class TempleServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleService
        fields = "__all__"

class TempleServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleService
        fields = "__all__"

class ServiceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBooking
        fields = "__all__"