from django.urls import path
from . import views

urlpatterns = [
    path("temples/", views.TempleListView.as_view()),
    path("temples/<int:pk>/", views.TempleDetailView.as_view()),
    path("services/", views.ServiceListView.as_view()),
    path("services/<int:pk>/", views.ServiceDetailView.as_view()),
    path("temples/<int:temple_id>/services", views.TempleServiceListView.as_view()),
    path("temples/services/<int:pk>", views.TempleServiceDetailView.as_view()),
    path("bookings", views.ServiceBookingListView.as_view()),
    path("bookings/<int:pk>", views.ServiceBookingDetailView.as_view()),
]
