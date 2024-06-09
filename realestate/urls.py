"""
URL configuration for realestate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('users.urls')),  # Include the user URLs
    path('register/', include('users.urls')),  # Include the register URLs
    path('users/', include('users.urls')),  # Include all user-related URLs
    path('', lambda request: redirect('login')),  # Redirect root URL to login
    path('', include('listings.urls')),  # Ensure 'listings.urls' handles other paths correctly
]
