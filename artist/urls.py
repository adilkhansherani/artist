"""artist URL Configuration

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
from rest_framework.routers import DefaultRouter
from band.views import UserDetailAPI,RegisterUserAPIView
from rest_framework.authtoken import views

from api import views

router = DefaultRouter()
#router.register(r'artists', views.ArtistViewSet)
#router.register(r'works', views.WorkViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', views.UserRegistrationView.as_view (), name='register'),
    path('api/login/', views.obtain_auth_token, name='login'),
    path('api/works/', views.filter_works_by_work_type, name='filter_works_by_work_type'),
    path('api/works/artist/', views.filter_works_by_artist, name='filter_works_by_artist'),
    path('api/artists/', views.ArtistListCreateView.as_view(), name='artist-list-create'),
    path('api/artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('api/works/', views.WorkListCreateView.as_view(), name='work-list-create'),
    path('api/works/<int:pk>/', views.WorkDetailView.as_view(), name='work-detail'),

]