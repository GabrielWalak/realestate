from django.shortcuts import render
from .models import Nieruchomosc, Najemca, UmowaNajmu, Oplata
from .forms import ZdjecieForm, NieruchomoscForm


def lista_nieruchomosci(request):
    nieruchomosci = Nieruchomosc.objects.select_related('ID_adresu').prefetch_related('zdjecie_set').order_by('-Cena')  # Pobierz wszystkie nieruchomości, sortuj wg ceny
    kontekst = {'nieruchomosci': nieruchomosci}
    return render(request, 'lista_nieruchomosci.html', kontekst)  # Wyświetl listę


def edytuj_nieruchomosc(request):
    nieruchomosc = Nieruchomosc.objects.all()

    return render(request, 'lista_nieruchomosci.html', {'nieruchomosc': nieruchomosc})

def dodaj_nieruchomosc(request):
    if request.method == 'POST':
        form = NieruchomoscForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_nieruchomosci')
    else:
        form = NieruchomoscForm()
    return render(request, 'dodaj_nieruchomosc.html', {'form': form})

def lista_najemcow(request):
    najemcy = Najemca.objects.all().prefetch_related('ID_najemcy')
    return render(request, 'lista_najemcow.html', {'najemcy': najemcy})

def kalendarz_najmow(request):
    # Implementacja logiki dla kalendarza
    return render(request, 'kalendarz_najmow.html')

def lista_oplat(request):
    oplaty = Oplata.objects.all()
    return render(request, 'lista_oplat.html', {'oplaty': oplaty})

def raporty(request):
    # Implementacja logiki dla raportów
    return render(request, 'raporty.html')

def ustawienia(request):
    # Implementacja logiki dla ustawień
    return render(request, 'ustawienia.html')







from django.shortcuts import render, redirect
from .forms import ZdjecieForm
from .models import Zdjecie, Nieruchomosc

def dodaj_zdjecie(request, nieruchomosc_id):
    nieruchomosc = Nieruchomosc.objects.get(pk=nieruchomosc_id)
    if request.method == 'POST':
        form = ZdjecieForm(request.POST, request.FILES)
        if form.is_valid():
            zdjecie = form.save(commit=False)
            zdjecie.ID_nieruchomosci = nieruchomosc
            zdjecie.save()
            return redirect('lista_nieruchomosci')  # Przekieruj na listę nieruchomości
    else:
        form = ZdjecieForm()
    return render(request, 'dodaj_zdjecie.html', {'form': form, 'nieruchomosc': nieruchomosc})
