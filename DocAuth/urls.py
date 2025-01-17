"""DocAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from apps.rbac.views.token import CustomObtainPairView
from apps.business import urls as apps_url

urlpatterns = [
    path('admin', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api/token/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1', include('apps.rbac.urls')),
    path('api/v1/projectApp', include('apps.business.urls')),
    path('api/v1/business', include(apps_url)),

    path('api/v1/business/', include('apps.business.urls'))
]
