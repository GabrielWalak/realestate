# users/urls.py

from django.urls import path
from . import views
from listings.views import lista_nieruchomosci

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('lista_nieruchomosci/', lista_nieruchomosci, name='lista_nieruchomosci'),
]
