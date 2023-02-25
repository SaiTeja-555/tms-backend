from django.urls import path
from . import views

urlpatterns = [
    # path("users/", views.CustomUserCreate.as_view()),

    path("temples/", views.TempleListView.as_view()),
    path("temples/<int:pk>", views.TempleDetailView.as_view()),
    path("services/", views.ServiceListView.as_view()),
    path("services/<int:pk>", views.ServiceDetailView.as_view()),
    path("temples/<int:temple_id>/services/", views.TempleServiceListView.as_view()),
    path("temple-services/<int:pk>", views.TempleServiceDetailView.as_view()),
    path("bookings/", views.ServiceBookingListView.as_view()),
    path("bookings/<int:pk>", views.ServiceBookingDetailView.as_view()),
    path("temples/<int:temple_id>/gallery/", views.TemplePicListView.as_view()),
    path("temple-gallery/<int:pk>", views.TemplePicDetailView.as_view()),
    path("api/token/blacklist/", views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name = "blacklist"),
    path("api/google/", views.GoogleView.as_view(), name="google"),
    path("hello/", views.HelloView.as_view())
]
