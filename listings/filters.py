import django_filters
from .models import Nieruchomosc
from django.db.models import Q

class AdresSearchFilter(django_filters.FilterSet):
    adres = django_filters.CharFilter(
        method='filter_by_address', label='Szukaj po adresie'
    )

    class Meta:
        model = Nieruchomosc
        fields = []

    def filter_by_address(self, queryset, name , value):
        query_parts = value.split()  # Split the search query into words
        qs = queryset
        for part in query_parts:
            qs = qs.filter(
                Q(ID_adresu__Ulica__icontains=part) | Q(ID_adresu__Miasto__icontains=part)
            )
        return qs
class NieruchomosciFilter(django_filters.FilterSet):
    Powierzchnia = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'step': 'any'})
    )
    Liczba_pokoi = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'step': 'any'})
    )
    Cena = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'step': 'any'})
    )
    Status = django_filters.ChoiceFilter(choices=Nieruchomosc.STATUS_CHOICES)
    Typ_nieruchomosci = django_filters.ChoiceFilter(choices=Nieruchomosc.TYP_CHOICES)

    class Meta:
        model = Nieruchomosc
        fields = ['Powierzchnia', 'Liczba_pokoi', 'Cena', 'Status', 'Typ_nieruchomosci']


class SortFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        # Note: use '-field_name' for descending order
        choices=[
            ('-Cena', 'Cena malejąco'),
            ('Cena', 'Cena rosnąco'),
        ],
        label='Sortowanie'
    )

    class Meta:
        model = Nieruchomosc
        fields = ['ordering']