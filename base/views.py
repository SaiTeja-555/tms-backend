from django.shortcuts import render
from rest_framework import mixins, generics
from rest_framework.response import Response
from base.models import Service, ServiceBooking, Temple, TempleService

from base.serializers import ServiceBookingSerializer, ServiceSerializer, TempleSerializer, TempleServiceSerializer

class TempleListView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Temple.objects.all()
    serializer_class = TempleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TempleDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Temple.objects.all()
    serializer_class = TempleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class ServiceListView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ServiceDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class TempleServiceListView(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    serializer_class = TempleServiceSerializer

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