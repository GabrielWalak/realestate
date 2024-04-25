from django import forms
from .models import Zdjecie
from .models import Nieruchomosc

class ZdjecieForm(forms.ModelForm):
    class Meta:
        model = Zdjecie
        fields = ('Obraz', 'ID_nieruchomosci')

class NieruchomoscForm(forms.ModelForm):
    class Meta:
        model = Nieruchomosc
        fields = '__all__'  # Lub określ pola, które chcesz uwzględnić