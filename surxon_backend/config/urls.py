"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import health_check
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Surxon Mebel Platform API",
      default_version='v1',
      description="API documentation for Surxon Mebel Platform",
      terms_of_service="www.google.com",
      contact=openapi.Contact(email="contact@surxonmebel.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include('apps.authentication.urls')),
    path("api/products/", include('apps.products.urls')),

    # path("api/brands/", include('apps.brands.urls')),
    path("health/", health_check, name="health_check"),

    # Swagger and Redoc documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve static and media files in development and production
if settings.DEBUG or True:  # Always serve for Railway deployment
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
