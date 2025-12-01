from django.shortcuts import render
from .models import Slowko


def strona_glowna(request):
    # Losuje jedno słówko. Jeśli baza pusta, zmienna będzie None
    fiszka = Slowko.objects.order_by('?').first()

    # Przekazujemy fiszkę do HTML-a
    return render(request, 'index.html', {'fiszka': fiszka})