from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Temples API",
        default_version='v1',
        description="Welcome to the world of Temples",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/token/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),
    path('', include('base.urls')),
    path('auth/', include('authentication.urls')),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
