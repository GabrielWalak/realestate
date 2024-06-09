from django import forms
from .models import Zdjecie
from .models import Nieruchomosc
from .models import Najemca


class ZdjecieForm(forms.ModelForm):
    class Meta:
        model = Zdjecie
        fields = ('Obraz', 'ID_nieruchomosci')

class NieruchomoscForm(forms.ModelForm):
    class Meta:
        model = Nieruchomosc
        fields = '__all__'  # Lub określ pola, które chcesz uwzględnić

class EdytujNieruchomoscForm(forms.Form):
    typ = forms.CharField(max_length=100, required=False)
    status = forms.CharField(max_length=100, required=False)
    cena = forms.FloatField(required=False)
    powierzchnia = forms.FloatField(required=False)
    liczba_pokoi = forms.IntegerField(required=False)

    class NajemcaForm(forms.ModelForm):
        class Meta:
            model = Najemca
            fields = '__all__'