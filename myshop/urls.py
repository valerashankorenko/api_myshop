from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="API для магазина продуктов",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="valerashankorenko@yandex.by"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token-auth/', obtain_auth_token, name='token-auth'),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('swagger<format>/',
         schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/',
         schema_view.with_ui(
             'swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui(
             'redoc',
             cache_timeout=0),
         name='schema-redoc'
         ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
