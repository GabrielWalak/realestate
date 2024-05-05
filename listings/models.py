from django.db import models

class Adres(models.Model):
    ID_adresu = models.AutoField(primary_key=True)
    Kraj = models.CharField(max_length=100)
    Miasto = models.CharField(max_length=100)
    Kod_pocztowy = models.CharField(max_length=20)
    Ulica = models.CharField(max_length=255)
    Numer_domu = models.CharField(max_length=10)
    Numer_mieszkania = models.CharField(max_length=10, blank=True, null=True)  # Opcjonalne

    class Meta:
        db_table='Adresy'
    def __str__(self):
        return f"{self.Ulica} {self.Numer_domu}, {self.Kod_pocztowy} {self.Miasto}"

class Nieruchomosc(models.Model):
    STATUS_CHOICES = [
        ('Na Sprzedaż', 'Na Sprzedaż'),
        ('Wynajęte', 'Wynajęte'),
        ('Do wynajęcia', 'Do wynajęcia'),
        ('Do remontu', 'Do remontu')
        # ... add more choices as needed ...
    ]
    TYP_CHOICES = [
        ('Dom', 'Dom'),
        ('Mieszkanie', 'Mieszkanie'),
        # ... add more choices as needed ...
    ]
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    ID_nieruchomosci = models.AutoField(primary_key=True)
    ID_adresu = models.ForeignKey(Adres, on_delete=models.CASCADE, db_column='ID_adresu')
    Powierzchnia = models.DecimalField(max_digits=10, decimal_places=2)
    Liczba_pokoi = models.IntegerField()
    Cena = models.DecimalField(max_digits=10, decimal_places=2)
    Typ_nieruchomosci = models.CharField(max_length=50, choices=TYP_CHOICES)
    Opis = models.TextField(blank=True)  # Opcjonalne


    class Meta:
        db_table='Nieruchomosci'


    def __str__(self):
        return f"{self.Typ_nieruchomosci}, {self.Powierzchnia} m2, {self.ID_adresu}"

class Najemca(models.Model):
    ID_najemcy = models.AutoField(primary_key=True)
    Imie = models.CharField(max_length=100)
    Nazwisko = models.CharField(max_length=100)
    Telefon = models.CharField(max_length=15)
    Email = models.EmailField(max_length=100)
    Data_rozpoczecia_najmu = models.DateField(blank=True, null=True)  # Opcjonalne
    Data_zakonczenia_najmu = models.DateField(blank=True, null=True)  # Opcjonalne
    ID_nieruchomosci = models.ForeignKey(Nieruchomosc, on_delete=models.SET_NULL, blank=True, null=True, db_column='ID_nieruchomosci')  # Relacja z Nieruchomosc, opcjonalne

    class Meta:
        db_table='Najemcy'
    def __str__(self):
        return f"{self.Imie} {self.Nazwisko}"

class UmowaNajmu(models.Model):
    ID_umowy = models.AutoField(primary_key=True)
    ID_najemcy = models.ForeignKey(Najemca, on_delete=models.CASCADE, db_column='ID_najemcy')  # Relacja z Najemca
    ID_nieruchomosci = models.ForeignKey(Nieruchomosc, on_delete=models.CASCADE, db_column='ID_nieruchomosci')  # Relacja z Nieruchomosc
    Data_rozpoczecia = models.DateField()
    Data_zakonczenia = models.DateField()
    Oplata_miesieczna = models.DecimalField(max_digits=10, decimal_places=2)
    Kaucja = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=50)

    class Meta:
        db_table='Umowy_najmu'

    def __str__(self):
        return f"Umowa {self.ID_umowy} ({self.ID_najemcy})"

class Oplata(models.Model):
    ID_oplaty = models.AutoField(primary_key=True)
    ID_umowy = models.ForeignKey(UmowaNajmu, on_delete=models.CASCADE,db_column='ID_umowy')  # Relacja z UmowaNajmu
    Data_platnosci = models.DateField()
    Kwota = models.DecimalField(max_digits=10, decimal_places=2)
    Typ_oplaty = models.CharField(max_length=50)

    class Meta:
        db_table='Oplaty'

    def __str__(self):
        return f"{self.Typ_oplaty} - {self.Kwota} PLN"

class Zdjecie(models.Model):
    ID_zdjecia = models.AutoField(primary_key=True)
    Obraz = models.ImageField(upload_to='zdjecia_nieruchomosci')  # Przechowuje ścieżkę do pliku
    ID_nieruchomosci = models.ForeignKey(Nieruchomosc, on_delete=models.CASCADE , db_column='ID_nieruchomosci')  # Relacja z Nieruchomosc
    class Meta:
        db_table='Zdjecia'