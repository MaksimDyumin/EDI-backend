"""
URL configuration for edi_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest.views import (DocumentsViewsSet, SignaturesView, 
                        SignatureDownloadView, UsersView,
                        ProfileView)


router = routers.SimpleRouter()
router.register(r'documents', DocumentsViewsSet, basename='document')

# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
# domains_router.register(r'nameservers', NameserverViewSet, basename='domain-nameservers'

urlpatterns = [
    path('documents/<int:pk>/signatures/', SignaturesView.as_view()),
    path('signatures/<int:pk>/', SignatureDownloadView.as_view()),
    path('users/', UsersView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'', include(router.urls)),
    
]