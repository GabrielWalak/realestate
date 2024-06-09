from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('lista', views.lista_nieruchomosci, name='lista_nieruchomosci'),
    path('nieruchomosci/dodaj/', views.dodaj_nieruchomosc, name='dodaj_nieruchomosc'),
    path('nieruchomosci/<int:nieruchomosc_id>/dodaj_zdjecie/', views.dodaj_zdjecie, name='dodaj_zdjecie'),
    path('nieruchomosci/<int:nieruchomosc_ID>/edytuj/', views.edytuj_nieruchomosc, name='edytuj_nieruchomosc'),
    path('najemcy/', views.lista_najemcow, name='lista_najemcow'),
    path('kalendarz/', views.kalendarz_najmow, name='kalendarz_najmow'),
    path('oplaty/', views.lista_oplat, name='lista_oplat'),
    path('raporty/', views.raporty, name='raporty'),
    path('ustawienia/', views.ustawienia, name='ustawienia'),
    path('nieruchomosci/<int:nieruchomosc_ID>/edytuj/zmien_nieruchomosc', views.zmien_nieruchomosc, name='zmien_nieruchomosc'),
    path('nieruchomosci/<int:ID_nieruchomosci>/', views.szczegoly_nieruchomosci, name='nieruchomosc_szczegoly'),
    path('zmien_tlo/', views.zmien_tlo, name='zmien_tlo'),
    path('zmien-czcionke/', views.zmien_czcionke, name='zmien_czcionke'),
    path('api/najmy/', views.get_najmy, name='api-najmy'),
    path('oplaty/', views.lista_oplat, name='lista_oplat'),
    path('usun_oplate/<int:oplata_id>/', views.usun_oplate, name='usun_oplate'),
    path('najemcy/', views.lista_najemcow, name='lista_najemcow'),
    path('najemcy/<int:najemca_id>/edytuj/', views.edytuj_najemce, name='edytuj_najemce')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)