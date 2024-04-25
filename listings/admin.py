from django.contrib import admin
from .models import Adres, Nieruchomosc, Najemca, UmowaNajmu, Oplata, Zdjecie  # Importuj modele

# Rejestracja modeli
admin.site.register(Adres)
admin.site.register(Nieruchomosc)
admin.site.register(Najemca)
admin.site.register(UmowaNajmu)
admin.site.register(Oplata)
admin.site.register(Zdjecie)