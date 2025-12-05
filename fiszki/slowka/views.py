from django.shortcuts import render
from django.http import HttpResponse
from .models import Slowko

def szukaj_slowka(request):
    # 2. LOGIKA: Pobieramy losowe słówko z bazy
    # .order_by('?') to sposób Django na losowanie rekordu
    # .first() bierze pierwszy wynik z tej posortowanej losowo listy
    wylosowane_slowko = Slowko.objects.order_by('?').first()

    # 3. PRZEKAZANIE: Pakujemy dane do słownika
    # Klucz 'fiszka' musi pasować do tego, co wpisałeś w HTML ({{ fiszka.angielski }})
    context = {
        'fiszka': wylosowane_slowko
    }

    # Renderujemy plik index.html z naszymi danymi
    return render(request, 'index.html', context)

def ping(request):
    return HttpResponse("Pong!")