from django.db import models


class Slowko(models.Model):
    # To sprawi, że Django będzie zarządzać tą tabelą (ważne!)
    angielski = models.CharField(max_length=255)
    polski = models.CharField(max_length=255)

    # Nowe kolumny dla Twoich danych z CSV
    wymowa = models.CharField(max_length=255, blank=True, null=True)
    kategoria = models.CharField(max_length=100, default='Ogólne')

    # Magazyn na czasowniki nieregularne
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.angielski} - {self.polski}"