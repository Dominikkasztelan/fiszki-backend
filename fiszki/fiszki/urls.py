from django.contrib import admin
from django.urls import path
# Importujemy nasze funkcje z aplikacji 'slowka'
from slowka.views import szukaj_slowka, ping

urlpatterns = [
    # Panel administratora
    path('admin/', admin.site.urls),

    # Nasze widoki
    # 1. Jak wejdziesz na /szukaj/ -> uruchomi się szukaj_slowka
    path('szukaj/', szukaj_slowka, name='szukaj_slowka'),

    # 2. Jak wejdziesz na /ping/ -> uruchomi się ping (test działania)
    path('ping/', ping, name='ping'),

    # 3. POPRAWKA: Strona główna (pusty ciąg znaków) też uruchamia wyszukiwarkę
    path('', szukaj_slowka, name='index'),
]