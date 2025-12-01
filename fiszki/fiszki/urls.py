from django.contrib import admin
from django.urls import path
from slowka.views import strona_glowna  # Importujemy Twój widok

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', strona_glowna),  # Pusta ścieżka ('') to strona główna
]