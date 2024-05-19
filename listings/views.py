from django.shortcuts import render
from .models import Nieruchomosc, Najemca, UmowaNajmu, Oplata
from .forms import ZdjecieForm, NieruchomoscForm, EdytujNieruchomoscForm
from .filters import NieruchomosciFilter, AdresSearchFilter, SortFilter


def lista_nieruchomosci(request):
    nieruchomosci_list = Nieruchomosc.objects.all()
    adres_search_filter = AdresSearchFilter(request.GET, queryset=nieruchomosci_list)
    nieruchomosci_filter = NieruchomosciFilter(request.GET, queryset=adres_search_filter.qs)
    sort_filter = SortFilter(request.GET, queryset=nieruchomosci_filter.qs)
    nieruchomosci = sort_filter.qs

    theme = request.session.get('theme', 'light')  # Pobiera motyw z sesji; domyślnie 'light'

    kontekst = {
        'nieruchomosci': nieruchomosci,
        'nieruchomosci_filter': nieruchomosci_filter,
        'adres_search_filter': adres_search_filter,
        'sort_filter': sort_filter,
        'theme': theme  # Dodaj motyw do kontekstu
    }
    return render(request, 'lista_nieruchomosci.html', kontekst)




def edytuj_nieruchomosc(request, nieruchomosc_ID):
    nieruchomosc = Nieruchomosc.objects.filter(ID_nieruchomosci=nieruchomosc_ID)
    print(request, nieruchomosc_ID)
    return render(request, 'edytuj_nieruchomosc.html', {'nieruchomosc': nieruchomosc[0]})

def dodaj_nieruchomosc(request):
    theme = request.session.get('theme', 'light') 
    font_size = request.session.get('font_size', 'medium')
    if request.method == 'POST':
        form = NieruchomoscForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_nieruchomosci')
    else:
        form = NieruchomoscForm()
    return render(request, 'dodaj_nieruchomosc.html', {'form': form, 'theme': theme, 'theme': theme})

def lista_najemcow(request):
    theme = request.session.get('theme', 'dark')
    font_size = request.session.get('font_size', 'medium')
    najemcy = Najemca.objects.all().prefetch_related('ID_najemcy')
    return render(request, 'lista_najemcow.html', {'najemcy': najemcy,'theme': theme,  'font_size': font_size})

def kalendarz_najmow(request):
    theme = request.session.get('theme', 'dark')
    font_size = request.session.get('font_size', 'medium')
    return render(request, 'kalendarz_najmow.html',{'theme': theme, 'font_size': font_size} )

def lista_oplat(request):
    theme = request.session.get('theme', 'dark')
    font_size = request.session.get('font_size', 'medium')
    oplaty = Oplata.objects.all()
    return render(request, 'lista_oplat.html', {'oplaty': oplaty, 'theme': theme, 'font_size': font_size})

def raporty(request):
    theme = request.session.get('theme', 'dark')
    font_size = request.session.get('font_size', 'medium')
    return render(request, 'raporty.html', {'theme': theme, 'font_size': font_size})

def ustawienia(request):
    if request.method == 'POST':
        request.session['theme'] = request.POST.get('theme', 'light')
        request.session['font_size'] = request.POST.get('font_size', 'medium')
        return redirect('ustawienia')

    theme = request.session.get('theme', 'light')
    font_size = request.session.get('font_size', 'medium')
    return render(request, 'ustawienia.html', {'theme': theme, 'font_size': font_size})


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
        


def zmien_tlo(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        request.session['theme'] = theme
    return redirect('ustawienia')

def zmien_czcionke(request):
    if request.method == 'POST':
        font_size = request.POST.get('font_size', 'medium')  
        request.session['font_size'] = font_size
    return redirect('ustawienia')

from django.shortcuts import render
import matplotlib.pyplot as plt
from .models import Oplata
import io
import urllib, base64
from django.db.models import Sum

def generate_report(request):
    # Fetch payment data from the database
    fees_data = Oplata.objects.values('Typ_oplaty').annotate(total_amount=Sum('Kwota')).order_by('Typ_oplaty')

    # Prepare data for plotting
    categories = [fee['Typ_oplaty'] for fee in fees_data]
    values = [fee['total_amount'] for fee in fees_data]

    # Generate a plot
    fig, ax = plt.subplots()
    ax.bar(categories, values, color='skyblue')
    ax.set_title('Financial Overview by Fee Type')
    ax.set_xlabel('Type of Fee')
    ax.set_ylabel('Total Amount (PLN)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to a string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close(fig)  # Close the figure to free up memory

    return render(request, 'raporty.html', {'image': uri})

#Tymek 11.05.2024 kalendarz

#from django.http import JsonResponse
#from .models import UmowaNajmu
#def get_najmy(request):
#    najmy = UmowaNajmu.objects.all()
#    data = [{
#        'title': f"Najem od {najem.ID_najemcy.Imie} {najem.ID_najemcy.Nazwisko}",
#        'start': najem.Data_rozpoczecia.strftime('%Y-%m-%d'),
#        'end': najem.Data_zakonczenia.strftime('%Y-%m-%d')
#   } for najem in najmy]
#    return JsonResponse(data, safe=False)


#Tymek tego samego dnia(czyli 11.05.2024), lista oplat
from django.shortcuts import render
#from .models import Oplata, Najemca

def lista_oplat(request):
    theme = request.session.get('theme', 'dark')
    oplaty = Oplata.objects.select_related('ID_umowy__ID_najemcy').all()  # Zakładając, że istnieje relacja ID_umowy do UmowaNajmu i UmowaNajmu ma relację ID_najemcy do Najemca
    return render(request, 'lista_oplat.html', {'oplaty': oplaty,'theme': theme})


#Tymek, 19.05 modyfikacja kalendarza
from django.http import JsonResponse
from .models import UmowaNajmu

def get_najmy(request):
    najmy = UmowaNajmu.objects.all()
    data = []
    for najem in najmy:
        data.append({
            'title': f"Rozpoczęcie: {najem.ID_najemcy.Imie} {najem.ID_najemcy.Nazwisko}",
            'start': najem.Data_rozpoczecia.strftime('%Y-%m-%d'),
            'allDay': True
        })
        data.append({
            'title': f"Zakończenie: {najem.ID_najemcy.Imie} {najem.ID_najemcy.Nazwisko}",
            'start': najem.Data_zakonczenia.strftime('%Y-%m-%d'),
            'allDay': True
        })
    return JsonResponse(data, safe=False)

#Tymek, ciagle 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Oplata

def usun_oplate(request, oplata_id):
    oplata = get_object_or_404(Oplata, pk=oplata_id)
    if request.method == 'POST':
        oplata.delete()
        return redirect('lista_oplat')
    return render(request, 'lista_oplat.html')



