from django.db import models

class Slowko(models.Model):  # <--- Musi być dokładnie "Slowko"
    angielski = models.CharField(max_length=100)
    polski = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.angielski} - {self.polski}"