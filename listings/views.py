from django.shortcuts import render
from .models import Nieruchomosc, Najemca, UmowaNajmu, Oplata
from .forms import ZdjecieForm, NieruchomoscForm, EdytujNieruchomoscForm
from .filters import NieruchomosciFilter, AdresSearchFilter, SortFilter


def lista_nieruchomosci(request):
    nieruchomosci_list = Nieruchomosc.objects.all()
    adres_search_filter = AdresSearchFilter(request.GET, queryset=nieruchomosci_list)
    nieruchomosci_filter = NieruchomosciFilter(request.GET, queryset=adres_search_filter.qs)
    sort_filter = SortFilter(request.GET, queryset=nieruchomosci_filter.qs)

    # Use the sorted queryset
    nieruchomosci = sort_filter.qs

    kontekst = {
        'nieruchomosci': nieruchomosci,
        'nieruchomosci_filter': nieruchomosci_filter,
        'adres_search_filter': adres_search_filter,
        'sort_filter': sort_filter
    }
    return render(request, 'lista_nieruchomosci.html', kontekst)  # Wyświetl listę


def edytuj_nieruchomosc(request, nieruchomosc_ID):
    nieruchomosc = Nieruchomosc.objects.filter(ID_nieruchomosci=nieruchomosc_ID)
    print(request, nieruchomosc_ID)
    return render(request, 'edytuj_nieruchomosc.html', {'nieruchomosc': nieruchomosc[0]})

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


def zmien_nieruchomosc(request, nieruchomosc_ID):
    nieruchomosc = Nieruchomosc.objects.filter(ID_nieruchomosci=nieruchomosc_ID)[0]

    print(nieruchomosc_ID, nieruchomosc)
    if request.method == "POST":
        form = EdytujNieruchomoscForm(request.POST)
        if form.is_valid():
            nieruchomosc.Typ_nieruchomosci = form.cleaned_data["typ"]
            nieruchomosc.Status = form.cleaned_data["status"]
            nieruchomosc.Cena = form.cleaned_data["cena"]
            nieruchomosc.Powierzchnia = form.cleaned_data["powierzchnia"]
            nieruchomosc.Liczba_pokoi = form.cleaned_data["liczba_pokoi"]
            nieruchomosc.save()
            return redirect("lista_nieruchomosci")